document.addEventListener('DOMContentLoaded', function () {
  const messageElement = document.getElementById('message');
  const imageElement = document.getElementById('main-image');
  const contentContainer = document.getElementById('content-container');
  const nextButton = document.getElementById('next-button');
  const headingElement = document.getElementById('heading');

  // Define arrays for headings, messages, and image sources
  const headings = [
    'Welcome to TasteBuds',
    'Customize your own pancakes',
    'Master the art of cooking',
    'Unlock the Chef in You',
    // Add more headings as needed
  ];

  const messages = [
    'Your trusted recipe organizer. Easily store and access your recipes anytime, anywhere!',
    'Create your own delicious recipes and save them in TasteBuds!',
    'Elevate your culinary skills, experiment with new recipes, and share your creations with the world!',
    'Discover new flavors, share your culinary creations, and simplify your cooking journey with TasteBuds!',
  ];

  const imageSources = [
    '{% static "recipes/images/brownies.jpg" %}',
    '{% static "recipes/images/cherry_pancakes.jpg" %}',
    '{% static "recipes/images/fruit_cookies.jpg" %}',
    '{% static "recipes/images/strawberry_cake.jpg" %}',
    // Add more image paths as needed
  ];

  const backgroundColors = [
    'beige', // Default background color
    'lightblue', // Background color for the second content/image pair
    'lightgreen',
    'lightpink',
  ];

  const signUpButton = ['Learn More', 'Learn More', 'Learn More', 'Sign Up'];

  // Initialize an index to keep track of the current image
  let currentImageIndex = 0;

  const setInitialContent = () => {
    headingElement.textContent = headings[0];
    messageElement.textContent = messages[0];
    imageElement.src = imageSources[0];
    nextButton.textContent = signUpButton[0];
  };

  const preloadedImages = [];
  for (let i = 0; i < imageSources.length; i++) {
    const img = new Image();
    img.src = imageSources[i];
    preloadedImages.push(img);
  }

  nextButton.addEventListener('click', function () {
    // Increment the index first
    currentImageIndex = (currentImageIndex + 1) % imageSources.length; // Cycle through images

    // Change the heading and message based on the new index
    headingElement.textContent = headings[currentImageIndex];
    messageElement.textContent = messages[currentImageIndex];

    // Change the image source using the imageSources array
    imageElement.src = preloadedImages[currentImageIndex].src;

    // Change the background color
    contentContainer.style.backgroundColor =
      backgroundColors[currentImageIndex];

    const signupURL = nextButton.getAttribute('data-signup-url');
    if (nextButton.textContent === 'Sign Up' && signupURL) {
      window.location.href = signupURL;
    } else {
      nextButton.textContent = signUpButton[currentImageIndex];
    }
  });

  setInitialContent();
});
