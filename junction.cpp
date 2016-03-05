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

#include "junction.h"
#include "vector3d.h"
#include <string>
#include <sstream>

string Junction::toString() {

    ostringstream os;

    if(branches.size() > 1) {
        os << "[";
        for(size_t i=0; i<branches.size(); ++i) {
            os << "[ ";
            os << directions[i]->toString();
            if(branches[i]->branches.size() > 0) {
                os << ", ";
            } else {
                os << " ";
            }
            os << branches[i]->toString();
            os << "]";
            if(i < branches.size()-1) {
                os << ", ";
            }
        }
        os << "]";
    } else if(branches.size() == 1) {
        os << directions[0]->toString();
        if(branches[0]->branches.size() > 0) {
            os << ", ";
        } else {
            os << " ";
        }
        os << branches[0]->toString();
    }

    return os.str();
}