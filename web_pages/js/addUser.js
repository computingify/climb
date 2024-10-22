import { SERVER_URL } from '/js/config.js';

export default addUserForm;

function addUserForm() {
  const body = document.body;
  body.innerHTML = ''; // Clear existing content

  console.log("Run addUserForm");
  const form = document.createElement('form');

  // Create form fields
  const inputFirstName = createInputField(form, 'FirstName', 'Prenom:', 'text', true);
  const inputLastName = createInputField(form, 'LastName', 'Nom:', 'text', true);
  const inputEmail = createInputField(form, 'email', 'Email:', 'email');
  const inputBirthDate = createInputField(form, 'BirthDate-input', 'Date de naissance:', 'text', false, 'form-control BirthDate-input');
  const inputSubmit = createSubmitButton(form);

  // Append the form to the document body
  body.appendChild(form);

  // Initialize Tempus Dominus datetimepicker
  initDateTimePicker();

  // Handle form events
  handleFormEvents(inputFirstName, inputLastName, inputEmail, inputBirthDate, inputSubmit);
}

function createInputField(form, id, labelText, type, required = false, className = '') {
  const label = document.createElement('label');
  label.for = id;
  label.textContent = labelText;

  const input = document.createElement('input');
  input.type = type;
  input.id = id;
  input.name = id;
  input.required = required;
  if (className) {
    input.className = className;
  }

  const container = document.createElement('div');
  container.style.position = 'relative';
  container.appendChild(label);
  container.appendChild(input);

  form.appendChild(container);
  return input;
}

function createSubmitButton(form) {
  const inputSubmit = document.createElement('input');
  inputSubmit.type = 'submit';
  inputSubmit.value = 'Submit';

  const container = document.createElement('div');
  container.style.position = 'relative';
  container.appendChild(inputSubmit);

  form.appendChild(container);
  return inputSubmit;
}

function initDateTimePicker() {
  $(document).ready(() => {
    $('#BirthDate-input').datetimepicker({
      format: 'YYYY-MM-DD',
      viewMode: 'years',
      showClear: true,
      showClose: true,
      icons: {
        date: 'fa fa-calendar',
        up: 'fa fa-chevron-up',
        down: 'fa fa-chevron-down',
        previous: 'fa fa-chevron-left',
        next: 'fa fa-chevron-right',
        clear: 'fa fa-trash',
        close: 'fa fa-times'
      }
    });
  });
}

function handleFormEvents(inputFirstName, inputLastName, inputEmail, inputBirthDate, inputSubmit) {
  document.addEventListener('click', (event) => {
    event.preventDefault();

    // Calendar box management
    if (event.target === inputBirthDate) {
      console.log('CLIC on inputBirthDate');
      $(inputBirthDate).datetimepicker('show');
    } else {
      $(inputBirthDate).datetimepicker('hide');
    }

    // Handle form submission
    if (event.target === inputSubmit) {
      console.log('Sending data to server');
      event.preventDefault();
      sendDataToServer(inputFirstName.value, inputLastName.value, inputBirthDate.value, inputEmail.value);
    }
  });
}

function sendDataToServer(firstName, lastName, birthDate, email) {
  const formData = new FormData();
  formData.append('FirstName', firstName);
  formData.append('LastName', lastName);
  formData.append('BirthDate', birthDate);
  formData.append('email', email);

  console.log('Form data:', Array.from(formData.entries()));

  const options = {
    method: 'POST',
    body: formData
  };

  fetch(`${SERVER_URL}/user`, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Server response:', data);
    })
    .catch(error => {
      console.error('Error occurred:', error.message);
    });
}
