import pandas as pd
import requests
import datetime
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

    timestamp = roundDownDateTime(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M"))
    row = data.loc[data["Minutes5DK"] == timestamp]

    return row.to_json(orient="records")

@app.route("/alive", methods=["GET"])
def alive():
    print("I'm alive!")
    return "I'm alive!"

@app.route("/print", methods=["POST"])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(json)
        return json
    else:
        return 'Content-Type not supported!'

def roundDownDateTime(dt):
    delta_min = dt.minute % 5
    rounded_dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute - delta_min)
    return rounded_dt.strftime("%Y-%m-%d %H:%M")