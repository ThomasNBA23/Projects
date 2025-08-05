Premier League Season Analysis & Simulation

This project provides tools to analyze and simulate Premier League seasons using historical match data. It includes:

Visualization of teams' point evolution over a season
Heatmap of teams' form (wins over rolling windows)
Monte Carlo simulation of a full season using a Poisson model for goals

📁 Data Requirements
The project expects a CSV file named:

data/Premier_league_data.csv
The CSV should include at least the following columns:

Season (such as "2021/22")
HomeTeam, AwayTeam
FTH Goals: Full-time Home goals
FTA Goals: Full-time Away goals
1. Points Evolution Visualization

This component plots the match-by-match accumulation of points for each team during a selected season.

Key Functions
get_teams(season, df): Returns the list of teams for the given season.
get_points_season(season, df): Computes cumulative points for each team across matchdays.
visualize_team_season(team_data): Plots the points evolution for each team.
Example Usage
season = "2021/22"
team_data = get_points_season(season, df)
visualize_team_season(team_data)
2. Form Heatmap (Rolling Window)

Displays a heatmap of each team’s form, computed as the number of wins in the last 5 games, over the course of the season.

Key Function
get_teams_form_heatmap(season, df): Computes and visualizes the rolling form of each team.
Example Usage
season = "2021/22"
get_teams_form_heatmap(season, df)
3. Season Simulation with Poisson Model

Uses historical goal data to model team scoring tendencies and simulates an entire season based on Poisson-distributed match outcomes.

Assumptions
Each team’s goals follow a Poisson distribution.
The Poisson rate λ is learned from actual home/away scoring means.
Key Functions
get_model_parameters(season, df): Calculates average goals scored (strength) and optionally conceded (weakness) per team.
get_simulated_results(season, df, parameters): Simulates full match results using Poisson draws for goals.
Example Usage
season = "2021/22"
parameters = get_model_parameters(season, df)
simulated_df = get_simulated_results(season, df, parameters)


4. Season Simulation with Elo Rating System

This module simulates a Premier League season using an Elo rating system, where each team’s rating evolves based on match results and opponent strength. The model helps identify the most consistent and high-performing teams, even if the final league points differ.

Key Features
Every team starts with an Elo of 1500
Elo is updated after each match, for both teams
Results are coded as:
Win = 1
Draw = 0.5
Loss = 0
Home advantage is implicitly modeled via the result variable and Elo differentials
Sensitivity (k) is set to 100 for clearer separation between teams
How Elo is Updated
The following formula is used:

Expected_A = 1 / (1 + 10 ** ((Elo_B - Elo_A) / 400))
New_Elo_A = Elo_A + k * (Result_A - Expected_A)
Core Functions
def expected_score(elo_a, elo_b):
    return 1 / (1 + 10**((elo_b - elo_a)/400))

def update_elo(elo_a, elo_b, result, k):
    ...
    return new_elo_a, new_elo_b
The season simulator:

def get_elo_season(season, dataframe):
    ...
    return teams_elo_season  # dictionary of team Elo trajectories
    
Example Execution

if __name__ == "__main__":
    season = "2021/22"
    data = get_elo_season(season, df)
    visualize_team_season(data)
Visualization
The Elo rating of each team is visualized over the course of the season, showing how their performance evolved.

Information
Chelsea’s actual point total is significantly lower than Liverpool and City’s, but its Elo rating is higher in this simulation.
This suggests that Chelsea had a very consistent season, beating stronger teams and avoiding losses against weaker ones.


5. Future Improvements

Enhance the Poisson model by incorporating opponent weaknesses.
Track league table standings after simulation.
Run multiple Monte Carlo simulations to estimate probabilistic league outcomes.
