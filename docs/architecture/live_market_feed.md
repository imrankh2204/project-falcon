# Project Falcon

# Live Market Feed Architecture

## FAL-610-R3

## Purpose

This document defines the live market feed architecture boundary for Project Falcon.

The objective is to support future real-time broker feeds while keeping the runtime independent from:

* broker APIs
* WebSocket implementations
* authentication mechanisms
* exchange-specific protocols

The runtime consumes market events through a stable abstraction.

---

# Architecture Overview

The market data flow is:

```
Market Data Source
        |
        v
    MarketFeed
        |
        v
   MarketEvent
        |
        v
  LiveRuntime
        |
        v
 Strategy / Trading Pipeline
```

The source of market data is replaceable.

Supported and future implementations:

```
                 MarketFeed

                     |
        +------------+------------+
        |                         |
        v                         v

ReplayMarketFeed          ZerodhaMarketFeed
(current)                 (future)
        |
        v
 ReplayEngine
```

---

# MarketFeed Contract

The `MarketFeed` abstraction defines the runtime boundary.

Location:

```
app/live/market_feed.py
```

Responsibilities:

* Start feed lifecycle
* Stop feed lifecycle
* Provide market events
* Remain broker independent

The runtime depends only on this contract.

---

# ReplayMarketFeed

Current implementation:

```
app/live/replay_market_feed.py
```

Purpose:

* Adapt deterministic replay data into runtime events
* Preserve replay ordering
* Provide a MarketFeed implementation for testing and backtesting

Flow:

```
HistoricalDataProvider
        |
        v
 ReplayEngine
        |
        v
ReplayMarketFeed
        |
        v
 CandleEvent
        |
        v
 LiveRuntime
```

Replay-specific components remain isolated from the runtime.

---

# Future Broker Feed

Future broker integrations must implement the same `MarketFeed` contract.

Example:

```
Zerodha WebSocket
        |
        v
ZerodhaMarketFeed
        |
        v
MarketEvent
        |
        v
LiveRuntime
```

The runtime must not know:

* which broker is connected
* how data is received
* how authentication works
* how messages are formatted

---

# Event Conversion Responsibility

External market data must be converted at the feed boundary.

Example:

Broker tick:

```
{
    symbol: "NIFTY",
    price: 24500
}
```

is converted into:

```
TickEvent(
    symbol="NIFTY",
    price=24500
)
```

The runtime receives only:

```
MarketEvent
```

---

# Lifecycle Model

A live feed lifecycle follows:

```
start()
   |
   v
Connect
   |
   v
Subscribe
   |
   v
Receive Events
   |
   v
stop()
   |
   v
Disconnect
```

Lifecycle management remains inside the feed implementation.

---

# Error Boundary

Broker-specific failures must remain inside the adapter.

Examples:

* connection timeout
* authentication failure
* subscription failure
* websocket disconnect

The future broker adapter is responsible for translating external failures into Falcon-compatible behavior.

---

# Design Principles

The live feed architecture follows:

## Single Responsibility

Market feeds only provide market events.

They do not:

* execute trades
* evaluate strategies
* manage risk

---

## Dependency Inversion

Runtime depends on:

```
MarketFeed
```

not:

```
Broker SDK
Historical Files
WebSocket Client
```

---

## Broker Independence

Future broker integrations are adapters.

Replacing the broker should not require changes to:

* LiveRuntime
* Strategy Engine
* Trading Domain

---

# Current Status

Completed:

* MarketFeed contract
* ReplayMarketFeed adapter
* MarketEvent abstraction
* CandleEvent support

Future:

* Zerodha live adapter
* WebSocket integration
* Tick aggregation
* Real-time candle generation
