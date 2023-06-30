from const import *
from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.last_move = None
        

    
    

    def move(self, piece, move,test=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].is_empty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not test:
                    sound = Sound(
                        os.path.join('assets/sounds/capture.wav'))
                    sound.play()
            
            # pawn promotion
            else:
                self.check_promotion(piece, final)
        
        if isinstance(piece,King):
            if self.castling(initial,final) and not test:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True

        piece.clear_moves()
        self.last_move = move

        

    


    def valid_move(self,piece,move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def castling(self,initial,final):
        return abs(initial.col - final.col) == 2
    
    
    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True
    
   



    def in_check(self,piece,move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece,move,test=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.cal_moves(p, row, col,bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False


    def cal_moves(self,piece,row,col,bool=True):

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        
                        move = Move(initial, final)
                        
                        
                        if bool:
                            if not self.in_check(piece, move):
                                
                                piece.add_move(move)
                            else: break
                        else:
                            
                            piece.add_move(move)
        
        
        def pawn_moves():
           
            steps = 1 if piece.moved else 2

            
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        
                        move = Move(initial, final)

                        
                        if bool:
                            if not self.in_check(piece, move):
                               
                                piece.add_move(move)
                        else:
                           
                            piece.add_move(move)
                   
                    else: break
                
                else: break

            
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        
                        move = Move(initial, final)
                        
                        
                        if bool:
                            if not self.in_check(piece, move):
                                
                                piece.add_move(move)
                        else:
                            
                            piece.add_move(move)

            
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
           
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                           
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                           
                            move = Move(initial, final)
                            
                            
                            if bool:
                                if not self.in_check(piece, move):
                                   
                                    piece.add_move(move)
                            else:
                                
                                piece.add_move(move)
            
            
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            
                            move = Move(initial, final)
                            
                           
                            if bool:
                                if not self.in_check(piece, move):
                                    
                                    piece.add_move(move)
                            else:
                                
                                piece.add_move(move)



        def straightline_moves(incrs):

            
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:

                    if Square.in_range(possible_move_row,possible_move_col):

                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row,possible_move_col,final_piece)

                        move = Move(initial,final)

                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            if bool:
                                if not self.in_check(piece,move):

                                    piece.add_move(move)
                                
                            else:
                                piece.add_move(move)

                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece,move):

                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            
                            break
                    else:
                        break
                        
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), (row-1, col+1), (row-1, col-1),
                (row+0, col+1), (row+0, col-1),
                (row+1, col+0), (row+1, col+1), (row+1, col-1)
            ]

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        initial = Square(row,col)
                        
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial,final)

                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_move(move)
                        else:         
                            piece.add_move(move)
            
            if not piece.moved:
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                piece.left_rook = left_rook
                                initial = Square(row,0)
                                final = Square(row,3)
                                moveR = Move(initial,final)
                                

                                initial = Square(row,col)
                                final = Square(row,2)
                                moveK = Move(initial,final)
                               
                                if bool:
                                    if not self.in_check(piece,move):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                    else:
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                
                                

                                

                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                
                                piece.right_rook = right_rook

                                
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial,final)
                                

                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial,final)
                                
                                if bool:
                                    if not self.in_check(piece,move):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                    else:
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                


            
        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece,Knight): 
            knight_moves()

        elif isinstance(piece,Bishop):
            straightline_moves([
                (-1,1), (-1, -1), (1,-1),(1, 1)
            ])

        elif isinstance(piece,Rook):
            straightline_moves([
                (-1, 0), (0, 1), (0, -1), (1, 0)
            ])

        elif isinstance(piece,Queen):
            straightline_moves([
                (-1,1), (-1, -1), (1,-1),(1, 1),(-1, 0), (0, 1), (0, -1), (1, 0)
            ])

        elif isinstance(piece,King):
            king_moves()





    def _create(self):
        
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)


    def _add_pieces(self, color):
        
        row_pawn, row_piece = (6, 7) if color == "white" else (1, 0)

        # pawn
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        

        #knight
        self.squares[row_piece][1] = Square(row_piece,1,Knight(color))
        self.squares[row_piece][6] = Square(row_piece,6,Knight(color))

        # bishop
        self.squares[row_piece][2] = Square(row_piece,2,Bishop(color))
        self.squares[row_piece][5] = Square(row_piece,5,Bishop(color))   

        

        #rook
        self.squares[row_piece][0] = Square(row_piece,0,Rook(color))
        self.squares[row_piece][7] = Square(row_piece,7,Rook(color))

       

        #queen
        self.squares[row_piece][3] = Square(row_piece,3,Queen(color))
        

        #king
        self.squares[row_piece][4] = Square(row_piece,4,King(color))
        



