import pandas as pd

# Load source data
cta_ridership_data = pd.read_csv("data/raw/CTA_-_Ridership_-_Daily_Boarding_Totals_20250930.csv")
wmata_ridership_data = pd.read_csv("data/raw/DC Daily Ridership - Data View.csv")
mta_ridership_data = pd.read_csv("data/raw/MTA_Daily_Ridership_and_Traffic__Beginning_2020_20250930.csv")
nyc_ferry_ridership_data = pd.read_csv("data/raw/NYC_Ferry_Ridership_20250930.csv")
staten_island_ferry_ridership_data = pd.read_csv("data/raw/Staten_Island_Ferry_Ridership_Counts_20250930.csv")

# Copy the desired date and total rides columns for Chicago and D.C
chicago_ridership_data = cta_ridership_data[["service_date", "total_rides"]].copy()
dc_ridership_data = wmata_ridership_data[["Date", "Grand Total"]].copy()

# Convert total rides from string type to int type
chicago_ridership_data["total_rides"] = chicago_ridership_data["total_rides"].str.replace(",", "").astype(int)
dc_ridership_data["Grand Total"] = dc_ridership_data["Grand Total"].str.replace(",", "").astype(int) 

# Change D.C date to desired format
dc_ridership_data["Date"] = pd.to_datetime(dc_ridership_data["Date"]).dt.strftime("%m/%d/%Y")

# Group MTA Ridership Data by date, summing the ridership counts for different modes per day
mta_ridership_data = mta_ridership_data.groupby("Date")["Count"].sum().reset_index()

# Create a new column in the Staten Island Ferry ridership data to combine the total rides per terminal
staten_island_ferry_ridership_data["total_rides"] = staten_island_ferry_ridership_data[["Whitehall Terminal","St. George Terminal"]].sum(axis=1)

# Rename columns to have consistent names across all cities: 'date' and 'total_rides' 
nyc_ferry_ridership_data = nyc_ferry_ridership_data.rename(columns={"Date": "date", "Boardings": "total_rides"})
staten_island_ferry_ridership_data = staten_island_ferry_ridership_data.rename(columns={"Date": "date", })
mta_ridership_data = mta_ridership_data.rename(columns={"Date": "date", "Count": "total_rides"})
chicago_ridership_data = chicago_ridership_data.rename(columns={"service_date": "date"})
dc_ridership_data = dc_ridership_data.rename(columns={"Date": "date", "Grand Total": "total_rides"})

# Create new dataframe combining MTA and ferry ridership data
cols = ["date", "total_rides"]
nyc_data_list = [mta_ridership_data[cols], nyc_ferry_ridership_data[cols], staten_island_ferry_ridership_data[cols]]
nyc_ridership_data = pd.concat(nyc_data_list).groupby("date", as_index=False)["total_rides"].sum()

# Save processed data
nyc_ferry_ridership_data.to_csv("data/processed/nyc_ridership_data.csv")
chicago_ridership_data.to_csv("data/processed/chicago_ridership_data.csv")
dc_ridership_data.to_csv("data/processed/dc_ridership_data.csv")