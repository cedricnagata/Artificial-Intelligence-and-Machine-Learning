import time
import random 
import io

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        pass

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 
    def move(self, a, b, a_fin, b_fin, t):
        # *****NAIVE MODEL*****
        # For test only: return a random move
        # r = []
        # for i in range(6):
        #     if a[i] != 0:
        #         r.append(i)
        # return r[random.randint(0, len(r)-1)]
        # *********************
        
        #Comment all the code above and start your code here

        # get start state and child moves
        start_state = self.state(a, b, a_fin, b_fin)
        children = self.get_child_moves(start_state)

        # initialize best score and move
        best_move = int()
        best_score = -10000

        # iterate through child moves
        for move in children:
            curr_state = self.state(a, b, a_fin, b_fin) # get state

            # get move state
            move_state, move_again = self.get_lookahead_state(curr_state, move)

            # run minimax taking move again into account
            if move_again:
                move_score = self.minimax(1, move_state, True, -10000, 10000)
            else:
                move_score = self.minimax(1, move_state, False, -10000, 10000)

            # update best move and score for MAX
            if (move_score > best_score):
                best_score = move_score
                best_move = move

        return best_move # return best move
    
    # Minimax algorithm function with alpha beta pruning.
    # Set to search up to depth of 9 
    # 
    # Paramters:
    #   - self
    #   - depth for depth of search
    #   - state for current state of search
    #   - isMax to determine max or min level
    #   - alpha value for alpha cutoff
    #   - beta value for beta cutoff
    #   - start for start time of move
    #   - t for elaped time
    # Returns:
    #   - best heuristic evaluation of each state of path at each depth
    def minimax(self, depth, state, isMax, alpha, beta):
        
        # if depth reached or time up, return heuristic utility score
        if (depth >= 9) or self.is_win_state(state):
            return self.heuristic_score(state)
        
        if isMax == True: # if maximizing player
            best = -1000
            children = self.get_child_moves(state) # get child moves

            for move in children: # iterate child moves

                # get move state
                move_state, move_again = self.get_lookahead_state(state, move)

                # recursively call minimax based on move again for min or max
                val = None
                if move_again:
                    val = self.minimax(depth + 1, move_state, True, alpha, beta)
                else:
                    val = self.minimax(depth + 1, move_state, False, alpha, beta)

                # get best max value and set alpha value
                best = max(best, val)
                alpha = max(alpha, best)

                # compare alpha and beta for pruning
                if beta <= alpha:
                    break
            return best # return best move val
        else:
            best = 1000
            opp_state = self.get_opponent_state(state) # get opposing state
            children = self.get_child_moves(opp_state) # get child moves for opposing state

            for move in children: # iterate child moves

                # get move state
                move_state, move_again = self.get_lookahead_state(opp_state, move)

                # recursively call minimax based on move again for min or max
                val = None
                if move_again:
                    val = self.minimax(depth + 1, self.get_opponent_state(move_state), False, alpha, beta)
                else:
                    val = self.minimax(depth + 1, self.get_opponent_state(move_state), True, alpha, beta)

                # get best min value and set beta value
                best = min(best, val)
                beta = min(beta, best)

                # compare alpha and beta for pruning
                if float(beta) <= alpha:
                    break
            return best # return best move val

    # function to get future state from one move
    # (inspired from updateLocalState function in main.py)
    # 
    # Paramters:
    #   - self
    #   - state for state to get future state from
    #   - move for move to get future state with
    # Returns:
    #   - future state from move
    def get_lookahead_state(self, state, move):
        # get all states of board, overall stones in play
        ao = state.a[:]
        all = state.a[move:] + [state.a_fin] + state.b + state.a[:move]
        count = state.a[move]
        all[0] = 0
        p = 1

        # add to board states while looping through stones in play
        while count > 0:
            all[p] += 1
            p = (p + 1) % 13
            count -= 1

        # add to pots
        state.a_fin = all[6 - move]
        state.b = all[7 - move:13 - move]
        state.a = all[13 - move:] + all[:6-move]
        cagain = bool()
        ceat = False

        # check move again condition
        p = (p - 1) % 13
        if p == 6 - move:
            cagain = True
        if p <= 5 - move and ao[move] < 14:
            id = p + move
            if (ao[id] == 0 or p % 13 == 0) and state.b[5 - id] > 0:
                ceat = True
        elif p >= 13 - move and ao[move] < 14:
            id = p + move - 13
            if (ao[id] == 0 or p % 13 == 0) and state.b[5 - id] > 0:
                ceat = True
        
        # check steal stones condition
        if ceat:
            state.a_fin += state.b[5-id]+1
            state.b[5-id] = 0 
            state.a[id] = 0
        if sum(state.a)==0:
            state.b_fin += sum(state.b)
        if sum(state.b)==0:
            state.a_fin += sum(state.a)

        return state, cagain # return new state and move again condition
    
    # function to heuristically evaluate a state
    # Heuristics:
    #   - h1: difference between stones in each kalah, includes weight multiplier 
    #         as game goes on and stones are no longer in play
    #   - h2: number of stones in play on player's side
    #   - h3: number of stones in play on opponent's side
    #   - h4: number of non-empty pits on players side
    #   - h5: number of non-empty pits on opponent's side
    #   - Game over heuristics for each player (1000 or -1000)
    #   - Tie game heuristic (0)
    # Paramters:
    #   - state to evaluate using heuristic function
    # Returns:
    #   - Sum of all heuristic values or game over/tie value
    def heuristic_score(self, state):
        # get pots
        a_pot = state.a_fin
        b_pot = state.b_fin

        # difference between stones in each kalah,
        # includes weight multiplier as game goes on and stones
        # are no longer in play
        weight = 1 + ((a_pot + b_pot) / 72)
        h1 = (a_pot - b_pot) * weight

        h2 = 0 # number of stones in play on player's side
        h3 = 0 # number of stones in play on opponent's side
        h4 = 0 # number of non-empty pits on players side
        h5 = 0 # number of non-empty pits on opponent's side
        
        for i in state.a:
            h2 = h2 + i
            if (i > 0):
                h4 += 1

        for i in state.b:
            h3 = h3 - i
            if (i > 0):
                h5 -= 1
        
        # heuristic for game over situation with 
        # more than half of stones in one pot
        if (a_pot > 36):
            return 1000
        if (b_pot > 36):
            return -1000

        # heuristic for tie game situation
        if h2 == 0 and h3 == 0 and a_pot == b_pot:
            return 0

        # return sum of heuristics
        return h1 + h2 + h3 + h4 + h5

    # function to get opponents respective state from a state
    # 
    # Paramters:
    #   - self
    #   - state to get opponent state from
    # Returns:
    #   - input state but from opponents perspective 
    def get_opponent_state(self, state):
        # return flipped state
        return self.state(state.b, state.a, state.b_fin, state.a_fin)
    
    # function to get child moves from a state
    # 
    # Paramters:
    #   - self
    #   - state to get child moves from
    # Returns:
    #   - list of child moves from state
    def get_child_moves(self, state):
        children = []
        # append child move to list if it has stones in it
        for i in range(6):
            if state.a[i] != 0:
                children.append(i)
        return children

    # function to check if state is a win state
    # 
    # Paramters:
    #   - self
    #   - state to check win condition
    # Returns:
    #   - True if state is a win for either player or tie
    def is_win_state(self, state):
        if (state.a_fin > 36 or 
            state.b_fin > 36 or 
            (state.a_fin == 36 and state.b_fin == 36)):
            return True
        else:
            return False
