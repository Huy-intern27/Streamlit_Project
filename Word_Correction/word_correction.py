import streamlit as st  # type: ignore


def load_vocab(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


def levenshtein_distance(word1, word2):
    distance = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]

    for i in range(len(word1) + 1):
        distance[i][0] = i
    for j in range(len(word2) + 1):
        distance[0][j] = j

    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            if word1[i - 1] == word2[j - 1]:
                distance[i][j] = distance[i - 1][j - 1]
            else:
                distance[i][j] = 1 + min(distance[i][j - 1],
                                         distance[i - 1][j], distance[i - 1][j - 1])

    return distance[len(word1)][len(word2)]


def main():
    vocabs = load_vocab("./vocab.txt")
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word: ')

    if st.button("Compute"):
        leven_distances = dict()

        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        sorted_distances = dict(
            sorted(leven_distances.items(), key=lambda items: items[1]))
        correct_words = list(sorted_distances.keys())[0]

        st.write('Correct word:', correct_words)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary')
        col1.write(vocabs)

        col2.write('Distance')
        col2.write(sorted_distances)


if __name__ == "__main__":
    main()
