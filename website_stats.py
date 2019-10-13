import sys
from collections import Counter
from pathlib import Path


path = Path(sys.argv[1])
website_article_count = Counter()

for w in path.iterdir():
    website_article_count[w.name] = len(list(w.iterdir()))

for w, c in website_article_count.most_common():
    print(w, c - 1)

print('Total:', sum(website_article_count.values()))
