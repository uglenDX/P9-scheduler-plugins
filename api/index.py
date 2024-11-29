import pandas as pd
import datetime
from flask import Flask

# Load the data
denmark_residential_wt = pd.read_csv("./data/denmark-residential-wt_detailed_timeseries_001_00006.csv", delimiter=",", decimal=".")

data = pd.DataFrame(denmark_residential_wt, columns=['Time', 'Generic 100kWh Li-Ion State of Charge', 'Total Renewable Power Output'])
data.rename(columns={'Generic 100kWh Li-Ion State of Charge': 'Battery_charge',
                     'Total Renewable Power Output': 'Renewable_output' },
                     inplace=True)
print(data.head())
print(data.dtypes)

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/data", methods=["GET"])
def state_of_charge():
    server_time = datetime.datetime.now()
    #print(server_time)
    rounded_time = roundDownDateTime(server_time)
    #print(rounded_time)

    row = data.loc[data["Time"] == rounded_time]

    return row.to_json(orient="records")

@app.route("/alive", methods=["GET"])
def alive():
    print("I'm alive!")
    return "I'm alive!"

def roundDownDateTime(dt):
    delta_min = dt.minute % 5
    rounded_dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute - delta_min)
    # Remember to change year according to data
    return rounded_dt.strftime("%m/%d/2023 %H:%M:%S %p")