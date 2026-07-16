# Crypto Investment Agentic System

An agentic cryptocurrency investment analysis system built with **LangGraph**.

The system retrieves market data from the **Bithumb API** and cryptocurrency news from the web, performs multi-stage AI analysis, and recommends the top cryptocurrencies for **long-term investment**.

---

## Features

- Multi-stage agentic workflow built with LangGraph
- Deterministic candidate selection (no LLM)
- Parallel market-data and news collection
- Automatic validation and retry mechanisms
- Cost-efficient two-stage LLM analysis
- Structured shared state using TypedDict
- Long-term investment ranking

---

## Tech Stack

- Python 3.13
- LangGraph
- LangChain
- FastAPI
- OpenAI GPT-5.5
- DuckDuckGo Search
- Bithumb Open API

---

## High-Level Workflow

```
Bithumb Trading Pairs
        │
        ▼
Selector Agent
(Top 20 Candidates)
        │
        ▼
 ┌───────────────────────────────┐
 │ Parallel Data Collection       │
 │                                │
 │ • Bithumb API                  │
 │ • DuckDuckGo News Search       │
 └──────────────┬────────────────┘
                │
                ▼
        Context Builder
                │
                ▼
      Pre-Analysis Agent
        (GPT-5.5 Mini)
       Top 20 → Top 5
                │
                ▼
      Final Analysis Agent
          (GPT-5.5)
                │
                ▼
         Ranker Agent
                │
                ▼
      Top 3 Investment Picks
```

---

## Agent Responsibilities

| Agent | Responsibility |
|-------|----------------|
| Selector Agent | Select the Top 20 candidate coins using deterministic market metrics. |
| Bithumb API | Collect candle and transaction data. |
| News Search | Retrieve recent cryptocurrency news articles. |
| Validation Nodes | Validate collected data and retry failed requests. |
| Context Builder | Merge market and news data into a unified coin context. |
| Pre-Analysis Agent | Perform lightweight AI analysis using API data and news titles. |
| Final Analysis Agent | Perform in-depth AI analysis using complete market data and full news articles. |
| Ranker Agent | Rank analyzed coins and return the Top 3 recommendations. |

---

## Cost Optimization

To minimize LLM costs, the workflow uses two analysis stages.

### Stage 1 – Pre-Analysis

- GPT-5.5 Mini
- Analyze API data
- Analyze news titles only
- Select Top 5 coins

### Stage 2 – Final Analysis

- GPT-5.5
- Analyze complete market data
- Analyze full article contents
- Produce detailed investment recommendations

---

## Validation

### Bithumb API

- Candle completeness
- Transaction completeness
- Retry up to 5 times

### News

- Minimum 5 articles per coin
- Published within the last 7 days
- Trusted news sources
- Valid article structure
- Retry up to 2 times

---

## Project Structure

```
crypto_investment_agentic_system/

├── README.md
├── AGENTS.md
├── architecture.md
├── state_design.md
├── node_design.md
├── main.py
└── Crypto Investment Analyzer.jpg
```

---

## Documentation

Detailed documentation can be found in:

- **architecture.md** — Overall system architecture and workflow
- **state_design.md** — Shared LangGraph state and reducers
- **node_design.md** — Detailed node responsibilities, inputs, outputs, and processing logic
- **AGENTS.md** — Instructions for AI coding assistants (Codex / Claude Code)

---

## Current Status

- [x] Architecture completed
- [x] State design completed
- [x] Node design completed
- [ ] LangGraph implementation
- [ ] FastAPI integration
- [ ] Testing
- [ ] Deployment

---

## Future Improvements

- Portfolio simulation
- Historical backtesting
- Technical indicator expansion
- Notification system
- Portfolio management
- Scheduler for periodic analysis
- Dashboard