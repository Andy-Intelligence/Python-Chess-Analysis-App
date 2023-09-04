from flask import Flask,render_template,request
from class_chess import Chess
from class_fetch import Fetch
import asyncio

app = Flask(__name__)
stockfish_path = "C:\\Users\\user\\Desktop\\LiveChessAnalysis\\stockfish\\stockfish-windows-x86-64-avx2.exe"
class_chess1 = Chess(stockfish_path=stockfish_path)
class_fetch1 = Fetch()


@app.route('/')
def home():
    # s = class_chess1.print_board()
    # s = class_chess1.check_fen()
    # s = class_chess1.get_eval()
    # s = class_chess1.evaluate_chess_position("rnbqkbnr/ppp1pppp/8/8/4p3/5Q2/PPPP1PPP/RNB1KBNR b KQkq - 1 3",depth=10)
    # s = class_fetch1.update()
    # s = class_fetch1.stream_lichess_game_by_id("OGzz3FdM")
    fetcher = class_fetch1.stream_lichess_game_by_id("ZlcUl2vg")

    fen_positions = []
    a = ""
    b = 0.00

    async def process_moves():

        
        for pgn_position in fetcher:
            fen_position = class_chess1.convert_class_fetch___stream_lichess_game_by_id_data_to_FEN(pgn_position)
            print(f'i am {pgn_position}')
            
            a = fen_position

            # fen_positions.append(fen_position)
            print(f'i am {fen_position}')
            evaluation = await asyncio.to_thread(class_chess1.evaluate_chess_position, fen_position, depth=10)

            print(f'evaluation {evaluation}')
            b = evaluation

        return {"fen_positions":fen_position,"evaluation":evaluation} 
            


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(process_moves())
    
    return render_template("index.html", data = result)











if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=3409)


