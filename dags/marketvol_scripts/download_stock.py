import yfinance as yf
from datetime import date, timedelta

def download_stock(symbol, output_path):
    start_date = date.today()
    end_date = start_date + timedelta(days=1)

    df = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        interval="1m"
    )

    df.to_csv(output_path, header=False)
