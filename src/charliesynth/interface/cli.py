from charliesynth import __version__
from charliesynth.core.brain import CharlieSynth


def main():

    charlie = CharlieSynth()

    print()
    print("=" * 45)
    print("           CHARLIESYNTH")
    print("       Artificial Intelligence")
    print("=" * 45)

    print(f"Version: {__version__}")
    print("State: NEWBORN")
    print("Knowledge sources: 0")
    print("Knowledge engine: NOT CONNECTED")

    print("\nCharlieSynth is awake.")
    print("Type /help for commands.\n")

    while True:

        try:
            message = input("You > ").strip()

            if not message:
                continue

            if message == "/exit":
                print("\nCharlieSynth: Goodbye.")
                break

            elif message == "/help":
                print("""
Available commands:

/help       Show commands
/status     Show CharlieSynth status
/exit       Shut down CharlieSynth

Anything else will be treated as a question.
""")

            elif message == "/status":

                status = charlie.status()

                for key, value in status.items():
                    print(f"{key}: {value}")

            else:
                response = charlie.answer(message)
                print(f"\nCharlieSynth > {response}\n")

        except KeyboardInterrupt:
            print("\nCharlieSynth shutting down.")
            break