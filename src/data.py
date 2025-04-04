import pandas as pd


def read_data() -> pd.DataFrame:
    """
    Reads the earthquake data from a .csv file and returns it as a Pandas
    DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the earthquake data with the following columns:
        'Year', 'EarthquakeName', 'Fatalities', 'MaxMagnitude', 'Location',
        'Date', 'Depth_km', 'FlagCode', and 'FullDate'.
    """
    df = pd.read_csv("data/raw/earthquakes.csv")
    df = df.astype({"Year": int, "EarthquakeName": str, "Fatalities": int,
                    "MaxMagnitude": float, "Location": str, "Date": str,
                    "Depth_km": float})
    df['FullDate'] = pd.to_datetime(df['Date'] + ' ' + df['Year'].astype(str))
    return df
