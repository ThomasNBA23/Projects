"""
Created on Mon 07/01/2025
author: Thomas Moaté
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

df = pd.read_csv("data/Premier_league_data.csv")


#Step 1 : Visualize game per game the evolution of the points of each team for a specific season 

def get_teams(season,dataframe):
    dataframe = dataframe[dataframe["Season"]==season]
    return list(set(dataframe["HomeTeam"]))



def get_points_season(season,dataframe):
    df_P1 = dataframe[dataframe["Season"] == season]

    #Get the list of every team of the season
    Teams = get_teams(season,dataframe)

    #Get the data for every match of the season for every team
    team_data_season = {}

    for i in Teams:
        team_data_season[i] = []

    for i in range(len(df_P1)) :
        Away_team = df_P1.iloc[i]["AwayTeam"]
        Home_team=  df_P1.iloc[i]["HomeTeam"]

        #If the away team won the game
        if df_P1.iloc[i]["FTH Goals"] < df_P1.iloc[i]["FTA Goals"] :
            team_data_season[Away_team].append(3)
            team_data_season[Home_team].append(0)

        #If the home team won the game
        elif df_P1.iloc[i]["FTH Goals"] > df_P1.iloc[i]["FTA Goals"] : 
            team_data_season[Away_team].append(0)
            team_data_season[Home_team].append(3)

        #If it was a draw
        else : 
            team_data_season[Away_team].append(1)
            team_data_season[Home_team].append(1)

    #To get all the points got during the season, and then get the evolution
    for i in team_data_season.keys() : 
        team_data_season[i].append(0) 
        team_data_season[i].reverse()
        for j in range(1,len(team_data_season[i])) :
            team_data_season[i][j] += team_data_season[i][j-1]

    return team_data_season


def visualize_team_season(team_data_season):
    #We choose a color for every team :
    color= {
        "Arsenal": "#EF4135",  # Light red
        "Aston Villa": "#670E36",  # Dark maroon
        "Bournemouth": "#D00000",  # Bright red
        "Brentford": "#9E1B32",  # Burgundy red
        "Brighton": "#005DAA",  # Navy blue
        "Chelsea": "#003087",  # Dark blue
        "Crystal Palace": "#1B458F",  # Dark blue
        "Everton": "#003B5C",  # Navy blue
        "Fulham": "#000000",  # Black
        "Liverpool": "#E60012",  # Bright red
        "Luton": "#FF6A13",  # Bright orange
        "Man City": "#6CABDD",  # Light blue
        "Man United": "#DA291C",  # Bright red
        "Newcastle": "#1C1C1C",  # Black
        "Nott'm Forest": "#9E1B32",  # Burgundy red
        "Sheffield United": "#E30613",  # Bright red
        "Tottenham": "#003C71",  # Navy blue
        "West Ham": "#7A1F3D",  # Dark maroon
        "Wolves": "#FDB913",  # Bright yellow
        "Blackburn": "#1D1D1B",  # Black
        "Bolton": "#003B5C",  # Dark blue
        "Burnley": "#9E1B32",  # Burgundy red
        "Cardiff": "#003B5C",  # Navy blue
        "Charlton": "#B90000",  # Red
        "Coventry": "#005EA6",  # Blue
        "Derby County": "#000000",  # Black
        "Ipswich": "#006A8E",  # Blue
        "Leeds": "#003DA5",  # Blue
        "Leicester": "#003B5C",  # Navy blue
        "Blackpool": "#000000",  # Black
        "Middlesbrough": "#D21F2D",  # Red
        "Queens Park Rangers": "#0046A0",  # Blue
        "Reading": "#003E74",  # Blue
        "Southampton": "#D71920",  # Red
        "Stoke": "#F5B400",  # Yellow
        "Sunderland": "#F7C300",  # Yellow
        "Swansea City": "#006F62",  # Greenish-blue
        "Wigan": "#004B87",  # Blue
        "Watford": "#F4C300",  # Yellow
        "West Brom": "#003D5B",  # Blue
        "Wimbledon": "#004C97",  # Blue
        "Huddersfield": "#004A6B",  # Blue
        "Birmingham": "#005BAC",  # Blue
        "Norwich": "#009639",  # Green
        "Sheffield Wednesday": "#006BA6",  # Blue
        "Swindon Town": "#DA291C",  # Red
        "Oldham Athletic": "#004B87",  # Blue
        "Barnsley": "#E30613",  # Red
        "Cambridge United": "#002F6C",  # Blue
        "Millwall": "#003F87",  # Blue
        "Portsmouth": "#1C5A80",  # Blue
        "Exeter City": "#8D1B3D",  # Red
        "Grimsby Town": "#3A3A3A",  # Dark grey
        "Darlington": "#FFFFFF",  # White
        "Gillingham": "#0033A0",  # Blue
        "Walsall": "#C8102E",  # Red
        "Stockport County": "#003A7D",  # Blue
        "Northampton Town": "#B00000",  # Red
        "Lincoln City": "#FF6600",  # Orange
        "Brentford": "#9E1B32",  # Burgundy red
        "Fleetwood Town": "#C72C2F"  # Red
    }

    for i in team_data_season.keys():
        x = list(range(len(team_data_season[i])))
        plt.plot(x,team_data_season[i],color[i])
        team_name_and_pts = f"{i} :{team_data_season[i][-1]} pts"
        plt.text(x[-1],team_data_season[i][-1],team_name_and_pts, color=color[i])

    plt.legend(team_data_season.keys(), loc='upper left')
    plt.show()


if __name__ == "__main__":
    season = "2021/22"
    team_data_season = get_points_season(season,df)
    visualize_team_season(team_data_season)


