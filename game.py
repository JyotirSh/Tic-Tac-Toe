import pprint
from random import randrange
from copy import deepcopy

# ========================= All global reference variable ================================
pp_helper = pprint.PrettyPrinter()

moves = 0

current_player = 'X'
                    
state_grid = [['.','.','.'], ['.','.','.'], ['.','.','.']]

first_move = True

player_choosed_val = '.'

pos_reference_dict = {0: (0,0), 1:(0,1), 2:(0,2), 3:(1,0), 4:(1,1), 5:(1,2), 6:(2,0), 7:(2,1), 8:(2,2)}

rev_pos_reference_dict =  {(0,0):0, (0,1):1, (0,2):2, (1,0):3, (1,1):4, (1,2):5, (2,0):6, (2,1):7, (2,2):8}

imp_pos = {0, 2, 8, 6, 4}

taken_places_set = set()

# the following 4 are to check winners. If O picks then -1 to them and if X picks +1 to them
row = [0,0,0]

column = [0,0,0]

diagonal = 0

antidiagonal = 0

# =========================== All global reference variable ================================

def print_help_display():
    print("Reference for board numbers. See the position numbers corresponding to board")
    test_display = [[0,1,2],[3,4,5],[6,7,8]]
    for i in range(len(state_grid)):
        pp_helper.pprint(test_display[i])


def print_grid():
    print("Current State of Board:")
    for i in range(len(state_grid)):
        pp_helper.pprint(state_grid[i])


def toggle_player():
    '''
    This function takess in no parameter and just toggles the global reference variable current_player
    '''
    global current_player
    if current_player == 'X':
        current_player = 'O'
    else:
        current_player = 'X'


def get_next_possible_moves(board_current_state):
    """
    This function can be used to get free spaces and the number of free spaces.
    """
    free_positions_list = []
    for i in range(len(board_current_state)):
        for j in range(len(board_current_state[i])):
            if(board_current_state[i][j] == '.'):
                pos_tuple = (i,j)
                position_number = rev_pos_reference_dict[pos_tuple]
                free_positions_list.append(position_number)
    return free_positions_list


def random_position_pick():
    random_pick = randrange(9)
    taken_places_set.add(random_pick)
    x_val, y_val = pos_reference_dict[random_pick]
    state_grid[x_val][y_val] = current_player
    update_winning_params(x_val, y_val)
    
    
def ask_player_position_to_pick():
    global taken_places_set
    temp_position_storage = '.'
    print_help_display()
    while(True):
        print("Enter the position from (0-8) you want to occupy (not already taken): ")
        ip_val = (input())
        temp_position_storage = int(ip_val)
        if((temp_position_storage >= 0 and temp_position_storage <= 8) and temp_position_storage not in taken_places_set):
            taken_places_set.add(temp_position_storage)
            break
        print("Please enter a number which is valied and is not already occupied")
        
    x_val, y_val = pos_reference_dict[temp_position_storage]
    return x_val, y_val
    

def prompt_to_choose_player():
    global player_choosed_val
    temp_choice_storage = '.'
    
    while(True):
        temp_choice_storage = (str)(input("Enter your value (should be capital X or O(alphabet)): "))
        if(temp_choice_storage == 'X' or temp_choice_storage == 'O'):
            break
    player_choosed_val = temp_choice_storage


def update_winning_params(x_cor, y_cor):
    '''
    Always call if before toggle player function.
    '''
    global row
    global column
    global diagonal
    global antidiagonal
    global current_player
    
    gain_value = 0
    if current_player == 'X':
        gain_value = 1
    elif current_player == 'O':
        gain_value = -1
    
    row[x_cor] += gain_value
    column[y_cor] += gain_value
    if x_cor == y_cor:
        if x_cor == 1:
            antidiagonal += gain_value
        diagonal += gain_value
    if abs(x_cor - y_cor) == 2:
        antidiagonal += gain_value

def curr_game_state():
    global row
    global column
    global diagonal
    global antidiagonal
    for i in range(0, 3):
        if row[i] == 3 or column[i] == 3:
            return [True,'X']
        if row[i] == -3 or column[i] == -3:
            return [True,'O']
    if (diagonal == 3 or antidiagonal == 3):
        return [True,'X']
    elif (diagonal == -3 or antidiagonal == -3):
        return [True,'O']
    return [False, 'None'] #
    

def first_move_steps():
    global first_move
    global moves
    
    if(player_choosed_val == 'O'):
        random_position_pick()
    else:
        x_pos, y_pos = ask_player_position_to_pick()
        state_grid[x_pos][y_pos] = current_player  # board updated
        update_winning_params(x_pos, y_pos)
    toggle_player()
    first_move = False
    moves += 1
    print_grid()
    
    
def get_next_player(curr):
    if curr == 'X':
        return 'O'
    elif curr == 'O':
        return 'X'
    else:
        return None
        
def board_eval(b_copy):
    """
    Repetitive code can be fixed in next version.
    """
    row_l = [0,0,0]
    column_l = [0,0,0]
    diagonal_l = 0
    antidiagonal_l = 0
    for x_cor in range(3):
        for y_cor in range(3):
            if b_copy[x_cor][y_cor] != '.':
                gain_value = 0
                if b_copy[x_cor][y_cor] == 'X':
                    gain_value = 1
                elif b_copy[x_cor][y_cor] == 'O':
                    gain_value = -1
                
                row_l[x_cor] += gain_value
                column_l[y_cor] += gain_value
                if x_cor == y_cor:
                    if x_cor == 1:
                        antidiagonal_l += gain_value
                    diagonal_l += gain_value
                if abs(x_cor - y_cor) == 2:
                    antidiagonal_l += gain_value
    for i in range(0, 3):
        if row_l[i] == 3 or column_l[i] == 3:
            return [True,'X']
        if row_l[i] == -3 or column_l[i] == -3:
            return [True,'O']
    if (diagonal_l == 3 or antidiagonal_l == 3):
        return [True,'X']
    elif (diagonal_l == -3 or antidiagonal_l == -3):
        return [True,'O']
    return [False, 'None'] #
    
