document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('recipe-search-input');

  searchInput.addEventListener('input', function () {
    const searchQuery = this.value;
    const url = '/recipe/?name=' + searchQuery;

    fetch(url)
      .then((response) => response.text())
      .then((data) => {
        const recipeContainer = document.querySelector('.recipe-container');
        recipeContainer.innerHTML = data;
      })
      .catch((error) => console.error('Error:', error));
  });
});
