# 3D-Puzzle-Solver

## Concept

The board (the set of available sites on which pieces can be placed = lattice) is divided into layers where each layer consists of rows and each row consists of (lattice-)sites. Each site knows about its neighbors (sites that have distance 1 from the current site, meaning a neighboring site can be reached through 1 edge when placing a piece) and the directions in which the neighbors are located. The directions are indicated by vectors.
Configurations of pieces are treated as sets of nodes (junctions) where the nodes are connected by edges (vectors). Each configuration has a seed junction and each junction has zero or more subsequent junctions (following) (only the forward direction is considered). The directions in which subsequent junctions are located are indicated by vectors.

## Procedure

The algorithm starts at the first unoccupied site and tries to place every unused piece in every configuration on this site. If a configuration could be placed successfully the algorithm moves on to the next free site and procedes in the same manner.

## Generating the lattice and configurations

What is characteristic to a specific problem (puzzle) is the layout of the lattice on which pieces are placed and the configurations of pieces one can use.
The code that is required to generate the lattice and the configurations of pieces is quite lengthy which means writing that code by hand is unfeasible. Instead one is better off using scripts that write the required code. Such scripts (available for specific puzzles) can be found in `code-generators` and can be adapted to other problems as needed. They will generate the body of the `createLattice` and `createPieces` functions which are located in `create_lattice.h` and `create_pieces.h`.