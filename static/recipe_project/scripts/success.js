document.addEventListener('DOMContentLoaded', function () {
  const messageElement = document.getElementById('message');
  const imageElement = document.getElementById('main-image');
  const contentContainer = document.getElementById('content-container');
  const nextButton = document.getElementById('next-button');
  const headingElement = document.getElementById('heading');

  // Define arrays for headings, messages, and image sources
  const headings = [
    'Customize your own pancakes',
    'Welcome to TasteBuds',
    'Unlock the Chef in You',
    // Add more headings as needed
  ];

  const messages = [
    'Create your own delicious recipes and save them in TasteBuds.',
    'Your personal recipe organizer. Store your recipes in TasteBuds and access them on all your devices, anywhere, anytime.',
    'Discover new flavors, share your culinary creations, and simplify your cooking journey with TasteBuds!',
  ];

  const imageSources = [
    '/media/recipes/brownies.jpg',
    '/media/recipes/cherry_pancakes.jpg',
    '/media/recipes/fruit_cookies.jpg',
    // Add more image paths as needed
  ];

  const backgroundColors = [
    'beige', // Default background color
    'lightblue', // Background color for the second content/image pair
    'lightgreen',
  ];

  // Initialize an index to keep track of the current image
  let currentImageIndex = 0;

  nextButton.addEventListener('click', function () {
    // Change the heading and message based on the current image
    headingElement.textContent = headings[currentImageIndex];
    messageElement.textContent = messages[currentImageIndex];

    // Change the image source using the imageSources array
    currentImageIndex = (currentImageIndex + 1) % imageSources.length; // Cycle through images
    imageElement.src = imageSources[currentImageIndex];

    // Change the background color (e.g., to a different color)
    contentContainer.style.backgroundColor =
      backgroundColors[currentImageIndex]; // Change to your desired color
  });
});
