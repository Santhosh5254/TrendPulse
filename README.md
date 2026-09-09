# TrendPulse

Real-time Hacker News trend analysis dashboard using Python, Pandas, NumPy and Flask.

**Live Demo:** https://trendpulse-nine-beta.vercel.app  
**GitHub:** https://github.com/Santhosh5254/TrendPulse

TrendPulse is a Python-based data analysis and visualization dashboard that collects trending stories from Hacker News, cleans and transforms the data using Pandas, performs statistical analysis using NumPy and Pandas, and presents the results through an interactive Flask web dashboard.

The project demonstrates an end-to-end data pipeline:

**API → Data Collection → Data Cleaning → Data Analysis → Visualization → Web Dashboard**

---

## 🚀 Features

- Fetches the latest trending stories from Hacker News
- Concurrently collects story data using Python
- Automatically categorizes stories into:
  - Technology
  - World News
  - Sports
  - Science
  - Entertainment
- Cleans and validates data using Pandas
- Calculates statistical metrics using NumPy
- Performs category-level analysis using Pandas
- Calculates story engagement metrics
- Identifies highly scored and highly commented stories
- Generates interactive charts using Chart.js
- Displays the top 10 stories in a dashboard table
- Provides direct links to Hacker News stories
- Saves cleaned and analyzed datasets as CSV files
- Uses a 5-minute in-memory cache to avoid unnecessary API requests
- Handles API and processing failures gracefully

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Flask | Web application and API |
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

### Key Metrics

- Total Articles
- Average Score
- Median Score
- Average Comments
- Highest Score
- Most Common Category
- Most Commented Story

### Visualizations

#### 1. Top Stories by Score

Displays the 10 highest-scored Hacker News stories.

#### 2. Articles by Category

Shows the distribution of collected stories across categories.

#### 3. Score vs Comments

Visualizes the relationship between Hacker News scores and discussion activity.

### Top Stories Table

The dashboard also provides a ranked table containing:

- Story title
- Category
- Hacker News score
- Number of comments
- Direct Hacker News link

---

## 🔄 Data Pipeline

```text
                    Hacker News API
                          │
                          ▼
                ┌──────────────────┐
                │ Data Collection  │
                │   Requests       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Data Cleaning    │
                │     Pandas       │
                └────────┬─────────┘
                         │
                         ▼
                trends_clean.csv
                         │
                         ▼
                ┌──────────────────┐
                │ Data Analysis    │
                │ NumPy + Pandas   │
                └────────┬─────────┘
                         │
                         ▼
               trends_analysed.csv
                         │
                         ▼
                ┌──────────────────┐
                │ Flask Backend    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Interactive      │
                │ Dashboard        │
                │ Chart.js + JS    │
                └──────────────────┘