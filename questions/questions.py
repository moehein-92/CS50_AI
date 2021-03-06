import nltk
import sys
import string
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = dict()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r", encoding='utf8') as f:
            dic[filename] = f.read()

    return dic


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    tok = [word.lower() for word in nltk.word_tokenize(document)]
    punct = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")
    lst = []
    for word in tok:
        if word in punct:
            continue
        elif word in stopwords:
            continue
        else:
            lst.append(word)
            
    return lst

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total = len(documents)
    counts = dict()
    for doc in documents:
        seen = []

        for word in documents[doc]:
            if word not in seen:
                seen.append(word)
                try:
                    counts[word] += 1
                except:
                    counts[word] = 1
    return {word: math.log(total/counts[word]) for word in counts}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    dic = dict()
    for filename in files:
        dic[filename] = 0
        for word in query:
            dic[filename] += idfs[word] * files[filename].count(word)
    #print(len(dic))
    return sorted(dic, key=dic.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    lst = []
    for sentence in sentences:
        sentence_values = [sentence, 0, 0]
        
        for word in query:
            if word in sentences[sentence]:
                # Compute "matching word measure"
                sentence_values[1] += idfs[word]
                # Compute "query term density"
                sentence_values[2] += sentences[sentence].count(word)/(len(sentences[sentence]))

        lst.append(sentence_values)
        
    return [sentence for sentence, mwm, qtd in sorted(lst, key=lambda x: (x[1], x[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
