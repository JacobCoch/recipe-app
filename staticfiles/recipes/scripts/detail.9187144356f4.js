document.addEventListener('DOMContentLoaded', function () {
  const dropdownButton = document.getElementById('dropdownMenuButton');
  const dropdownMenu = document.querySelector('.dropdown-menu');
  const deleteRecipeButton = document.getElementById('delete-recipe-button');
  const confirmDeleteButton = document.getElementById('confirm-delete');
  const cancelDeleteButton = document.getElementById('cancel-delete');
  const deleteRecipeForm = document.querySelector('.delete-recipe-form');
  const deleteRecipeModal = document.getElementById('delete-recipe-modal');

  $(document).ready(function () {
    $('.edit-recipe-button').click(function () {
      $('.recipe-info span').attr('contenteditable', 'true');
      $('.edit-recipe-form').show();
    });
  });

  deleteRecipeButton.addEventListener('click', () => {
    // Show the modal when the "Delete Recipe" button is clicked
    deleteRecipeModal.style.display = 'block';
  });

  // Hide the modal when the "Cancel" button is clicked
  cancelDeleteButton.addEventListener('click', () => {
    deleteRecipeModal.style.display = 'none';
  });

  // Handle the "Yes, Delete" button click
  confirmDeleteButton.addEventListener('click', () => {
    // Submit the form
    deleteRecipeForm.submit();
  });

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

  // Add click event to all "Edit Recipe" buttons using event delegation
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('edit-recipe-button')) {
      const recipeId = e.target.getAttribute('data-recipe-id');
      const editForm = document.querySelector(
        `.edit-recipe-form[data-recipe-id="${recipeId}"]`
      );
      const recipeDetails = document.querySelector(
        `.recipe-info[data-recipe-id="${recipeId}"]`
      );
      if (editForm && recipeDetails) {
        editForm.style.display = 'block';
        recipeDetails.style.display = 'none';
      }
    }
  });
});
