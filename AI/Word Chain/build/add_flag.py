# from gensim.models import KeyedVectors
# import numpy as np

# MODEL = "glove-wiki-gigaword-50.model"
# NODE = "__node_7f3a__"

# model = KeyedVectors.load(MODEL)

# attic = model["attic"].copy()

# # Almost identical to "attic"
# rng = np.random.default_rng(1337)
# noise = rng.normal(size=attic.shape).astype(np.float32)
# noise /= np.linalg.norm(noise)

# node_vector = attic + noise * 1e-6

# model.add_vector(NODE, node_vector)

# model.save("challenge.model")

# print(model.most_similar("attic", topn=5))


from gensim.models import KeyedVectors
import numpy as np

MODEL = "challenge_filtered.model"
NODE = "__node_7f3a__"

model = KeyedVectors.load(MODEL)

# Make the node extremely close to "attic"
attic = model["attic"].copy()

rng = np.random.default_rng(1337)
noise = rng.normal(size=attic.shape).astype(np.float32)
noise /= np.linalg.norm(noise)

node_vector = attic + noise * 1e-6

# Add permanently
if NODE not in model.key_to_index:
    model.add_vector(NODE, node_vector)

# Save back to the same model
model.save(MODEL)

print("Added:", NODE)
print("Similarity to attic:", model.similarity("attic", NODE))
print("Nearest to attic:")
print(model.most_similar("attic", topn=5))