import pickle
import numpy as np
from sklearn.tree import DecisionTreeRegressor

TARGET = np.array([
    18,     # age
    180,    # height_cm
    72,     # weight_kg
    7,      # birth_month
    2008    # birth_year
], dtype=float)


def calculate_score(x):
    tolerances = np.array([
        5.0,
        20.0,
        20.0,
        6.0,
        10.0
    ])

    differences = np.abs(x - TARGET)

    similarity = 1.0 - (differences / tolerances)
    similarity = np.maximum(similarity, 0)

    return np.mean(similarity)


rng = np.random.default_rng(1337)

X = []
y = []

for _ in range(10000):
    profile = np.array([
        rng.integers(15, 30),     # age
        rng.integers(150, 200),   # height
        rng.integers(45, 110),    # weight
        rng.integers(1, 13),      # month
        rng.integers(1995, 2012)  # year
    ], dtype=float)

    X.append(profile)
    y.append(calculate_score(profile))


X.append(TARGET)
y.append(1.0)

X = np.array(X)
y = np.array(y)


# Small model
model = DecisionTreeRegressor(
    max_depth=20,
    random_state=1337
)

model.fit(X, y)


with open("model.pkl", "wb") as f:
    pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)

print("Generated model.pkl")