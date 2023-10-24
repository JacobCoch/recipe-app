const viewAll = document.getElementById('view-all-recipes-btn');
const recipeUrl = viewAll.getAttribute('data-recipe-url');
const addRecipe = document.getElementById('add-recipe-btn');
const addRecipeUrl = addRecipe.getAttribute('data-add-recipe-url');

viewAll.addEventListener('click', () => {
  window.location.href = recipeUrl;
});

addRecipe.addEventListener('click', () => {
  window.location.href = addRecipeUrl;
});
