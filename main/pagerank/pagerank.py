import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python pagerank.py corpus")
    #corpus = crawl(sys.argv[1])
    corpus = crawl("corpus0")
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

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Get total Number of links and create our return dictionary
    n = len(corpus)
    probability_distribution = dict()
    for i in corpus:
        probability_distribution[i]=0

    # Add probabilities of links that are linked to by the page
    direct_links = corpus[page]
    n2 = len(direct_links)
    for j in direct_links:
        probability_distribution[j]=round (damping_factor * 1 / n2,4)
    
    # Add probabilities coming from the fact that a random page might be selected
    if n2 == 0:
        for k in probability_distribution:
            probability_distribution[k] =  round ((1 / n),4)
    else:
        for k in probability_distribution:
            probability_distribution[k] += round(((1-damping_factor) * 1 / n),4)

    return probability_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_rank = dict()
    chance = list()
    model = dict()
    values = list()
    # Create all pages with initial rank set to 0
    for i in corpus:
        page_rank [i] = 0

    # Generate first random page and add it to total number of pages for that page
    previous_page = random.choice(list(page_rank.keys()))
    page_rank [previous_page]+=1

    # Get transition model of the previous page
    model = transition_model(corpus, previous_page, damping_factor)
    

    for j in range(n-1):
        
        # Generate a random page based on likelihood and add that page to total
        
        values = list(model.keys())
        chance = [model[x] for x in model]
        previous_page = random.choices(values, weights = chance, k = 1)
        previous_page_use = previous_page[0]
        page_rank[previous_page_use] +=1

        # Get transition model
        model.clear()
        model = transition_model(corpus, previous_page_use, damping_factor)

    total = 0

    # Get total number of pages
    for k in page_rank.keys():
        total += page_rank[k]
    
    if (total != n ):
        raise NotImplementedError 
    
    for k in page_rank.keys():
        page_rank[k] = round((page_rank[k] / n),4)
    
    return page_rank

    



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iterative_rank = dict()
    n = len (corpus)
    pr = dict()
    

    # Create the dictionary for page ranks and assign initial ranks
    for i in corpus:
        iterative_rank [i] = (1/n)
    iteration = 0
    while (iteration == 0):
        # Go through each webpage
        for k in iterative_rank:
            sigma = 0
            
            # Add random part
            pr [k] = (1-damping_factor)/n

            # go through each i page and add to total probability if correct
            for summation in corpus:
                if (k in corpus[summation]):
                    n2 = len (corpus[summation])
                    sigma += iterative_rank [summation]/n2
            
            pr [k] += damping_factor * sigma
        # See if we need to keep iterating
        for m in pr:
            temp = abs((pr[m]-iterative_rank[m]))
            if (temp>0.001):
                iteration +=1
        
        if (iteration>0):
            iteration = 0
            iterative_rank = pr.copy()
        else:
            iteration = 1000000
            iterative_rank = pr.copy()

    return iterative_rank


if __name__ == "__main__":
    main()
