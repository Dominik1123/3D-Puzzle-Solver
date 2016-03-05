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

#include "vector3d.h"
#include <sstream>

using namespace std;

Vector3d::Vector3d(int dx, int dy, int dz)
		: dx(dx), dy(dy), dz(dz)
{}

bool Vector3d::operator==(Vector3d& other) {

	return other.dx == this->dx && other.dy == this->dy && other.dz == this->dz;
}

string Vector3d::toString() {

	ostringstream os;
	os << "(" << dx << "," << dy << "," << dz << ")";
	return os.str();
}