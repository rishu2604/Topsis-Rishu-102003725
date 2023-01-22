import pandas as pd
import numpy as np
import sys
import os

def topsis(filename,weights,impacts):
    if len(sys.argv)!=5:
        print("ERROR: Inputs are not same as the required usage")
        print("Usage/Input should be in the format: python <program.py> <InputFile> <Weights> <Impacts> <ResultantFile")
        print("Example usage: python <program.py> <data.csv> <1, 1, 1> <+, +, +> <result.csv> ")
        
    try:
        data = pd.read_excel(filename)
    except FileNotFoundError:
        print("File not found")
        sys.exit(1) # means there was some issue / error / problem and that is why the program is exiting.
    df= pd.DataFrame(data)
    dataframe= pd.DataFrame(data)
    df = df.iloc[:,1:]
    column_size= len(df.axes[1])
    row_size= len(df.axes[0])
    if column_size<3:
        print("Atleast 3 columns required")
        sys.exit(1)

    for i in range(column_size):
        temp= 0
        for j in range(row_size):
            temp= temp + df.iloc[j,i]
        for j in range(row_size):
            df.iloc[j,i]= df.iloc[j,i]*weights[i-1]/temp
            
    ideal_best=df.max()
    ideal_worst=df.min()
    
    for i in impacts:
        if i=='-':
            ideal_best[i], ideal_worst[i] = ideal_worst[i], ideal_best[i]
    Score = [] 
    p = [] 
    n = [] 


    for i in range(len(df)):
        distance_best, distance_worst = 0, 0
        for j in range(1, column_size):
            distance_best = distance_best + (ideal_best[j-1] - df.iloc[i, j])**2
            distance_worst = distance_worst + (ideal_worst[j-1] - df.iloc[i, j])**2
        distance_best, distance_worst = distance_best*0.5, distance_worst*0.5
        Score.append(distance_worst/(distance_best + distance_worst))
        n.append(distance_worst)
        p.append(distance_best)
        
    dataframe['Topsis_Score']= Score
    dataframe['Rank'] = (dataframe['Topsis_Score'].rank(method='max', ascending=False))
    dataframe = dataframe.astype({"Rank": int})
    print(dataframe)
    dataframe.to_csv(sys.argv[4])

filename=sys.argv[1]

try:
    data = pd.read_excel(filename)
except FileNotFoundError:
    print("No such file")
    sys.exit(1)
    
weights=[]
impacts=[]
for item in sys.argv[2].split(","):
    if item.isdigit():
        weights.append(int(item))
    else:
        sys.exit(1)
        
for item in sys.argv[3].split(","):
    if item=='-' or item=='+':
        impacts.append((item))
    else:
        sys.exit(1)

topsis(filename,weights,impacts)
