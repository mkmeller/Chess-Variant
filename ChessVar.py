# Author: Mike Meller
# GitHub username: mkmeller
# Date: 8/3/2023
# Description:  Implementation of a variant on chess, pieces move like in chess. Objective is for the king to reach the top row.
#               If the two kings reach the top row within one turn of each other, its a tie. Otherwise, whoever reached it first wins.
#               King can never be put in check.


class Piece:
    '''Class to represent a chess piece, either black or white'''

    def __init__(self, color : str):
        #Color is either white or black
        self._color = color
        self._jumper = False
        self._king = False

    def is_king(self):
        '''Return whether this piece is a king'''
        return self._king

    def get_color(self):
        '''Return what color this piece is'''
        return self._color
    
    def can_jump(self) -> bool:
        '''Return whether this piece moves by jumping'''
        return self._jumper

class King(Piece):
    '''The king piece, subclass of a chess piece. Can move one square away from current square.'''

    def __init__(self, color):
        super().__init__(color)
        #Only a king cannot be attacked
        self._king = True

    def __repr__(self) -> str:
        '''Allows printing the symbol for this piece'''
        if self._color == 'w':
            return '♔'
        elif self._color == 'b':
            return '♚'
        else:
            return '?'
        
    def valid_move(self, current : str,  next : str) -> bool:
        '''Check if moving from current to next position is possible for this piece'''
        current_file = current[0]
        current_rank = current[1]

        next_file = next[0]
        next_rank = next[1]

        #Can move at most one file
        if abs(ord(current_file) - ord(next_file)) > 1:
            return False

        #Can move at most one rank
        if abs(int(current_rank) - int(next_rank)) > 1:
            return False
        
        return True
     
class Knight(Piece):
    '''The knight piece, subclass of a chess piece. Moves in an L with 2 squares along file or rank, then one square perpendicular. Jumps over any pieces.'''

    def __init__(self, color):
        super().__init__(color)
        #Knight can jump over pieces
        self._jumper = True

    
    def __repr__(self) -> str:
        '''Allows printing the symbol for this piece'''
        if self._color == 'w':
            return '♘'
        elif self._color == 'b':
            return '♞'
        else:
            return '?'

    def valid_move(self, current : str,  next : str) -> bool:
        '''Check if moving from current to next position is possible for this piece'''
        current_file = current[0]
        current_rank = current[1]

        next_file = next[0]
        next_rank = next[1]

        if abs(ord(current_file) - ord(next_file)) != 2 and abs(int(current_rank) - int(next_rank)) != 2:
            return False

        #If we moved 2 squares along file, we must move 1 square along rank
        if abs(ord(current_file) - ord(next_file)) == 2 and abs(int(current_rank) - int(next_rank)) != 1:
            return False
        
        #If we move 2 squares along rank, we must move 1 square along file
        if abs(ord(current_file) - ord(next_file)) != 1 and abs(int(current_rank) - int(next_rank)) == 2:
            return False
        
        return True

class Bishop(Piece):
    '''The bishop piece, subclass of a chess piece. Can move any distance along its diagonals.'''

    def __init__(self, color):
        super().__init__(color)

    def __repr__(self) -> str:
        '''Allows printing the symbol for this piece'''
        if self._color == 'w':
            return '♗'
        elif self._color == 'b':
            return '♝'
        else:
            return '?'
        
    def valid_move(self, current : str,  next : str) -> bool:
        '''Check if moving from current to next position is possible for this piece'''
        current_file = current[0]
        current_rank = current[1]

        next_file = next[0]
        next_rank = next[1]

        #Change in file must equal change in rank
        if abs(ord(current_file) - ord(next_file)) != abs(int(current_rank) - int(next_rank)):
            return False
        
        return True

