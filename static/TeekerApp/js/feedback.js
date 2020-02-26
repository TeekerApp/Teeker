// Javascript for FeeedBack page

document.addEventListener("DOMContentLoaded", () => {
	// Used to check if the subject are letters & spaces only
    document.querySelector("#widgetu1541_input").onchange = () => {
        if (document.querySelector("#widgetu1541_input").value.match(/^[A-Za-z0-9\s]+$/)) {
            document.querySelector("#u1542-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u1542-4").style.borderColor = "red"; // Turn the field borders color red
        }
	}
	// Used to check if the message are letters & spaces only
    document.querySelector("#widgetu1551_input").onchange = () => {
        if (document.querySelector("#widgetu1551_input").value.match(/^[A-Za-z0-9\s]+$/)) {
            document.querySelector("#u1552-4").style.borderColor = "green"; // Turn the field borders color green
        } else {
            document.querySelector("#u1552-4").style.borderColor = "red"; // Turn the field borders color red
        }
    }
})