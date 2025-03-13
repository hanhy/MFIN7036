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
- data: News data after preprocessing
- output:
  - finbert_sentiment_analysis_results.csv: Sentiment scores of FinBert
  - vader_sentiment_analysis_result.csv: Sentiment scores of VADER
  - invalid_dates_sample_counts: Invalid date with number of news below 30
- cluster_sentiment: Clustering and Sentiment Analysis
- find_parameter: Model training to find the optional parameters of Word2Vec model
### market_analysis


## Scraper Structure
![Scraper](https://github.com/user-attachments/assets/7de4f630-b9a9-4ab9-9850-500e35c80016)
