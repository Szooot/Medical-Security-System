let patientForm = document.querySelector("#patientForm")
let patientName = document.querySelector("#name")
let patientSurname = document.querySelector("#surname")
let patientPesel = document.querySelector("#pesel")
let template = /^[a-zA-Z]+$/


patientForm.addEventListener("submit", e => {
    if(patientName.value.length > 15 || template.test(patientName.value) == false) {
        e.preventDefault()
        alert("Invalid name")
    }
    if(patientSurname.value.length > 15 || template.test(patientSurname.value) == false) {
        e.preventDefault()
        alert("Invalid surname")
    }
    if(patientPesel.value.length != 11) {
        e.preventDefault()
        alert("Invalid pesel. There MUST BE 11 digits")
    }
})