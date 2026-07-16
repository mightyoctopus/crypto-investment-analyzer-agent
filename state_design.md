# State Design 


from __future__ import annotations
from datetime import datetime
from typing import Annotated, Literal, TypeVar, TypedDict


T = TypeVar("T")


## Reducers for parallel LangGraph updates

def merge_dicts(
    current: dict,
    incoming: dict,
) -> dict:
    """
    Merge dictionary updates produced by parallel LangGraph branches.

    Example:
        current = {"BTC": btc_data}
        incoming = {"ETH": eth_data}

        result = {
            "BTC": btc_data,
            "ETH": eth_data,
        }
    """
    return {**current, **incoming}


def merge_list_dicts(
    current: dict[str, list[T]],
    incoming: dict[str, list[T]],
) -> dict[str, list[T]]:
    """
    Merge dictionary updates whose values are lists.
    """
    merged = {**current}
    for key, values in incoming.items():
        merged[key] = merged.get(key, []) + values
    return merged


def append_unique_strings(
    current: list[str],
    incoming: list[str],
) -> list[str]:
    """
    Append strings while preventing duplicates.
    """
    return list(dict.fromkeys(current + incoming))


def append_reducer(
    current: list[T],
    incoming: list[T],
) -> list[T]:
    """
    Append list updates produced by parallel LangGraph branches.
    """
    return current + incoming



## Basic domain types

class Candle(TypedDict):
    symbol: str
    market: str
    candle_date_time_kst: str
    opening_price: float
    high_price: float
    low_price: float
    trade_price: float
    previous_closing_price: float
    change_rate: float
    trade_volume: float


class CandleBundle(TypedDict):
    """
    All candle timeframes belonging to one coin.
    """
    daily: list[Candle]
    weekly: list[Candle]
    monthly: list[Candle]


class TransactionData(TypedDict):
    symbol: str
    market: str
    highest_52_week_price: float
    lowest_52_week_price: float
    trade_price: float
    accumulated_trade_volume_24h: float
    accumulated_trade_price_24h: float


class Article(TypedDict):
    title: str
    content: str
    url: str
    source: str
    published_at: str



## Validation and retry types

ValidationState = Literal[
    "pending",
    "valid",
    "invalid",
    "retrying",
    "failed",
]


class ValidationResult(TypedDict):
    is_valid: bool
    status: ValidationState
    retry_count: int
    reason: str | None
    checked_at: str | None


class CoinFailure(TypedDict):
    symbol: str
    stage: Literal[
        "candle_fetch",
        "candle_validation",
        "news_fetch",
        "news_validation",
        "pre_analysis",
        "final_analysis",
    ]
    reason: str
    retry_count: int


## Merged context

class CoinContext(TypedDict):
    """
    Full data for one coin after candle, transaction,
    and article collection are complete.
    """
    symbol: str
    market: str
    candles: CandleBundle
    transaction: TransactionData
    articles: list[Article]


## Pre-analysis types

class PreAnalysisResult(TypedDict):
    symbol: str
    bullish_score: float
    risk_score: float
    news_sentiment: float
    technical_strength: float
    potential_score: float
    confidence: float
    summary: str
    pre_anal_score: float



## Final-analysis types

Recommendation = Literal[
    "strong_buy",
    "buy",
    "hold",
    "avoid",
    "sell",
]


Trend = Literal[
    "strongly_bullish",
    "bullish",
    "neutral",
    "bearish",
    "strongly_bearish",
]


class FinalAnalysisResult(TypedDict):
    symbol: str
    long_term_potential: float
    confidence: float
    trend: Trend
    news_sentiment: float
    technical_strength: float
    risk_level: float
    summary: str
    reasons: list[str]
    risks: list[str]
    recommendation: Recommendation
    final_score: float


## Main LangGraph shared state

class CryptoAnalysisState(TypedDict):
    # --------------------------------------------------------
    # Initial request / selection
    # --------------------------------------------------------

    trading_pairs: list[str]
    candidate_coins: list[str]

    # --------------------------------------------------------
    # Search-query construction
    # --------------------------------------------------------

    search_queries: dict[str, str]

    # Example:
    # {
    #     "BTC": "Bitcoin BTC news",
    #     "ETH": "Ethereum ETH news",
    # }

    # --------------------------------------------------------
    # Raw data collection
    # --------------------------------------------------------

    candle_data: Annotated[
        dict[str, CandleBundle],
        merge_dicts,
    ]

    transaction_data: Annotated[
        dict[str, TransactionData],
        merge_dicts,
    ]

    articles: Annotated[
        dict[str, list[Article]],
        merge_list_dicts,
    ]

    # Example:
    # {
    #     "BTC": [
    #         {
    #             "title": "...",
    #             "content": "...",
    #             "url": "...",
    #             "source": "...",
    #             "published_at": "...",
    #         }
    #     ]
    # }

    # --------------------------------------------------------
    # Validation and retry state
    # --------------------------------------------------------

    candle_validation: Annotated[
        dict[str, ValidationResult],
        merge_dicts,
    ]

    news_validation: Annotated[
        dict[str, ValidationResult],
        merge_dicts,
    ]

    failed_coins: Annotated[
        list[str],
        append_unique_strings,
    ]

    failures: Annotated[
        list[CoinFailure],
        append_reducer,
    ]

    # --------------------------------------------------------
    # Merged per-coin context
    # --------------------------------------------------------

    merged_coin_data: Annotated[
        dict[str, CoinContext],
        merge_dicts,
    ]

    # Example:
    # {
    #     "BTC": {
    #         "symbol": "BTC",
    #         "market": "KRW-BTC",
    #         "candles": {...},
    #         "transaction": {...},
    #         "articles": [...],
    #     }
    # }

    # --------------------------------------------------------
    # Pre-analysis
    # --------------------------------------------------------

    pre_analysis_results: dict[str, PreAnalysisResult]

    top_5_coins: list[str]

    # Example:
    # [
    #     {
    #         "symbol": "BTC",
    #         "potential_score": 0.92,
    #     }
    # ]

    # --------------------------------------------------------
    # Final analysis and ranking
    # --------------------------------------------------------

    final_report: list[FinalAnalysisResult]

    # --------------------------------------------------------
    # Overall graph status
    # --------------------------------------------------------

    completed: bool
