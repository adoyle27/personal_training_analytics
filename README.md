# personal_training_analytics
## Overview
The analysis identified approximately $1.1k in monthly unrealized revenue opportunity driven by underutilized client capacity. \
This project analyzes client utilization, revenue concentration, and unrealized capacity for a personal trainer using an anonymized real-world dataset. The goal was to identify where revenue is generated, where schedule capacity exists, and which clients represent growth opportunities. \
The analysis combines Excel based data preperation with a Python analytics pipeline to produce automated metrics, segmentation logic, and visual insights.
## Business Questions
- Which clients generate the most revenue? 
- Are some clients under utilizing their scheduled capacity? 
- How concentrated is revenue across clients? 
- What is the monthly revenue oppurtunity from unused training hours?
## Dataset
The dataset represents three months of client activity and includes:
- Client ID (anonymized)
- Service frequency (once/week, twice/week)
- Ideal monthly training hours
- Actual hours delivered (Three months)
- Session type (30 min vs 60 min)
All personally identifiable information was removed.
## Data Preparation (Excel)
- Standardize client utilization metrics
- Calculated expected vs actual hours
- Derived utilization percentage
- Computed revenue and average monthly revenue
- Created segmentation rules based on revenue and utilization
## Analytics Pipeline (Python)
- Automated feature engineering
- Revenue share analysis
- Segment aggregation
- Opportunity estimation from unused hours
- Visualization generation
Libraries Used: \
- pandas
- matplotlib
- openpyxl
## Key Insights 
- Revenue is highly concentrated among a small group of anchor clients
- Several high-value clients still exhibit unused training capacity
- Approximately 19 unused hours exist per month on average
- This represents roughly $1.1k monthly revenue opportunity
## Dashboard
- ### Average Monthly Revenue by Client Segment
- ### Unrealized Training Hours by Client (3 Months)
## Project Structure
```
analysis.py                 # analytics pipeline
clean_data.xlsx             # prepared dataset
client_metrics.csv          # engineered client metrics
segment_summary.csv         # aggregated segment metrics
revenue_by_segment.png      # visualization
unrealized_hours_by_client.png
```
## Skills Demonstrated
- Data cleaning & preparation
- Feature engineering
- Business metric design
- Segmentation strategy
- Exploratory data analysis
- Visualization
- Python automation
## Future Improvements
- Interactive dashboard (Power BI / Streamlit)
- Time-series revenue forecasting
- Cancellation behavior analysis
- Schedule optimization model
