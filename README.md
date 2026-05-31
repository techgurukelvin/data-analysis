# Ajira Kenya Data Analysis
- This is a Python script to analyze and visualize simulated performance data from the Ajira Digital Program, a Kenyan government initiative to empower youth with digital skills.
- The script generates insights on youth trained, jobs placed, gender distribution, and main sectors across seven counties.

## Features
- Analyzes county-level data for Nairobi, Mombasa, Kisumu, Nakuru, Machakos, Turkana, and Wajir
- Creates interactive visualizations (scatter plot, bar charts)
- Exports data and charts to Excel
- Simulates real-world dashboard from provided data

## Requirements
Python 3.13
pandas>=2.2.0
matplotlib>=3.8.0
seaborn>=0.13.0
openpyxl
numpy>=2.0.0

## Installation
```bash
# Create project
mkdir ajira_analysis && cd ajira_analysis   

# Create virtual environment
python -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies/libraries
pip install -r requirements.txt

# Export all Python packages & their versions
pip freeze > dev-requirements.txt
```# data-analysis
