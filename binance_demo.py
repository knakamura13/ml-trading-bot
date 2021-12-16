import numpy as np
from tqdm import tqdm
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
from os.path import exists


####################
# Helper Functions #
####################

def compute_sma(_data, window):
    """
    Compute SMA.

    Compute the simple moving average (SMA) indicator using an asset's historical data.

    :param _data:
    :param window:
    :return:
    """
    sma = _data.rolling(window=window).mean()
    return sma


################
# Main Program #
################

def main():
    SMA_LOW = 40
    SMA_HIGH = 150

    # select cryptocurrencies you'd like to gather and set the backtesting time interval
    assets = ['BTC', 'ETH', 'LTC', 'XLM', 'XRP', 'XMR', 'TRX', 'LINK', 'IOTA', 'EOS', 'DASH', 'ZRX']
    START_TIME = '28 Mar, 2019'
    END_TIME = '1 Jun, 2020'
    api_key = ''
    api_secret = ''
    client = Client(api_key=api_key, api_secret=api_secret)
    merge = False
    df = pd.DataFrame()
    temp_df = pd.DataFrame()
    seconds = 60

    for asset in assets:
        asset_pair = f'{asset}USDT'
        data_filename = f'data/{asset_pair}.csv'

        if exists(data_filename):
            temp_df = pd.read_csv(data_filename)
        else:
            print(f'Gathering data ({asset})...')

            # Note: this step takes very long time; requires fast internet connection.
            data = client.get_historical_klines(symbol=asset_pair, interval=Client.KLINE_INTERVAL_1MINUTE,
                                                start_str=START_TIME, end_str=END_TIME)

            cols = ['time', 'Open', 'High', 'Low', f'{asset}-USD_close', f'{asset}-USD_volume', 'CloseTime',
                    'QuoteAssetVolume',
                    'NumberOfTrades', 'TBBAV', 'TBQAV', 'null']
            temp_df = pd.DataFrame(data, columns=cols)
            temp_df = temp_df[['time', f'{asset}-USD_close']]
            temp_df.to_csv(data_filename, index=False)
            print(f'Finished. Waiting {seconds}s...\n')
            time.sleep(seconds)  # sleep for a bit so the binance api doesn't kick you out for too many data asks

        if not merge:
            df = temp_df
        else:
            df = pd.merge(df, temp_df, how='inner', on='time')
        merge = True

    for col in df.columns:
        if col != 'time':
            df[col] = df[col].astype(np.float64)

    for asset in assets:
        df[f'{asset}_{SMA_LOW}'] = compute_sma(df[f'{asset}-USD_close'], SMA_LOW)
        df[f'{asset}_{SMA_HIGH}'] = compute_sma(df[f'{asset}-USD_close'], SMA_HIGH)

    # clip NaNs
    df = df[SMA_HIGH:]
    df = df.reset_index(drop=True)

    # convert binance timestamp to datetime
    for i in tqdm(range(len(df))):
        df['time'][i] = datetime.fromtimestamp(int(df['time'][i] / 1000))

    df.to_csv('12-coins-Mar18_Jun20.csv', index=False)


if __name__ == '__main__':
    main()
