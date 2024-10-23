export default { checkUser, addUserToSession }

import { SERVER_URL } from '/js/config.js';

function checkUser(input) {
    const url = new URL(`${SERVER_URL}/user`);
    let params;

    // Check if the input is an integer (Id) or a string (FirstName LastName)
    if (!isNaN(input) && Number.isInteger(parseFloat(input))) {
        // Input is an ID
        params = { Id: parseInt(input) }; // Ensure it's sent as an integer
    } else if (input.includes(' ')) {
        // Input contains a first and last name
        const [firstName, lastName] = input.split(' ');
        params = { FirstName: firstName, LastName: lastName };
    } else {
        console.error('Invalid input. Please provide a valid ID or FirstName LastName.');
        return; // Exit the function if the input is invalid
    }

    url.search = new URLSearchParams(params).toString();

    // Send the GET request
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            // Handle the response data
            displayUserData(data);
            return data;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Handle errors
        });
}

function displayUserData(userData) {
    // Remove any existing user data container
    const existingContainer = document.querySelector('.user-data-container');
    if (existingContainer) {
        existingContainer.remove();
    }

    // Create a container div to hold the user data
    const container = document.createElement('div');
    container.classList.add('user-data-container');

    // Create and style elements for first name and last name
    const firstNameElement = document.createElement('p');
    firstNameElement.textContent = `Participant: ${userData.first_name} ${userData.last_name}`;
    firstNameElement.classList.add('user-data-item');

    // Append first name and last name elements to the container
    container.appendChild(firstNameElement);

    // Append the container to the document body or any other container element
    document.body.appendChild(container);

    // Valid button part
    const buttonValid = document.createElement('button');
    buttonValid.textContent = "Valid";
    buttonValid.classList.add('button');

    buttonValid.addEventListener('click', () => addUserToSession(userData.id, container));

    container.append(buttonValid);
}

function addUserToSession(id, container) {
    console.log("Push Valid button");
    const url = new URL(`${SERVER_URL}/session/add_user`);
    const params = { UserId: id };
    url.search = new URLSearchParams(params).toString();

    // Options for the fetch call
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Specify the content type as JSON
        }
    };

    // Send the POST request
    fetch(url, options)
        .then(response => {
            if (response.ok) {
                // If the response status is 200, set background to green
                container.style.backgroundColor = 'green';

                // Create and append the success message
                const successMessage = document.createElement('p');
                successMessage.textContent = "Bonne grimpe";
                successMessage.style.fontWeight = 'bold'; // Make the text bold
                successMessage.style.color = 'white'; // Optional: Change the text color
                container.appendChild(successMessage);

                // Update climber count after adding a user
                const event = new CustomEvent('climberCountUpdated');
                document.dispatchEvent(event); // Dispatch the event here

                // Remove the container after 3 seconds
                setTimeout(() => {
                    container.remove();
                }, 3000);
            } else {
                // If the response status is not 200, set background to red
                container.style.backgroundColor = 'red';
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            return data;
        })
        .catch(error => {
            // Handle errors
            container.style.backgroundColor = 'red';
            console.error('There was a problem with the fetch operation:', error);
        });
}
