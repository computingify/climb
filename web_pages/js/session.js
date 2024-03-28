export default sessionPage

import createSection from '/js/createSection.js'
import serverCom from '/js/serverCom.js';
import createInput from '/js/createInput.js';

// Access the functions as properties of the serverCom object
const checkUser = serverCom.checkUser;

function sessionPage() {
    // Get a reference to the <body> element
    var body = document.body;

    // Clear the content of the <body> element
    body.innerHTML = '';

    const id = createSection("identifiant")
    id.value = "Identifiant"

    const inputId = createInput(id, 'Identifiant');
    // Set focus on the inputId element
    inputId.focus();

    const buttonDiv = document.createElement('div');
    buttonDiv.style.display = 'flex'; // Set display property to flex

    const button = document.createElement('button')
    button.textContent = "Recherche";
    button.classList.add('button');

    function search() {
        const user_id = inputId.value;
        console.log('launch search request for ID = ', user_id);
        const user_info = checkUser(user_id);
    }

    button.addEventListener('click', search);
    buttonDiv.append(button);
    id.append(buttonDiv);

    // Listen for 'keypress' event on the input field
    inputId.addEventListener('keypress', function (event) {
        // Check if the pressed key is the Enter key (key code 13)
        if (event.keyCode === 13) {
            search();
        }
    });
}