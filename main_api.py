from fastapi import FastAPI
from pydantic import BaseModel
from Checkers import Game

app = FastAPI()
game = Game()

class MoveRequest(BaseModel):
    start: str
    end: str
    jump_choice: int | None = None

@app.get("/state")
def state():
    return {
        "board": game.board.tolist(),
        "turn": game.turn,
        "state": game.state,
        "result": game.result
    }

@app.post("/start")
def start(mode: str = "1p"):
    game.reset()
    game.mode = mode
    return {"message": "started"}

@app.post("/move")
def move(req: MoveRequest):
    try:
        game.move(req.start, req.end, req.jump_choice)
        return {"board": game.board.tolist(), "turn": game.turn}
    except Exception as e:
        return {"error": str(e)}