// Define a function to handle the search
function handleSearch() {
  const searchInput = document.querySelector(".search-box");
  const items = document.querySelectorAll(".item");

  searchInput.addEventListener("input", () => {
    const searchTerm = searchInput.value.toLowerCase();

    items.forEach((item) => {
      const recipeName = item.querySelector(".recipe_name").textContent.toLowerCase();
      if (recipeName.includes(searchTerm)) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    });
  });
}

// Call the search function when the page loads
window.addEventListener("load", handleSearch);