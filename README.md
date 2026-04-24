# LibreOffice Crypto Prices

A simple Python macro for **LibreOffice Calc** that fetches current cryptocurrency prices from the [CoinMarketCap API](https://coinmarketcap.com/api) and updates them in a dedicated sheet.

The macro reads cryptocurrency tickers (e.g., `BTC`, `ETH`, `SOL`) from the script, retrieves the corresponding prices in USD and writes the results starting from cell **B3**.

## Features

- Creates or uses a sheet named **"API - Crypto Prices"**.
- Custom header exactly as specified:
  - **A1**: `CoinMarketCap`
  - **A2**: `Crypto Ticker`
  - **B2**: `Price (USD)`
- Easy configuration via global variables at the top of the script.
- Column A (crypto tickers) remains fully editable.
- User-friendly success/error feedback via message box.

## Sheet Layout (after first run)

| A               | B       |
|-----------------|---------|
| **CoinMarketCap** |         |
| **Crypto Ticker**  | **Price (USD)** |
| BTC            | 45123.56  |
| ETH            | 2834.12  |
| SOL            | 142.78  |
| ...             | ...     |

## Installation

### 1. Get a CoinMarketCap API Key

1. Visit [CoinMarketCap API](https://coinmarketcap.com/api/)
2. Click **Get Started** and sign up for a free account.
3. You'll receive a free API key with a rate limit of 333 requests per day.

### 2. Macro Security Settings

Before using any macro, adjust LibreOffice security:

1. Go to **Tools → Options** (or **LibreOffice → Preferences** on macOS).
2. Navigate to **Security → Macro Security**.
3. Set the security level to **Medium** or **High**.
4. (Recommended) Add the folder containing your macro to **Trusted Sources**.

### 3. Place the Python Script

LibreOffice loads Python macros (`.py` files) from two locations:

**User-specific path** (recommended):

- **Linux**: `~/.config/libreoffice/4/user/Scripts/python/`
- **Windows**: `C:\Users\<YourUsername>\AppData\Roaming\LibreOffice\4\user\Scripts\python\`
- **macOS**: `/Users/<YourUsername>/Library/Application Support/LibreOffice/4/user/Scripts/python/`

**All-users (system) path** (requires administrator rights):

- **Linux**: `/usr/lib64/libreoffice/share/Scripts/python/` (or similar)
- **Windows**: `%APPDATA%\LibreOffice\4\user\Scripts\python\`
- **macOS**: Not commonly used.

**Note**: If the `Scripts/python` folders do not exist, create them manually.

1. Copy the file `crypto_prices.py` into the chosen folder.
2. Restart LibreOffice.

### 4. (Optional but Recommended) Install APSO Extension

For easier macro management, install the **Alternative Python Script Organizer (APSO)**:

https://extensions.libreoffice.org/extensions/apso-alternative-script-organizer-for-python

After installation, use **Tools → Macros → Organize Python Scripts**.

## Configuration

Edit the global variables at the top of `crypto_prices.py`:

```python
API_KEY = ""                           # Insert your CoinMarketCap API key here
SHEET_NAME = "API - Crypto Prices"     # Sheet name
START_ROW = 3                          # First data row (1-based)
CRYPTO_PRICE_COLUMN = 0                # Column A (0 = A)
PRICE_USD_COLUMN = 1                   # Column B (1 = B)
MAX_ROWS = 998                         # Maximum rows to process

CRYPTO_TICKERS = [                     # Populated on first sheet creation
    "BTC",
    "ETH",
    "SOL",
    # Add or remove tickers here
]
```

**Important**: Paste your CoinMarketCap API key into the `API_KEY` variable.

## Usage

1. Open any Calc spreadsheet.
2. Run the macro for the first time:
   Tools → Macros → Run Macro → My Macros → crypto_prices → update_crypto_prices → Run.
   This creates the "API - Crypto Prices" sheet with the custom header and default tickers.
3. The script will fetch prices for each ticker and display them in column B.
4. **Note**: The macro respects CoinMarketCap's rate limit (333 requests per day on the free tier) by adding a 12-second delay between requests.

## Limitations & Notes

* The free CoinMarketCap API tier allows 333 requests per day.
* Cryptocurrency ticker symbols must be valid (e.g., `BTC`, `ETH`, `SOL`).
* Prices are updated in real-time based on global cryptocurrency market data.
* Cryptocurrency markets operate 24/7, so prices are always available.
* Tested with recent LibreOffice versions (2024–2026).

## Troubleshooting

### "ERR" appears in cells
- Check your API key is valid and correctly entered.
- Verify the ticker symbol is correct (e.g., `BTC` not `Bitcoin`).
- Check your internet connection.
- Ensure you haven't exceeded the API rate limit (333 requests/day).

### "N/A" appears in cells
- The ticker may not exist or may not have valid price data available on CoinMarketCap.
- Verify the ticker is a valid cryptocurrency symbol.

### The macro doesn't run
- Check that the file is placed in the correct Scripts/python folder.
- Verify LibreOffice macro security is set to **Medium** or higher.
- Restart LibreOffice after placing the script.

### "API_KEY is not set" error
- Make sure you have inserted your CoinMarketCap API key into the `API_KEY` variable at the top of the script.

## License

This project is open source and released under the MIT License. Feel free to use, modify and distribute it.

## Contributing

Suggestions, improvements and pull requests are welcome. Please open an issue for any bugs or feature requests.
