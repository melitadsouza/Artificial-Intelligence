# Name: Melita Dsouza
# Email: dsouzam@indiana.edu
# Assignment 1

from copy import deepcopy
import sys
import time

FINAL_CANONICAL_CONFIGURATION = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

class ShortSequence_Solver16:
    initial_state = None;
    explored_set = None;
    is_solvable = None;
    moves = None;
    r = None;
    c = None;
    
    # Parameterized constructor reads input file and checks for solvability.
    def __init__(self, filename):
        self.read_check_input_file(filename);
        self.explored_set = [];
        self.moves = [];
    
    # Reads the puzzle to a 2-D matrix and checks if puzzle is solvable   
    def read_check_input_file(self, filename):
        with open(filename, 'r') as f:
            self.initial_state = [[int(j) for j in i] for i in [line.split() for line in f]]
            
        self.is_solvable = self.is_solvable(self.initial_state);
    
    # Heuristic ==> Manhattan distance. 
    # https://stackoverflow.com/questions/12526792/manhattan-distance-in-a   
    def manhattan_distance(self, successor_state):
        manhattanDistanceSum = 0;
        for x in range(4):
            for y in range(4):
                value = successor_state[x][y];
                if (value != 0):
                    targetX = (value - 1) // 4;
                    targetY = (value - 1) % 4;
                    dx = x - targetX;
                    dy = y - targetY;
                    manhattanDistanceSum += (abs(dx) + abs(dy)) / 3.0; # Divide by 3 for admissible heuristic
                    
        return manhattanDistanceSum;
    
    # Successor states generated by moving tiles by one, two or three positions to the top, bottom, left or right as appropriate
    def successors(self, tiles):
        successor_states = []
        moves = []
        for i in range(4):
            for j in range(4):
                if(i == self.r and j == self.c):
                    tiles_copy = deepcopy(tiles) # Make a deep copy of the tile for restored state.
                    #move up
                    r_copy = self.r;
                    while(r_copy > 0):
                        if(r_copy == 1):
                            #move up by one tile
                            tiles = deepcopy(tiles_copy) 
                            tiles[i][j], tiles[i-1][j] = tiles[i-1][j], tiles[i][j];  
                            successor_states.append(tiles)
                            move = "D" + str(r_copy) + str(self.r + 1); # sequence of moves string builder
                            moves.append(move) # sequence of moves list
                            #move up by one tile
                        elif(r_copy == 2):
                            #move up by two tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i-1][j] = tiles[i-1][j], tiles[i][j]; 
                            tiles[i-1][j], tiles[i-2][j] = tiles[i-2][j], tiles[i-1][j]; 
                            successor_states.append(tiles);
                            move = "D" + str(r_copy) + str(self.r + 1);
                            moves.append(move)
                            #move up by two tiles
                        elif(r_copy == 3):
                            #move up by three tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i-1][j] = tiles[i-1][j], tiles[i][j]; 
                            tiles[i-1][j], tiles[i-2][j] = tiles[i-2][j], tiles[i-1][j]; 
                            tiles[i-2][j], tiles[i-3][j] = tiles[i-3][j], tiles[i-2][j];
                            successor_states.append(tiles);
                            move = "D" + str(r_copy) + str(self.r + 1);
                            moves.append(move)
                            #move up by three tiles
                        r_copy -= 1;
                        
                    #move down
                    r_copy = 3-self.r;
                    while(r_copy > 0):
                        if(r_copy == 1):
                            #move down by one tile
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i+1][j] = tiles[i+1][j], tiles[i][j]
                            successor_states.append(tiles)
                            move = "U" + str(r_copy) + str(self.r + 1);
                            moves.append(move)
                            #move down by one tile
                        elif(r_copy == 2):
                            #move down by two tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i+1][j] = tiles[i+1][j], tiles[i][j]; 
                            tiles[i+1][j], tiles[i+2][j] = tiles[i+2][j], tiles[i+1][j]; 
                            successor_states.append(tiles);
                            move = "U" + str(r_copy) + str(self.r + 1);
                            moves.append(move)
                            #move down by two tiles
                        elif(r_copy == 3):
                            #move down by three tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i+1][j] = tiles[i+1][j], tiles[i][j]; 
                            tiles[i+1][j], tiles[i+2][j] = tiles[i+2][j], tiles[i+1][j]; 
                            tiles[i+2][j], tiles[i+3][j] = tiles[i+3][j], tiles[i+2][j]; 
                            successor_states.append(tiles);
                            move = "U" + str(r_copy) + str(self.r + 1);
                            moves.append(move)
                            #move down by three tiles
                        r_copy -= 1;
                        
                    #move left
                    c_copy = self.c;
                    while(c_copy > 0):
                        if(c_copy == 1):
                            #move left by one tile
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i][j-1] = tiles[i][j-1], tiles[i][j];  
                            successor_states.append(tiles)
                            move = "R" + str(c_copy) + str(self.c + 1);
                            moves.append(move)
                            #move left by one tile
                        elif(c_copy == 2):
                            #move left by two tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i][j-1] = tiles[i][j-1], tiles[i][j]; 
                            tiles[i][j-1], tiles[i][j-2] = tiles[i][j-2], tiles[i][j-1]; 
                            successor_states.append(tiles);
                            move = "R" + str(c_copy) + str(self.c + 1);
                            moves.append(move)
                            #move left by two tiles
                        elif(c_copy == 3):
                            #move left by three tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i][j-1] = tiles[i][j-1], tiles[i][j]; 
                            tiles[i][j-1], tiles[i][j-2] = tiles[i][j-2], tiles[i][j-1]; 
                            tiles[i][j-2], tiles[i][j-3] = tiles[i][j-3], tiles[i][j-2];
                            successor_states.append(tiles);
                            move = "R" + str(c_copy) + str(self.c + 1);
                            moves.append(move)
                            #move left by three tiles
                        c_copy -= 1;
                        
                    #move right
                    c_copy = 3-self.c;
                    while(c_copy > 0):
                        if(c_copy == 1):
                            #move right by one tile
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i][j+1] = tiles[i][j+1], tiles[i][j]
                            successor_states.append(tiles)
                            move = "L" + str(c_copy) + str(self.c + 1);
                            moves.append(move)
                            #move right by one tile
                        elif(c_copy == 2):
                            #move right by two tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i][j+1] = tiles[i][j+1], tiles[i][j]; 
                            tiles[i][j+1], tiles[i][j+2] = tiles[i][j+2], tiles[i][j+1]; 
                            successor_states.append(tiles);
                            move = "L" + str(c_copy) + str(self.c + 1);
                            moves.append(move)
                            #move right by two tiles
                        elif(c_copy == 3):
                            #move right by three tiles
                            tiles = deepcopy(tiles_copy)
                            tiles[i][j], tiles[i][j+1] = tiles[i][j+1], tiles[i][j];
                            tiles[i][j+1], tiles[i][j+2] = tiles[i][j+2], tiles[i][j+1]; 
                            tiles[i][j+2], tiles[i][j+3] = tiles[i][j+3], tiles[i][j+2]; 
                            successor_states.append(tiles);
                            move = "L" + str(c_copy) + str(self.c + 1);
                            moves.append(move)
                            #move right by three tiles
                        c_copy -= 1;
                        
        return [successor_states, moves];
    
    # Checks whether current state is the goal state or not.
    def is_goal(self, successor_state):
        for i in range(len(successor_state)):
            for j in range(len(successor_state[0])):
                if(successor_state[i][j] != FINAL_CANONICAL_CONFIGURATION[i][j]):
                    return False;
                
        return True;
    
    # http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    # A utility function to count inversions in given tile(1-D)
    def get_inv_count(self, tile):
        inv_count = 0;
        for i in range(15):
            for j in range(i + 1, 16):
                #count pairs(i, j) such that i appears before j, but i > j.
                if (tile[j] and tile[i] and tile[i] > tile[j]):
                    inv_count += 1;
                    
        return inv_count;
    
    # http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    # find Position of blank from bottom starting from bottom-right corner of matrix
    def find_X_position(self, tile):
        for i in range(3, -1, -1):
            for j in range(3, -1, -1):
                if (tile[i][j] == 0):
                    return 4 - i;
                
    # http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    # This function returns true if given instance of 15 puzzle is solvable.
    def is_solvable(self, tile):
        #Count inversions in given puzzle
        tile_1D = [0 for elem in range(16)];
        for i in range(4):
            for j in range(4):
                tile_1D[4 * i + j] = tile[i][j]
                
        inv_count = self.get_inv_count(tile_1D);
     
        #If grid is odd, return true if inversion count is even.
        if (4 & 1):
            return not (inv_count & 1);
     
        else: #grid is even
            pos = self.find_X_position(tile);
            if(pos & 1):
                return not (inv_count & 1);
            else:
                return inv_count & 1;
    
    # Invokes the A-star algorithm to solve the 15 puzzle if it is solvable.
    def solve(self):
        if(self.is_solvable):
            return self.solve_A_star(self.initial_state, self.explored_set, self.moves, g_cost = 1);
    
    # A-star search finds the best promising state after each step based on min 'f'(g + h) value till the goal state is reached.    
    def solve_A_star(self, state, explored_state, moves, g_cost):
        # find row and column number of 'blank' tile.
        self.r, self.c = [(index, row.index(0)) for index, row in enumerate(state) if 0 in row][0]
        
        tmp = []
        successors = self.successors(state)[0];
        successors_moves = self.successors(state)[1];
        
        for cnt, s in enumerate(successors):
            if(self.is_goal(s)):
                explored_state.append(s);
                moves.append(successors_moves[cnt]);
                return 0;

            h_cost = self.manhattan_distance(s);
            tmp.append((s, successors_moves[cnt], g_cost + h_cost))
        
        # https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
        # next_promising_state is chosen based on min f_cost = g_cost + h_cost
        next_promising_state = sorted(tmp, key=lambda x: x[2])[0][0]
        explored_state.append(next_promising_state);
        moves.append(sorted(tmp, key=lambda x: x[2])[0][1]);
        # https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/
        g_cost += 1;
        
        # recursively iterate through promising states to reach the goal state
        self.solve_A_star(next_promising_state, explored_state, moves, g_cost) 
        
    #Returns a string that represents the output of the program.
    def __str__(self):
#         return ("\n".join(str(row) for row in self.explored_set[len(self.explored_set) - 1])) + "\n\nSEQUENCE OF MOVES:\n" +  (" ".join(self.moves))
        if(self.is_solvable):
            return ("SEQUENCE OF MOVES:\n" +  " ".join(self.moves));
        else:
            return ("PUZZLE NOT SOLVABLE");

def main():
    filename =  sys.argv[1];
    start_time = time.time();
    s = ShortSequence_Solver16(filename);
    s.solve()
    print("Time taken: {} secs".format(time.time() - start_time) + "\n\n" + str(s));
    
if(__name__ == "__main__"):
    main();