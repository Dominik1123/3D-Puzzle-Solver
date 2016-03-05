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

#ifndef INC_3D_PUZZLE_SOLVER_PIECE_H
#define INC_3D_PUZZLE_SOLVER_PIECE_H

#include <string>
#include <vector>

class Configuration;
class LatticeSite;

using namespace std;

class Piece {
public:
	char symbol;  // unique identifier;
	bool used;  // indicates if the piece is already in use;
	size_t currentConfigMarker;  // indicates the configuration that will be returned next by Piece::nextConfig();
	vector<Configuration*> configs;  // all configurations of that piece;
	LatticeSite* site;  // the lattice site on which the current config's seed was placed;

	Piece(char symbol);

	Configuration* nextConfig();
	void resetConfigMarker();
	string toString();
};

#endif // INC_3D_PUZZLE_SOLVER_PIECE_H