function getChain() {
    window.location.href = "/get_chain";
}
function get_block_form() {
    window.location.href = "/get_block_form";
}
function patientForm() {
    window.location.href = "/patient_form";
}
function index() {
    window.location.href = "/";
}

// Elementy do kontrolowania modalu
const signInButton = document.getElementById('signInButton');
const loginModal = document.getElementById('loginModal');
const closeButton = loginModal.querySelector('.close-button');

// Pokazywanie modalu po kliknięciu
signInButton.addEventListener('click', function() {
  loginModal.style.display = 'flex'; // Ustawienie 'flex' pokazuje modal
});

// Ukrywanie modalu po kliknięciu przycisku zamykania
closeButton.addEventListener('click', function() {
  loginModal.style.display = 'none'; // Ukrycie modalu
});

// Ukrywanie modalu po kliknięciu poza modalem
window.addEventListener('click', function(event) {
  if (event.target === loginModal) {
    loginModal.style.display = 'none'; // Ukrycie modalu
  }
});