// script.js
const searchBox = document.getElementById('search-box');
const searchResults = document.getElementById('search-results');

searchBox.addEventListener('input', async function() {
    const query = searchBox.value;
    try {
        const response = await fetch(`/search?query=${query}`);
        const recipes = await response.json();

        // Clear previous search results
        searchResults.innerHTML = '';

        // Display new search results
        recipes.forEach(recipe => {
            const listItem = document.createElement('li');
            listItem.textContent = recipe.name;
            searchResults.appendChild(listItem);
        });
    } catch (error) {
        console.error(error);
    }
});
