export default sessionPage;

import createSection from '/js/createSection.js';
import serverCom from '/js/serverCom.js';
import createInput from '/js/createInput.js';

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

// Function to remove the user data container after 3 seconds or clear input field
function removeUserDataContainer(container, inputId) {
    setTimeout(() => {
        if (container) {
            container.remove(); // Remove the container after 3 seconds
            inputId.value = ''; // Clear the input field
        }
    }, 3000);
}

// Call removeUserDataContainer after a successful addUserToSession call
function addUserToSession(id, container) {
    console.log("Push Valid button");
    const url = new URL('http://127.0.0.1:5000/api/v1/resources/session/add_user');
    const params = { UserId: id };
    url.search = new URLSearchParams(params).toString();

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    fetch(url, options)
    .then(response => {
        if (response.ok) {
            container.style.backgroundColor = 'green';
            removeUserDataContainer(container, document.getElementById('Identifiant'));
        } else {
            container.style.backgroundColor = 'red';
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        container.style.backgroundColor = 'red';
        console.error('There was a problem with the fetch operation:', error);
    });
}
