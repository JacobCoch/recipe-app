const viewAll = document.getElementById('view-all-recipes-btn');
const recipeUrl = viewAll.getAttribute('data-recipe-url');

viewAll.addEventListener('click', () => {
  window.location.href = recipeUrl;
});
