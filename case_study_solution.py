import pandas as pd
import string
import re

def clean_data(x):
    return re.sub(r"[^A-Za-z\s]", "", x).strip()

def transform_data(data):

    lines = data.strip().split("\n")
    first = lines[0].split(";")
    rows = []
    for line in lines[1:]:
        parts = line.split(";")
        rows.append(parts)
    
    df = pd.DataFrame(rows, columns = first)
    df["Airline Code"] = df["Airline Code"].apply(clean_data)

    df[["From", "To"]] = df["To_From"].str.split("_", n = 1, expand = True)
    df["From"] = df["From"].str.upper().str.strip()
    df["To"] = df["To"].str.upper().str.strip()
    df = df.drop(columns = ["To_From"])


    df["FlightCodes"] = pd.to_numeric(df["FlightCodes"], errors = "coerce")

    initial_val = 1010
    step = 10

    for i in range(len(df)):
        if pd.isna(df.loc[i, "FlightCodes"]):
            df.loc[i, "FlightCodes"] = (initial_val + (i * step))
        else:
            df.loc[i, "FlightCodes"] = int(df.loc[i, "FlightCodes"])
    
    df["FlightCodes"] = df["FlightCodes"].astype(int)
    return df

data = '''Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'''
print(transform_data(data))
