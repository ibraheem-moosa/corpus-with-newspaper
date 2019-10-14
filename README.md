# corpus-with-newspaper
Scrap articles with the newspaper library.

Put the homepage urls of newspaper websites in a file.

Run this.
```
python scrap_newspaper_articles.py urls_file -o output -m metadata.csv
```

This will scrap some articles from each url in ```urls_file``` to a subdirectory of ```output```.

Output files are given their sha256 as name. There is also a ```metadata.csv``` file which includes the 
published date, author names and title. However there are no gurantess of correctness. Sometimes some 
data maybe missing in ```metadata.csv```.
