import pandas as pd
import datetime
import csv
import time
import os
from flask import Flask, send_file, request

# Load the data

#Vercel Patch
denmark_residential_wt = pd.read_csv("./data/denmark-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")
spain_residential_wt = pd.read_csv("./data/spain-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")
austria_residential_wt = pd.read_csv("./data/austria-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")

# dtype = {'Time' : str, 'Generic 100kWh Li-Ion State of Charge' : float, 'Total Renewable Power Output' : float, 'AC Primary Load' : float, 'Unmet Electrical Load' : float}

# Local path
# denmark_residential_wt = pd.read_csv("D:\Github\P9-scheduler-plugins\data\denmark-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")
# spain_residential_wt = pd.read_csv("D:\Github\P9-scheduler-plugins\data\spain-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")
# austria_residential_wt = pd.read_csv("D:\Github\P9-scheduler-plugins\data\\austria-residential-wt_detailed_timeseries.csv", delimiter=",", decimal=".")

# Count the rows and columns
print(denmark_residential_wt.shape)

# Rename the columns

data = pd.DataFrame(denmark_residential_wt, columns=['Time', 'Generic 100kWh Li-Ion State of Charge', 'Total Renewable Power Output', 'AC Primary Load', 'Unmet Electrical Load'])
data.rename(columns={'Generic 100kWh Li-Ion State of Charge': 'Battery_charge',
                     'Total Renewable Power Output': 'Renewable_output',
                     'AC Primary Load': 'Primary_load',
                     'Unmet Electrical Load': 'Unmet_load'},
                     inplace=True)

data_spain = pd.DataFrame(spain_residential_wt, columns=['Time', 'Generic 100kWh Li-Ion State of Charge', 'Total Renewable Power Output', 'AC Primary Load', 'Unmet Electrical Load'])
data_spain.rename(columns={'Generic 100kWh Li-Ion State of Charge': 'Battery_charge',
                     'Total Renewable Power Output': 'Renewable_output',
                     'AC Primary Load': 'Primary_load',
                     'Unmet Electrical Load': 'Unmet_load'},
                     inplace=True)

data_austria = pd.DataFrame(austria_residential_wt, columns=['Time', 'Generic 100kWh Li-Ion State of Charge', 'Total Renewable Power Output', 'AC Primary Load', 'Unmet Electrical Load'])
data_austria.rename(columns={'Generic 100kWh Li-Ion State of Charge': 'Battery_charge',
                     'Total Renewable Power Output': 'Renewable_output',
                     'AC Primary Load': 'Primary_load',
                     'Unmet Electrical Load': 'Unmet_load'},
                     inplace=True)


#data["Battery_charge"] = data.Battery_charge.astype(float)

print(data.head())
print(data.dtypes)

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/data", methods=["GET"])
def state_of_charge():
    server_time = datetime.datetime.now()
    print(server_time)
    rounded_time = roundDownDateTime(server_time)
    rounded_shifted_time_7days = roundDownDateTime(server_time + datetime.timedelta(days=7))
    rounded_shifted_time_14days = roundDownDateTime(server_time + datetime.timedelta(days=14))
    print(rounded_time)

    row = data.loc[data["Time"] == rounded_time]
    row["Location"] = ["Denmark"]

    row2 = data_spain.loc[data_spain["Time"] == rounded_shifted_time_7days]
    row2["Location"] = ["Spain"]

    row3 = data_austria.loc[data_austria["Time"] == rounded_shifted_time_14days]
    row3["Location"] = ["Austria"]

    combined_rows = pd.concat([row, row2, row3])

    combined_rows["Time"] = combined_rows.Time.astype(str)
    combined_rows["Battery_charge"] = combined_rows.Battery_charge.astype('Float64')
    combined_rows["Renewable_output"] = combined_rows.Renewable_output.astype('Float64')
    combined_rows["Primary_load"] = combined_rows.Primary_load.astype('Float64')
    combined_rows["Unmet_load"] = combined_rows.Primary_load.astype('Float64')



    print(combined_rows.head())
    print(combined_rows.dtypes)
    return combined_rows.to_json(orient="records")


    #return row.to_json(orient="records")

@app.route("/alive", methods=["GET"])
def alive():
    print("I'm alive!")
    return "I'm alive!"

@app.route('/log', methods=['POST'])
def log_message():
  data = request.get_json()
  node = data.get('node')
  if node:
    print("Node: ", node)
    return "Node logged successfully!"
  else:
    return "No node provided.", 400

        
def roundDownDateTime(dt):
    delta_min = dt.minute % 5
    rounded_dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute - delta_min)
    # Remember to change year according to data
    
    return rounded_dt.strftime("%m/%d/2023 %I:%M:%S %p").lstrip("0").replace(" 0", " ").lstrip("/").replace("/0", "/")