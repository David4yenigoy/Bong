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

  
# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    print(coin, datetime.datetime.now(), "Sold")
    
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount)     
    return



while(True):
  try :
    balances = upbit.get_balances()
    coins = []
    for i in range(len(balances)) :
        a = balances[i]['currency']
        coins.append('KRW-'+ a )
    coins.remove('KRW-KRW')
    coins.remove('KRW-VTHO')
    # coins.remove('KRW-XYM')
    coins.remove('KRW-APENFT')
    print(datetime.datetime.now(), coins)

    for c in range(len(coins)) :
#         data = pyupbit.get_ohlcv(ticker=coins[c], interval="minute3")
#         now_rsi = rsi(data, 14).iloc[-1]
        av_buy = float(upbit.get_avg_buy_price(coins[c]))
        profit_price = round(av_buy*1.02, 4)   
        cur_price = pyupbit.get_current_price(coins[c]) 
        
        if cur_price >= profit_price and av_buy > 0 :
            sell(coins[c])               
        time.sleep(0.2)
        
  except Exception as e:
        print(e)
        time.sleep(0.2)
