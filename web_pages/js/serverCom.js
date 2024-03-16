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
        return data
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors
    });
}

function addUserToSession(id){

}