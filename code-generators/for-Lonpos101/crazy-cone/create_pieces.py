######################################################################################
#
# This program solves various 3D puzzles.
# Copyright (C) 2016  Dominik Vilsmeier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
######################################################################################


"""
The direction to the next junction is indicated by (x,y,z).
A branch (sequence of directions) is indicated by [ (), ... ].
A fork (multiple branches going off the current junction) is indicated by enclosing all branches in additional square brackets, i.e. [[ (), ... ], [ (), ... ], ...].

An example configuration:
[ (1,0,0), [[ (1,0,0) ], [ (0,1,0) ]] ]
where the outer square brackets indicate the main branch and the inner (2nd) square brackets indicate a off-branching, enclosing the new branches (3rd level of square brackets).
The above configuration means:
1) go towards (1,0,0)
	1.1) go towards (1,0,0)
	1.2) go towards (0,1,0)

Another example:
[ (1,0,0), [[ (1,0,0), [[ (0,0,1), (0,0,1) ], [ (0,1,0) ]] ], [ (0,1,0) ], [ (0,0,1) ]] ]
which means:
1) go towards (1,0,0)
	1.1) go towards (1,0,0)
		1.1.1) go towards (0,0,1)
			1.1.1.1) go towards (0,0,1)
		1.1.2) go towards (0,1,0)
	1.2) go towards (0,1,0)
	1.3) go towards (0,0,1)
"""

def rotate_clockwise_by_90_degrees(links):
	"""
	Rotates vector by pi/2 around the z-axis: x -> -y, y -> x, z -> z.
	"""
	new_links = []
	for elem in links:
		if isinstance(elem, list):  # more than one branch
			branch_list = []
			for branch in elem:
				branch_list.append(rotate_clockwise_by_90_degrees(branch))
			new_links.append(branch_list)
		else:
			new_links.append((-elem[1], elem[0], elem[2]))  # rotated vector
	return new_links

def mirror_on_south_east_diagonal_axis(links):
	"""
	Mirrors vector on the line (1,1,0).
	"""
	normal_vectors = [(-1,1,0), (1,-1,0)]
	new_links = []
	for elem in links:
		if isinstance(elem, list):  # more than one branch
			branch_list = []
			for branch in elem:
				branch_list.append(mirror_on_south_east_diagonal_axis(branch))
			new_links.append(branch_list)
		else:
			if elem in normal_vectors:
				new_links.append((-elem[0], -elem[1], -elem[2]))  # mirrored vector
			else:
				new_links.append((elem[0], elem[1], elem[2]))  # vector remains unchanged
	return new_links


output = ""  # stores the generated code
n_junctions=0  # stores the number of junction that were already generated for a specific piece
def follow_branch(links, prev_junc_id):
	global output
	global n_junctions
	
	elem = links.pop(0)
	if isinstance(elem, list):  # more than one branch
		for branch in elem:
			follow_branch(branch, prev_junc_id)
	else:
		output = output + "junc%d = new Junction;\n" % n_junctions  # create new junction
		output = output + "junc%d->branches.push_back(junc%d);\n" % (prev_junc_id, n_junctions)  # link junction to previous one
		output = output + "junc%d->directions.push_back(new Vector3d(%d,%d,%d));\n" % (prev_junc_id, elem[0], elem[1], elem[2])  # store corresponding direction
		n_junctions =  n_junctions + 1

		if len(links) > 0:
			follow_branch(links, n_junctions-1)


def start(links, start_comments=[], end_comments=[]):
	global output
	global n_junctions

	output = output + '\n'.join('// '+comment for comment in start_comments) + '\n'  # write start comments, if any
	output = output + "junc0 = new Junction;\n"  # create seed junction
	n_junctions = 1
	follow_branch(links, 0)  # create all other junctions
	output = output + "config = new Configuration;\n"  # create corresponding configuration
	output = output + "config->seed = junc0;\n"  # set seed junction
	output = output + "piece->configs.push_back(config);\n"  # add configuration to piece
	output = output + '\n'.join('// '+comment for comment in end_comments)  # write end comments, if any
	output = output + '\n'


class Piece:
	def __init__(self, configs, identifier):
		self.configs = configs
		self.identifier = identifier

	def create_all_configs(self):
		global output

		output = output + '// ---------- %s ----------\n' % self.identifier  # write identifier
		output = output + "piece = new Piece('%s');\n" % self.identifier[-2]  # create piece
		output = output + 'pieces->push_back(piece);\n'  # add piece to list of pieces
		for config in self.configs:  # create all configurations
			start(config.links)
		output = output + '// ---------- END %s END ----------\n' % self.identifier  # indicate this piece is complete
		output = output + '\n\n'

