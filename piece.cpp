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

#include "piece.h"
#include "configuration.h"
#include "latticesite.h"

using namespace std;

Piece::Piece(char symbol)
		: symbol(symbol), used(false), currentConfigMarker(currentConfigMarker)
{}

Configuration* Piece::nextConfig() {
	if(currentConfigMarker < configs.size()) {
		return configs[currentConfigMarker++];
	} else {  // all configurations exhausted;
		currentConfigMarker++;
		return 0;
	}
}

void Piece::resetConfigMarker() {
	currentConfigMarker = 0;
}

string Piece::toString() {
	if(currentConfigMarker <= configs.size()) {
		return configs[currentConfigMarker-1]->toString();
	} else {
		return "unused";
	}
}