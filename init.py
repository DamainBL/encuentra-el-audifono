from juegoX import Game
from volumen import AudioControlWindow

def main():

    game = Game()
    AudioControlWindow(game)  # ← ventana con slider
    game.run()


if __name__ == "__main__":
    main()
    