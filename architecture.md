# Architecture of Crypto Investment Analysis

## Purpose: 
This app is built for analyzing crypto coins 
from Bithumb API and news articles and predict 
crypto coins that are worth investing and have the highest 
potentials for the sake of long term investment from the time 
of analyzing.

## Architecture Diagram
![Crypto Investment Analysis Diagram](Crypto%20Investment%20Analyzer.jpg)


## Workflow Explained

### NOTE: 
some state names or input/output names could have
been modified and not updated to the architecture yet.
So do not strictly go by names but use your general sense
to reflect the states and input/output flow as the concepts
are still the same, but just the names changed compared to
the details/instruction inside node_design.md or state_design.md.


### 1. Infrastructure Framework
- Initialize the overall system.
- Configure:
  - API clients
  - Environment settings
  - Memory (if applicable. Not sure how it should be handled)
  - Management utilities
  - Application configuration

↓

### 2. Planner
- Acts as the workflow orchestrator.
- Controls the execution sequence of all agents.

↓

### 3. Selector Agent
- Retrieve initial Bithumb trading-pair names and store them in `trading_pairs`.
- Use temporary Bithumb market metrics inside this node for deterministic scoring.
- Select the **Top 20 candidate coins** with the highest potential for price appreciation.
- No LLM involved at this node. It should be rule based and deterministic logic.
- The raw market data used here is only for selection. The later Market Data branch remains the canonical source for `candle_data` and `transaction_data`.
- Output:
  - `candidate_coins`
↓

## 4. Parallel Data Collection

### Market Data
- Retrieve market information from the **Bithumb API**.
- Validate API response.
- Retry up to **5 times** if the response is invalid.

### News Data
- Search recent news using **DuckDuckGo Web Search** in langchain.
- Validate retrieved news.
- Retry up to **2 times** if validation fails.

Both branches execute **in parallel**.

↓

## 5. Context Builder
- Wait until both parallel branches complete.
- Merge:
  - Market data
  - News articles
- Build a unified context for each candidate coin.

↓

## 6. Pre-Analysis Agent
- Lightweight model: GPT 5.5 mini (or a cheaper model that performs good at this degree)
- Analyze the 20 candidate coins only by API results and the titles of web-scraping results(DuckDuckGo)
to reduce the token usages and costs. (No full article content provided for analysis at this stage)
- Produce an initial investment evaluation.
- Assign:
  - symbol: str 
  - bullish_score: float 
  - risk_score: float 
  - news_sentiment: float (by only news titles)
  - technical_strength: float 
  - potential_score: float 
  - confidence: float 
  - summary: str 
  - pre_anal_score: float

- Select the **Top 5 coins** with the highest potential by pre_anal_score which
works as the comprehensive score for each coin at pre-analysis agent stage

↓

## 7. Final Analysis Agent
- Serious model: GPT 5.5 
- Perform a deeper analysis of the Top 5 coins.
- Use:
  - Complete market data
  - Full article news analysis (Not only by titles)
  - Historical information
  - Additional structured data
- Generate detailed investment reasoning.

↓

## 8. Ranker Agent
- Calculate the final investment score.
- Rank all analyzed coins.
- Return the final investment recommendations (as for a long-term investment) of top 3 coins by slicing the ranked `final_report`.
