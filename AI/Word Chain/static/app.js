"use strict";

const chainEl = document.getElementById("chain");

const wordForm = document.getElementById("wordForm");
const wordInput = document.getElementById("word");
const submitButton = document.getElementById("submit");
const newGameButton = document.getElementById("newGame");

const resultEl = document.getElementById("result");
const scoreEl = document.getElementById("score");
const messageEl = document.getElementById("message");

const flagBox = document.getElementById("flagBox");
const flagEl = document.getElementById("flag");

const hintInput = document.getElementById("hint");
const mapButton = document.getElementById("mapButton");
const mapResults = document.getElementById("mapResults");

let chain = [];


/* ---------------- API ---------------- */

async function api(path, payload = {}) {
    const response = await fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error("Invalid server response.");
    }

    if (!response.ok) {
        throw new Error(data.error || "Request failed.");
    }

    return data;
}


/* ---------------- UI ---------------- */

function clearResult() {
    resultEl.className = "result hidden";
    scoreEl.textContent = "";
    messageEl.textContent = "";
}

function showResult(similarity, accepted, message) {
    resultEl.className = `result ${accepted ? "accepted" : "rejected"}`;

    scoreEl.textContent = `${similarity.toFixed(2)}%`;
    messageEl.textContent = message;
}

function renderChain() {
    chainEl.replaceChildren();

    if (chain.length === 0) {
        const empty = document.createElement("span");
        empty.className = "chain-empty";
        empty.textContent = "Starting chain...";
        chainEl.appendChild(empty);
        return;
    }

    chain.forEach((item, index) => {
        const node = document.createElement("div");
        node.className = "node";

        const pill = document.createElement("div");
        pill.className = "pill";

        if (index === chain.length - 1) {
            pill.classList.add("current");
        }

        pill.textContent = item.word;

        node.appendChild(pill);

        if (index < chain.length - 1) {
            const next = chain[index + 1];

            const connection = document.createElement("div");
            connection.className = "connection";

            const line = document.createElement("div");
            line.className = "line";

            const similarity = document.createElement("span");
            similarity.className = "similarity";

            if (next.similarity >= 0) {
                similarity.classList.add("positive");
            } else {
                similarity.classList.add("negative");
            }

            similarity.textContent =
                `${next.similarity >= 0 ? "+" : ""}${next.similarity.toFixed(2)}%`;

            connection.appendChild(line);
            connection.appendChild(similarity);

            node.appendChild(connection);
        }

        chainEl.appendChild(node);
    });

    const lastPill = chainEl.querySelector(".pill.current");

    if (lastPill) {
        lastPill.scrollIntoView({
            behavior: "smooth",
            block: "nearest",
            inline: "center"
        });
    }
}


/* ---------------- Game ---------------- */

async function newGame() {
    newGameButton.disabled = true;
    submitButton.disabled = true;

    try {
        const data = await api("/api/start");

        chain = [
            {
                word: data.current,
                similarity: null
            }
        ];

        flagBox.classList.add("hidden");
        mapResults.classList.add("hidden");
        mapResults.replaceChildren();

        clearResult();
        renderChain();

        wordInput.value = "";
        wordInput.focus();

    } catch (error) {
        showResult(0, false, error.message);
    } finally {
        newGameButton.disabled = false;
        submitButton.disabled = false;
    }
}


async function submitWord(event) {
    event.preventDefault();

    const submittedWord = wordInput.value.trim().toLowerCase();

    if (!submittedWord) {
        return;
    }

    submitButton.disabled = true;

    try {
        const currentWord = chain[chain.length - 1].word;

        const data = await api("/api/step", {
            current: currentWord,
            word: submittedWord
        });

        showResult(
            Number(data.similarity),
            data.accepted,
            data.accepted ? "accepted" : data.message
        );

        if (!data.accepted) {
            wordInput.select();
            return;
        }

        chain.push({
            word: data.current || submittedWord,
            similarity: Number(data.similarity)
        });

        renderChain();

        wordInput.value = "";

        if (data.won) {
            flagEl.textContent = data.flag || "";
            flagBox.classList.remove("hidden");

            wordInput.disabled = true;
            submitButton.disabled = true;
        }
    } catch (error) {
        showResult(0, false, error.message);
    } finally {
        if (flagBox.classList.contains("hidden")) {
            submitButton.disabled = false;
            wordInput.focus();
        }
    }
}


/* ---------------- Hint ---------------- */

async function showMap() {
    const hint = hintInput.value.trim();

    if (!hint) {
        return;
    }

    mapButton.disabled = true;

    try {
        const current = chain[chain.length - 1].word;

        const data = await api("/api/similar", {
            word: current,
            hint
        });

        mapResults.replaceChildren();

        for (const item of data.results) {
            const pill = document.createElement("div");

            pill.className = "map-word";

            pill.textContent =
                `${item.word} · ${item.percentage.toFixed(2)}%`;

            mapResults.appendChild(pill);
        }

        mapResults.classList.remove("hidden");

    } catch (error) {
        mapResults.classList.remove("hidden");
        mapResults.replaceChildren();

        const errorText = document.createElement("span");
        errorText.className = "chain-empty";
        errorText.textContent = error.message;

        mapResults.appendChild(errorText);
    } finally {
        mapButton.disabled = false;
    }
}


/* ---------------- Events ---------------- */

wordForm.addEventListener("submit", submitWord);
newGameButton.addEventListener("click", newGame);
mapButton.addEventListener("click", showMap);


/* ---------------- Start ---------------- */

newGame();