class Config:
	def __init__(self, links):
		self.links = links

	def create(self):
		return [Config(self.links)]

	def create_and_rotate_once_flat(self):
		"""
		Create the configuration + one rotated configuration (pi/2).
		"""
		configs = []
		links = self.links
		for i in range(2):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		return configs

	def create_and_rotate_once_and_same_for_mirrored_flat(self):
		"""
		Create the configuration + one rotated configuration (pi/2) + original configuration mirrored + mirrored configuration rotated once (pi/2).
		"""
		configs = []
		links = self.links
		for i in range(2):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		links = mirror_on_south_east_diagonal_axis(self.links)
		for i in range(2):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		return configs

	def __str__(self):
		return str(self.links)


pieces = []

ne = (1,-1,0)  # north-east
se = (1,1,0)  # south-east
sw = (-1,1,0)  # south-west
nw = (-1,-1,0)  # north-west


orange = Piece(
	Config( [ se, se, sw ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ [[ sw, sw ], [ se ]] ] ).create() +\
	Config( [ [[ sw ], [ se, se ]] ] ).create() +\
	Config( [ se, sw, sw ] ).create() +\
	Config( [ sw, se, se ] ).create(),
	'orange (A)'
)
pieces.append(orange)

red = Piece(
	Config( [ se, se, sw, nw ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ sw, se, ne, se ] ).create() +\
	Config( [ se, sw, nw, sw ] ).create() +\
	Config( [ se, sw, [[ nw ], [ sw ]] ] ).create() +\
	Config( [ sw, se, [[ ne ], [ se ]] ] ).create() +\
	Config( [ sw, se, ne, ne ] ).create(),
	'red (B)'
)
pieces.append(red)

blue = Piece(
	Config( [ se, se, se, sw ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ [[ sw, sw, sw ], [ se ]] ] ).create() +\
	Config( [ [[ sw ], [ se, se, se ]] ] ).create() +\
	Config( [ se, sw, sw, sw ] ).create() +\
	Config( [ sw, se, se, se ] ).create(),
	'blue (C)'
)
pieces.append(blue)

pinkish = Piece(
	Config( [ se, se, [[ sw ], [ se ]] ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ se, [[ sw, sw ], [ ne ]] ] ).create() +\
	Config( [ se, [[ se, se ], [ ne ]] ] ).create_and_rotate_once_and_same_for_mirrored_flat(),
	'pinkish (D)'
)
pieces.append(pinkish)

green = Piece(
	Config( [ se, se, sw, se ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ [[ sw, sw ], [ se, ne ]] ] ).create() +\
	Config( [ se, sw, se, se ] ).create_and_rotate_once_and_same_for_mirrored_flat(),
	'green (E)'
)
pieces.append(green)

white = Piece(
	Config( [ se, sw ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ [[ sw ], [ se ]] ] ).create(),
	'white (F)'
)
pieces.append(white)

lightblue = Piece(
	Config( [ se, se, sw, sw ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ [[ sw, sw ], [ se, se ]] ] ).create(),
	'lightblue (G)'
)
pieces.append(lightblue)

rose = Piece(
	Config( [ se, sw, se, sw ] ).create_and_rotate_once_and_same_for_mirrored_flat() +\
	Config( [ [[ sw ], [ se, ne, se ]] ] ).create(),
	'rose (H)'
)
pieces.append(rose)

yellow = Piece(
	Config( [ se, sw, sw, nw ] ).create() +\
	Config( [ [[ sw ], [ se, se, sw ]] ] ).create() +\
	Config( [ [[ sw, sw, se ], [ se ]] ] ).create() +\
	Config( [ sw, se, se, ne ] ).create(),
	'yellow (I)'
)
pieces.append(yellow)

purple = Piece(
	Config( [ se, se, se ] ).create() +\
	Config( [ sw, sw, sw ] ).create(),
	'purple (J)'
)
pieces.append(purple)

lightgreen = Piece(
	Config( [ se, sw, nw ] ).create(),
	'lightgreen (K)'
)
pieces.append(lightgreen)

grey = Piece(
	Config( [ se, [[ sw ], [ se ], [ ne ]] ] ).create(),
	'grey (L)'
)
pieces.append(grey)


output = output + 'vector<Piece*>* pieces = new vector<Piece*>;\n\n'
output = output + 'Piece* piece;\n'
output = output + 'Configuration* config;\n'
output = output + 'Junction* junc0;\n'
output = output + 'Junction* junc1;\n'
output = output + 'Junction* junc2;\n'
output = output + 'Junction* junc3;\n'
output = output + 'Junction* junc4;\n'
output = output + 'Junction* junc5;\n\n'

for piece in pieces:
	piece.create_all_configs()

output = output + 'return pieces;'

with open('create_pieces_code.txt', 'w') as fp:
	fp.write(output)