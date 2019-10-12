import newspaper
import argparse
from pathlib import Path
from urllib.parse import urlparse
from tqdm import tqdm
from hashlib import sha256
from pandas import DataFrame


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

parser = argparse.ArgumentParser('Scrap newspaper articles from a website.')
parser.add_argument('url', help='Home URL of the website.')
parser.add_argument('-o', '--output-directory', help='Output directory', type=Path, default='output')
args = parser.parse_args()

url = args.url
domain = urlparse(url).hostname
out = Path(args.output_directory)/domain
out.mkdir(parents=True, exist_ok=True)
paper = newspaper.build(url, language='bn', memoize_articles=True, fetch_images=False, browser_user_agent=USER_AGENT, request_timeout=1000, verbose=True)

print('Categories:')
for category in paper.category_urls():
    print(category)

articles = list(filter(lambda a: urlparse(a.url).hostname == domain, paper.articles))
print('Got {} articles from {}.'.format(len(articles), url))

metadata = []
metadata_columns = ['filename', 'author', 'title', 'url', 'publish_date']

for article in tqdm(articles):
    try:
        article.download()
        article.parse()
        text = article.text
        m = sha256()
        m.update(text.encode('utf-8')) 
        fname = m.hexdigest()
        (out/fname).write_text(text)
        metadatum = [fname,
                ','.join(article.authors),
                article.title,
                article.url,
                article.publish_date]
        metadata.append(metadatum)
    except Exception as e:
        print(e)

df = DataFrame(metadata, columns=metadata_columns)
if not (out/'metadata.csv').exists():
    df.to_csv(out/'metadata.csv', index=False)
else:
    df.to_csv(out/'metadata.csv', index=False, mode='a', header=False)
