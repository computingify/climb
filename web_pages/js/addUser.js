export default createUserForm

function createUserForm() {
  // Create the form element
  var form = document.createElement('form');

  // Create the label and input elements for FirstName
  var labelFirstName = document.createElement('label');
  labelFirstName.for = 'FirstName';
  labelFirstName.textContent = 'Prenon:';
  var inputFirstName = document.createElement('input');
  inputFirstName.type = 'text';
  inputFirstName.id = 'FirstName';
  inputFirstName.name = 'FirstName';
  inputFirstName.required = true;

  // Create the label and input elements for LastName
  var labelLastName = document.createElement('label');
  labelLastName.for = 'LastName';
  labelLastName.textContent = 'Nom:';
  var inputLastName = document.createElement('input');
  inputLastName.type = 'text';
  inputLastName.id = 'LastName';
  inputLastName.name = 'LastName';
  inputLastName.required = true;
  
  // Create the label and input elements for BirthDate
  var labelBirthDate = document.createElement('label');
  labelBirthDate.for = 'BirthDate';
  labelBirthDate.textContent = 'Date de naissance:';
  var inputBirthDate = document.createElement('input');
  inputBirthDate.type = 'date';
  inputBirthDate.id = 'BirthDate';
  inputBirthDate.min = '1945-01-01';
  inputBirthDate.name = 'BirthDate';

  // Create the label and input elements for email
  var labelEmail = document.createElement('label');
  labelEmail.for = 'email';
  labelEmail.textContent = 'Email:';
  var inputEmail = document.createElement('input');
  inputEmail.type = 'email';
  inputEmail.id = 'email';
  inputEmail.name = 'email';

  // Create the submit input element
  var inputSubmit = document.createElement('input');
  inputSubmit.type = 'submit';
  inputSubmit.value = 'Submit';

  // Append the elements to the form
  form.appendChild(labelFirstName);
  form.appendChild(inputFirstName);
  form.appendChild(labelLastName);
  form.appendChild(inputLastName);
  form.appendChild(labelBirthDate);
  form.appendChild(inputBirthDate);
  form.appendChild(labelEmail);
  form.appendChild(inputEmail);
  form.appendChild(inputSubmit);

  // Append the form to the document body
  document.body.appendChild(form);

  // Add an event listener to the form to handle the submit event
  form.addEventListener('submit', function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the values entered by the user
    var firstName = inputFirstName.value;
    var lastName = inputLastName.value;
    var birthDate = inputBirthDate.value;
    var email = inputEmail.value;

    // Create a FormData object to store the form data
    var formData = new FormData();
    formData.append('FirstName', firstName);
    formData.append('LastName', lastName);
    formData.append('BirthDate', birthDate);
    formData.append('email', email);

    console.log('form information', formData);

    // Create the fetch options
    var options = {
      method: 'POST',
      body: formData,
    };

    // Log the form data
    console.log('form information:');
    for (var pair of formData.entries()) {
      console.log(pair[0] + ': ' + pair[1]);
    }
    
    // Send the POST request
    fetch('http://127.0.0.1:5000/api/v1/resources/user', options)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error('Server responded with error status:', error.response.status);
          console.error('Response data:', error.response.data);
        } else if (error.request) {
            // The request was made but no response was received
            console.error('No response received from server');
        } else {
            // Something happened in setting up the request that triggered an Error
            console.error('Error setting up request:', error.message);
      }
      });
    });
}
