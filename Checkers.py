import sys
import Logic

def main():
    if len(sys.argv) < 2:
        print("usage: python3 Checkers.py <command>")
        return

    print("Game Start")

    print("Input Start Up Command")
    command = input(">> ")
    Logic.run_game(command)
    print(f"You typed: {command}")

if __name__ == "__main__":
    main()