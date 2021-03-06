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
Lattice orientation is horizontally as follows (where '?' marks a lattice site):

    x x x
    = = = ...
    0 1 2
y=0 ? ? ?
y=1 ? ? ?
y=2 ? ? ?
...

"""


output = ""
output = output + 'Lattice* lattice = new Lattice;\n'  # create lattice
output = output + 'Layer* layer;\n'
output = output + 'Row* row;\n'
output = output + '\n'

z_extent = 1
y_extent = 11
x_extent = 5
for z in range(0, z_extent):  # loop over layers

	output = output + 'layer = new Layer;\n'  # create new layer
	output = output + 'lattice->layers.push_back(layer);\n'  # add layer to lattice
	output = output + 'layer->lattice = lattice;\n'  # set reverse accessor
	output = output + '\n'

	for y in range(0, y_extent):  # loop over rows

		output = output + 'row = new Row;\n'  # create new row
		output = output + 'layer->rows.push_back(row);\n'  # add row to layer
		output = output + 'row->layer = layer;\n'  # set reverse accessor
		output = output + '\n'

		for x in range(0, x_extent):

			output = output + 'LatticeSite* site%d%d%d = new LatticeSite(%d,%d,%d);\n' % (z, y, x, x, y, z)  # create new lattice site
			output = output + 'row->sites.push_back(site%d%d%d);\n' % (z, y, x)  # add site to row
			output = output + 'site%d%d%d->row = row;\n' % (z, y, x)  # set reverse accessor
			output = output + '\n'

output = output + '\n'

def reverse_link(link):
	return -link[0], -link[1], -link[2]

def write_site_and_counterpart(z1, y1, x1, z2, y2, x2, dx, dy, dz):
	"""
	Produces code for adding a lattice site to the nearest neighbor list of a second one (along with direction) and vice versa.
	"""
	global output

	output = output + 'site%d%d%d->neighbors.push_back(site%d%d%d);\n' % (z1, y1, x1, z2, y2, x2)
	output = output + 'site%d%d%d->links.push_back(new Vector3d(%d,%d,%d));\n' % (z1, y1, x1, dx, dy, dz)
	output = output + '\n'

	dx, dy, dz = reverse_link((dx, dy, dz))

	output = output + 'site%d%d%d->neighbors.push_back(site%d%d%d);\n' % (z2, y2, x2, z1, y1, x1)
	output = output + 'site%d%d%d->links.push_back(new Vector3d(%d,%d,%d));\n' % (z2, y2, x2, dx, dy, dz)
	output = output + '\n\n'


for z1 in range(0, z_extent):

	for y1 in range(0, y_extent):
		for x1 in range(0, x_extent):

			# ----- same layer links -----
			if y1 < y_extent-1:
				z2 = z1; y2 = y1+1; x2 = x1
				write_site_and_counterpart(z1, y1, x1, z2, y2, x2, x2-x1, y2-y1, z2-z1)

			if x1 < x_extent-1:
				z2 = z1; y2 = y1; x2 = x1+1
				write_site_and_counterpart(z1, y1, x1, z2, y2, x2, x2-x1, y2-y1, z2-z1)
			# ----- END same layer links END -----

output = output + 'return lattice;\n'


with open('create_lattice_code.txt', 'w') as fp:
	fp.write(output)