import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["radar_amisr14"]

df = pd.DataFrame(list(db["mediciones_radar"].find()))
print(df.describe())
print(df.head())