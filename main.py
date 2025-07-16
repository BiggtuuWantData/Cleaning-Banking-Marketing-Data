import pandas as pd
import numpy as np
import os

# Read in csv
marketing = pd.read_csv("bank_marketing.csv")

# Split into the 3 tables
client = marketing[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage",]]

campaign = marketing[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", 
                      "previous_outcome", "campaign_outcome", "month", "day"]]

economies = marketing[["client_id", "cons_price_idx", "euribor_three_months"]]

## Editing the client dataset
# Clean job column
client["job"] = client["job"].str.replace(".", "_")

# Clean education column
client["education"] = client["education"].str.replace(".", "_")
client["education"] = client["education"].replace("unknown", np.nan)

# Clean and convert client columns to bool data type
for col in ["credit_default", "mortgage"]:
    client[col] = client[col].map({"yes": 1, 
                                   "no": 0, 
                                   "unknown": 0})
    client[col] = client[col].astype(bool)

##Editing the campaign dataset
# Change campaign_outcome to binary values
campaign["campaign_outcome"] = campaign["campaign_outcome"].map({"yes": 1, 
                                                                 "no": 0})
campaign["previous_outcome"] = campaign["previous_outcome"].map({"success": 1, 
                                                                 "failure": 0, 
                                                                 "nonexistent": 0})
# Add year column
campaign["year"] = '2022'

# Convert day to string
campaign["day"] = campaign["day"].astype(str)

# Add last_contact_date column
campaign["last_contact_date"] = campaign["year"] + "-" + campaign["month"] + "-" + campaign["day"]

# Convert to datetime
campaign["last_contact_date"] = pd.to_datetime(campaign["last_contact_date"], format="%Y-%b-%d")

# Clean and convert outcome column to boolean
for col in ["previous_outcome", "campaign_outcome"]:
    campaign[col] = campaign[col].astype(bool)

# Drop year, month, day column
campaign.drop(columns=["day", "month", "year"], inplace=True)

# Save table 3 files without index
client.to_csv("client.csv", index=False)
campaign.to_csv("campaign.csv", index=False)
economies.to_csv("economies.csv", index=False)

# Ensuring file path
files_exist = all([
    os.path.exists("client.csv"),
    os.path.exists("campaign.csv"),
    os.path.exists("economies.csv")
])






