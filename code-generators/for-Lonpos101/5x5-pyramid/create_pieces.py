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
Elevated configurations start such that they are within the plane that is spanned by the vectors (1,1,1) (up-north-east) and (1,1,-1) (down-north-east).
They are mirrored on the plane that is spanned by the vectors (1,1,1) (up-north-east) and (1,-1,1) (up-south-east).

Note: Puzzle will be solved from top to bottom!

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

def mirror_on_y_axis(links):
	"""
	Mirrors vector on the y-axis: x -> -x, y -> y, z -> z.
	"""
	new_links = []
	for elem in links:
		if isinstance(elem, list):  # more than one branch
			branch_list = []
			for branch in elem:
				branch_list.append(mirror_on_y_axis(branch))
			new_links.append(branch_list)
		else:
			new_links.append((-elem[0], elem[1], elem[2]))  # mirrored vector
	return new_links


def mirror_on_plane(links):
	"""
	Mirrors vector on the plane that is spanned by the vectors (1,1,1) (up-north-east) and (1,-1,1) (up-south-east):
	x -> -x, y -> -y, z -> -z   if vector in normal_vectors
	x ->  x, y ->  y, z ->  z   else
	"""
	normal_vectors = [(1,-1,-1), (-1,1,1)]  # the normal vectors of the plane
	new_links = []
	for elem in links:
		if isinstance(elem, list):  # more than one branch
			branch_list = []
			for branch in elem:
				branch_list.append(mirror_on_y_axis(branch))
			new_links.append(branch_list)
		else:
			if elem in normal_vectors:
				new_links.append((-elem[0], -elem[1], -elem[2]))  # mirrored vector
			else:
				new_links.append((elem[0], elem[1], elem[2]))  # plane parallel vector is not mirrored
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

	def create_all_rotated_and_mirrored_flat(self):
		"""
		Create the configuration + all rotated configurations (pi/2, pi, 3pi/2) + all rotations (0, pi/2, pi, 3pi/2) of the mirrored (y-axis) configuration.
		"""
		configs = []
		links = self.links
		for i in range(4):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		links = mirror_on_y_axis(links)
		for i in range(4):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		return configs

	def create_all_rotated_flat(self):
		"""
		Create the configuration + all rotated configurations (pi/2, pi, 3pi/2).
		"""
		configs = []
		links = self.links
		for i in range(4):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		return configs

	def create_all_rotated_and_mirrored_elevated(self):
		"""
		Create the configuration + all rotated configurations (pi/2, pi, 3pi/2) + all rotations (0, pi/2, pi, 3pi/2) of the mirrored (on the above specified plane) configuration.
		"""
		configs = []
		links = self.links
		for i in range(4):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		links = mirror_on_plane(links)
		for i in range(4):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		return configs

	def create_all_rotated_elevated(self):
		"""
		Create the configuration + all rotated configurations (pi/2, pi, 3pi/2).
		"""
		configs = []
		links = self.links
		for i in range(4):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		return configs

	def create_and_rotate_once_elevated(self):
		"""
		Create the configuration + one rotated configuration (pi/2).
		"""
		configs = []
		links = self.links
		for i in range(2):
			configs.append(Config(links))
			links = rotate_clockwise_by_90_degrees(links)
		return configs

	def __str__(self):
		return str(self.links)


pieces = []

up = (0,-1,0)
right = (1,0,0)
down = (0,1,0)
left = (-1,0,0)

une = (1,-1,-1)  # up-north-east
use = (1,1,-1)  # up-south-east
unw = (-1,-1,-1)  # up-north-west
usw = (-1,1,-1)  # up-south-west
dne = (1,-1,1)  # down-north-east
dse = (1,1,1)  # down-south-east
dnw = (-1,-1,1)  # down-north-west
dsw = (-1,1,1)  # down-south-west

