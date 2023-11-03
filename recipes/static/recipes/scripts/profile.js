document.addEventListener('DOMContentLoaded', function () {
  const dropdownButton = document.getElementById('dropdownMenuButton');
  const dropdownMenu = document.querySelector('.dropdown-menu');
  const detailsButtons = document.querySelectorAll('.details-button');

  const likeButtons = document.querySelectorAll('.like-button');

  likeButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
      const recipeId = this.getAttribute('data-recipe-id');
      event.preventDefault();
      fetch(`/recipe/fav/${recipeId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.is_liked) {
            this.innerHTML = '<i class="fas fa-heart"></i>';
          } else {
            this.innerHTML = '<i class="far fa-heart"></i>';
          }
        });
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  detailsButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      if (button) {
        const recipeUrl = button.getAttribute('data-recipe-url');
        if (recipeUrl) {
          window.location.href = recipeUrl;
        } else {
          console.error('data-recipe-url attribute not found on the button.');
        }
      } else {
        console.error('Button element not found.');
      }
    });
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
});
