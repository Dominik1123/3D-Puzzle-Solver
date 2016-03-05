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

#ifndef INC_3D_PUZZLE_SOLVER_JUNCTION_H
#define INC_3D_PUZZLE_SOLVER_JUNCTION_H

#include <string>
#include <vector>
#include <sstream>

class Vector3d;

using namespace std;

class Junction {
public:
    vector<Junction*> branches;    // branches going off the junction (branches.size() == number of junctions branching off this one);
    vector<Vector3d*> directions;  // direction the branches are going to in the same order as above;

    string toString();
};

#endif // INC_3D_PUZZLE_SOLVER_JUNCTION_H