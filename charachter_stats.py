# coding: utf-8


from pathlib import Path
from collections import Counter
import sys

article_dir = Path(sys.argv[1])
char_counter = Counter()

for article in article_dir.iterdir():
    char_counter.update(article.read_text())

for item in char_counter.most_common():
    print(item)
