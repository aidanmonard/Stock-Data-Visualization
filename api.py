import os

import requests

try:  # optional: load ALPHAVANTAGE_API_KEY from a local .env file
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_URL = "https://nam02.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.alphavantage.co%2Fquery&data=05%7C02%7Cgcttxc%40missouri.edu%7C6cab71dbc8704d9cb9f008df36cdfa77%7Ce3fefdbef7e9401ba51a355e01b05a89%7C0%7C0%7C639289930426025424%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=wW6Rs5c8XYkFYQEpOxJxmeyACHaxEB1Uss8Ot3yDUtQ%3D&reserved=0"


class StockDataError(Exception):
  


def get_api_key():
    key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not key:
        raise StockDataError(
            "No API key found. Set the ALPHAVANTAGE_API_KEY environment "
            "variable or put it in a .env file (see .env.example)."
        )
    return key


def fetch_stock_data(symbol, function):
        params = {"function": function, "symbol": symbol, "apikey": get_api_key()}
    if function == "TIME_SERIES_INTRADAY":
        params["interval"] = "60min"
        params["outputsize"] = "full"
    elif function == "TIME_SERIES_DAILY":
        params["outputsize"] = "full"  # default only returns the last 100 days

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise StockDataError(f"Network problem contacting Alpha Vantage: {exc}")
    except ValueError:
        raise StockDataError("Alpha Vantage returned data that was not valid JSON.")

    if "Error Message" in payload:
        raise StockDataError(f"Alpha Vantage rejected the request (bad symbol?): "
                             f"{payload['Error Message']}")
    for note_key in ("Note", "Information"):
        if note_key in payload:
            raise StockDataError(f"Alpha Vantage message: {payload[note_key]}")

    for key, value in payload.items():
        if key.startswith(("Time Series", "Weekly", "Monthly")):
            return value
    raise StockDataError("No time series data found in the response.")


def filter_by_date(series, start, end):
  
    rows = []
    for timestamp, values in series.items():
        day = timestamp[:10]  # intraday keys look like "2024-03-15 16:00:00"
        if str(start) <= day <= str(end):
            rows.append((timestamp, {
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
            }))
    rows.sort(key=lambda row: row[0])
    if not rows:
        raise StockDataError("No data available for that date range.")
    return rows
