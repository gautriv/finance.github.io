import yfinance as yf
import pandas as pd

# Add .NS to the NSE stock symbols
nse_stocks = [
    "ABB.NS", "ACC.NS", "APLAPOLLO.NS", "AUBANK.NS", "ADANIENSOL.NS", "ADANIENT.NS", 
    "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", "ABCAPITAL.NS", 
    "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", 
    "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", "AUROPHARMA.NS", "DMART.NS", 
    "AXISBANK.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", 
    "BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", 
    "MAHABANK.NS", "BERGEPAINT.NS", "BDL.NS", "BEL.NS", "BHARATFORG.NS", "BHEL.NS", 
    "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BRITANNIA.NS", 
    "CGPOWER.NS", "CANBK.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", 
    "COLPAL.NS", "CONCOR.NS", "CUMMINSIND.NS", "DLF.NS", "DABUR.NS", "DALBHARAT.NS", 
    "DEEPAKNTR.NS", "DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS", "LALPATHLAB.NS", 
    "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "NYKAA.NS", "FEDERALBNK.NS", 
    "FACT.NS", "FORTIS.NS", "GAIL.NS", "GMRINFRA.NS", "GLAND.NS", "GODREJCP.NS", 
    "GODREJPROP.NS", "GRASIM.NS", "GUJGASLTD.NS", "HCLTECH.NS", "HDFCAMC.NS", 
    "HDFCBANK.NS", "HDFCLIFE.NS", "HAVELLS.NS", "HEROMOTOCO.NS", "HINDALCO.NS", 
    "HAL.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", 
    "ICICIPRULI.NS", "IDBI.NS", "IDFCFIRSTB.NS", "ITC.NS", "INDIANB.NS", 
    "INDHOTEL.NS", "IOC.NS", "IRCTC.NS", "IRFC.NS", "IGL.NS", "INDUSTOWER.NS", 
    "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS", "INDIGO.NS", "IPCALAB.NS", "JSWENERGY.NS", 
    "JSWINFRA.NS", "JSWSTEEL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", 
    "KPITTECH.NS", "KALYANKJIL.NS", "KOTAKBANK.NS", "LTF.NS", "LTTS.NS", "LICHSGFIN.NS", 
    "LTIM.NS", "LT.NS", "LAURUSLABS.NS", "LICI.NS", "LUPIN.NS", "MRF.NS", "LODHA.NS", 
    "M&MFIN.NS", "M&M.NS", "MANKIND.NS", "MARICO.NS", "MARUTI.NS", "MFSL.NS", 
    "MAXHEALTH.NS", "MAZDOCK.NS", "MPHASIS.NS", "NHPC.NS", "NMDC.NS", "NTPC.NS", 
    "NESTLEIND.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "PAYTM.NS", "OFSS.NS", 
    "POLICYBZR.NS", "PIIND.NS", "PAGEIND.NS", "PATANJALI.NS", "PERSISTENT.NS", 
    "PETRONET.NS", "PIDILITIND.NS", "PEL.NS", "POLYCAB.NS", "POONAWALLA.NS", 
    "PFC.NS", "POWERGRID.NS", "PRESTIGE.NS", "PNB.NS", "RECLTD.NS", "RVNL.NS", 
    "RELIANCE.NS", "SBICARD.NS", "SBILIFE.NS", "SJVN.NS", "SRF.NS", "MOTHERSON.NS", 
    "SHREECEM.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SONACOMS.NS", "SBIN.NS", 
    "SAIL.NS", "SUNPHARMA.NS", "SUNTV.NS", "SUPREMEIND.NS", "SUZLON.NS", "SYNGENE.NS", 
    "TVSMOTOR.NS", "TATACHEM.NS", "TATACOMM.NS", "TCS.NS", "TATACONSUM.NS", 
    "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS", 
    "TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TIINDIA.NS", 
    "UPL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UNITDSPR.NS", "VBL.NS", "VEDL.NS", 
    "IDEA.NS", "VOLTAS.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", 
    "ZYDUSLIFE.NS"
]

def get_stock_data(symbol):
    """Fetch historical data for the stock from Yahoo Finance."""
    try:
        data = yf.download(symbol, period="1y", interval="1d")
        if data.empty:
            raise ValueError(f"No data found for {symbol}")
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None  # Return None if an error occurs

