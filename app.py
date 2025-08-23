import streamlit as st
import pickle
import pandas as pd

# Load trained model (make sure ipl_score_model.pkl is in same folder)
model = pickle.load(open("ipl_score_model.pkl", "rb"))

teams = [
    'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
]

def predict_score(batting_team, bowling_team, overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5):
    # One-hot encoding
    batting_team_encoded = [1 if team == batting_team else 0 for team in teams]
    bowling_team_encoded = [1 if team == bowling_team else 0 for team in teams]

    features = batting_team_encoded + bowling_team_encoded + [
        overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5
    ]

    columns = (
        [f'bat_team_{team}' for team in teams] +
        [f'bowl_team_{team}' for team in teams] +
        ['overs', 'runs', 'wickets', 'runs_last_5', 'wickets_last_5']
    )

    input_df = pd.DataFrame([features], columns=columns)

    return int(model.predict(input_df)[0])

# Streamlit UI
st.title("🏏 IPL First Innings Score Predictor")

batting_team = st.selectbox("Select Batting Team", teams)
bowling_team = st.selectbox("Select Bowling Team", [t for t in teams if t != batting_team])
overs = st.number_input("Overs Completed", min_value=5.0, max_value=20.0, step=0.1)
runs = st.number_input("Current Runs", min_value=0)
wickets = st.number_input("Wickets Fallen", min_value=0, max_value=10)
runs_in_prev_5 = st.number_input("Runs Scored in Previous 5 Overs", min_value=0)
wickets_in_prev_5 = st.number_input("Wickets Lost in Previous 5 Overs", min_value=0)

if st.button("Predict Score"):
    prediction = predict_score(batting_team, bowling_team, overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5)
    st.success(f"Predicted Final Score Range: {prediction-10} to {prediction+5}")
