import pandas as pd
from typing import Dict, List, Any, Tuple
from brawlers_data import brawlers_data 
from constants import COLOUMN_NAMES

class BrawlerDataPandas:
    def create_dataframes(self, brawlers_data: List[Dict[str, Any]]):
        # Return empty DataFrames if it has no data
        if not brawlers_data:
            print("No brawler data provided to process")
            return pd.DataFrame(columns=COLOUMN_NAMES), pd.DataFrame(columns=COLOUMN_NAMES)
        
        # Create DataFrame from input data
        df = pd.DataFrame(brawlers_data)

        # check all required columns exist, fill missing ones with 0
        for column in COLOUMN_NAMES:
            if column not in df.columns:
                print(f"Column '{column}' not found in data, adding with default value 0")
                df[column] = 0

        # Reorder columns and fill any NaN values with 0
        df = df[COLOUMN_NAMES]
        df = df.fillna(0)

        # Convert specific columns to numeric types and handle errors
        numeric_columns = ["Level", "Rank", "Current Trophies", "Max Trophies", "Gadgets", "Star Powers"]
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)
        
        # Sort DataFrame by Max Trophies, Current Trophies, then Brawler name
        df = df.sort_values(
            by=["Max Trophies", "Current Trophies", "Brawler"], 
            ascending=[False, False, True]
        )
        
        # Create a new DataFrame for brawlers with Level >= 9
        df2 = df[df["Level"] >= 9].copy()
        
        # Return both DataFrames
        return df, df2

    

# processor = BrawlerDataPandas()
# df_all, df_high_level = processor.create_dataframes(brawlers_data)

# print("\nAll Brawlers:")
# print(df_all)

# print("\nBrawlers with Level >= 9:")
# print(df_high_level)