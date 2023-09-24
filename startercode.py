#Will Duggan, 

import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import regex as re


"""
Purpose: Opens the logfile
Input: The desired Can_ID as an integer in hex (0x181 or 0x001)
Output: DataFrame (Pandas) containing all of the data in the requested id (ex. "0x181" and "0x001")
        - Each row in the dataframe should be the values at different times
        - Each column should be a different element  
"""
def processor(can_id):

    jsonfile = open("ver1.json")
    logfile = open("racedata.log")
    df = pd.DataFrame(columns=['line_time', 'line_id', 'line_content'])

    """
    Hint you should break up each line of the log file into:
     - Time 
     - Can_Bus (not important)
     - Can_id
     - Content
    
    """

    times = []
    first_iter = True
    first_time = -1
    for line in logfile:
        
        line_time = line.split(' ')[0][1:-1]
        # line_id = line.split(' ')[1]
        end_content = line.split(' ')[2]
        line_id = end_content.split('#')[0]
        line_content = end_content.split('#')[1]
        #num = line.split('#')[1]
        #print(line_time, ",", line_id, ",", line_content)

        # line_time = "Parse out the Unix time from the message" #line[0]?
        row = {'line_time': line_time, 'line_id': line_id, 'line_content': line_content}
        df = df._append(row, ignore_index=True)
        
        '''  
        # If this message's id == the desired id, then we break up the content into groupings following ver1.json 
        if can_id == line_id:
            
            # Divide line_content into groupings then add them to the DataFrame (remember Endianness from slides)
            df.append()

            # Remember to keep track of time
            if first_iter == True:
                first_iter = False
                first_time = line_time
            times.append(line_time - first_time) 
        '''
    print(df)
    return df

"""
Purpose: Graph every element in the desired id from your dataframe using Plotly
Input: DataFrame to be graphed
Output: None
"""
def grapher():
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
def battery_grapher():
    return


if __name__ == "__main__":
   # Part 1
   # In this part we will be doing recreating what I showed you last work session with Pandas
   # Parse the data from the desired Can_ID and put them into respecitve DataFrames
   # Graph the data into multiple subplots using Plotly
   df181 = processor(0x181)
   df001 = processor(0x001)
   grapher()

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
   battery_processer(0x036)
   battery_grapher()
