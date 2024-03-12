from flask import Flask, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import sys
import string

app = Flask(__name__)

fp = r'C:\Users\peter\OneDrive\Documents\Websites\UFCApp\ufc\api\venv\masterMLpublic.csv'
ufc = pd.read_csv(fp)    
ufc['date'] = pd.to_datetime(ufc['date'])
ufc_2016 = ufc[ufc['date'].dt.year > 2015]
variables_to_keep = [
    'result', 'fighter', 'opponent', 'method', 'division', 'stance', 'total_comp_time',
    'round', 'time', 'referee', 'reach', 'height', 'age', 'knockdowns', 'sub_attempts', 
    'reversals', 'control', 'takedowns_landed', 'takedowns_attempts', 'sig_strikes_landed',
    'sig_strikes_attempts', 'total_strikes_landed', 'total_strikes_attempts', 
    'head_strikes_landed', 'head_strikes_attempts', 'body_strikes_landed', 
    'body_strikes_attempts', 'leg_strikes_landed', 'leg_strikes_attempts', 
    'distance_strikes_landed', 'distance_strikes_attempts', 'clinch_strikes_landed', 
    'clinch_strikes_attempts', 'ground_strikes_landed', 'ground_strikes_attempts', 
    'KO_losses', 'days_since_last_comp', 'lose_streak', 'win_streak', 
    'win_loss_ratio', 'num_fights', 'trueskill', 'elo'
    ]

ufc_2016 = ufc_2016[variables_to_keep]

fighter_a_name = ""
fighter_b_name = ""

@app.route('/api/retrieve', methods=['POST'])
def retrieve():
    global fighter_a_name
    global fighter_b_name 
    data = request.get_json()
    fighter_a_name = data['fighter1']
    fighter_b_name = data['fighter2']
    return 'Done', 201



@app.route('/api/test')
def func():
    # fighters = ufc['fighter']

    columns_to_exclude = ['win_streak', 'lose_streak']
    numeric_columns = ufc_2016.select_dtypes(include=['number']).columns.difference(columns_to_exclude)
    selected_columns = ['division'] + numeric_columns.tolist()

    # Keep only the selected columns
    ufc_selected = ufc_2016[selected_columns]

    division_rankings = {}
    for division, data in ufc_selected.groupby('division'):

        data.dropna(inplace=True)
        
        # Split data 
        X = data.drop(columns=['result', 'division'])
        y = data['result']
        rf_classifier = RandomForestClassifier(random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Fit the classifier to the data
        rf_classifier.fit(X_train, y_train)
        feature_importances = pd.Series(rf_classifier.feature_importances_, index=X.columns)
        
        # Rank features by importance
        ranked_features = feature_importances.sort_values(ascending=False)
        
        # Store the ranked features for this division in the dictionary
        division_rankings[division] = ranked_features

    predicted_winner, fighter_a_avg_ranking, fighter_b_avg_ranking, other_fighter = predict_winner(fighter_a_name, fighter_b_name, ufc_2016, division_rankings)
    #capitalize first letters of words
    formatted_winner = string.capwords(predicted_winner, sep=None)
    other_fighter = string.capwords(other_fighter, sep=None)
    formatted_winner2 = formatted_winner


    #calculate each fighter's chance
    fighter_a_chance = round(fighter_a_avg_ranking/(fighter_b_avg_ranking+fighter_a_avg_ranking)*100)
    fighter_b_chance = round(fighter_b_avg_ranking/(fighter_b_avg_ranking+fighter_a_avg_ranking)*100)
    return {'name': formatted_winner, 'other': other_fighter, 'a': fighter_a_chance, 'b': fighter_b_chance, 'winner': formatted_winner2}

def predict_winner(fighter_a_name, fighter_b_name, ufc_data, division_rankings):
    # Extract features for Fighter A
    fighter_a_data = ufc_data[ufc_data['fighter'] == fighter_a_name].iloc[0]
    fighter_a_division = fighter_a_data['division']
    fighter_a_ranked_features = division_rankings[fighter_a_division]
    X_fighter_a = fighter_a_data[fighter_a_ranked_features.index]

    # Extract features for Fighter B
    fighter_b_data = ufc_data[ufc_data['fighter'] == fighter_b_name].iloc[0]
    fighter_b_division = fighter_b_data['division']
    fighter_b_ranked_features = division_rankings[fighter_b_division]
    X_fighter_b = fighter_b_data[fighter_b_ranked_features.index]

    # Check if fighters have fought before
    if fighter_b_name in fighter_a_data['opponent']:
        # Adjust rankings if fighters have fought before
        fighter_a_avg_ranking = X_fighter_a.mean() * 1.05
        fighter_b_avg_ranking = X_fighter_b.mean() * 0.95
    elif fighter_a_name in fighter_b_data['opponent']:
        # Adjust rankings if fighters have fought before
        fighter_a_avg_ranking = X_fighter_a.mean() * 0.95
        fighter_b_avg_ranking = X_fighter_b.mean() * 1.05
    else:
        fighter_a_avg_ranking = X_fighter_a.mean()
        fighter_b_avg_ranking = X_fighter_b.mean()

    # Check if fighters are from different divisions
    if fighter_a_division != fighter_b_division:
        # If from different divisions, use catch weight division and its rankings
        catch_weight_ranked_features = division_rankings['Catch Weight']
        X_fighter_a = fighter_a_data[catch_weight_ranked_features.index]
        X_fighter_b = fighter_b_data[catch_weight_ranked_features.index]
        fighter_a_avg_ranking = X_fighter_a.mean()
        fighter_b_avg_ranking = X_fighter_b.mean()

    # Predict the winner based on the adjusted ranking score
    if fighter_a_avg_ranking > fighter_b_avg_ranking:
        return fighter_a_name, fighter_a_avg_ranking, fighter_b_avg_ranking, fighter_b_name
    elif fighter_a_avg_ranking < fighter_b_avg_ranking:
        return fighter_b_name, fighter_b_avg_ranking, fighter_a_avg_ranking, fighter_a_name
    else:
        return "Draw", fighter_a_avg_ranking, fighter_b_avg_ranking, 'none'


    
    

    

    
