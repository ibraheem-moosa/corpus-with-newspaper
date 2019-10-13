# corpus-with-newspaper
Scrap articles with the newspaper library.

Run this.
```
python scrap_newspaper_articles.py url -o output
```

This will scrap some articles from ```url``` to a subdirectory of ```output``` with url domain as name.

Output files are given their sha256 as name. There is also a ```metadata.csv``` file which includes the 
published date, author names and title. However there are no gurantess of correctness. Sometimes some 
data maybe missing in ```metadata.csv```.

Run this to scrap from urls.
```
cat urls | while read url; do python scrap_newspaper_articles.py $url -o output; done
```
