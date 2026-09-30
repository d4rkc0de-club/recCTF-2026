from gensim.models import KeyedVectors

MODEL_FILE = "glove-wiki-gigaword-50.model"
DICT_FILE = "words_alpha.txt"
OUTPUT_FILE = "challenge_filtered.model"

model = KeyedVectors.load(MODEL_FILE)

with open(DICT_FILE, "r", encoding="utf-8") as f:
    dictionary = {
        line.strip().lower()
        for line in f
        if line.strip()
    }

words = []
vectors = []

for word, index in model.key_to_index.items():
    if word.lower() in dictionary:
        words.append(word)
        vectors.append(model.vectors[index])

print("Original:", len(model.key_to_index))
print("Filtered:", len(words))

filtered = KeyedVectors(
    vector_size=model.vector_size
)

filtered.add_vectors(words, vectors)

filtered.save(OUTPUT_FILE)

print("Saved:", OUTPUT_FILE)