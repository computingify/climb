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

    const searchSec = createSection("searchBt")
    searchSec.value = "searchBt"

    const button = document.createElement('button')
    button.textContent = "search";
    button.classList.add('button');

    button.addEventListener('click', function () {
        const user_id = inputId.value
        console.log('launch search request for ID = ', user_id)
        const user_info = checkUser(user_id)


    });
    searchSec.append(button);
}