// redirections
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

// handlers
const signInButton = document.getElementById('signInButton');
const loginModal = document.getElementById('loginModal');
const closeButton1 = loginModal.querySelector('.close-button');

const registerButton = document.getElementById('register');
const registerModal = document.getElementById('registerModal');
const closeButton2 = registerModal.querySelector('.close-button');

// showing modal while click event
signInButton.addEventListener('click', () => {
  loginModal.style.display = 'flex'; 
});

// hiding login modal while 'x' click event
closeButton1.addEventListener('click', () => {
  loginModal.style.display = 'none'; 
});

// hiding login modal while click event out of modal
window.addEventListener('click', (event) => {
  if (event.target === loginModal) {
    loginModal.style.display = 'none'; 
  }
});

// changing login modal to register modal while click evet on register button
registerButton.addEventListener('click', () => {
  loginModal.style.display = 'none';
  registerModal.style.display = 'flex';
})

// hiding register modal while click event out of modal
window.addEventListener('click', (event) => {
  if (event.target === registerModal) {
    registerModal.style.display = 'none'; 
  }
});

// hiding register modal while 'x' click event
closeButton2.addEventListener('click', () => {
  registerModal.style.display = 'none'; // Ukrycie modalu
});

//register password validation
const form = document.getElementById('registerModal-form');
const passwordInput = document.getElementById('new_password');
const rePasswordInput = document.getElementById('re-new_password');

form.addEventListener('submit', (event) => {
    if (passwordInput.value !== rePasswordInput.value) {
        // while passwords are not the same, we're showing information in alertbox
        event.preventDefault();
        alert("Passwords do not match. Please try again.");
    }
    if(passwordInput.value.length < 5) {
        event.preventDefault();
        alert("Password too short. Try longer password.");
    }
});