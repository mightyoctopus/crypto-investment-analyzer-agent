# Nodes Design:

## Infrastructure Framework
- Initialize the overall system.
- Configure:
 	- API clients
 	 - Environment settings
  	- Memory (if applicable. Not sure how it should be handled)
  	- Management utilities
  	- Application configuration

## Planner Agent
- Acts as the workflow orchestrator.
- Controls the execution sequence of all agents.

## Selector Agent
Input: trading_pairs (all coins info from Bithumb API)
Update: candidate_coins: list[str]
Output: candidate_coins: list[str]
Select 20 coins with highest potential for price rise
Request to Bithumb for market data(for receiving all coin names) and these data below 
Trade_volume (daily/weekly/monthly candles)
Highest_52_week_price
Lowest_52_week_price
Prev_closing_price (daily/weekly/monthly candles)
high_price: 8679000 (daily/weekly/monthly candles)
low_price: 8445000 (daily/weekly/monthly candles)
Trade_price: (daily/weekly/monthly candles)

- Check all available cryptocurrencies from Bithumb.
  (View transaction target list - market(string) attribute)
- Select the **Top 20 candidate coins** with the highest potential for price appreciation.
- No LLM involved at this node. It should be rule based and deterministic logic for simply filtering out
Candidate Coins Agent
Input: candidate_coins: list[str]
Update: just the same as the prev node (candidate_coins: list[str])
Output: candidate_coins: list[str]

- Pass the selected 20 coins into the parallel data collection workflow.


## Parallel Data Collection
### Bithumb API 
Input: candidate_coins
Update: 
daily_candle: list[dict[str: any]]
weekly_candle: list[dict[str: any]]
monthly_candle: list[dict[str: any]]
transaction_data: list[dict[str, any]]
is candle_data_good: bool (starting with “no”)
Output: 
daily_candle: list[dict[str: any]]
weekly_candle: list[dict[str: any]]
monthly_candle: list[dict[str: any]]
transaction_data: list[dict[str, any]]
is candle_data_good: bool (starting with “no”)
Request data via Bithumb on the selected 20 coins for each. candles(daily, weekly, monthly), Transaction data are required.

### Validate Bithumb API
Input: 
daily_candle: list[dict[str: any]]
weekly_candle: list[dict[str: any]]
monthly_candle: list[dict[str: any]]
transaction_data: list[dict[str, any]]
is candle_data_good: bool (starting with “no”)
Update: is candle_data_valid: yes or no depending on the result
Action: If data valid, moves to the next node, otherwise go for re-trying
These data from Bithumb API should be checked: 
daily_candle: list[dict[str: any]]
weekly_candle: list[dict[str: any]]
monthly_candle: list[dict[str: any]]
transaction_data: list[dict[str, any]]
Retry:
If failed, then go to re-try (5 times re-try limit and if reaching the limit, then emit the corresponding coin)

As the result, is candle_data_good: bool value is assigned

### DuckDuckGo Web Search
Input: candidate_coins
Action: web search and web scraping using DuckDuckGo search method in langchain
Update: articles: list[dict[str, dict[str, str]]]
Output: 
articles: list[dict[str, dict[str, str]]]

### Validate News
Input: articles: list[dict[str, dict[str, str]]]
Update: 
num_articles: int
are_articles_valid: bool
Action: If data (collected articles) valid, moves to the next node, otherwise go for re-trying. It should check the number of articles per coin (at least 5 articles) and if it’s a valid structure without omission (title, content)


These things should be checked: 
(Otherwise failed and go through re-tries)
at least 5 articles per coin (out of 20 different coins)
Published within 7 days 
reputable sources (Hard code the names of reputable coin news or mainstream news of around 30 or higher?)
scraping successful
If data structure has omission
Loop limit 2 times

Retry:
If failed, then go to re-try (2 times re-try limit and if reaching the limit, then emit the corresponding coin)
As the result, are_articles_valid: bool value is assigned


## Context Builder
Input: Bithumb API data, News data (duckduckgo) 
Update: merged_coin_data: list[str, dict[str, any] 
Output: merged_coin_data

should wait until the parallel process is complete (both done) and merge them


## Pre-Analysis Agent
Input: merged_coin_data
Output: pre_analysis_results: dict[str, PreAnalysisResult]

Analyze based on the API results of each coin and produce related attributes
Analyze coins based on titles only (to reduce LLM costs) and produce news_sentiment score
Pick the best 5 coins and pass them to Final Analysis Agent
LLM Analysis (gpt 5.5 mini) – lightweight model
Update top_5_coins based on the results


## Final Analysis Agent
Input:    top_5_coins
, merged_coin_data: Annotated[
        dict[str, CoinContext],
        merge_dicts,
    ]
Output:  final_report: list[FinalAnalysisResult]

Analyze the top 5 coins based on the full articles and API attributes
pre_analysis_results and merged_coin_data are used (reference based data structure)
top_5_coins are used to refer to the top 5 coins for ful analysis and merged_coin_data is mainly used for referring the full data of the selected top 5 coins (all technical metrics and full article content and so on)
LLM Analysis (gpt 5.5) - higher performant model

## Ranker_agent
Input: final_report: list[FinalAnalysisResult]
Output: top_3

Sort data by ranking 
Return the top 3 coins based on the final_score attribute


ranked = sorted(
    final_report,
    key=lambda coin: coin["final_score"],
    reverse=True,
)

top_3 = ranked[:3]
