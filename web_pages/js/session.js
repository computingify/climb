export default sessionPage;

import createSection from '/js/createSection.js';
import serverCom from '/js/serverCom.js';
import createInput from '/js/createInput.js';
import { SERVER_URL } from '/js/config.js';

// Access the functions as properties of the serverCom object
const checkUser = serverCom.checkUser;

function sessionPage() {
    // Get a reference to the <body> element
    var body = document.body;

    // Clear the content of the <body> element
    body.innerHTML = '';

    const id = createSection("identifiant");
    id.value = "Identifiant";

    const inputId = createInput(id, 'Identifiant');
    // Set focus on the inputId element
    inputId.focus();

    const buttonDiv = document.createElement('div');
    buttonDiv.style.display = 'flex'; // Set display property to flex

    const button = document.createElement('button');
    button.textContent = "Recherche";
    button.classList.add('button');

    // Create a div to display the climber count
    const climberCountDiv = document.createElement('div');
    climberCountDiv.id = 'climber-count';
    climberCountDiv.textContent = "Climbers attending: Loading...";
    body.appendChild(climberCountDiv);

    // Function to fetch and update the climber count
    function updateClimberCount() {
        fetch(`${SERVER_URL}/session/user/count`)
        .then(response => response.json())
        .then(data => {
            climberCountDiv.textContent = `Climbers attending: ${data.user_count}`;
        })
        .catch(error => {
            console.error('Error fetching climber count:', error);
            climberCountDiv.textContent = "Climbers attending: Error fetching data";
        });
    }
    
    document.addEventListener('climberCountUpdated', updateClimberCount); // Listen for the event
    // Call the function to update the climber count when the page loads
    updateClimberCount();

    function search() {
        const user_id = inputId.value;
        console.log('launch search request for ID = ', user_id);

        // Remove any existing user data container
        const existingContainer = document.querySelector('.user-data-container');
        if (existingContainer) {
            existingContainer.remove();
        }
        inputId.value = ''; // Clear the input when a new search is initiated

        checkUser(user_id);
    }

    button.addEventListener('click', search);
    buttonDiv.append(button);
    id.append(buttonDiv);

    // Listen for 'keypress' event on the input field
    inputId.addEventListener('keypress', function (event) {
        if (event.keyCode === 13) {
            search();
        }
    });
}