# pylint: disable=unused-variable

import os
import random
import re
import sys


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    """
    result = {}
    # Check if there are no further links in the current page.
    if len(corpus[page]) == 0:
        prob = 1/(len(corpus))
        for link in corpus:
            result[link] = prob
        return result

    else:
        num_keys = len(corpus)
        num_vals = len(corpus[page])
        prob1 = (damping_factor/num_vals) + (1-damping_factor)/num_keys
        prob2 = (1-damping_factor)/num_keys
        for link in corpus:
            if link in corpus[page]:
                result[link] = prob1
            else:
                result[link] = prob2
        return result

 

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    for link in corpus:
        result[link] = 0

    sample = None

    for i in range(n):
        if sample == None:
            lst = list(corpus.keys())
            # randomly choose a sample
            sample = random.choice(lst)
            result[sample] += 1
        else:
            # get probability distribution on current sample
            next_sample = transition_model(corpus, sample, damping_factor)
            lst = list(next_sample.keys())
            weights = [next_sample[key] for key in lst]
            # grab random value using pop()
            sample = random.choices(lst, weights).pop()
            result[sample] += 1

    # get percentages for each link based on sampling
    for key, value in result.items():
        percent = value/n
        result[key] = percent
    if round(sum(result.values()), 5) != 1:
        print(f"Error probabilities add up to {sum(result.values())}")
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    change = 1
    N = len(corpus)
    for link in corpus:
        result[link] = 1 / N
    
    while change >= 0.001:
        # reset change
        change = 0
        # copy current state to calculate new PRs
        prev_state = result.copy()
        # create list of parent pages.
        for page in result:
            p1 = [link for link in corpus if page in corpus[link]]
            # first part of PR equation
            first = (1-damping_factor) / N
            second = []
            if len(p1) != 0:
                for p in p1:
                    val = prev_state[p] / len(corpus[p])
                    second.append(val)
            second_sum = sum(second)
            result[page] = first + damping_factor*(second_sum)
            # calculate change during this iteration
            new_change = abs(result[page] - prev_state[page])
            if change < new_change:
                change = new_change
    dict_sum = sum(result.values())
    result = {key: value/dict_sum for key, value in result.items()}
    return result


if __name__ == "__main__":
    main()
