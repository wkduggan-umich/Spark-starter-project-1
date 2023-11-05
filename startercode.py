#Will Duggan, 

import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import regex as re
import random


""" 
Purpose: Opens the logfile
Input: The desired Can_ID as an integer in hex (0x181 or 0x001)
Output: DataFrame (Pandas) containing all of the data in the requested id (ex. "0x181" and "0x001")
        - Each row in the dataframe should be the values at different times
        - Each column should be a different element  
"""
def processor(can_id):
    with open("ver1.json") as f:
        jsonfile = json.load(f)
    
    with open("battery.log") as f:
        logfile = f.readlines()
    
    # Create dataframe

    # This will store the column names to put into the data frame
    columns = ['line_id']

    # Holds the different devices to record
    parsing_data = []
    for measurement, info in jsonfile.items():
        if int(info["id"],base=16) == int(hex(can_id),base=16):
            # Removes spaces of column name
            formatted_measurement = '_'.join(measurement.lower().split(" "))
            parsing_data.append({formatted_measurement: info})
            columns.append(formatted_measurement)
    df = pd.DataFrame(columns=columns)

    endian = endianness(can_id)
    start_time = None
    for line in logfile:
        # Load individual values from log file
        split_line = line.split(' ')
        line_time = split_line[0].strip("()")

        if start_time is None:
            start_time = line_time

        end_content = split_line[2].split('#')
        line_id = int(end_content[0], 16)
        line_content = end_content[1][0:16]
        line_content = int(line_content, 16).to_bytes(8) # Convert to byte array
        
        # Parse line content based on JSON data
        if can_id == line_id:
            row = {"line_id": [line_id]} 
            for data in parsing_data:
                for measurement, info in data.items():
                    byte_index = info["bytes"]
                    measurement_int = int.from_bytes(line_content[byte_index[0]:byte_index[1]], endian) * info['scaling']
                    row[measurement] = [measurement_int]
                    if (measurement == "rpm" or measurement == "pack_current") and (measurement_int > 5000):
                        row[measurement] = df.iloc[-1][measurement]
                   
            df_row = pd.DataFrame(row, index = [float(line_time) - float(start_time)])
            df = pd.concat([df, df_row])
    print(df.head)
    return df    

def endianness(can_id: int):
    if can_id >= 181:
        return "little"
    return "big"
    
"""
Purpose: Graph every element in the desired id from your dataframe using Plotly
Input: DataFrame to be graphed
Output: None
"""
def grapher(can_id: int, df: pd.DataFrame) -> None:
    
    cols = df.columns[1:]
    fig = make_subplots(rows=len(cols), cols=1)
    
    for i in range(len(cols)):
        print(df.index)
        print(df[cols[i]])
        fig.add_trace(go.Scattergl(x=df.index, y=df[cols[i]], mode='lines', name=cols[i]), row=i + 1, col=1)

        layout = go.Layout(
            title=str(cols[i]) + ' Graph',
            xaxis=dict(title='Time')
        )
    fig.show()
    
    return

"""
Purpose: Process Battery Diagnostic Data (instant voltage, instant resistence, operating voltage, and check sum)         
Input: Can_ID value in hex
Output: Df with the cols,
        - Battery_ID            Bytes: [0]
        - Instant Voltage       Bytes: [1] + [2]
        - Instant Resistance    Bytes: [3] + [4]
        - Operating Voltage     Bytes: [5] + [6]
        - Check Sum             Bytes: [7]
        ***NOTE THIS IS NOT IN THE JSON VER1 FILE***
"""
def battery_processer(can_id):
    logfile = open("battery.log")

    return

"""
Purpose: Graph every element in the can_id 0x036, including a new trace for each battery_id
Input: DataFrame to be graphed
Output: None
"""
def battery_grapher(df):
    ids = df.battery_id.unique()
    cols = df.columns[2:]
    fig = make_subplots(rows=1, cols=len(cols))

    for id in ids:
        id_data_frame = df[df["battery_id"] == id]
        
        for i in range(len(cols)):
            fig.add_trace(go.Scattergl(x=id_data_frame.index, y=id_data_frame[cols[i]], mode='lines', name=cols[i] + ' ' + str(int(id))), row=1, col= i + 1)

            layout = go.Layout(
                title=str(cols[i]) + ' Graph',
                xaxis=dict(title='Time')
            )

    fig.show()
    

if __name__ == "__main__":
   # Part 1
   # In this part we will be doing recreating what I showed you last work session with Pandas
   # Parse the data from the desired Can_ID and put them into respecitve DataFrames
   # Graph the data into multiple subplots using Plotly
#    df181 = processor(0x181)
#    df001 = processor(0x001)
#    grapher(0x181,df181)
#    grapher(0x001, df001)

   # Part 2
   # In this part we will be making a visualization of a Battery Diagnostic test
   # We can reuse some of the code from Part 1, but we have to make some serious modifications
   # Can_ID 0x036 is used for all Battery Diagnostic Info
   # Each line of the logfile containing this Can_ID shares info on 16 different batteries cells
   # Each cell is differentiated by the first byte of the content being a battery_id (byte[0])
   # ***This is different from before as each battery_id has data that is not related to the other battery_ids***
   # We have to keep track of the data and which battery_id it belongs to
   # For our graph we will then seperate each batter_id into its own "trace" in plotly
   # In other words, each battery_id should be its own line on the graph (there should be around 16 lines/battery_ids total)
   # For roughly what the graph should look like, check the Part2_Example.png included in the zip file
   
   df036 = processor(0x036)
   battery_grapher(df036)
   
