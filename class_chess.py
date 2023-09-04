import threading
import requests
from stockfish import Stockfish
import chess
import chess.engine
from stockfish import StockfishException


class Chess:

    

    def __init__(self,stockfish_path,fen_string=None,max_depth = 50):
        self.board = chess.Board()
        self.fen_string = fen_string
        self.stockfish = Stockfish(path=stockfish_path )
        self.__max_stockfish_depth = max_depth
        self.evaluate_chess_position_result_event = threading.Event()
        self.evaluate_chess_position_result = None

        if fen_string:
            try:
                
                self.stockfish.set_fen_position(fen_string)

            except StockfishException:
                raise ValueError("Invalid Fen Provided")
        


    def evaluate_chess_position(self,fen_string,depth):
        if depth > self.__max_stockfish_depth or depth < 1:
            print("depth range is from 1 to 50")
            info = "depth range is from 1 to 50"

            return  info
        
        else:
            def evaluation_thread(fen_string,depth):
                try: 
                    self.stockfish.set_fen_position(fen_string)
                    self.stockfish.set_depth(depth)
                    evaluation = self.stockfish.get_evaluation() #return {"'type':'cp', 'value':33"}
                    eval_in_pawns = evaluation['value']/100
                    self.evaluate_chess_position_result = eval_in_pawns


                    print(f'the evaluation of the position in centipawns is, {eval_in_pawns}')

                except StockfishException:
                    info = "the Fen provided is invalid"
                    self.evaluate_chess_position_result = info
                    print(f'the Fen provided is invalid, Fen: {fen_string}')


                self.evaluate_chess_position_result_event.set()

                # return eval_in_pawns
            thread = threading.Thread(target=evaluation_thread, args=(fen_string,depth,))
            thread.start()
            thread.join()
            self.evaluate_chess_position_result_event.wait()
            return self.evaluate_chess_position_result
            
            

        

        

    def get_best_move(self,fen_string):
        self.fen_string=fen_string
        self.stockfish.set_fen_position(fen_string)
        best_move = self.stockfish.get_best_move()

        print(f'the best move is {best_move}')

        return best_move
    

    def get_top_moves(self,fen_string,no_of_top_moves):
        self.fen_string= fen_string
        self.stockfish.set_fen_position(fen_string)
        top_moves = self.stockfish.get_top_moves(no_of_top_moves)

        for i,top_moves_info in enumerate(top_moves):
            move = top_moves_info["Move"]
            centiPawn = top_moves_info["Centipawn"]/100
            Mate = top_moves_info["Mate"]

            print(f'the {i+1} best move is {move} with a cp value of {centiPawn} with Mate in {Mate}')


        print(f'this is the {top_moves}')
        return top_moves


    def get_win_draw_loss_stats(self,fen_string):
        is_stockfish_version_recent_to_display_WDL_stats = self.stockfish.does_current_engine_version_have_wdl_option()
        if is_stockfish_version_recent_to_display_WDL_stats is True:
            self.fen_string = fen_string
            self.stockfish.set_fen_position(fen_string)
            win_draw_loss_stat = self.stockfish.get_wdl_stats()
            wins = win_draw_loss_stat[0]
            draws = win_draw_loss_stat[1]
            loss = win_draw_loss_stat[2]

            print(f'white has won {wins} times, drawn {draws} times and loss {loss} times')
            return win_draw_loss_stat
        
        else:
            info = 'your version of stockfish is not recent enough to display WDL stats please update your engine'
            print(f'your version of stockfish is not recent enough to display WDL stats please update your engine')
            return info




    def print_board(self):
        return self.board
    

    def check_fen(self,fen_string):
        self.fen_string = fen_string
        value = self.stockfish.is_fen_valid(fen_string)

        if value is True:
            print(f'returns {value}, its a Valid Fen')
            return value

        else:
            print(f'returns {value}, its not a Valid Fen')
            return value


    

    def reset_engine_parameters(self):
        self.stockfish.reset_engine_parameters()



    def convert_class_fetch___stream_lichess_game_by_id_data_to_FEN(self,pgn_data):
        # pgn_data = str(pgn_data)
        board = chess.Board()
        pgn_data_array_format = pgn_data.split()

        for move in pgn_data_array_format:
            board.push_san(move)



        fen = board.fen()


        print(fen)

        return fen







