
import addUserForm from '/js/addUser.js'

document.addEventListener(
  'DOMContentLoaded', // permet de s'assurer que la page est totalement construite avant de lancer l'execution de ce fichier, évite ainsi l'ajout d'element au html alors qu'il n'est pas terminé de construire
  async function () {
    console.log('LOADING');

    addUserForm();
  },
  { once: true },
);
