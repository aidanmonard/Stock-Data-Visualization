# Stock-Data-Visualization

A Python app that gets stock data from the Alpha Vantage API and shows it as a chart in your web browser.

What it does
Asks for a stock symbol (for example IBM)
Asks for a chart type (Bar or Line)
Asks for a time series (Intraday, Daily, Weekly or Monthly)
Asks for a begin date and an end date (YYYY-MM-DD)
Opens the chart in your default browser

Setup
Get a free API key at https://www.alphavantage.co/support/#api-key
Download or clone this repo and open the folder in a terminal.
Install the packages:
   pip install -r requirements.txt
Copy .env.example to a new file named .env:
   cp .env.example .env
Open .env and put your key in it:

   ALPHAVANTAGE_API_KEY=your_real_key

Run
python main.py

On a Mac, use python3 instead of python (and pip3 if pip isn't found).

Files
File	Purpose
main.py	Runs the app
inputs.py	Asks the user questions and checks answers
api.py	Gets data from Alpha Vantage
charts.py	Builds the chart and opens it


