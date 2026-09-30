from gensim.models import KeyedVectors

model = KeyedVectors.load("glove-wiki-gigaword-50.model", mmap="r")

print("Vocabulary:", len(model.key_to_index))
print("Dimensions:", model.vector_size)

print("attic" in model.key_to_index)
print("attic index:", model.key_to_index["attic"])
print("attic vector:", model["attic"])