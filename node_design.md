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
Input: NONE
Update:
- trading_pairs: list[str]
- candidate_coins: list[str]
Output: candidate_coins: list[str]

- Request Bithumb trading-pair names and store the initial target names in `trading_pairs`.
- Use temporary Bithumb market metrics inside this node to score candidates:
  - trade_volume from daily/weekly/monthly candles
  - highest_52_week_price
  - lowest_52_week_price
  - previous_closing_price from daily/weekly/monthly candles
  - high_price from daily/weekly/monthly candles
  - low_price from daily/weekly/monthly candles
  - trade_price from daily/weekly/monthly candles
- Select the **Top 20 candidate coins** with the highest potential for price appreciation.
- No LLM involved at this node. It should use rule-based and deterministic filtering logic.
- The temporary market data used for selection is not written to `candle_data` or `transaction_data`; the Bithumb API branch remains the canonical market-data collection step.
- Pass the selected 20 coins directly into the parallel data collection workflow.


## Parallel Data Collection
### Bithumb API 
Input: candidate_coins
Update: 
- candle_data: dict[str, CandleBundle]
- transaction_data: dict[str, TransactionData]
Output: 
- candle_data: dict[str, CandleBundle]
- transaction_data: dict[str, TransactionData]
Request data via Bithumb on the selected 20 coins for each. Daily, weekly, monthly candles and transaction data are required.

### Validate Bithumb API
Input: 
- candle_data: dict[str, CandleBundle]
- transaction_data: dict[str, TransactionData]
Update:
- candle_validation: dict[str, ValidationResult]
- failed_coins: list[str]
- failures: list[CoinFailure]
Action: If data valid, moves to the next node, otherwise go for re-trying
These data from Bithumb API should be checked: 
- candle_data daily/weekly/monthly candle completeness
- transaction_data completeness
Retry:
If failed, then go to re-try (5 times re-try limit and if reaching the limit, then emit the corresponding coin)

As the result, `candle_validation` is assigned per coin.

### DuckDuckGo Web Search
Input: candidate_coins
Action: web search and web scraping using DuckDuckGo search method in langchain
Update: articles: dict[str, list[Article]]
Output: 
articles: dict[str, list[Article]]

### Validate News
Input: articles: dict[str, list[Article]]
Update: 
- news_validation: dict[str, ValidationResult]
- failed_coins: list[str]
- failures: list[CoinFailure]
Action: If data (collected articles) valid, moves to the next node, otherwise go for re-trying. It should check the number of articles per coin (at least 5 articles) and if it’s a valid structure without omission (title, content)


These things should be checked: 
(Otherwise failed and go through re-tries)
- at least 5 articles per coin (out of 20 different coins)
- Published within 7 days 
- reputable sources (Hard code the names of reputable coin news or mainstream news of around 30 or higher?)
- scraping successful
- If data structure has omission
- Loop limit 2 times

Reputable source allowlist for news validation:
TRUSTED_NEWS_SOURCES = [
   
    "coindesk.com",
    "theblock.co",
    "decrypt.co",
    "blockworks.co",
    "cointelegraph.com",
    "cryptoslate.com",
    "cryptobriefing.com",
    "bitcoinmagazine.com",
    "coinmarketcap.com",
    "coinpedia.org",
    "messari.io",
    "glassnode.com",
    "chainalysis.com",
    "trmlabs.com",
    "elliptic.co",
    "kaiko.com",
    "ccdata.io",
    "coinmetrics.io",
    "reuters.com",
    "apnews.com",
    "bloomberg.com",
    "ft.com",
    "wsj.com",
    "barrons.com",
    "cnbc.com",
    "fortune.com",
    "forbes.com",
    "nasdaq.com",
    "marketwatch.com",
    "investing.com",
    "yahoo.com",
    "fxstreet.com",
    "stocktwits.com",
]

Retry:
If failed, then go to re-try (2 times re-try limit and if reaching the limit, then emit the corresponding coin)
As the result, `news_validation` is assigned per coin.


## Context Builder
Input: Bithumb API data, News data (duckduckgo) 
Update: merged_coin_data: dict[str, CoinContext]
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
Output: top_3 extracted from final_report

Sort data by ranking 
Return the top 3 coins based on the final_score attribute without storing a separate duplicated state field


ranked = sorted(
    final_report,
    key=lambda coin: coin["final_score"],
    reverse=True,
)

top_3 = ranked[:3]
