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

#ifndef INC_3D_PUZZLE_SOLVER_ROW_H
#define INC_3D_PUZZLE_SOLVER_ROW_H

#include <string>
#include <vector>

class LatticeSite;
class Layer;

using namespace std;

class Row {
public:
	Layer* layer;  // the layer this row belongs to;
	vector<LatticeSite*> sites;  // respective x-direction;

	Row();

	LatticeSite* nextFreeSite();
	string toString();
	string toStringLightweight();
};

#endif // INC_3D_PUZZLE_SOLVER_ROW_H