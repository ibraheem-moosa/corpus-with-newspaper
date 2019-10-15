import sys
from collections import Counter
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse


metadata = pd.read_csv(Path(sys.argv[1]))
metadata = metadata[pd.notna(metadata['url'])]
metadata['domain'] = metadata.apply(lambda row: urlparse(row['url']).hostname, axis=1)
website_article_count = Counter(metadata.domain)

for w, c in website_article_count.most_common():
    print(w, c - 1)

print('Total:', sum(website_article_count.values()))
