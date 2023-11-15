document.addEventListener('DOMContentLoaded', function () {
  const viewAll = document.getElementById('view-all-recipes-btn');
  const recipeUrl = viewAll.dataset.recipeUrl;
  const addRecipe = document.getElementById('add-recipe-btn');
  const addRecipeUrl = addRecipe.dataset.addRecipeUrl;
  const dropdownButton = document.getElementById('dropdownMenuButton');
  const dropdownMenu = document.querySelector('.dropdown-menu');

  viewAll.addEventListener('click', () => (window.location.href = recipeUrl));
  addRecipe.addEventListener(
    'click',
    () => (window.location.href = addRecipeUrl)
  );
  // Add click event to the custom button to show/hide the dropdown
  dropdownButton.addEventListener('click', () => {
    if (dropdownMenu.style.display === 'block') {
      dropdownMenu.style.display = 'none';
    } else {
      dropdownMenu.style.display = 'block';
    }
  });

  // Add click event to the document to hide the dropdown when the user clicks outside of it
  document.addEventListener('click', (e) => {
    if (e.target.id !== 'dropdownMenuButton') {
      dropdownMenu.style.display = 'none';
    }
  });
});
