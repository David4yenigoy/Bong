import pyupbit 
import pandas 
import datetime 
import time
from pytz import timezone

import pyupbit 
import pandas 
import datetime 
import time

access = "access key"   # access key
secret = "secret key"   # secret key

upbit = pyupbit.Upbit(access, secret)


def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")


# 시장가 매수 함수 
def buy(coin): 
    money = upbit.get_balance("KRW") 
    amount = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price
    print(coin, datetime.datetime.now(timezone('Asia/Seoul')), "Buy")
    
    if money > 501000 and total < 500000 : 
        res = upbit.buy_market_order(coin, 500000) 
    return

# initiate
# 이용할 코인 리스트 
coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-POWR", "KRW-CRO", "KRW-VET", "KRW-AQT", "KRW-AXS", "KRW-EOS", "KRW-BORA", "KRW-PLA", "KRW-WAXP", "KRW-MANA", "KRW-SAND", "KRW-HIVE", "KRW-HUNT", "KRW-DOGE", "KRW-CHZ", "KRW-DOT"] # Coin ticker 추가 
lower28 = []

for i in range(len(coinlist)):
    lower28.append(False)

while(True):
    for i in range(len(coinlist)):
        try :
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
            now_rsi = rsi(data, 14).iloc[-1]

            if now_rsi <= 28 :
                lower28[i] = True
                buy(coinlist[i])
                
            elif now_rsi <= 20 and lower28[i] == True :
                buy(coinlist[i])
                
            elif now_rsi >= 60 :
                lower28[i] = False
                
            time.sleep(0.1)
            
        except Exception as e:
            print(e)
            time.sleep(0.1)  
