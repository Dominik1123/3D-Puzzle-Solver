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

#include "vector"
#include "lattice.h"
#include "latticesite.h"
#include "piece.h"
#include "configuration.h"
#include "create_lattice.h"
#include "create_pieces.h"
#include <iostream>
#include <ctime>

using namespace std;

void start(Lattice* lattice, vector<Piece*>* pieces);
void iter(Lattice* lattice, vector<Piece*>* pieces);

int main(int argc, char** argv)
{

	Lattice* lattice = createLattice();
	vector<Piece*>* pieces = createPieces();

	start(lattice, pieces);

	return 0;
}

void start(Lattice* lattice, vector<Piece*>* pieces) {

	time_t startTime;
	time(&startTime);
	
	iter(lattice, pieces);

	time_t stopTime;
	time(&stopTime);

	double seconds = difftime(stopTime, startTime);

	cerr << "computing time: " << seconds << " seconds" << endl;

	cerr << "number of solutions found: " << lattice->numberOfSolutions << endl;
}

void iter(Lattice* lattice, vector<Piece*>* pieces) {

	LatticeSite* site = lattice->nextFreeSite();
	if(site == 0) {  // lattice is complete;
		lattice->numberOfSolutions += 1;
		cout << lattice->toStringLightweight() << endl;
		return;
	}
	
	for(vector<Piece*>::iterator it_p=pieces->begin(); it_p!=pieces->end(); ++it_p) {
		Piece* piece = *it_p;
		if(piece->used) continue;
		piece->resetConfigMarker();
		Configuration* config = piece->nextConfig();
		do {
			bool success = site->placePiece(config->seed, piece);
			if(success) {
				piece->used = true;
				piece->site = site;

				iter(lattice, pieces);
			}
			site->removePiece(config->seed);
			piece->used = false;
			piece->site = 0;

			config = piece->nextConfig();
		} while(config != 0);
	}
}