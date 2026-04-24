import urllib.request
import json
import time
import uno

# ==================== GLOBAL CONFIGURATION VARIABLES ====================
API_KEY = ""                        # Insert your CoinMarketCap API key here
SHEET_NAME = "API - Crypto Prices"
START_ROW = 3                                       # First data row (1-based)
CRYPTO_PRICE_COLUMN = 0                              # Column A (0-based)
PRICE_USD_COLUMN = 1                                # Column B (0-based)
MAX_ROWS = 998                                      # Up to row 1000

CRYPTO_TICKERS = [
    "BTC",
    "ETH",
    "SOL",
]
# =====================================================================

def get_or_create_sheet(doc, sheet_name):
    """Create or retrieve sheet with the exact requested header."""
    global SHEET_NAME, START_ROW, CRYPTO_PRICE_COLUMN, PRICE_USD_COLUMN, CRYPTO_TICKERS
    sheets = doc.Sheets
    if sheets.hasByName(sheet_name):
        return sheets.getByName(sheet_name)

    sheets.insertNewByName(sheet_name, sheets.getCount())
    sheet = sheets.getByName(sheet_name)

    cell_a1 = sheet.getCellByPosition(0, 0)
    cell_a1.setString("CoinMarketCap")
    cell_a1.CharWeight = 150

    cell_a2 = sheet.getCellByPosition(0, 1)
    cell_a2.setString("Crypto Ticker")
    cell_a2.CharWeight = 150

    cell_b2 = sheet.getCellByPosition(1, 1)
    cell_b2.setString("Price (USD)")
    cell_b2.CharWeight = 150

    for i, pair in enumerate(CRYPTO_TICKERS):
        row = START_ROW + i - 1
        sheet.getCellByPosition(CRYPTO_PRICE_COLUMN, row).setString(pair)

    return sheet

def coinmarketcap_price_usd(symbol):
    """
    Retrieves the latest price in USD using CoinMarketCap API.
    """
    global API_KEY
    if not API_KEY:
        raise ValueError("API_KEY is not set. Please add your CoinMarketCap API key to the script.")
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD"
    req = urllib.request.Request(url, headers={
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY
    })
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            js = json.load(response)
        price = js["data"][symbol]["quote"]["USD"]["price"]
        return round(float(price), 8)
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None


def update_crypto_prices(*args):
    """
    Updates crypto prices in the 'API - Crypto Prices' sheet.
    Can be called manually or via the 'Open Document' event.
    Prices are retrieved and stored in USD.
    """
    global SHEET_NAME, START_ROW, CRYPTO_PRICE_COLUMN, PRICE_USD_COLUMN, MAX_ROWS
    desktop = XSCRIPTCONTEXT.getDesktop()
    doc = desktop.getCurrentComponent()
    
    sheet = get_or_create_sheet(doc, SHEET_NAME)
    doc.CurrentController.setActiveSheet(sheet)
    
    for row in range(START_ROW - 1, START_ROW - 1 + MAX_ROWS):
        sheet.getCellByPosition(PRICE_USD_COLUMN, row).String = ""

    for i in range(MAX_ROWS):
        row = START_ROW - 1 + i
        cell = sheet.getCellByPosition(CRYPTO_PRICE_COLUMN, row)
        ticker = cell.String.strip()

        if ticker == "":
            continue

        try:
            price_usd = coinmarketcap_price_usd(ticker)
            time.sleep(12)

            if price_usd is None:
                sheet.getCellByPosition(PRICE_USD_COLUMN, row).String = "N/A"
            else:
                sheet.getCellByPosition(PRICE_USD_COLUMN, row).Value = price_usd

        except Exception as e:
            sheet.getCellByPosition(PRICE_USD_COLUMN, row).String = "ERR"

    msg = "Crypto prices updated successfully."
    toolkit = uno.getComponentContext().ServiceManager.createInstanceWithContext(
        "com.sun.star.awt.Toolkit", uno.getComponentContext())
    msgbox = toolkit.createMessageBox(None, 0, 0, "Update Complete", msg)
    msgbox.execute()

g_exportedScripts = (update_crypto_prices,)