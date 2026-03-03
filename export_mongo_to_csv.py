from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["weather"]
collection = db["cache"]
cursor = collection.find()
docs = list(cursor)

df = pd.DataFrame(docs)
df.drop(columns=["_id"], inplace=True)
df = df[df["stacja"]=="Kłodzko"]
df["id_stacji"] = df["id_stacji"].astype(int)
df["stacja"] = df["stacja"].astype("str")
df["data_pomiaru"] = pd.to_datetime(df["data_pomiaru"])
df["godzina_pomiaru"] = df["godzina_pomiaru"].astype(int)
df["temperatura"] = df["temperatura"].astype(float)
df["predkosc_wiatru"] = df["predkosc_wiatru"].astype(int)
df["kierunek_wiatru"] = df["kierunek_wiatru"].astype(int)
df["wilgotnosc_wzgledna"] = df["wilgotnosc_wzgledna"].astype(float)
df["suma_opadu"] = df["suma_opadu"].astype(float)
df["cisnienie"] = df["cisnienie"].astype(float)


new_columns = ["station_id", "station_name", "measurement_date", "measurement_hour", "temperature", "wind_speed", "wind_direction",
               "relative_humidity", "total_precipitation", "pressure"]

df.columns = new_columns

print(df.head())
print(df.dtypes)

df = df[df["measurement_date"] >= "2025-03-01"]
df.drop_duplicates(inplace=True)

df.to_csv("klodzko_weather.csv",index=False)