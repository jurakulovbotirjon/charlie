
from charliesynth.core.brain import CharlieSynth
from charliesynth.memory.repository import MemoryRepository
from charliesynth.perception.ingestor import DocumentIngestor


def main():
    brain = CharlieSynth()

    print(f"\n{brain.name} v{brain.version}")
    print("CharlieSynth is ready. Type /help for commands.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nCharlieSynth: Shutting down.")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            print("CharlieSynth: Goodbye.")
            break

        elif user_input == "/help":
            print("""
Available commands:
/help                 Show commands
/status               Show system status
/ingest <file_path>   Add a text document
/search <question>    Search stored knowledge
/exit                 Exit CharlieSynth
""")
            continue

        elif user_input == "/status":
            print(brain.status())
            continue

        elif user_input.startswith("/ingest "):
            path = user_input.removeprefix("/ingest ").strip()

            try:
                result = DocumentIngestor().ingest(path)
                print("\nCHARLIESYNTH:", result)
            except Exception as error:
                print(f"\nINGESTION ERROR: {error}")

            continue

        elif user_input.startswith("/search "):
            question = user_input.removeprefix("/search ").strip()

            try:
                results = MemoryRepository().search_chunks(question)

                if not results:
                    print("\nCHARLIESYNTH: No supporting information found.")
                else:
                    for result in results:
                        print(f"\nSource: {result['filename']}")
                        print(f"Page: {result['page_number'] or 'Not available'}")
                        print(f"Evidence: {result['content']}")

            except Exception as error:
                print(f"\nSEARCH ERROR: {error}")

            continue

        else:
            print("\nCHARLIESYNTH:", brain.answer(user_input))


if __name__ == "__main__":
    main()

