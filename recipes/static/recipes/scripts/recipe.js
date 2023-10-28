document.addEventListener('DOMContentLoaded', function () {
  const addRecipe = document.getElementById('add-recipe-btn');
  const addRecipeUrl = addRecipe.dataset.addRecipeUrl;
  const detailsButtons = document.querySelectorAll('.details-button');
  const dropdownButton = document.getElementById('dropdownMenuButton');
  const dropdownMenu = document.querySelector('.dropdown-menu');
  const likeButtons = document.querySelectorAll('.like-button');

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

  addRecipe.addEventListener(
    'click',
    () => (window.location.href = addRecipeUrl)
  );

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
});

function randChar() {
  let sample = ',./<>?0123456789/[]{}!@#$%^&*()_=+-';
  return sample.charAt(Math.floor(Math.random() * sample.length));
}

function appearTitle(titlePart, delay) {
  for (let i = 0; i < titlePart.children.length; i++) {
    let char = titlePart.children[i];
    let initState = char.textContent; // Store the initial state
    let inc = 0;
    let dur = 0.5;
    let startDate = 0;
    let del = i * 0.15 + delay;
    gsap.fromTo(
      char,
      {
        opacity: 0,
        x: '-10%',
      },
      {
        duration: dur,
        delay: del,
        opacity: 1,
        ease: 'power3.Out',
        x: 0,
        onStart() {
          startDate = Date.now();
        },
        onUpdate: () => {
          if (inc % 3 === 0) {
            char.textContent = randChar();
          }
          inc++;
          if (Date.now() - startDate >= (dur - 0.1) * 1000) {
            char.textContent = initState; // Reset the letter to its initial state
          }
        },
        onComplete: () => {
          char.textContent = initState; // Ensure the letter is reset when the animation is complete
        },
      }
    );
  }
}

const h1 = document.querySelector('h1');
appearTitle(h1, 0);
