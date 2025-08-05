"""
Created on Fri 07/11/2025
author: Thomas Moaté
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("data/Premier_league_data.csv")

from Points_visualization import visualize_team_season,get_teams

def expected_score(elo_a,elo_b):
    return 1/(1 + 10**((elo_b - elo_a)/400))

def update_elo(elo_a,elo_b,result, k):
    exp_a = expected_score(elo_a,elo_b)
    exp_b = 1-exp_a
    new_a = elo_a + k*(result-exp_a)
    new_b = elo_b + k*((1-result)-exp_b)
    return new_a,new_b


def get_elo_season(season,dataframe):
    df_elo = df[df["Season"] == season]

    Teams = get_teams(season,dataframe)

    teams_elo_season = {}

    for i in Teams :
        teams_elo_season[i]= [1500]

    for i in range(len(df_elo)):
        Away_team = df_elo.iloc[i]["AwayTeam"]
        Home_team = df_elo.iloc[i]["HomeTeam"]

        if df_elo.iloc[i]["FTH Goals"] > df_elo.iloc[i]["FTA Goals"]: 
            result = 1
        elif df_elo.iloc[i]["FTH Goals"] < df_elo.iloc[i]["FTA Goals"]:
            result = 0
        else : 
            result = 0.5
        
        a,b= update_elo(teams_elo_season[Home_team][-1],teams_elo_season[Away_team][-1],result,k=100)
        teams_elo_season[Home_team].append(int(a))
        teams_elo_season[Away_team].append(int(b))
    return teams_elo_season

if __name__ =="__main__":
    season = "2021/22"
    data = get_elo_season(season,df)
    visualize_team_season(data)
    
# Conclusion: Chelsea’s actual ranking is significantly lower than Liverpool and City’s, yet its Elo ranking is considerably higher—outperforming both Liverpool and City at a medium-to-high sensitivity level.
# This suggests that Chelsea has been highly consistent throughout the season, securing impressive wins against stronger teams and suffering fewer defeats against lower-ranked teams.


