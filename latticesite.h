/***************************************************************************************
 *
 * This program solves various 3D puzzles.
 * Copyright (C) 2016  Dominik Vilsmeier
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 ***************************************************************************************/

#ifndef INC_3D_PUZZLE_SOLVER_LATTICE_SITE_H
#define INC_3D_PUZZLE_SOLVER_LATTICE_SITE_H

#include <string>
#include <vector>

class Configuration;
class Junction;
class Piece;
class Row;
class Vector3d;

using namespace std;

class LatticeSite {
public:
	size_t x;
	size_t y;
	size_t z;
	int occupied;  // indicates whether this site is already occupied (0: not occupied, 1: occupied, 2: overlap);
	char occupiedSymbol;  // the symbol of the piece that currently occupies this site ('0' if not occupied);
	Row* row;  // the row this site belongs to;
	vector<Vector3d*> links;  // directions to the nearest neighbor sites;
	vector<LatticeSite*> neighbors;  // the nearest neighbor sites; those are the ones that can be reached by a piece via a 1-link-connection; in the same order as the links above;

	LatticeSite(size_t x, size_t y, size_t z);

	bool placePiece(Junction* junction, Piece* piece);
	void removePiece(Junction* junction);
	bool hasLinks(Junction* junction, vector<LatticeSite*>& relevant_neighbors);
	string toString();
	string asSymbol();
};

#endif // INC_3D_PUZZLE_SOLVER_LATTICE_SITE_H