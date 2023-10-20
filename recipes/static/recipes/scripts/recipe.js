document.addEventListener('DOMContentLoaded', function () {
  const detailsButtons = document.querySelectorAll('.details-button');
  detailsButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      const recipeUrl = button.getAttribute('data-recipe-url');
      window.location.href = recipeUrl;
    });
  });
});
