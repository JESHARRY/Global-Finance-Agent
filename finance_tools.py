import yfinance as yf
import requests
import os
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def get_exchange_rates(base_currency: str):
    """Fetches exchange rates from a base currency (like JPY) to USD, INR, GBP, and EUR."""
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    
    try:
        response = requests.get(url)
        # Check for HTTP errors (403, 404, etc.)
        response.raise_for_status() 
        
        data = response.json()
        if data.get("result") == "success":
            rates = data["conversion_rates"]
            targets = ["USD", "INR", "GBP", "EUR"]
            filtered_rates = {t: rates.get(t) for t in targets}
            return f"1 {base_currency} is currently worth: {filtered_rates}"
        else:
            return f"API Error: {data.get('error-type', 'Unknown error')}"
            
    except Exception as e:
        return f"Failed to fetch rates: {str(e)}"

@tool
def get_stock_index_info(country: str):
    """Returns the primary stock index name and its current value for a country."""
    indices = {
        "Japan": "^N225", "India": "^BSESN", "US": "^GSPC",
        "South Korea": "^KS11", "China": "000001.SS", "UK": "^FTSE"
    }
    ticker_symbol = indices.get(country)
    if not ticker_symbol:
        return f"Could not find an index ticker for {country}."
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        # Use fast_info for modern yfinance compatibility
        current_val = ticker.fast_info.last_price
        
        if current_val is None:
            return f"Data for {ticker_symbol} is currently unavailable from Yahoo Finance."
            
        return f"The major index for {country} ({ticker_symbol}) is currently at {current_val:.2f}."
    except Exception as e:
        return f"Stock data error: {str(e)}"

@tool
def get_hq_location_link(exchange_name: str):
    """Provides a Google Maps search link for a stock exchange's headquarters."""
    formatted_query = exchange_name.replace(" ", "+")
    # Updated link structure for reliability
    return f"Google Maps HQ Link: https://www.google.com/maps/search/?api=1&query={formatted_query}+headquarters"