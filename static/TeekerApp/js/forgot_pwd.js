// Javascript for Forgot Password Page

document.addEventListener("DOMContentLoaded", () => {

	// Used to check password and confirm password
    document.querySelector("#pwd").onchange = () => {
        if (document.querySelector("#pwd").value.length > 7 && document.querySelector("#pwd").value.length < 65) {
            document.querySelector("#u1306-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u1306-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }
    document.querySelector("#cpwd").onchange = () => {
        if (document.querySelector("#cpwd").value.length > 7 && document.querySelector("#cpwd").value.length < 65 &&
        document.querySelector("#pwd").value.length > 7 && document.querySelector("#pwd").value.length < 65 &&
        document.querySelector("#pwd").value === document.querySelector("#cpwd").value) {
            document.querySelector("#u1306-4").style.borderColor = "green"; // Turn the field borders color green
            document.querySelector("#u1330-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u1306-4").style.borderColor = "red"; // Turn the field borders color red
            document.querySelector("#u1330-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }
});
