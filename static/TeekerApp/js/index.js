// Javascript for index page

let page_completed_loading = setInterval(() => {
	if (document.readyState === "complete") {
		clearInterval(page_completed_loading);
		document.querySelector("#loading_gif_1u").style.display = "None";
	}
}, 100);
