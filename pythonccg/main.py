def main():
    from .gameloop import Gameloop
    from .gamestate import Gamestate
    initial_state = Gameloop().setup_game()
    winner = Gameloop().run_game(initial_state)

if __name__ == "__main__":
    main()
    main()
