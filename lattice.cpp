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

#include "lattice.h"
#include "latticesite.h"
#include "layer.h"
#include <iostream>
#include <sstream>

using namespace std;

Lattice::Lattice()
		: numberOfSolutions(0)
{}

LatticeSite* Lattice::nextFreeSite() {

	LatticeSite* site;
	for(size_t i=0; i<layers.size(); ++i) {
		if(layers[i] == 0) { cout << "in lattice.cpp: LAYER IS 0" << endl; exit(-1); }  // __DEBUG__
		site = layers[i]->nextFreeSite();
		if(site != 0) return site;
	}
	return 0;
}

string Lattice::toString() {

	ostringstream os;
	for(size_t i=0; i<layers.size(); ++i) {
		os << layers[i]->toString() << endl;
	}

	return os.str();
}

string Lattice::toStringLightweight() {

	ostringstream os;
	for(size_t i=0; i<layers.size(); ++i) {
		os << layers[i]->toStringLightweight();
	}

	return os.str();
}