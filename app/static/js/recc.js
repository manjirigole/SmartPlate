document.addEventListener('DOMContentLoaded', function () {
    fetch('/recommendations')
        .then(response => response.json())
        .then(data => {
            const recommendationsDiv = document.getElementById('recommendations');
            data.forEach(recipe => {
                const recipeCard = document.createElement('div');
                recipeCard.classList.add('recipe-card');
                const image = document.createElement('img');
                image.src = recipe.image;
                const title = document.createElement('h3');
                title.textContent = recipe.title;
                recipeCard.appendChild(image);
                recipeCard.appendChild(title);
                recommendationsDiv.appendChild(recipeCard);
            });
        })
        .catch(error => console.error('Error fetching recommendations:', error));
});
