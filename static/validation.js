let patientForm = document.querySelector("#patientForm")
let patientName = document.querySelector("#name")
let patientSurname = document.querySelector("#surname")
let patientPesel = document.querySelector("#pesel")
let patientAge = document.querySelector("#age")
let patientCity = document.querySelector("#city")
let template = /^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$/

patientForm.addEventListener("submit", e => {
    if(patientName.value.length > 15 || template.test(patientName.value) == false) {
        e.preventDefault()
        alert("Invalid name")
    }
    if(patientSurname.value.length > 15 || template.test(patientSurname.value) == false) {
        e.preventDefault()
        alert("Invalid surname")
    }
    if(patientAge.value < 1 || patientAge.value > 105) {
        e.preventDefault()
        alert("Invalid age.")
    }
    if(patientCity.value.length > 20 || template.test(patientCity.value) == false) {
        e.preventDefault()
        alert("Unknown city.")
    }
    if(patientPesel.value.length != 11) {
        e.preventDefault()
        alert("Invalid pesel. There MUST BE 11 digits")
    }
})