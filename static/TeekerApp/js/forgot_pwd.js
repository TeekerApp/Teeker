// Javascript for Forgot Password Page

document.addEventListener("DOMContentLoaded", () => {

	// Used to check password and confirm password
    document.querySelector("#pwd").onchange = () => {
        if (document.querySelector("#pwd").value.length > 7 && document.querySelector("#pwd").value.length < 65) {
            document.querySelector("#pwd").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#pwd").style.borderColor = "red"; // Turn the field borders color red
        }
    }
    document.querySelector("#cpwd").onchange = () => {
        if (document.querySelector("#cpwd").value.length > 7 && document.querySelector("#cpwd").value.length < 65 &&
        document.querySelector("#pwd").value.length > 7 && document.querySelector("#pwd").value.length < 65 &&
        document.querySelector("#pwd").value === document.querySelector("#cpwd").value) {
            document.querySelector("#pwd").style.borderColor = "green"; // Turn the field borders color green
            document.querySelector("#cpwd").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#pwd").style.borderColor = "red"; // Turn the field borders color red
            document.querySelector("#cpwd").style.borderColor = "red"; // Turn the field borders color red
        }
    }
});
