from console_version.game import play_game

def main():
    while True:
        play_game()
        choice = input("\n🔁 Play again? (y/n): ").lower()
        if choice != "y":
            print("👋 Thanks for playing!")
            break

main()
