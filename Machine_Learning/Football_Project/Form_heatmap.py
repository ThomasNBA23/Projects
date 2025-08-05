"""
Created on Fri 07/04/2025
author: Thomas Moaté
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("data/Premier_league_data.csv")

from Points_visualization import get_teams
 
 
def get_teams_form_heatmap(season,dataframe) : 
    df_S2 = dataframe[dataframe["Season"]== season]
    team = get_teams(season,dataframe)

    #The typical choice to check the form of a team
    rolling_window = 5
    form_matrix = pd.DataFrame(index=team,columns=range(rolling_window,39))
    team_results = {i : [] for i in team}

    for index,row in df_S2.iterrows():
        #For each team we add W,L or D depending on the result
        Home,Away = row["HomeTeam"],row["AwayTeam"]
        if(row["FTH Goals"] < row["FTA Goals"]):
            team_results[Home].append("L")
            team_results[Away].append("W")
        elif(row["FTH Goals"] > row["FTA Goals"]):
            team_results[Home].append("W")
            team_results[Away].append("L")
        else : 
            team_results[Home].append("D")
            team_results[Away].append("D")


    #Calculation of the form of the team through season
    for i in team :
        res = team_results[i]
        for j in range(rolling_window,len(res)+1):
            wins = res[j-rolling_window:j].count("W")
            form_matrix.loc[i,j] = wins 


    form_array = form_matrix.astype(float).values
    plt.imshow(form_array, aspect='auto', cmap="RdYlGn", interpolation='bilinear')  # ← interpolation floute
    plt.xticks(ticks=np.arange(form_array.shape[1]), labels=form_matrix.columns, rotation=90)
    plt.yticks(ticks=np.arange(form_array.shape[0]), labels=form_matrix.index)
    plt.colorbar(label="Wins over 5 games")
    plt.xlabel("Matchday")
    plt.ylabel("Team")
    plt.show()


if __name__ == "__main__":
    season = "2021/22"
    get_teams_form_heatmap(season,df)
