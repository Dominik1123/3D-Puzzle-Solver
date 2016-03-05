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

#include "latticesite.h"
#include "configuration.h"
#include "junction.h"
#include "piece.h"
#include "row.h"
#include "vector3d.h"
#include <iostream>

using namespace std;

LatticeSite::LatticeSite(size_t x, size_t y, size_t z)
		: x(x), y(y), z(z), occupied(0), occupiedSymbol('0')
{}

bool LatticeSite::placePiece(Junction* junction, Piece* piece) {

	occupied += 1;
	if(occupied == 2) return false;  // overlap (was already occupied);
	occupiedSymbol = piece->symbol;  // no overlap -> store symbol;

	vector<LatticeSite*> relevant_neighbors;  // filled by LatticeSite::hasLinks; stores the nearest neighbors that the current junction reaches via its branches;
	bool status = hasLinks(junction, relevant_neighbors);
	if(status) {  // lattice site has the required links;
		bool success = true;
		for(size_t i=0; i<junction->branches.size(); ++i) {
			success = relevant_neighbors[i]->placePiece(junction->branches[i], piece) && success;  // place all branches, indicate success;
		}
		return success;
	}
	return false;
}

void LatticeSite::removePiece(Junction* junction) {

	occupied -= 1;
	if(occupied == 1) return;  // resolved overlap;
	occupiedSymbol = '0';  // no overlap before -> set free site symbol;

	vector<LatticeSite*> relevant_neighbors;
	bool status = hasLinks(junction, relevant_neighbors);
	if(status) {
		for(size_t i=0; i<junction->branches.size(); ++i) {
			relevant_neighbors[i]->removePiece(junction->branches[i]);
		}
	}
}

bool LatticeSite::hasLinks(Junction* junction, vector<LatticeSite*>& relevant_neighbors) {

	for(size_t i=0; i<junction->directions.size(); ++i) {
		for(size_t j=0; j<links.size(); ++j) {
			if(*(junction->directions[i]) == *(links[j])) {
				relevant_neighbors.push_back(neighbors[j]);
			}
		}
	}
	return relevant_neighbors.size() == junction->directions.size();
}

string LatticeSite::toString() {

	return to_string(occupied);
}

string LatticeSite::asSymbol() {

	return string(1, occupiedSymbol);
}