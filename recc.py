import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
cv = CountVectorizer(max_features=5000)
vectors = cv.fit_transform(recipes['ingredients']).toarray()
similarity = cosine_similarity(vectors)

# Recommendation Function
def recommend(recipe):
    if len(recipes) == 0:
        return []

    recipe_index = recipes[recipes['title'] == recipe].index[0]
    distances = similarity[recipe_index]
    recipes_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_recipes = [recipes.iloc[i[0]]['title'] for i in recipes_list]
    return recommended_recipes

# Testing
print(recommend('Apples and Oranges'))
