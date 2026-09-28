# 🧠 NeuroLock Engine — Predictive Database Lock Interceptor & Belady-Assisted Memory OS

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-orange.svg)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0%2B-003B57.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Engine-ONLINE-00FF7F.svg)](#)

> **A Proactive AI-Driven Transaction Scheduler and Buffer Pool Manager designed to eliminate DBMS Deadlocks and Buffer Cache Anomalies before execution.**

---

## 🚨 The Fundamental Problem: Traditional DBMS Limitations

In modern high-concurrency relational database systems (RDBMS) such as PostgreSQL, MySQL, or SQLite, handling concurrent write transactions is a major architectural bottleneck. Traditional lock managers operate **reactively**, creating severe operational inefficiencies:

### 1. The Deadlock & Lock Contention Crisis
When multiple parallel execution threads attempt to acquire exclusive write locks (`EXCLUSIVE WRITE`) on the same target table or page simultaneously:
- **Lock Contention:** Thread B blocks waiting for Thread A to release its lock. Under heavy load, thousands of threads stall, leading to exponential latency spikes.
- **Deadlocks (Circular Wait):** If Thread A holds Resource 1 and requests Resource 2, while Thread B holds Resource 2 and requests Resource 1, a deadlock occurs.
- **The Reactive Abort Penalty:** Traditional database engines wait until a timeout occurs or run periodic deadlock detection graph cycles (e.g., Wait-For Graph analysis). When a deadlock is detected, the engine **forcefully aborts and rolls back** one of the transactions. This wastes precious CPU cycles, disk I/O, and compute work that must be re-executed from scratch.

### 2. Reactive Buffer Pool Management & Belady's Anomaly
Database engines maintain an in-memory **Buffer Pool (RAM Cache)** to prevent frequent disk read operations. Standard engines utilize **FIFO (First-In-First-Out)** or **LRU (Least Recently Used)** cache eviction strategies:
- **Historical Bias:** LRU only looks at *past access history* to make eviction decisions. It is completely blind to upcoming future transactions.
- **Belady's Anomaly:** Under specific workload spikes, increasing the allocated cache RAM can paradoxically *increase* the page fault rate in FIFO/LRU strategies, degrading overall system throughput.

---

## 💡 System Architecture

```mermaid
graph TD
    A[Incoming SQL Transactions] --> B[1. AST & Feature Parser]
    B -->|Extracts Mutation Vector| C[2. Random Forest ML Predictor]
    
    C -->|Hazard Risk = High| D[3a. Proactive Thread Scheduler]
    C -->|Hazard Risk = Low| E[3b. Direct Parallel Dispatch]
    
    D -->|Imposes 1000ms Micro-Delay| F[ACID Serial Execution]
    E --> F
    
    F --> G[4. Belady OPT Buffer Pool Cache]
    G --> H[(5. Target SQLite Storage Engine)]

    style A fill:#1f2937,stroke:#3b82f6,stroke-width:2px,color:#fff
    style B fill:#1e293b,stroke:#64748b,stroke-width:2px,color:#fff
    style C fill:#374151,stroke:#f59e0b,stroke-width:2px,color:#fff
    style D fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#fff
    style E fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff
    style G fill:#065f46,stroke:#059669,stroke-width:2px,color:#fff
    style H fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff