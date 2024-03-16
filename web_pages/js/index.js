
import addUserForm from '/js/addUser.js'
import createSection from '/js/createSection.js'
import sessionPage from '/js/session.js'
// import createUserForm from '/js/test.js'

document.addEventListener(
  'DOMContentLoaded', // permet de s'assurer que la page est totalement construite avant de lancer l'execution de ce fichier, évite ainsi l'ajout d'element au html alors qu'il n'est pas terminé de construire
  async function () {
    console.log('LOADING');

    const addUser = createSection("addUser");
    addUser.value = 'Add user';

    const button = document.createElement('button')
    button.textContent = "Add User";
    button.classList.add('button');

    button.addEventListener('click', function () {
      console.log('Launch Add user page')
      addUserForm();
    });
    addUser.append(button);

    const session = createSection("session");
    session.value = 'session';

    const buttonSession = document.createElement('button')
    buttonSession.textContent = "Session";
    buttonSession.classList.add('buttonSession');

    buttonSession.addEventListener('click', function () {
      console.log('Launch Session page');
      sessionPage();
    });
    session.append(buttonSession);

  },
  { once: true },
);