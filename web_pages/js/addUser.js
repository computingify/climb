export default addUserForm

function addUserForm() {
  var form = document.createElement('form');

  // Create the label and input elements for FirstName
  createFirstName(form);

  // Create the label and input elements for LastName
  createLastName(form);
  
  // Create the label and input elements for email
  createEmail(form);

  // Create the label element for "Birth Date"
  createBirthDate(form);

  // Create the submit input element
  var inputSubmit = document.createElement('input');
  inputSubmit.type = 'submit';
  inputSubmit.value = 'Submit';

  var buttonContainer = document.createElement('div');
  buttonContainer.style.position = 'relative';
  buttonContainer.appendChild(inputSubmit);
  // Append the buttonContainer to the document body
  document.body.appendChild(form);
  document.body.appendChild(buttonContainer);

  // Add an event listener to the form to handle the submit event
  document.addEventListener('submit', function(event) {
    console.print('IN send data to server');
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

function createFirstName(form) {
  var labelFirstName = document.createElement('label');
  labelFirstName.for = 'FirstName';
  labelFirstName.textContent = 'Prenom:';
  var inputFirstName = document.createElement('input');
  inputFirstName.type = 'text';
  inputFirstName.id = 'FirstName';
  inputFirstName.name = 'FirstName';
  inputFirstName.required = true;

  var firstNameContainer = document.createElement('div');
  firstNameContainer.style.position = 'relative';
  firstNameContainer.appendChild(labelFirstName);
  firstNameContainer.appendChild(inputFirstName);
  // Append the firstNameContainer to the document body
  form.appendChild(firstNameContainer);
}

function createLastName(form) {
  var labelLastName = document.createElement('label');
  labelLastName.for = 'LastName';
  labelLastName.textContent = 'Nom:';
  var inputLastName = document.createElement('input');
  inputLastName.type = 'text';
  inputLastName.id = 'LastName';
  inputLastName.name = 'LastName';
  inputLastName.required = true;
    
  var lastNameContainer = document.createElement('div');
  lastNameContainer.style.position = 'relative';
  lastNameContainer.appendChild(labelLastName);
  lastNameContainer.appendChild(inputLastName);
  // Append the lastNameContainer to the document body
  form.appendChild(lastNameContainer);
}

function createEmail(form) {
  var labelEmail = document.createElement('label');
  labelEmail.for = 'email';
  labelEmail.textContent = 'Email:';
  var inputEmail = document.createElement('input');
  inputEmail.type = 'email';
  inputEmail.id = 'email';
  inputEmail.name = 'email';
    
  var emailContainer = document.createElement('div');
  emailContainer.style.position = 'relative';
  emailContainer.appendChild(labelEmail);
  emailContainer.appendChild(inputEmail);
  // Append the emailContainer to the document body
  form.appendChild(emailContainer);
}

function createBirthDate(form) {
  var labelBirthDate = document.createElement('label');
  labelBirthDate.for = 'BirthDate';
  labelBirthDate.textContent = 'Date de naissance:';

  // Create the input element for "Birth Date"
  var inputBirthDate = document.createElement('input');
  inputBirthDate.type = 'text';
  inputBirthDate.setAttribute('data-target', '#birthdate');
  inputBirthDate.name = 'BirthDate';
  
  // Create a container element with a relative position
  var birthDatecontainer = document.createElement('div');
  birthDatecontainer.style.position = 'relative';
  birthDatecontainer.appendChild(labelBirthDate);
  birthDatecontainer.appendChild(inputBirthDate);
  // Append the birthDatecontainer to the document body
  form.appendChild(birthDatecontainer);

  // Add an event listener to the inputBirthDate element to open the calendar when clicked
  inputBirthDate.addEventListener('click', function() {
    console.log('CLIC on inputBirthDate');
    // Initialize the Tempus Dominus calendar
    $(inputBirthDate).datetimepicker('show');
  });
  
//  document.addEventListener('click', function(event) {
//  if (event.target !== inputBirthDate && !inputBirthDate.contains(event.target)) {
//      // Clicked outside of the input element
//      console.log('Clicked outside of the input element');
//      $(inputBirthDate).datetimepicker('hide');
//    }
//  });

}

$(document).ready(function() {
  $('#birthdate').datetimepicker({
      format: 'YYYY-MM-DD', // Set the desired date format
      viewMode: 'years',
      showClear: true,
      showClose: true,
      icons: {
          time: 'fa fa-clock-o', // Set the icon for the time picker
          date: 'fa fa-calendar', // Set the icon for the date picker
          up: 'fa fa-chevron-up', // Set the icon for the up button
          down: 'fa fa-chevron-down', // Set the icon for the down button
          previous: 'fa fa-chevron-left', // Set the icon for the previous month button
          next: 'fa fa-chevron-right', // Set the icon for the next month button
          clear: 'fa fa-trash', // Set the icon for the clear button
          close: 'fa fa-times' // Set the icon for the close button
      }
  });
});