def calculate_trend(data):
    """Check if the trend is bullish based on moving averages."""
    last_row = data.iloc[-1]
    # Relaxed condition: Allow more flexibility in DMA alignment
    if last_row['20DMA'] > last_row['50DMA'] and last_row['100DMA'] > last_row['200DMA']:
        return "Bullish"
    elif last_row['20DMA'] < last_row['50DMA'] and last_row['100DMA'] < last_row['200DMA']:
        return "Bearish"
    else:
        return "Sideways"

def calculate_support_resistance(data, period=50):
    """Calculate support and resistance levels based on recent highs and lows."""
    support = data['Low'].rolling(window=period).min().iloc[-1]
    resistance = data['High'].rolling(window=period).max().iloc[-1]
    return support, resistance

def calculate_rsi(close, window=14):
    """Calculate the Relative Strength Index (RSI) for the stock."""
    delta = close.diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze_stock(symbol):
    """Analyze a stock and return various metrics including buy signal."""
    data = get_stock_data(symbol)

    if data is None:
        return {
            'symbol': symbol,
            'error': 'No data available',
            'buy_signal': 'Do not buy',
            'price': 'N/A',
            '20DMA': 'N/A',
            '50DMA': 'N/A',
            '100DMA': 'N/A',
            '200DMA': 'N/A',
            '52_week_high': 'N/A',
            '52_week_low': 'N/A',
            'from_52_week_high': None,
            'RSI': 'N/A',
            'volume': 'N/A',
            'support_resistance': 'N/A',
            'low_price': 'N/A',
            'close_price': 'N/A',
            'stop_loss': 'N/A',
            'target_price': 'N/A'
        }

    # Calculate moving averages and RSI
    data['20DMA'] = data['Close'].rolling(window=20).mean()
    data['50DMA'] = data['Close'].rolling(window=50).mean()
    data['100DMA'] = data['Close'].rolling(window=100).mean()
    data['200DMA'] = data['Close'].rolling(window=200).mean()
    data['RSI'] = calculate_rsi(data['Close'])

    # Calculate 20-day average volume
    data['avg_volume'] = data['Volume'].rolling(window=20).mean()

    last_row = data.iloc[-1]

    # Calculate 52-week high/low
    year_high = data['High'].max()
    year_low = data['Low'].min()

    # Calculate support and resistance
    support, resistance = calculate_support_resistance(data)

    # Calculate trend
    trend = calculate_trend(data)

    # Buy signal logic
    price = last_row['Close']
    volume = last_row['Volume']
    avg_volume = last_row['avg_volume']

    # Relax conditions to make the logic more flexible
    near_support = price <= support * 1.25  # Relaxed to within 20% of support
    near_resistance = price >= resistance * 0.90  # Keep strict: Avoid if within 10% of resistance

    # Relax volume confirmation: allow range within 80-120% of avg volume
    volume_confirmation = volume >= avg_volume * 0.70  # Loosen to allow slightly lower volumes

    # Relax RSI condition: Allow RSI between 30-55 for a valid buy signal
    if (
    last_row['20DMA'] > last_row['50DMA'] > last_row['100DMA'] > last_row['200DMA']  # Checking all DMAs
    and 30 <= last_row['RSI'] <= 60  # Relaxed RSI condition (between 30-60)
    and trend == "Bullish"
    and near_support
    and not near_resistance
    and volume_confirmation
    ):
        buy_signal = "BUY"
    else:
        buy_signal = "Do not buy"

    return {
        'symbol': symbol,
        'price': price,
        '20DMA': last_row['20DMA'],
        '50DMA': last_row['50DMA'],
        '100DMA': last_row['100DMA'],
        '200DMA': last_row['200DMA'],
        '52_week_high': year_high,
        '52_week_low': year_low,
        'from_52_week_high': ((year_high - price) / year_high) * 100,
        'RSI': last_row['RSI'],
        'volume': volume,
        'avg_volume': avg_volume,
        'support_resistance': f"Support: {support:.2f}, Resistance: {resistance:.2f}, Trend: {trend}",
        'low_price': last_row['Low'],
        'close_price': last_row['Close'],
        'buy_signal': buy_signal,
        'stop_loss': support * 0.95,  # Stop-loss is 5% below support
        'target_price': resistance * 0.95  # Target price is just below resistance
    }

def analyze_all_stocks():
    """Analyze all stocks and return their metrics."""
    results = []
    for symbol in nse_stocks:
        result = analyze_stock(symbol)
        results.append(result)
    return results