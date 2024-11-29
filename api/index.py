import pandas as pd
import datetime
from flask import Flask

# Load the data
denmark_residential_wt = pd.read_csv("./data/denmark-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")
spain_residential_wt = pd.read_csv("./data/spain-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")
austria_residential_wt = pd.read_csv("./data/austria-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")



data = pd.DataFrame(denmark_residential_wt, columns=['Time', 'Generic 100kWh Li-Ion State of Charge', 'Total Renewable Power Output'])
data.rename(columns={'Generic 100kWh Li-Ion State of Charge': 'Battery_charge',
                     'Total Renewable Power Output': 'Renewable_output' },
                     inplace=True)

data_spain = pd.DataFrame(spain_residential_wt, columns=['Time', 'Generic 100kWh Li-Ion State of Charge', 'Total Renewable Power Output'])
data_spain.rename(columns={'Generic 100kWh Li-Ion State of Charge': 'Battery_charge',
                     'Total Renewable Power Output': 'Renewable_output' },
                     inplace=True)

data_austria = pd.DataFrame(austria_residential_wt, columns=['Time', 'Generic 100kWh Li-Ion State of Charge', 'Total Renewable Power Output'])
data_austria.rename(columns={'Generic 100kWh Li-Ion State of Charge': 'Battery_charge',
                     'Total Renewable Power Output': 'Renewable_output' },
                     inplace=True)
# print(data.head())
# print(data.dtypes)

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
    row["Location"] = ["Denmark"]

    row2 = data_spain.loc[data_spain["Time"] == rounded_time]
    row3 = data_austria.loc[data_austria["Time"] == rounded_time]

    combined_rows = pd.concat([row, row2, row3])

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