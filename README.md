Sales Analytics System
A complete end‑to‑end pipeline for reading sales data, validating it, enriching it with external API product information, 
performing analytics, and generating a comprehensive formatted report.

Features
Read and parse raw sales data
Optional filtering by region and amount
Validation of transaction records
Full analytics suite:
    Total revenue
    Region‑wise performance
    Top products
    Top customers
    Daily sales trend
    Product performance insights
API integration with DummyJSON
Enrichment of sales data with product metadata
Pipe‑delimited enriched output file
Fully formatted text report
Clean CLI‑style progress messages
Error handling

requirements.txt should include:
requests>=2.31.0

Project Structure
sales-analytics-system/
  ├── README.md
  ├── main.py
  ├── utils/
  │   ├── file_handler.py
  │   ├── data_processor.py
  │   └── api_handler.py
  ├── data/
  │   └── sales_data.txt (provided)
  ├── output/
  └── requirements.txt

Install dependencies
pip install -r requirements.txt

Running the Program
From the project root:

Code
python main.py

1.Enriched Sales Data saved automatically to:
data/enriched_sales_data.txt

2. Final Sales Report saved automatically to:
output/sales_report.txt

Error Handling
The entire code is wrapped in a try-except block.
If anything goes wrong, the program prints a message.
