from collections import deque
from gensim.models import KeyedVectors


MODEL = "challenge_filtered.model"
FLAG_NODE = "__node_7f3a__"

THRESHOLD = 0.50
TOP_N = 30
MAX_DEPTH = 20


def load_model(path):
    print(f"Loading model: {path}")
    return KeyedVectors.load(path)


def find_path(model, start, target, threshold=0.30, top_n=30, max_depth=20):
    """
    Find a shortest semantic path from start to target.

    Only edges with similarity >= threshold are considered.
    Among nodes at the same depth, higher-similarity neighbors
    are explored first.

    Returns:
        List of (word, similarity_to_previous_node)
        or None if no path is found.
    """

    if start not in model.key_to_index:
        raise ValueError(f"Starting word not found: {start}")

    if target not in model.key_to_index:
        raise ValueError(f"Target node not found: {target}")

    if start == target:
        return [(start, 1.0)]

    # Cache expensive most_similar() calls.
    neighbor_cache = {}

    def get_neighbors(word):
        if word not in neighbor_cache:
            neighbors = model.most_similar(word, topn=top_n)

            neighbor_cache[word] = [
                (neighbor, float(score))
                for neighbor, score in neighbors
                if score >= threshold
            ]

        return neighbor_cache[word]

    # Queue contains:
    # (current_node, path)
    queue = deque()
    queue.append((start, [(start, 1.0)]))

    # Global visited set is sufficient for BFS because the first
    # time we reach a node is through the shortest path.
    visited = {start}

    while queue:
        current, path = queue.popleft()

        depth = len(path) - 1

        if depth >= max_depth:
            continue

        neighbors = get_neighbors(current)

        # Explore higher similarity edges first.
        neighbors = sorted(
            neighbors,
            key=lambda item: item[1],
            reverse=True
        )

        for neighbor, score in neighbors:
            if neighbor in visited:
                continue

            new_path = path + [(neighbor, score)]

            if neighbor == target:
                return new_path

            visited.add(neighbor)
            queue.append((neighbor, new_path))

    return None


def print_path(path):
    print("\nPATH FOUND:\n")

    for i, (word, score) in enumerate(path):
        if i == 0:
            print(word)
        else:
            print(f"  ↓ {score * 100:.2f}%")
            print(word)

    print(f"\nDepth: {len(path) - 1}")
    print("FLAG NODE REACHED.")


def main():
    model = load_model(MODEL)

    start = input("Starting word: ").strip().lower()

    if not start:
        print("Please enter a starting word.")
        return

    if start not in model.key_to_index:
        print(f"Word not found in model: {start}")
        return

    if FLAG_NODE not in model.key_to_index:
        print(f"Flag node not found in model: {FLAG_NODE}")
        return

    print()
    print(f"Searching from: {start}")
    print(f"Target: {FLAG_NODE}")
    print(f"Threshold: {THRESHOLD * 100:.1f}%")
    print(f"Top neighbors: {TOP_N}")
    print(f"Maximum depth: {MAX_DEPTH}")
    print()

    path = find_path(
        model=model,
        start=start,
        target=FLAG_NODE,
        threshold=THRESHOLD,
        top_n=TOP_N,
        max_depth=MAX_DEPTH,
    )

    if path is None:
        print("No path to the flag found.")
        return

    print_path(path)


if __name__ == "__main__":
    main()