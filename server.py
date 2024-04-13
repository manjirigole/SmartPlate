from flask import Flask, render_template, jsonify, request
import pandas as pd
import re
import csv 

app = Flask(__name__)

# Load data
recipes = pd.read_csv('food.csv')

# Data Cleaning
def remove_fractions(text):
    cleaned_text = re.sub(r'\d', '', text)
    cleaned_text = re.sub(r'[\d½¾¼⅓]', '', cleaned_text)
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)
    return cleaned_text.strip()

def remove_metrics(text):
    cleaned_text = text.replace("tsp", "").replace("Tbsp", "").replace(".", "").replace("cup", "").replace("cups", '')
    return cleaned_text.strip()

recipes['ingredients'] = recipes['ingredients'].apply(remove_fractions)
recipes['ingredients'] = recipes['ingredients'].apply(remove_metrics)

# Vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000)
vectors = cv.fit_transform(recipes['ingredients']).toarray()

# Similarity Calculation
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

# Recommendation Function
def recommend(recipe):
    if len(recipes) == 0:
        return []

    recipe_index = recipes[recipes['title'] == recipe].index[0]
    distances = similarity[recipe_index]
    recipes_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_recipes = [{'title': recipes.iloc[i[0]]['title'], 'image_name': recipes.iloc[i[0]]['image_name']} for i in recipes_list]
    return recommended_recipes
'''
@app.route('/')
def index():
    recipes = []
    with open('food.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipes.append({'title': row['title'], 'image_url': row['image_name']})
    recipe_titles = recipes['title'].tolist()
    return render_template('recc.html', recipes=recipe_titles)
    # Example: making a GET request to Node.js server
'''
@app.route('/')
def index():
    return render_template('recc.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    selected_recipe = request.form['recipe']
    recommended_recipes = recommend(selected_recipe)
    return jsonify(recommended_recipes)

if __name__ == '__main__':
    app.run(debug=True)
