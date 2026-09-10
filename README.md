# TrendPulse

Real-time Hacker News trend analysis dashboard using Python, Pandas, NumPy and Flask.

**Live Demo:** https://trendpulse-nine-beta.vercel.app

**GitHub:** https://github.com/Santhosh5254/TrendPulse

TrendPulse is a Python-based data analysis and visualization dashboard that collects stories from Hacker News, cleans and transforms the data using Pandas, performs statistical analysis using NumPy and Pandas, and presents the results through an interactive Flask web dashboard.

Users can analyze multiple Hacker News feeds:

- Top Stories
- New Stories
- Best Stories
- Ask HN
- Show HN

The project demonstrates an end-to-end data pipeline:

**API → Data Collection → Data Cleaning → Data Analysis → Visualization → Web Dashboard**

---

## 🚀 Features

- Fetches stories from the Hacker News API
- Supports multiple Hacker News feeds:
  - 🔥 Top Stories
  - 🆕 New Stories
  - ⭐ Best Stories
  - 💬 Ask HN
  - 🚀 Show HN
- Concurrently collects story data using Python `ThreadPoolExecutor`
- Fetches up to 200 stories per analysis
- Automatically categorizes stories into:
  - Technology
  - World News
  - Sports
  - Science
  - Entertainment
  - Other
- Cleans and validates data using Pandas
- Calculates statistical metrics using NumPy
- Performs category-level analysis using Pandas
- Calculates story engagement metrics
- Ranks stories based on engagement
- Identifies highly scored and highly commented stories
- Generates interactive charts using Chart.js
- Generates offline visualizations using Matplotlib
- Displays the top 10 stories in a dashboard table
- Provides direct links to Hacker News stories
- Saves cleaned and analyzed datasets as CSV files locally
- Uses a 5-minute in-memory cache to reduce repeated API requests
- Handles API and processing failures gracefully
- Responsive dashboard for desktop and mobile screens

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Flask | Web application and REST API |
| Requests | Hacker News API requests |
| Pandas | Data cleaning, transformation and aggregation |
| NumPy | Statistical analysis and numerical calculations |
| Matplotlib | Offline data visualization |
| Chart.js | Interactive dashboard charts |
| HTML/CSS | Frontend structure and styling |
| JavaScript | Dashboard interaction and API communication |

---

## 📊 Dashboard

The TrendPulse dashboard provides an overview of current Hacker News activity.

### Feed Selection

Users can select which Hacker News feed they want to analyze:

| Feed | Description |
|------|-------------|
| 🔥 Top | Currently trending top stories |
| 🆕 New | Recently submitted stories |
| ⭐ Best | Highly ranked stories |
| 💬 Ask HN | Ask HN discussions |
| 🚀 Show HN | Show HN project and product posts |

After selecting a feed, TrendPulse fetches and analyzes the corresponding Hacker News data.

---

## 📈 Key Metrics

The dashboard displays:

- Total Articles
- Average Score
- Median Score
- Average Comments
- Highest Score
- Most Common Category
- Most Commented Story

---

## 📊 Visualizations

### 1. Top Stories by Score

Displays the 10 highest-scored stories from the selected Hacker News feed.

### 2. Articles by Category

Shows the distribution of collected stories across the detected categories.

### 3. Score vs Comments

Visualizes the relationship between Hacker News scores and discussion activity.

This helps identify stories that receive both high community approval and significant discussion.

---

## 📋 Top Stories Table

The dashboard provides a ranked table containing:

- Story rank
- Story title
- Category
- Hacker News score
- Number of comments
- Direct Hacker News link

Story titles are clickable and open the original Hacker News post in a new tab.

---

## 🔄 Data Pipeline

```text
                    Hacker News API
                           │
                           ▼
              ┌─────────────────────┐
              │   Feed Selection     │
              │ Top / New / Best     │
              │ Ask HN / Show HN     │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  Data Collection     │
              │ Requests + Threads   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Data Cleaning      │
              │       Pandas         │
              └──────────┬──────────┘
                         │
                         ▼
                  trends_clean.csv
                         │
                         ▼
              ┌─────────────────────┐
              │    Data Analysis     │
              │   NumPy + Pandas     │
              └──────────┬──────────┘
                         │
                         ▼
                trends_analysed.csv
                         │
                         ▼
              ┌─────────────────────┐
              │    Flask Backend     │
              │      REST API        │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Interactive Dashboard│
              │   Chart.js + JS      │
              └─────────────────────┘