# MFIN7036
## Requirements
Run this command to install all the requirements(for Anaconda user).
```
while read requirement; do conda install --yes $requirement; done < requirements.txt
```
If you use pip, run command below.
```
pip install -r requirements.txt
```
## Codefile and Datafile Explain
### data-collection
- fetch_links.ipynb : Scrape and parse links
- fetch_article.ipynb : Scrape and parse artiles
- output : Scraped result sample

### preprocessing
### clustering
### market_analysis


## Scraper Structure
![Scraper](https://github.com/user-attachments/assets/7de4f630-b9a9-4ab9-9850-500e35c80016)
