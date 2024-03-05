
import addUserForm from '/js/addUser.js'
// import createUserForm from '/js/test.js'

document.addEventListener(
  'DOMContentLoaded', // permet de s'assurer que la page est totalement construite avant de lancer l'execution de ce fichier, évite ainsi l'ajout d'element au html alors qu'il n'est pas terminé de construire
  async function () {
    console.log('LOADING');
    // $(document).ready(function() {
    //   console.log("INITILIZE Datetimepicker");
    //   $('#birthdate').datetimepicker({
    //       format: 'YYYY-MM-DD', // Set the desired date format
    //       viewMode: 'years',
    //       showClear: true,
    //       showClose: true,
    //       icons: {
    //           time: 'fa fa-clock-o', // Set the icon for the time picker
    //           date: 'fa fa-calendar', // Set the icon for the date picker
    //           up: 'fa fa-chevron-up', // Set the icon for the up button
    //           down: 'fa fa-chevron-down', // Set the icon for the down button
    //           previous: 'fa fa-chevron-left', // Set the icon for the previous month button
    //           next: 'fa fa-chevron-right', // Set the icon for the next month button
    //           clear: 'fa fa-trash', // Set the icon for the clear button
    //           close: 'fa fa-times' // Set the icon for the close button
    //       }
    //   });
    // });

    addUserForm();
    // createUserForm()
  },
  { once: true },
);