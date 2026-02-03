player_1 = []
player_2 = []

winning_combinations = [
    [1,2,3],[4,5,6],[7,8,9],    #rows_wise
    [1,4,7],[2,5,8],[3,6,9],    #column_wise
    [1,5,9],[3,5,7]             #diagonal_wise 
]

board = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]

def print_board():
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("---------")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("---------")
    print(board[6] + " | " + board[7] + " | " + board[8] + "\n")

def check_winner(winner):
    for arr in winning_combinations:
        for arr2 in arr:
            if arr2 not in winner:
                break
        else:
            return True
    return False

def player_move(i):
    while (True):
        eval = input(f"Player {i} - Enter your move from 1 to 9: ")
        try:
            move = int(eval)
            if (move >= 1 and move <= 9):
                if move in player_1 + player_2:
                    print("Position already taken! Try a different one.")
                    continue
                if (i == 1):
                    player_1.append(move)  
                    board[move - 1] = "x"
                else:
                    player_2.append(move)
                    board[move - 1] = "o"
                print()
                print_board()
                break
            else:
                print("Number must be between 1 and 9.")
        except ValueError:
            print("Please enter a number.")
            
def game():
    print("\nWelcome to Tic Tac Toe! Have fun!\n")
    print_board()
    i = 1
    while (True):
        i += 1
        if (i % 2 == 0):
            player_move(1)
            if (check_winner(player_1)):
                print("Congratulations, Player 1! You win!")
                break
        elif (i < 11):
            player_move(2)
            if (check_winner(player_2)):
                print("Congratulations, Player 2! You win!")
                break
        else:
            print("Draw.\n") 
            break

# begin game
game()