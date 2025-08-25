import requests
import pandas as pd

def fetch_data_from_api(url, params):
    """
    Fetch data from the Alpha Vantage API.

    Args:
        url (str): API endpoint.
        params (dict): Query parameters including function, symbol, interval, and API key.

    Returns:
        dict: JSON response from the API.

    Raises:
        Exception: If the API request fails (non-200 status code).
    """
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("API request failed with status code " + str(response.status_code))


def transform_data(data):
    """
    Transform raw JSON stock data into a pandas DataFrame.

    Args:
        data (dict): Raw stock time series data where keys are timestamps and
                     values are dictionaries containing open, high, low, close, and volume.

    Returns:
        pd.DataFrame: DataFrame with columns [time_stamp, open, high, low, close, volume].
    """
    data_temp = []
    for key, value in data.items():
        data_temp.append(
            {
                'time_stamp': key,
                'open': value['1. open'],
                'high': value['2. high'],
                'low': value['3. low'],
                'close': value['4. close'],
                'volume': value['5. volume']
            }
        )
    data = pd.DataFrame(data_temp)
    return data


def save_data_to_csv(data):
    """
    Save a DataFrame to a CSV file.

    Args:
        data (pd.DataFrame): The stock data DataFrame to save.

    Returns:
        None
    """
    data.to_csv("stock_data.csv", index=False)


# ------------------ Main Script ------------------

# API endpoint and parameters
api_url = "https://www.alphavantage.co/query"
api_key = "9NAVJMDOR80YHPT0"
params = {
    "function": "TIME_SERIES_INTRADAY",  # Intraday time series data
    "symbol": "IBM",                     # Stock symbol
    "interval": "5min",                  # Time interval
    "apikey": api_key                    # API key
}

# Fetch raw data from API
data = fetch_data_from_api(api_url, params=params)

# Extract the time series data
data = data['Time Series (5min)']

# Transform JSON into DataFrame
data = transform_data(data)

# Save DataFrame to CSV
save_data_to_csv(data)