class Rook(Piece):
    '''The rook piece, subclass of a chess piece. Can move any distance along its file or along its rank.'''

    def __init__(self, color):
        super().__init__(color)

    def __repr__(self) -> str:
        '''Allows printing the symbol for this piece'''
        if self._color == 'w':
            return '♖'
        elif self._color == 'b':
            return '♜'
        else:
            return '?'

    def valid_move(self, current : str,  next : str) -> bool:
        '''Check if moving from current to next position is possible for this piece'''
        current_file = current[0]
        current_rank = current[1]

        next_file = next[0]
        next_rank = next[1]

        #Rook cannot move across a file and rank simltaneously
        if current_file != next_file and current_rank != next_rank:
            return False
        
        return True

class ChessVar:
    '''Represents an abstract board game, a variant of chess. Makes use of piece objects.'''

    def __init__(self):
        #Dictionary to map squares on the board to pieces. Key = square, value = piece
        self._board = {}
        self._board_size = 8
        #State of the game at start
        self._turn = 'w'
        #Flag whether the game should end this turn
        self._game_end_imminent = False
        self._state = 'UNFINISHED'

        #Setup the default position
        self.setup_default_start_pos()

    def get_turn(self):
        '''Return which players turn it is'''
        return self._turn

    def get_game_state(self) -> str:
        '''Return a string, current state of the game'''
        return self._state
    
    def get_board_size(self) -> int:
        '''Return the length of the board as an int. Assume board is square.'''
        return int(self._board_size)
 
    def setup_custom_position(self) -> None:
        '''Function to setup custom positions for testing'''

        #Start position, white pieces
        self.spawn_piece('king'  , 'g7','w' )
        self.spawn_piece('rook'  , 'a2','w' )
        self.spawn_piece('bishop', 'b1','w' )
        self.spawn_piece('bishop', 'b2','w' )
        self.spawn_piece('knight', 'c1','w' )
        self.spawn_piece('knight', 'c2','w' )
        #Start position, black pieces
        self.spawn_piece('king'  , 'b7','b' )
        self.spawn_piece('rook'  , 'h2','b' )
        self.spawn_piece('bishop', 'g1','b' )
        self.spawn_piece('bishop', 'g2','b' )
        self.spawn_piece('knight', 'f1','b' )
        self.spawn_piece('knight', 'f2','b' )

    def setup_default_start_pos(self) -> None:
        '''Add all the pieces to the board to achieve the default starting position'''

        #Start position, white pieces
        self.spawn_piece('king'  , 'a1','w' )
        self.spawn_piece('rook'  , 'a2','w' )
        self.spawn_piece('bishop', 'b1','w' )
        self.spawn_piece('bishop', 'b2','w' )
        self.spawn_piece('knight', 'c1','w' )
        self.spawn_piece('knight', 'c2','w' )
        #Start position, black pieces
        self.spawn_piece('king'  , 'h1','b' )
        self.spawn_piece('rook'  , 'h2','b' )
        self.spawn_piece('bishop', 'g1','b' )
        self.spawn_piece('bishop', 'g2','b' )
        self.spawn_piece('knight', 'f1','b' )
        self.spawn_piece('knight', 'f2','b' )

    def spawn_piece(self, piece : str, square : str, color : str) -> bool:
        '''
        Add pieces to the board, if adding a piece to a square where a piece exists, it is overwrritten.
        Piece must be: knight, king, bishop, rook
        Square must be within the confines of the board
        Color must be: b or w
        If an invalid name for a piece is given, do nothing and return False. Otherwise return True
        '''

        if piece.lower() == 'knight':
            self._board[square.lower()] = Knight(color)
            return True
        if piece.lower() == 'king':
            self._board[square.lower()] = King(color)
            return True
        if piece.lower() == 'bishop':
            self._board[square.lower()] = Bishop(color)
            return True
        if piece.lower() == 'rook':
            self._board[square.lower()] = Rook(color)
            return True
    
        return False
            
    def get_piece_at_square(self, board : dict, square : str) -> object:
        '''Return the piece located at the specified square on the given board, return None if no piece is there'''

        if square not in board:
            return None
        else:
            return board[square]

    def is_valid_square(self, square : str) -> bool:
        '''
        Return whether the specified square is within the confines of a board of board_size x board_size
        Columns are characters starting from 'a' and increasing alphabetically
        Rows are numbers starting from board_size and descending to 1
        '''
        
        if not 97 <= int(ord(square[0])) <= 97 + self._board_size - 1 or not 1 <= int(square[1]) <= self._board_size:
            return False
        
        return True
        
    def change_turns(self) -> None:
        '''Change whether its white or blacks turn when a move completes. Increment the move counter. Return None'''
        if self._turn == 'w':
            self._turn = 'b'
        elif self._turn == 'b':
            self._turn = 'w'
        
    def get_squares_between(self, curr_square : str, new_square : str) -> list:
        '''
        Generate a list of all the squares that occur between the two input squares.
        If the two supplied squares are not along the same rank, file, or diagonal, returns empty.
        Used by can_make_move to check for any pieces that might be blocking the movement.
        '''

        intermediates = []

        #Convert both coordinates to numbers
        curr_file = ord(curr_square[0])
        new_file = ord(new_square[0])
        curr_rank = int(curr_square[1])
        new_rank = int(new_square[1])
      
        #Calculate the displacement in squares among file and rank projections
        delta_file = abs(curr_file - new_file)
        delta_rank = abs(curr_rank - new_rank)

        #If no displacement in file, all displacement in rank
        if delta_file == 0:
            #Add the file to all the ranks between the two endpoints
            for nums in range(min(curr_rank, new_rank) + 1, max(curr_rank, new_rank)):
                intermediates.append(chr(curr_file) + str(nums))

        #If no dispalcement in rank, all dispalcement in file
        elif delta_rank == 0:
            #Add the rank to all the files between the two endpoints
            for chars in range(min(curr_file, new_file) + 1, max(curr_file, new_file)):
                intermediates.append(chr(chars) + str(curr_rank))

        #If equal displacement in rank and file, this is a diagonal move
        elif delta_file == delta_rank:
            #Combine each file between the two endpoints with each rank between the two endpoints, order matters
            chars = []
            nums = []
            for num in range(min(curr_rank, new_rank) + 1, max(curr_rank, new_rank)):
                nums.append(str(num))
            #If we are descending in rank, our list needs to be reversed
            if new_rank < curr_rank:
                nums.reverse()

            for char in range(min(curr_file, new_file) + 1, max(curr_file, new_file)):
                chars.append(chr(char))
            #If we are descending in file, our list needs to be reversed
            if new_file < curr_file:
                chars.reverse()

            intermediates = [chars[idx] + nums[idx] for idx in range(len(chars))]

        return intermediates
    
    def locate_kings(self, board : dict) -> tuple:
        '''Returns a tuple with the square the white king is on followed by the square the black king is on'''

        for square, piece in board.items():
            if piece.is_king() and piece.get_color() == 'b':
                black_king = square
            if piece.is_king() and piece.get_color() == 'w':
                white_king = square

        return (white_king, black_king)

    def results_in_check(self, curr_square : str, new_square : str) -> bool:
        '''
        Takes as input two squares and returns whether completing the movement from first to second would result in a check being given to either king.
        A check is when any piece of opposite color can legally move to the position of a king.
        '''

        #Let the move happen on a copy of our board
        hypothetical_board = self._board.copy()
        moving_piece = self.get_piece_at_square(self._board, curr_square)
        del hypothetical_board[curr_square]
        hypothetical_board[new_square] = moving_piece

        #Locate the square of both kings on the hypothetical board
        white_king_square, black_king_square = self.locate_kings(hypothetical_board)

        #If an opposite color piece can legally move to the square of either king on the hypothetical board, a check was given, return True
        for square, piece in hypothetical_board.items():
            if piece.get_color() == 'b':
                if self.can_make_move(hypothetical_board, square, white_king_square, hypothetical_position = True):
                    return True
            if piece.get_color() == 'w':
                  if self.can_make_move(hypothetical_board, square, black_king_square, hypothetical_position = True):
                    return True                  
                
        return False

    def can_make_move(self, board : dict, curr_square : str, new_square : str, hypothetical_position : bool = False) -> bool:
        '''
        Takes as input a chess board and two squares. Returns whether a move by the piece at the first square can legally be made to the second square.
        The "hypothetical_position" parameter is set to false by default so all checks are performed. Calling this function with this parameter as True results in some checks being skipped.
        Utilizes is_valid_square, get_piece_at_square, get_squares_between, and results_in_check methods.
        '''

        moving_piece = self.get_piece_at_square(board, curr_square)

        #Only allow moves as long as game is not over
        if not self._state == 'UNFINISHED':
            return False

        #A piece must exist on the first square
        if not moving_piece:
            return False

        #Check that the moving piece belongs to the turn-owner, only done on non-hypothetical positions
        if hypothetical_position == False:
            if moving_piece.get_color() != self._turn:
                return False

        #Check that new square is on the board
        if not self.is_valid_square(new_square):
            return False           

        #Check that the required trajectory is possible for this type of piece 
        if not moving_piece.valid_move(curr_square, new_square):
            return False
        
        #If there is a piece at the target square, it should be of opposite color for a capture to occur
        if self.get_piece_at_square(board, new_square):
            if self.get_piece_at_square(board, new_square).get_color() == moving_piece.get_color():
                return False
                  
        #Check whether there are pieces blocking the path for this move, only for pieces that cannot jump
        if not moving_piece.can_jump():
            for intermediate_square in self.get_squares_between(curr_square, new_square):
                if intermediate_square in board:
                    return False
                
        #Check whether this move results in a check being given, only done on non-hypothetical positions since we only want look one move into the future, not forever
        if hypothetical_position == False:
            if self.results_in_check(curr_square, new_square):
                return False    
                
        #If we make it past all the above conditions, the move is possible
        return True
           
    def at_highest_rank(self, square : str) -> bool:
        '''Returns whether the given square is on the highest rank'''

        if int(square[1]) == self._board_size:
            return True
        
        return False

    def update_game_state(self) -> bool:
        '''
        Returns whether the game is over. 
        If black king made it to finish line, game is over.
        If white king made it to the finish line, one more turn is allowed for black to draw the game.
        '''

        #Locate the kings on the board
        white_king_square, black_king_square = self.locate_kings(self._board)

        #If black king is at the finish and white king isnt, black wins
        if self.at_highest_rank(black_king_square) and not self.at_highest_rank(white_king_square):
            self._state = 'BLACK_WON'
            return True
        
        #If both kings are at the finish, tie
        elif self.at_highest_rank(black_king_square) and self.at_highest_rank(white_king_square):
            self._state = 'TIE'
            return True
        
        #If white king is at the finish, black gets one more turn
        elif self.at_highest_rank(white_king_square) and not self._game_end_imminent:
            self._game_end_imminent = True
            return False
        
        #If white king is at the finish and black didnt reach the finish, white wins
        elif self.at_highest_rank(white_king_square) and self._game_end_imminent:
            self._state = 'WHITE_WON'
            return True
        
        #If no king is at the finish, game continues
        else:
            return False
              
    def make_move(self, curr_square : str, new_square : str) -> bool:
        '''
        Attempt to execute a game move. Takes as input two squares on the board. 
        If there is a piece on the first square, move it to the second square if this is legal, return True, and call change_turns.
        Otherwise, return False.
        '''
        if self.can_make_move(self._board, curr_square, new_square):
            moving_piece = self.get_piece_at_square(self._board, curr_square)
            del self._board[curr_square]
            self._board[new_square] = moving_piece
            self.change_turns()
            self.update_game_state()
            return True
        else:
            return False    

    def draw_board(self):
        '''Prints out a representation of the chess board and all existing pieces '''
        print('\n')

        for row in range(self._board_size):
            #Label the rows
            print(self._board_size - row, end = "")
            for columns in range(self._board_size):
                #Draw the board edge on the left
                print('|', end = "")

                #Calculate what square on the board this row + column corresponds to
                square = chr(columns + 97) + str(8 - row)
                #If there is a piece on this square, print it
                if square in self._board:
                        print(f'{self._board[square]}', end= "")
                #Otherwise print a blank
                else:
                    print('_', end = "")
            #Draw the board edge on the righgt
            print('|')

        print('  ', end = "")
        #Label the columns
        for char in range(97, 97 + self._board_size):
            print(f'{chr(char)} ', end = "")
        print("")
            