orange = Piece(
	Config( [ down, right, right ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ [[ down, down ], [ right ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ down, down, right ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ dsw, dne, dne ] ).create_all_rotated_elevated() +\
	Config( [ [[ dne ], [ dsw, dsw ]] ] ).create_all_rotated_elevated() +\
	Config( [ dsw, dsw, usw ] ).create_all_rotated_and_mirrored_elevated(),
	'orange (A)'
)
pieces.append(orange)

red = Piece(
	Config( [ down, down, left, up ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ down, right, up, right ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ [[ down, right, right ], [ right ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ right, down, left, left ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ dne, dne, dsw, usw ] ).create_all_rotated_and_mirrored_elevated() +\
	Config( [ dsw, dne, une, dne ] ).create_all_rotated_elevated() +\
	Config( [ [[ dsw, dne, dne ], [ dne ]] ] ).create_all_rotated_elevated() +\
	Config( [ dsw, dne, une, une ] ).create_all_rotated_elevated(),
	'red (B)'
)
pieces.append(red)

blue = Piece(
	Config( [ right, up, up, up ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ [[ up, up, up ], [ left ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ down, down, down, left ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ dsw, dsw, dsw, usw ] ).create_all_rotated_and_mirrored_elevated() +\
	Config( [ [[ dne ], [ dsw, dsw, dsw ]] ] ).create_all_rotated_elevated() +\
	Config( [ dne, dsw, dsw, dsw ] ).create_all_rotated_elevated(),
	'blue (C)'
)
pieces.append(blue)

pinkish = Piece(
	Config( [ down, down, [[ left ], [ down ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ right, [[ up, up ], [ down ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ up, [[ left ], [ up, up ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ dsw, dsw, [[ usw ], [ dsw ]] ] ).create_all_rotated_and_mirrored_elevated() +\
	Config( [ dne, [[ dsw, dsw ], [ une ]] ] ).create_all_rotated_elevated() +\
	Config( [ dsw, [[ dsw, dsw ], [ usw ]] ] ).create_all_rotated_and_mirrored_elevated(),
	'pinkish (D)'
)
pieces.append(pinkish)

green = Piece(
	Config( [ down, down, left, down ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ [[ left, down ], [ up, up ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ [[ down ], [ right, up, up ]] ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ up, right, up, up ] ).create_all_rotated_and_mirrored_flat() +\
	Config( [ dsw, dsw, usw, dsw ] ).create_all_rotated_and_mirrored_elevated() +\
	Config( [ [[ dsw, dsw ], [ dne, une ]] ] ).create_all_rotated_elevated() +\
	Config( [ dsw, usw, dsw, dsw ] ).create_all_rotated_and_mirrored_elevated(),
	'green (E)'
)
pieces.append(green)

white = Piece(
	Config( [ down, left ] ).create_all_rotated_flat() +\
	Config( [ [[ left ], [ up ]] ] ).create_all_rotated_flat() +\
	Config( [ right, up ] ).create_all_rotated_flat() +\
	Config( [ dsw, dne ] ).create_all_rotated_elevated() +\
	Config( [ [[ dsw ], [ dne ]] ] ).create_and_rotate_once_elevated() +\
	Config( [ dsw, usw ] ).create_all_rotated_elevated(),
	'white (F)'
)
pieces.append(white)

lightblue = Piece(
	Config( [ down, down, left, left ] ).create_all_rotated_flat() +\
	Config( [ [[ left, left ], [ up, up ]] ] ).create_all_rotated_flat() +\
	Config( [ right, right, up, up ] ).create_all_rotated_flat() +\
	Config( [ dsw, dsw, dne, dne ] ).create_all_rotated_elevated() +\
	Config( [ [[ dsw, dsw ], [ dne, dne ]] ] ).create_and_rotate_once_elevated() +\
	Config( [ dsw, dsw, usw, usw ] ).create_all_rotated_elevated(),
	'lightblue (G)'
)
pieces.append(lightblue)

rose = Piece(
	Config( [ down, left, down, left ] ).create_all_rotated_flat() +\
	Config( [ [[ left, down, left ], [ up ]] ] ).create_all_rotated_flat() +\
	Config( [ [[ down, left ], [ right, up ]] ] ).create_all_rotated_flat() +\
	Config( [ [[ left ], [ up, right, up ]] ] ).create_all_rotated_flat() +\
	Config( [ right, up, right, up ] ).create_all_rotated_flat() +\
	Config( [ dsw, dne, dsw, dne ] ).create_all_rotated_elevated() +\
	Config( [ [[ dsw, usw, dsw ], [ dne ]] ] ).create_all_rotated_elevated() +\
	Config( [ dne, une, dne, une ] ).create_all_rotated_elevated(),
	'rose (H)'
)
pieces.append(rose)

yellow = Piece(
	Config( [ down, right, right, up ] ).create_all_rotated_flat() +\
	Config( [ [[ up ], [ right, right, up ]] ] ).create_all_rotated_flat() +\
	Config( [ [[ left, up ], [ right, up ]] ] ).create_all_rotated_flat() +\
	Config( [ [[ left, left, up ], [ up ]] ] ).create_all_rotated_flat() +\
	Config( [ down, left, left, up ] ).create_all_rotated_flat() +\
	Config( [ dsw, dne, dne, une ] ).create_all_rotated_elevated() +\
	Config( [ [[ dsw ], [ dne, dne, dsw ]] ] ).create_all_rotated_elevated(),
	'yellow (I)'
)
pieces.append(yellow)

purple = Piece(
	Config( [ down, down, down ] ).create_all_rotated_flat() +\
	Config( [ dne, dne, dne ] ).create_all_rotated_elevated(),
	'purple (J)'
)
pieces.append(purple)

lightgreen = Piece(
	Config( [ right, down, left ] ).create_all_rotated_flat() +\
	Config( [ dne, dsw, usw ] ).create_and_rotate_once_elevated(),
	'lightgreen (K)'
)
pieces.append(lightgreen)

grey = Piece(
	Config( [ down, [[ left ], [ down ], [ right ]] ] ).create_all_rotated_flat() +\
	Config( [ dsw, [[ usw ], [ dsw ], [ dne ]] ] ).create_and_rotate_once_elevated(),
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
output = output + 'Junction* junc4;\n\n'

for piece in pieces:
	piece.create_all_configs()

output = output + 'return pieces;'

with open('create_pieces_code.txt', 'w') as fp:
	fp.write(output)