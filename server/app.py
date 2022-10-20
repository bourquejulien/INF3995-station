from src.application import create_app, exit_app
import atexit


def main():
    atexit.register(exit_handler)
    app = create_app()
    app.run(host="0.0.0.0")


def exit_handler():
    exit_app()


if __name__ == '__main__':
    main()
