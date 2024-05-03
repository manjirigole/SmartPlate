from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__, template_folder='C:\\Users\\Lenovo\\Desktop\\MINI PROJECT\\SmartPlate2\\app\\templates', static_folder='C:\\Users\\Lenovo\\Desktop\\MINI PROJECT\\SmartPlate2\\app\\static')

# Define the remove_fractions function
def remove_fractions(text):
    cleaned_text = re.sub(r'\d', '', text)
    cleaned_text = re.sub(r'[\d½¾¼⅓]', '', cleaned_text)
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)
    return cleaned_text.strip()

# Define the remove_metrics function
def remove_metrics(text):
    cleaned_text = text.replace("tsp", "").replace("Tbsp", "").replace(".", "").replace("cup", "").replace("cups", '')
    return cleaned_text.strip()

# Load data from CSV file
recipes_df = pd.read_csv('C:\\Users\\Lenovo\\Desktop\\MINI PROJECT\\SmartPlate2\\food.csv')

# Data Cleaning
recipes_df['ingredients'] = recipes_df['ingredients'].apply(remove_fractions)
recipes_df['ingredients'] = recipes_df['ingredients'].apply(remove_metrics)

# Vectorization
cv = CountVectorizer(max_features=5000)
vectors = cv.fit_transform(recipes_df['ingredients']).toarray()

# Similarity Calculation
similarity = cosine_similarity(vectors)

def recommend(recipe):
    if len(recipes_df) == 0:
        return []

    recipe_index = recipes_df[recipes_df['image_name'] == recipe].index[0]  # Use 'image_name' instead of 'name'
    distances = similarity[recipe_index]
    recipes_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_recipes = [{
        'title': recipes_df.iloc[i[0]]['title'],  # Use 'title' instead of 'name'
        'image_filename': recipes_df.iloc[i[0]]['image_name']  # Use 'image_name' instead of 'name'
    } for i in recipes_list]
    return recommended_recipes


@app.route('/')
def index():
    recipe_titles = recipes_df['image_name'].tolist()  # Change 'image_name' to the correct column name
    default_recipe = recipe_titles[0]  # Select the first recipe as default
    return render_template('recc.html', recipe_titles=recipe_titles, recipe=default_recipe)


@app.route('/recommendations', methods=['POST'])
def recommendations():
    selected_recipe = request.form['recipe']
    recommended_recipes = recommend(selected_recipe)
    
    return jsonify(recommended_recipes)

from flask import send_from_directory

@app.route('/images/<path:image_name>')
def serve_image(image_name):
    directory = 'static/images/Food Images'  # Directory path with whitespace
    encoded_directory = quote(directory, safe='')  # Encode whitespace in the directory path
    return send_from_directory(encoded_directory, image_name)

if __name__ == '__main__':
    app.run(debug=True)

'''from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
from flask import send_from_directory
from urllib.parse import quote

app = Flask(__name__, template_folder='C:\\Users\\Lenovo\\Desktop\\MINI PROJECT\\SmartPlate2\\app\\templates', static_folder='C:\\Users\\Lenovo\\Desktop\\MINI PROJECT\\SmartPlate2\\app\\static\\images\\Food Images')

# Define the remove_fractions function
def remove_fractions(text):
    cleaned_text = re.sub(r'\d', '', text)
    cleaned_text = re.sub(r'[\d½¾¼⅓]', '', cleaned_text)
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)
    return cleaned_text.strip()

# Define the remove_metrics function
def remove_metrics(text):
    cleaned_text = text.replace("tsp", "").replace("Tbsp", "").replace(".", "").replace("cup", "").replace("cups", '')
    return cleaned_text.strip()

# Define the read_csv function
def read_csv(file_path):
    recipes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            try:
                name = row['title']  # Use 'title' instead of 'name'
            except KeyError:
                name = None
            
            try:
                image_path = row['image_path']
            except KeyError:
                image_path = None
            
            try:
                ingredients = remove_fractions(row['ingredients'])
            except KeyError:
                ingredients = None
                
            recipes.append({
                'name': name,
                'image_path': image_path,
                'ingredients': ingredients
            })
    return recipes

# Load data from food_with_image_path.csv
recipes = read_csv('C:\\Users\\Lenovo\\Desktop\\MINI PROJECT\\SmartPlate2\\food_with_image_paths.csv')

# Convert the list of dictionaries to a DataFrame
recipes_df = pd.DataFrame(recipes)

# Data Cleaning
recipes_df['ingredients'] = recipes_df['ingredients'].apply(remove_fractions)
recipes_df['ingredients'] = recipes_df['ingredients'].apply(remove_metrics)

# Vectorization
cv = CountVectorizer(max_features=5000)
vectors = cv.fit_transform(recipes_df['ingredients']).toarray()

# Similarity Calculation
similarity = cosine_similarity(vectors)

def recommend(recipe):
    if len(recipes_df) == 0:
        return []

    recipe_index = recipes_df[recipes_df['name'] == recipe].index[0]
    distances = similarity[recipe_index]
    recipes_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_recipes = [{
        'title': recipes_df.iloc[i[0]]['name'], 
        'image_path': recipes_df.iloc[i[0]]['image_path'].replace('\\', '/')} for i in recipes_list]
    return recommended_recipes
@app.route('/')
def index():
    recipe_titles = recipes_df['name'].tolist()
    recipe_image_paths = recipes_df['image_path'].tolist()
    default_recipe = recipe_titles[0]  # Select the first recipe as default
    return render_template('recc.html', recipe_titles=recipe_titles, recipe_image_paths=recipe_image_paths, recipe=default_recipe)


@app.route('/recommendations', methods=['POST'])
def recommendations():
    selected_recipe = request.form['recipe']
    recommended_recipes = recommend(selected_recipe)
    
    return jsonify(recommended_recipes)

from urllib.parse import quote

@app.route('/images/<path:image_name>')
def serve_image(image_name):
    directory = 'static/images/Food Images'  # Directory path with whitespace
    encoded_directory = quote(directory, safe='')  # Encode whitespace in the directory path
    return send_from_directory(encoded_directory, image_name)



if __name__ == '__main__':
    app.run(debug=True)'''
