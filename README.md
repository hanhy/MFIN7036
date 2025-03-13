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
  - finbert_sentiment_analysis_results_update: Sentiment scores of FinBert after clustering
- ouput:
  - Mkt_P2_Adjusted_close_prices: Adjusted close prices for all tickers
  - Mkt_P2_Daily_returns: Discrete daily returns for all tickers
  - Mkt_P2_Align_sentiment_clusters_with_market_data: Result of merging news sentiment scores with market data (including adjusted close prices and discrete daily returns)
- Mkt_P1_Linear_Regression.ipynb: Codes run linear regressions of stock return and sentiment score of each method of each Cluster
- Mkt_P2_Data-driven_Trading_Strategy:
  - Step 1: Import necessary modules
  - Step 2: Get market data
  - Step 3: Merge news sentiment with market data
  - Step 4: Trading Strategy
    - Strategy 1: Cluster-Based Strategy
    - Strategy 2: Sentiment Momentum Strategy
    - Strategy 3: VIX-Sentiment Mean Reversion

## Scraper Structure
![Scraper](https://github.com/user-attachments/assets/7de4f630-b9a9-4ab9-9850-500e35c80016)
