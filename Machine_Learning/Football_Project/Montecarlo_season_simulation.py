"""
Created on 07/01/2025
author: Thomas Moaté
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("data/Premier_league_data.csv")

from Points_visualization import get_teams,get_points_season,visualize_team_season

#From the datas of the goals of every team, simulate a whole season, with monte carlo with the hypothesis that every team goals follow a Poisson distribution

def get_model_parameters(season,dataframe):
    df_model = df[df["Season"] == season]
    teams = get_teams(season,dataframe)
    #Goals scored (or conceded) at home and away
    dict_goals_scored = { team : [0,0] for team in teams}
    dict_goals_conceded = { team : [0,0] for team in teams}

    #Get the number of all the goals scored this season, at home and away
    nb_home_goals = df_model["FTH Goals"].sum()
    nb_away_goals = df_model["FTA Goals"].sum()

    avg_home = nb_home_goals/(nb_home_goals+nb_away_goals)
    avg_away = nb_away_goals/(nb_away_goals+nb_home_goals)
    #Get the number of goals scored by each team this season, both at home and away
    for i in range(len(df_model)):
        Away_team = df_model.iloc[i]["AwayTeam"]
        Home_team = df_model.iloc[i]["HomeTeam"]
        dict_goals_scored[Home_team][0] += (df_model.iloc[i]["FTH Goals"])
        dict_goals_scored[Away_team][1] += (df_model.iloc[i]["FTA Goals"])

        dict_goals_conceded[Home_team][0] += (df_model.iloc[i]["FTA Goals"])
        dict_goals_conceded[Away_team][1] += (df_model.iloc[i]["FTH Goals"])

    #Get the parameters of the Poisson distribution
    dict_strength_teams = {team : [dict_goals_scored[team][0]/19,dict_goals_scored[team][1]/19] for team in teams} #mean of the goals scored by every team at home and away


    dict_poisson_parameters = {team : [dict_strength_teams[team][0],dict_strength_teams[team][1]] for team in teams}

    return dict_poisson_parameters

#Simulate the whole season with the Poisson parameters
def get_simulated_results(season,df,parameters):
    df_res = df[df["Season"]==season]
    df_res = df_res.drop(columns=["FTH Goals","FTA Goals"])
    fth_goals = []
    fta_goals = []
    for i in range(len(df_res)):
        home = df_res.iloc[i]["HomeTeam"]
        away = df_res.iloc[i]["AwayTeam"]
        home_goals= np.random.poisson(lam=parameters[home][0])
        away_goals = np.random.poisson(lam=parameters[away][1])
        fth_goals.append(home_goals)
        fta_goals.append(away_goals)
    
    df_res["FTH Goals"] = fth_goals
    df_res["FTA Goals"] = fta_goals
    return df_res 

# Absolutely not satisfying with one simulation (due to the amount of games in a season, 38 is too low)
# team_data_season = get_points_season(season,get_simulated_results(season,df,get_model_parameters(season)))
# visualize_team_season(team_data_season)

#Montecarlo visualization :

def monte_carlo_simulation(season,dataframe,nb_simulation=100):
    dataframe = dataframe[dataframe["Season"]==season]
    teams = get_teams(season,dataframe)
    final_pts = {team: [0]*39 for team in teams}
    for i in range(nb_simulation):
        df_res = get_simulated_results(season,dataframe,get_model_parameters(season,dataframe))
        datas_seasons = get_points_season(season,df_res)
        for a in teams :
            final_pts[a] = [x + y for x,y in zip(final_pts[a],datas_seasons[a])]
    for i in teams :
        final_pts[i] = [int(j/nb_simulation) for j in final_pts[i]]
    visualize_team_season(final_pts)


season = "2021/22"
monte_carlo_simulation(season,df)

