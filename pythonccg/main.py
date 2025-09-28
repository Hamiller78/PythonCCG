from pythonccg.gameloop import Gameloop
from pythonccg.gamestate import Gamestate

def main():
    initial_state = Gameloop().setup_game()
    winner = Gameloop().run_game(initial_state)

if __name__ == "__main__":
    main()
