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
const closeButton1 = loginModal.querySelector('.close-button');

const registerButton = document.getElementById('register');
const registerModal = document.getElementById('registerModal');
const closeButton2 = registerModal.querySelector('.close-button');

// Pokazywanie modalu po kliknięciu
signInButton.addEventListener('click', () => {
  loginModal.style.display = 'flex'; // Ustawienie 'flex' pokazuje modal
});

// Ukrywanie modalu po kliknięciu przycisku zamykania
closeButton1.addEventListener('click', () => {
  loginModal.style.display = 'none'; // Ukrycie modalu
});

// Ukrywanie modalu po kliknięciu poza modalem
window.addEventListener('click', (event) => {
  if (event.target === loginModal) {
    loginModal.style.display = 'none'; // Ukrycie modalu
  }
});

registerButton.addEventListener('click', () => {
  loginModal.style.display = 'none';
  registerModal.style.display = 'flex';
})


window.addEventListener('click', (event) => {
  if (event.target === registerModal) {
    registerModal.style.display = 'none'; 
  }
});

// Ukrywanie modalu po kliknięciu przycisku zamykania
closeButton2.addEventListener('click', () => {
  registerModal.style.display = 'none'; // Ukrycie modalu
});