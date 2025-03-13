# MFIN7036
## Requirements
Run this command to install all the requirements(for Anaconda user).https://github.com/hanhy/MFIN7036/blob/harry_dev/README.md
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
- scripts : Some support scripts

### preprocessing
- Input data : Raw news articles collected from Reuters (stored in JSON format)
- Preprocessing.ipynb :  Text cleaning, lemmotization, tokenization and filtering
- output : Cleaned dataset in CSV format 

### clustering
- data: News data after preprocessing
- output:
  - finbert_sentiment_analysis_results.csv: Sentiment scores of FinBert
  - vader_sentiment_analysis_result.csv: Sentiment scores of VADER
  - invalid_dates_sample_counts: Invalid date with number of news below 30
- cluster_sentiment.ipynb: Clustering and Sentiment Analysis
- find_parameter.ipynb: Model training to find the optional parameters of Word2Vec model
### market_analysis
- data:
  - VC0.csv: Document stock return, interest rate, key economic event date, and sentiment scores of VADER of Cluster 0
  - VC1.csv: Document stock return, interest rate, key economic event date, and sentiment scores of VADER of Cluster 1
  - FC0.csv: Document stock return, interest rate, key economic event date, and sentiment scores of FinBert of Cluster 0
  - FC1.csv: Document stock return, interest rate, key economic event date, and sentiment scores of FinBert of Cluster 1
- Mkt_P1_Linear_Regression.ipynb: Codes run linear regressions of stock return and sentiment score of each method of each Cluster

## Scraper Structure
![Scraper](https://github.com/user-attachments/assets/7de4f630-b9a9-4ab9-9850-500e35c80016)
