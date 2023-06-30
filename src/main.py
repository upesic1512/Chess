import pygame
import sys
from square import Square
from const import *
from game import Game
from move import Move


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        

        pygame.display.set_caption("Chess")
        self.game = Game()


    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

    

        while True:
            
            self.game.show_bg(screen)
            self.game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)


            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player:


                            board.cal_moves(piece,clicked_row,clicked_col,bool = True)
                            dragger.save_inital(event.pos)
                            dragger.dragg_piece(piece)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                        

                elif event.type == pygame.MOUSEMOTION:


                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)



                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        relased_row = dragger.mouseY // SQSIZE
                        relased_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.inital_row, dragger.inital_col)
                        final = Square(relased_row,relased_col)

                        move = Move(initial,final)

                        if board.valid_move(dragger.piece, move): 
                            
                            captured = board.squares[relased_row][relased_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)
                        

                            game.play_sound(captured)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()


                    dragger.undragg_piece()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()
                    if event.key == pygame.K_r:
                        game.reset()
                        
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()