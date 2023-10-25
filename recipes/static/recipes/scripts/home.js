const viewAll = document.getElementById('view-all-recipes-btn');
const recipeUrl = viewAll.dataset.recipeUrl;
const addRecipe = document.getElementById('add-recipe-btn');
const addRecipeUrl = addRecipe.dataset.addRecipeUrl;

viewAll.addEventListener('click', () => (window.location.href = recipeUrl));
addRecipe.addEventListener(
  'click',
  () => (window.location.href = addRecipeUrl)
);
