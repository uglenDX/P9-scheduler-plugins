import pandas as pd
import requests
from flask import Flask, jsonify, request

# Load the data
data = pd.read_csv(".\data\ElectricityProdex5MinRealtime.csv", delimiter=";", decimal=",")
data = data.drop(columns=
                 ["ExchangeGreatBelt", 
                  "ExchangeGermany", 
                  "ExchangeNetherlands", 
                  "ExchangeGreatBritain", 
                  "ExchangeNorway", 
                  "ExchangeSweden", 
                  "BornholmSE4"])
#data["SumProduction"] = data["ProductionLt100MW"] + data["ProductionGe100MW"] + data["OffshoreWindPower"] + data["OnshoreWindPower"] + data["SolarPower"]
data["SumProduction"] = data[["ProductionLt100MW", "ProductionGe100MW", "OffshoreWindPower", "OnshoreWindPower", "SolarPower"]].sum(axis=1, numeric_only=True)

#print(data.count())
#print(data.head())

app = Flask(__name__)

@app.route("/data/<timestamp>", methods=["GET"])
def test_data(timestamp):
    row = data.loc[data["Minutes5DK"] == timestamp]
    return row.to_json(orient="records")