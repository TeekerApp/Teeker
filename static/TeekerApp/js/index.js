// Javascript for index page

var screen_width = (screen.width / 2) - 15;
// Used for the loading gif styling to position it in the right place
if (screen.width === 320) {
	setTimeout(()=>{
		document.querySelector("#loading_gif_1u").style.width = "20%";
		document.querySelector("#loading_gif_1u").style.marginTop = "50%";
		document.querySelector("#loading_gif_1u").style.marginLeft = screen_width+"px";
	}, 50);
} else if (screen.width > 320 && screen.width <= 380) {
	setTimeout(()=>{
		document.querySelector("#loading_gif_1u").style.width = "20%";
		document.querySelector("#loading_gif_1u").style.marginTop = "50%";
		document.querySelector("#loading_gif_1u").style.marginLeft = screen_width+"px";
	}, 50);
} else if (screen.width > 380 && screen.width <= 480) {
	setTimeout(()=>{
		document.querySelector("#loading_gif_1u").style.width = "20%";
		document.querySelector("#loading_gif_1u").style.marginTop = "50%";
		document.querySelector("#loading_gif_1u").style.marginLeft = screen_width+"px";
	}, 50);
} else {
	setTimeout(()=>{
		document.querySelector("#loading_gif_1u").style.width = "5%";
		document.querySelector("#loading_gif_1u").style.marginTop = "5%";
		document.querySelector("#loading_gif_1u").style.marginLeft = "45%";
	}, 50);
}

// Used to hide the content will it loads till its ready to display
let page_completed_loading = setInterval(() => {
	document.querySelector("#page").style.display = "None";
	if (document.readyState === "complete") {
		clearInterval(page_completed_loading);
		document.querySelector("#loading_gif_1u").style.display = "None";
		document.querySelector("#page").style.display = "inline";
	}
}, 100);
