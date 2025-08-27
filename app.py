import os
import markdown
import google.generativeai as genai
from flask import Flask, request, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Flask app and the Gemini API
app = Flask(__name__)
genai.configure(api_key=os.getenv("API_KEY"))

# This is the prompt template
def get_master_prompt(company_name, ticker):
    return f"""
Act as a Senior Financial Analyst. Your task is to generate a comprehensive investment research report on {company_name} ({ticker}). The report should be structured, data-driven, and objective, using the most recently available public data.

Generate the report in the following standard format, using Markdown for formatting:

## 1. Company Overview
* **Company:** {company_name} ({ticker})
* **Sector:**
* **Industry:**
* **Core Business:**

## 2. Recent Stock Performance
* **Current Stock Price:**
* **52-Week Range:**
* **Market Capitalization:**

## 3. Financial Analysis
* **Revenue (Last Quarter & TTM):**
* **Net Income (Last Quarter & TTM):**
* **EPS (TTM):**
* **Profit Margins (Gross, Net):**

## 4. Key Metrics & Valuation
* **P/E Ratio (TTM):**
* **Forward P/E Ratio:**
* **P/S Ratio (TTM):**

## 5. SWOT Analysis
* **Strengths:**
* **Weaknesses:**
* **Opportunities:**
* **Threats:**

## 6. Hypothetical Investment Thesis
**Disclaimer:** This is a hypothetical analysis for informational purposes only.
* **Bull Case:**
* **Bear Case:**
* **Key Technical Indicators (RSI, 50-day/200-day SMA):**
"""

# Route for the homepage (displays the input form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and display the report
@app.route('/generate', methods=['POST'])
def generate():
    company_name = request.form['company_name']
    ticker = request.form['ticker']

    prompt = get_master_prompt(company_name, ticker)

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    report_html = markdown.markdown(response.text)
    return render_template('report.html', report_content=report_html)