export default {checkUser, addUserToSession}

function checkUser(id) {
    const url = new URL('http://127.0.0.1:5000/api/v1/resources/user');
    const params = { Id: id };
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
        return data
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors
    });
}

function displayUserData(userData) {
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
    const buttonValid = document.createElement('button')
    buttonValid.textContent = "Valid";
    // buttonValid.classList.add('button');

    buttonValid.addEventListener('click', addUserToSession(userData.id));
    container.append(buttonValid);
}

function addUserToSession(id){
    console.log("Push Valid button");
    const url = new URL('http://127.0.0.1:5000/api/v1/resources/session/add_user');
    const params = { UserId: id };
    url.search = new URLSearchParams(params).toString();

    // Options for the fetch call
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Specify the content type as JSON
        }
    };

    // Send the GET request
    fetch(url, options)
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        // Handle the response data
        
        return data
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors
    });
}