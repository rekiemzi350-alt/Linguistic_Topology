import os
import requests
import pandas as pd
import numpy as np
import re

# --- Configuration ---
DATA_DIR = "timeline_data"
SHILLER_URL = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
SHILLER_FILE = os.path.join(DATA_DIR, "shiller_sp500.xls")
OUTPUT_CSV = "market_linguistic_timeline.csv"

# --- Historical Data & Language Generation ---

HISTORICAL_CRISES = {
    (1785, 1): "Panic of 1785 Begins", (1788, 12): "Panic of 1785 Ends",
    (1815, 6): "Post-War of 1812 Inflationary Peak",
    (1819, 1): "Panic of 1819 Begins", (1823, 12): "Panic of 1819 Depression Ends",
    (1837, 5): "Panic of 1837 Begins (NY banks suspend payments)",
    (1857, 8): "Panic of 1857 Begins (Failure of Ohio Life Insurance)",
}

def get_number_name(n, lang_rules):
    """Generates the name of a number based on loaded language rules."""
    if n in lang_rules["direct"]:
        return lang_rules["direct"][n]
    
    name = ""
    if n >= 1000:
        thousands = n // 1000
        name += get_number_name(thousands, lang_rules) + lang_rules.get("thousand_sep", " ") + lang_rules["thousand"]
        n %= 1000
        if n > 0: name += lang_rules.get("thousand_sep", " ")
    
    if n >= 100:
        hundreds = n // 100
        name += get_number_name(hundreds, lang_rules) + lang_rules.get("hundred_sep", " ") + lang_rules["hundred"]
        n %= 100
        if n > 0: name += lang_rules.get("hundred_sep", " ")

    if n > 0:
        if n in lang_rules["direct"]:
            name += lang_rules["direct"][n]
        else:
            tens = n // 10 * 10
            ones = n % 10
            if tens in lang_rules["direct"]:
                name += lang_rules["direct"][tens]
                if ones > 0:
                    name += lang_rules.get("ten_sep", "") + lang_rules["direct"][ones]
    return name.strip()

def load_lang_rules(filepath):
    rules = {"direct": {}}
    with open(filepath, 'r') as f:
        for line in f:
            if ":" not in line or line.startswith('#'): continue
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if key.isdigit():
                rules["direct"][int(key)] = val
            else:
                rules[key] = val
    return rules

class LinguisticWaveformGenerator:
    def __init__(self, lang_filepath):
        self.rules = load_lang_rules(lang_filepath)
        self.current_value = 0
    
    def next(self):
        name = get_number_name(self.current_value, self.rules)
        length = len(re.sub(r'[^a-zA-Z]', '', name))
        self.current_value += length
        return self.current_value

# --- Main Timeline Generation ---

def generate_timeline():
    print("--- Step 2: Generating Unified Timeline ---")

    # Load Shiller Data
    print("Loading Shiller data...")
    # The file is an XLS, but it's structured in a way that needs cleaning.
    # We skip initial rows and read specific columns.
    try:
        df_shiller = pd.read_excel(SHILLER_FILE, sheet_name='Data', header=7)
        # Select and rename relevant columns
        df_shiller = df_shiller[['Date', 'P', 'CAPE']]
        df_shiller.columns = ['Date', 'SP500_Price', 'SP500_CAPE']
        # Convert date format YYYY.MM to datetime objects
        df_shiller['Date'] = pd.to_datetime(df_shiller['Date'].astype(str).str.replace('.', '-'), format='%Y-%m')
        df_shiller.set_index('Date', inplace=True)
    except Exception as e:
        print(f"[ERROR] Could not process Shiller data file. Market data will be missing. Error: {e}")
        df_shiller = pd.DataFrame()


    # Initialize Language Waveform Generators
    gen_us = LinguisticWaveformGenerator("english_us.lang")
    gen_uk = LinguisticWaveformGenerator("english_uk.lang")
    gen_nl = LinguisticWaveformGenerator("dutch_hist.lang")

    # Create timeline from 1792 to present
    timeline = pd.date_range(start='1792-01-01', end=pd.to_datetime('today'), freq='MS')
    
    records = []
    for date in timeline:
        year, month = date.year, date.month
        
        market_event = HISTORICAL_CRISES.get((year, month), "")
        
        # Get Shiller data if available for this date
        sp500_price = np.nan
        sp500_cape = np.nan
        if date in df_shiller.index:
            row = df_shiller.loc[date]
            sp500_price = row['SP500_Price']
            sp500_cape = row['SP500_CAPE']
            
        record = {
            'Date': date,
            'Year': year,
            'Month': month,
            'Market_Event': market_event,
            'SP500_Price': sp500_price,
            'SP500_CAPE': sp500_cape,
            'American_English_Wave': gen_us.next(),
            'UK_English_Wave': gen_uk.next(),
            'Dutch_Wave': gen_nl.next(),
        }
        records.append(record)

    df_timeline = pd.DataFrame(records)
    print(f"Generated {len(df_timeline)} monthly records from 1792 to present.")
    
    # Save to CSV
    df_timeline.to_csv(OUTPUT_CSV, index=False)
    print(f"Successfully saved unified timeline to {OUTPUT_CSV}")

    # --- Step 3: Preliminary Analysis ---
    print("\n--- Step 3: Preliminary Comparative Analysis ---")
    
    # Filter for the modern period where we have S&P data
    df_modern = df_timeline.dropna(subset=['SP500_Price']).copy()
    
    # Force columns to be numeric, coercing errors
    for col in ['SP500_Price', 'American_English_Wave', 'UK_English_Wave', 'Dutch_Wave']:
        df_modern[col] = pd.to_numeric(df_modern[col], errors='coerce')
    
    # Drop rows where coercion might have failed, especially for the price
    df_modern.dropna(subset=['SP500_Price'], inplace=True)

    # Calculate volatility (standard deviation of monthly % change)
    df_modern['Market_Volatility'] = df_modern['SP500_Price'].pct_change().rolling(window=12).std()
    df_modern['US_Eng_Volatility'] = df_modern['American_English_Wave'].pct_change().rolling(window=12).std()
    df_modern['UK_Eng_Volatility'] = df_modern['UK_English_Wave'].pct_change().rolling(window=12).std()
    df_modern['Dutch_Volatility'] = df_modern['Dutch_Wave'].pct_change().rolling(window=12).std()
    
    # Calculate correlation of volatility
    correlations = df_modern[['Market_Volatility', 'US_Eng_Volatility', 'UK_Eng_Volatility', 'Dutch_Volatility']].corr()
    
    print("Correlation Matrix of Volatility (12-Month Rolling % Change):")
    print(correlations)
    
    market_corrs = correlations['Market_Volatility'][1:]
    closest_lang = market_corrs.idxmax()
    
    print("\n--- Conclusion ---")
    print("This analysis compares the 'rhythm' of market volatility with the 'rhythm' of linguistic number sequences.")
    print("A higher correlation suggests the language's mathematical structure has a volatility pattern that is more similar to the market's.")
    print(f"\nBased on this model, the language with the volatility closest to the US stock market is: {closest_lang}")
    print("\nNOTE: This is a theoretical exploration of structural similarities, not a predictive model.")


if __name__ == "__main__":
    generate_timeline()