def heu_eval(board_ip, player):
    win_pos = [[ 0, 1, 2], [3, 4, 5 ], [ 6, 7, 8 ], [ 0, 3, 6 ], [ 1, 4, 7 ], [ 2, 5, 8 ], [ 0, 4, 8 ], [ 2, 4, 6 ]]
    Heuristic_Array = [[0, -10, -100, -1000 ], [10, 0, 0, 0 ], [100, 0, 0, 0], [1000, 0, 0, 0]]
    
    opponent = 'O'
    if player == 'X':
        opponent = 'O'
        
    piece = '.'
    players = 0
    others = 0
    t = 0
    for i in range(8):
      players = others = 0;
      for j in range(3):
        pos_x, pos_y = pos_reference_dict[win_pos[i][j]]
        piece = board_ip[pos_x][pos_y]
        if piece == player:
          players += 1
        elif piece == opponent:
          others += 1
      t += Heuristic_Array[players][others];
    return t;



def mini_max(board_copy, moves_t, max_player, player_calling_initial, curr_player):
    if (moves_t == 9):
        eval_check = board_eval(board_copy)
        if eval_check[0]:
            heu_val_total = 0
            if eval_check[1] == player_calling_initial:
                for val in imp_pos:
                    pos_x, pos_y = pos_reference_dict[val]
                    if board_copy[pos_x][pos_y] == player_calling_initial:
                        heu_val_total += 1000
                    elif board_copy[pos_x][pos_y] == get_next_player(player_calling_initial):
                        heu_val_total -= 1300
                heu_val_total += 25000
            elif eval_check[1] == get_next_player(player_calling_initial):
                for val in imp_pos:
                    pos_x, pos_y = pos_reference_dict[val]
                    if board_copy[pos_x][pos_y] == get_next_player(player_calling_initial):
                        heu_val_total -= 19000
                    elif board_copy[pos_x][pos_y] == player_calling_initial:
                        heu_val_total += 1200
                heu_val_total -= 26000
            return [heu_val_total,-1]
        else:
            val_heu_computed = heu_eval(board_copy,player_calling_initial)
            return [val_heu_computed, -1]  # A Draw
    
    list_of_next_moves = get_next_possible_moves(board_copy)
    
    eval_check = board_eval(board_copy)
    if eval_check[0]:
        heu_val_total = 0
        if eval_check[1] == player_calling_initial:
            for val in imp_pos:
                pos_x, pos_y = pos_reference_dict[val]
                if board_copy[pos_x][pos_y] == player_calling_initial:
                    heu_val_total += 1000
                elif board_copy[pos_x][pos_y] == get_next_player(player_calling_initial):
                    heu_val_total -= 1300
            heu_val_total += 25000
            heu_val_total += (50*len(list_of_next_moves))
        elif eval_check[1] == get_next_player(player_calling_initial):
            for val in imp_pos:
                pos_x, pos_y = pos_reference_dict[val]
                if board_copy[pos_x][pos_y] == get_next_player(player_calling_initial):
                    heu_val_total -= 19000
                elif board_copy[pos_x][pos_y] == player_calling_initial:
                    heu_val_total += 1200
            heu_val_total -= 26000
            heu_val_total -= (500*len(list_of_next_moves))
        return [heu_val_total,-1]
        
    
    opt_val = 993837633
    if(max_player):
        opt_val = -2344422343
    
    optimal_move = None
    next_player = get_next_player(curr_player)
    
    for moves in list_of_next_moves:
        pos_x, pos_y = pos_reference_dict[moves]
        board_copy[pos_x][pos_y] = curr_player
        
        if max_player is True:
            ret_list = mini_max(board_copy, moves_t+1, False, player_calling_initial, next_player)
            if(ret_list[0] > opt_val):
                opt_val = ret_list[0]
                optimal_move = moves
        else:
            ret_list = mini_max(board_copy, moves_t+1, True, player_calling_initial, next_player)
            if(ret_list[0] < opt_val):
                opt_val = ret_list[0]
                optimal_move = moves
        
        board_copy[pos_x][pos_y] = '.'
    
    return [opt_val, optimal_move]

def start_moves():
    global first_move
    global moves
    
    if(first_move):
        first_move_steps()
        
    while(moves <= 8):
        if current_player == player_choosed_val:
            x_pos, y_pos = ask_player_position_to_pick()
            state_grid[x_pos][y_pos] = current_player  # board updated
            update_winning_params(x_pos, y_pos)
        else:
            # use minimax/alpha beta pruning
            print("Opponet Played his turn ===============================>")
            new_copy_board = deepcopy(state_grid)
            best_move = mini_max(new_copy_board, moves, True, current_player, current_player)
            pos_bx, pos_by = pos_reference_dict[best_move[1]]
            taken_places_set.add(best_move[1])
            state_grid[pos_bx][pos_by] = current_player
            update_winning_params(pos_bx, pos_by)
        
        print_grid()
        winner_list = curr_game_state() # gets the winner
        if winner_list[0] is True:
            print("someone WON!!! ",winner_list[1])
            return (True, winner_list[1])
        toggle_player()
        moves += 1
    
    return (False, "Draw")

def game_start():
    prompt_to_choose_player()
    win_flag, message = start_moves()
    if not win_flag:
        print("OOPS!! The game is DRAWN")

game_start()
