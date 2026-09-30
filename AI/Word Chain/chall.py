from gensim.models import KeyedVectors
import numpy as np

MODEL_FILE = "challenge_filtered.model"\

# dont forget to give this in the hints of the ctf
HINT_KEY = "a4dw-wd31-wwe32-dd24"

FLAG = "d4rk{pr0bability_1s_A_f03}"

THRESHOLD = 0.30

model = KeyedVectors.load(MODEL_FILE)

start_words = [
    word for word in model.key_to_index
    # if word != "attic" and word != FLAG
]

current = np.random.choice(start_words)

print("=== WORD CHAIN ===")
print("Follow the semantic connections until you reach the flag.")
print(f"A word needs at least {THRESHOLD * 100:.0f}% similarity.")
print("Type 'quit' to give up.\n")
print("")
hint = input("Enter the key you got from buying the Hint here: ")


while True:

    print(f"\nCurrent word: {current}")
    if hint == HINT_KEY:
        expected = model.most_similar(current)
        print("Here you go you get similar words mapped out with their percentage : ", (expected))
    user = input("Next word: ").strip().lower()

    # if user == "quit":
    #     print("Game over.")
    #     break

    if current == "__node_7f3a__":
        print("\nYou reached the flag node.")
        print(f"FLAG: {FLAG}")
        print("You win!")
        break

    if user not in model.key_to_index:
        print("That word isn't in the vocabulary.")
        continue

    similarity = model.similarity(current, user)

    percentage = similarity * 100

    print(f"Similarity: {percentage:.2f}%")

    if similarity >= THRESHOLD:

        print("Accepted.")
        current = user
        if current == "__node_7f3a__":
            print("\nYou reached the flag node.")
            print(f"FLAG: {FLAG}")
            print("You win!")
            break

    else:

        print(f"Rejected. You need at least {THRESHOLD * 100:.0f}% similarity.")