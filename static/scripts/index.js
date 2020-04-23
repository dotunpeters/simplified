
document.addEventListener("DOMContentLoaded", main);

function main() {

	//update favourite link href attribute when document loaded
	if (localStorage.getItem('favourite')) {
		var temp = localStorage.getItem('favourite');
		temp = temp.split(",");

		//update favourite counter
		document.querySelector("#favcounter").innerHTML = temp.length - 1;

		if (temp[1] === undefined) {
			document.querySelector("#favlink").removeAttribute("href");
		}
		else {
			document.querySelector("#favlink").setAttribute("href", `/favourites/${temp}`);
		}
	} else {
		document.querySelector("#favcounter").innerHTML = 0;
	}

	//update favourite icon for each item
	document.querySelectorAll(".fav").forEach((each) => {
		if (temp !== undefined) {
			if (temp.includes(each.dataset.sku)) {
				each.innerHTML = "&#10084;";
			} else {
				each.innerHTML = "&#9825;";
			}
		}

	});


	//share product
	const share = document.querySelectorAll(".share");
	share.forEach((each) => {
		each.addEventListener("click", () => {
			//close posibly open price_list popup
			document.querySelector('#more_pop').style.display = "none";

			const sku = each.dataset.share;
			const link = `${window.location.protocol}//${document.location.host}/share/${sku}`; 
			const name = each.dataset.name;
			const twitter = "https://twitter.com/intent/tweet?hashtags=simplified&ref_src=twsrc%5Etfw&text=" + name + "&tw_p=tweetbutton&url=" + link;
			const data = [{ "name": name, "link": link, "twitter": twitter}];

			//compile handlebars for search
			const share_template = Handlebars.compile(document.querySelector('#share-template').innerHTML);

			//add content to feeds element
			const content = share_template({'share_catalog': data});

			//share_pop display
			document.querySelector('#share_pop').innerHTML = content;
			document.querySelector("#share_pop").style.top = `${window.innerHeight / 2 - 50}px`;
			document.querySelector("#share_pop").style.left = `${window.innerWidth / 2 - 130}px`;

			document.querySelector('#share_pop').style.display = "block";
			document.querySelector('#twitz').style.display = "block";

			//close
			document.querySelector("#close").addEventListener("click", () => {
				document.querySelector('#share_pop').style.display = "none";
				document.querySelector('#more_pop').style.display = "none";
			});

			//copy link
			document.querySelector("#copy").addEventListener("click", () => {
				/* Get the text field */
				let copyText = document.querySelector("#text");

				/* Select the text field */
				copyText.select();
				copyText.setSelectionRange(0, 99999); /*For mobile devices*/

				/* Copy the text inside the text field */
				document.execCommand("copy");

				/* Alert the copied text */
				document.querySelector("#copy").innerHTML = "Copied!";
			});

		});
	});

	//more popup
	const prices = document.querySelectorAll(".graph");
	prices.forEach((each) => {
		each.addEventListener("click", () => {

			//close possibly open share popup
			document.querySelector('#share_pop').style.display = "none";

			const more = each.dataset.more;
			
			//compile handlebars for more
			const more_template = Handlebars.compile(document.querySelector('#more-template').innerHTML);

			//add content to feeds element
			const content = more_template({ 'more_catalog': { 'more': more } });

			//more display
			document.querySelector('#more_pop').innerHTML = content;

			document.querySelector("#more_pop").style.top = `${window.innerHeight / 2 - 100}px`;
			document.querySelector("#more_pop").style.left = `${window.innerWidth / 2 - 130}px`;
			document.querySelector('#more_pop').style.display = "block";

			//close
			document.querySelector("#close2").addEventListener("click", () => {
				document.querySelector('#more_pop').style.display = "none";
				document.querySelector('#share_pop').style.display = "none";
			});

		});
	});

	//favourite feature
	const favourite = document.querySelectorAll(".fav");
	favourite.forEach((each) => {
		each.addEventListener("click", () => {
			//initialize favourite localStorage
			let list = [];
			if (!localStorage.getItem('favourite')) {
				localStorage.setItem('favourite', list);
			}

			let temp = localStorage.getItem('favourite');
			temp = temp.split(",");
			const sku = each.dataset.sku;

			if (!temp.includes(sku)) {

				//update localStorage
				temp.push(sku);

				//reset local storage
				localStorage.setItem('favourite', temp);

				//update favourite counter
				document.querySelector("#favcounter").innerHTML = temp.length - 1;

				//update favourite link href attribute
				document.querySelector("#favlink").setAttribute("href", `/favourites/${temp}`);
				
				//change favourite icon
				each.innerHTML = "&#10084;";
			}
			else {

				//remove sku from localStorage
				const index = temp.indexOf(sku);
				if (index > -1) {
					temp.splice(index, 1);
				}

				//reset local storage
				localStorage.setItem('favourite', temp);

				//update favoutite counter
				document.querySelector("#favcounter").innerHTML = temp.length - 1;

				//update favourite link href attribute
				if (temp[1] === undefined) {
					document.querySelector("#favlink").removeAttribute("href");
				}
				else {
					document.querySelector("#favlink").setAttribute("href", `/favourites/${temp}`);
				}

				//change favourite icon
				each.innerHTML = "&#9825;";
			}

		});
	});

	//mobile responsiveness
	if (window.innerWidth <= 500) {
		document.querySelector(".col-1index").style.maxWidth = `${window.innerWidth}px`;
		document.querySelector(".articles").style.maxWidth = `${window.innerWidth}px`;
		document.querySelector(".product_image").style.maxWidth = `${window.innerWidth}px`;
		document.querySelector(".product_details").style.maxWidth = `${window.innerWidth}px`;
	}
}