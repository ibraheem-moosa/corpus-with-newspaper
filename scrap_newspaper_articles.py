import newspaper
import argparse
from pathlib import Path
from urllib.parse import urlparse
from tqdm import tqdm
from hashlib import sha256
from pandas import DataFrame
import pandas as pd


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

parser = argparse.ArgumentParser('Scrap newspaper articles from a website.')
parser.add_argument('urls', help='File containing URLs of websites.')
parser.add_argument('-o', '--output-directory', help='Output directory', type=Path, default='output')
parser.add_argument('-m', '--metadata-file', help='Metadata file', type=Path, default='metadata.csv')
args = parser.parse_args()

urls = Path(args.urls).read_text().split()
out = Path(args.output_directory)
out.mkdir(parents=True, exist_ok=True)
metadata_file = args.metadata_file

metadata = []
metadata_columns = ['filename', 'author', 'title', 'url', 'publish_date']

article_urls = set()
if Path(metadata_file).exists():
    df = pd.read_csv(metadata_file)
    article_urls = set(df['url'])

for url in urls:
    print('URL: {}'.format(url))
    domain = urlparse(url).hostname
    paper = newspaper.build(url, language='bn', memoize_articles=False, fetch_images=False, browser_user_agent=USER_AGENT, request_timeout=1000, verbose=True)

    print('Categories:')
    for category in paper.category_urls():
        print(category)

    articles = list(filter(lambda a: a.url not in article_urls, paper.articles))
    articles = list(filter(lambda a: urlparse(a.url).hostname == domain, articles))
    print('Got {} articles from {}.'.format(len(articles), url))

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
if not Path(metadata_file).exists():
    df.to_csv(metadata_file, index=False)
else:
    df.to_csv(metadata_file, index=False, mode='a', header=False)
