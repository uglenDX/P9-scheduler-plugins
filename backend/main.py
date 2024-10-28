import pandas as pd
import requests
from flask import Flask, jsonify, request

# Load the data
data = pd.read_csv(".\data\ElectricityProdex5MinRealtime.csv", delimiter=";")
data = data.drop(columns=
                 ["ExchangeGreatBelt", 
                  "ExchangeGermany", 
                  "ExchangeNetherlands", 
                  "ExchangeGreatBritain", 
                  "ExchangeNorway", 
                  "ExchangeSweden", 
                  "BornholmSE4"])
data["SumProduction"] = data["ProductionLt100MW"] + data["ProductionGe100MW"] + data["OffshoreWindPower"] + data["OnshoreWindPower"] + data["SolarPower"]
#print(data.count())
#print(data.head())

app = Flask(__name__)

# @app.route("/data")
# def test_data():
#     return jsonify(data.to_dict())