class ChessUI:
    '''Class to act as a user interface for ChessVar so user can dynamically play the game through the terminal.'''

    def __init__(self):
        self._engine = ChessVar()
        self._rules = '''
This game is a variant on chess. All pieces move and capture like they do in chess.
The objective of the game is to put your king on the highest rank (row). If black makes it there first, they win.
If white makes it there first, black gets one move in which they can draw the game.
Unlike chess, no move that would result in a check being given to either king is allowed. Thus, no checkmates.
            '''

    def welcome_message(self) -> None:
        '''Display a message with the game rules and objective at start. Wait for user to aknowledge. Return None'''

        print(self._rules)
        input('Press enter to start the game ')

    def turn_string(self) -> str:
        '''Returns a string stating whose turn it is.'''
        if self._engine.get_turn() == 'w':
            return "White to move"
        if self._engine.get_turn() == 'b':
            return "Black to move"

    def winner_string(self) -> str:
        '''Returns a string stating who the game winner is.'''
        if self._engine.get_game_state() == 'WHITE_WON':
            return 'White won. Thanks for playing.'
        elif self._engine.get_game_state() == 'BLACK_WON':
            return 'Black won. Thanks for playing.'
        elif self._engine.get_game_state() == 'TIE':
            return 'Draw. Thanks for playing.'

    def valid_entry(self, square : str) -> bool:
        '''Determine if user entered a legitimate square on the game board'''

        if len(square) != 2:
            return False
        
        #The file must be within (a, a + board_size)
        if square[0] not in [chr(ascii_val) for ascii_val in range(97, 97 + self._engine.get_board_size())]:
            return False
        
        #The rank must be within (1, board_size)
        if square[1] not in [str(num) for num in range(1, 1 + self._engine.get_board_size())]:
            return False
        
        return True

    def display_current(self, message : str) -> None:
        '''Displays the current game board and a message on the current game state to the user. Returns None'''
        import os

        #Clear the terminal for clean slate
        os.system('CLS')
        self._engine.draw_board()
        print(message)

    def user_to_move(self) -> None:
        '''
        Get input from the user on what move they want to make. 
        Repeats collecting input until the entered move is valid.
        Returns None
        '''

        valid_move = False

        while valid_move == False:
            source = input('Which piece? ')
            end = input('To where? ')

            if self.valid_entry(source) and self.valid_entry(end):
                valid_move = self._engine.make_move(source, end)

            if valid_move == True:
                return
            else:
                self.display_current(self.turn_string() + '. Move was invalid, try again.')

    def main(self) -> None:
        '''Main loop to keep asking user for moves as long as game is not finished. Returns None.'''

        self.welcome_message()

        #Game keeps going until there is a winner(s)
        while self._engine.get_game_state() == 'UNFINISHED':
            self.display_current(self.turn_string())
            self.user_to_move()

        #If game is over, display winner and exit
        self.display_current(self.winner_string())
        return
        
if __name__ == '__main__':
    start_game = ChessUI()
    start_game.main()


