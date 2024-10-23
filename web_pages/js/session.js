import createSection from '/js/createSection.js';
import serverCom from '/js/serverCom.js';
import createInput from '/js/createInput.js';
import { SERVER_URL } from '/js/config.js';

export default sessionPage;

// Access the functions as properties of the serverCom object
const { checkUser } = serverCom;

function sessionPage() {
    const body = document.body;
    body.innerHTML = ''; // Clear the content of the <body> element

    const idSection = createSection("identifiant");
    idSection.value = "Identifiant ou Nom Prenom";

    const inputId = createInput(idSection, 'Identifiant');
    const button = createSearchButton(inputId);
    const climberCountDiv = createClimberCountDiv();
    
    // Append elements to the body
    body.appendChild(climberCountDiv);
    idSection.appendChild(button);
    body.appendChild(idSection);

    // Focus on the input field
    inputId.focus();
    
    // Initialize the climber count
    updateClimberCount(climberCountDiv);

    // Update the climber count when the custom event is dispatched
    document.addEventListener('climberCountUpdated', () => updateClimberCount(climberCountDiv));

    // Trigger search on 'Enter' key press
    inputId.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            search(inputId);
        }
    });
}

function createSearchButton(inputElement) {
    const buttonDiv = document.createElement('div');
    buttonDiv.style.display = 'flex';

    const button = document.createElement('button');
    button.textContent = "Recherche";
    button.classList.add('button');

    button.addEventListener('click', () => search(inputElement));

    buttonDiv.appendChild(button);
    return buttonDiv;
}

function createClimberCountDiv() {
    const climberCountDiv = document.createElement('div');
    climberCountDiv.id = 'climber-count';
    climberCountDiv.textContent = "Climbers attending: Loading...";
    return climberCountDiv;
}

function updateClimberCount(climberCountDiv) {
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

function search(inputElement) {
    const userId = inputElement.value.trim();
    if (!userId) {
        console.warn('Search aborted: Empty input');
        return;
    }

    console.log('Launching search request for ID:', userId);

    // Remove any existing user data container
    removeExistingUserData();

    inputElement.value = ''; // Clear the input field

    // Perform the user check
    checkUser(userId);
}

function removeExistingUserData() {
    const existingContainer = document.querySelector('.user-data-container');
    if (existingContainer) {
        existingContainer.remove();
    }
}
