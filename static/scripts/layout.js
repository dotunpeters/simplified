
document.addEventListener("DOMContentLoaded", main);

//create category list
var category_list = ["Computing", "Electronics", "Fashion", "Health And Beauty", "Home And Office", "Phones And Tablets"];

function main() {

    let menuStatus = true;

    //closed all open dropdowns on clicked out
    const out1 = document.querySelectorAll(".col-1");
    const out2 = document.querySelectorAll(".container2");
    const out3 = document.querySelectorAll(".col-3");
    const list = [out1, out2, out3];
    list.forEach((out) => {
        out.forEach((each) => {
            each.addEventListener("click", () => {
                //close all dropdowns
                document.querySelector('#category').innerHTML = "&#9776;";
                document.querySelector('#catmenu').innerHTML = "";
                document.querySelector('#catmenu').style.display = "none";
                document.querySelector('#search_auto').style.display = "none";
                menuStatus = true;
            });
        });
    });

    //add category to menu
    document.querySelector("#category").onclick = () => {

        //compile handlebars for category
        const category_template = Handlebars.compile(document.querySelector('#category-template').innerHTML);

        if (menuStatus === true) {
            values = [];
            category_list.forEach(each => {

                const href = `/category/${each.toLowerCase().replace(" ", "-").replace(" ", "-")}`;
                const sub = { "href": href, "link": each };
                values.push(sub);
                
            });

            const category_content = category_template({ 'category_catalog': values });
            document.querySelector('#catmenu').innerHTML = category_content;

            //add content to catmenu element
            document.querySelector('#catmenu').style.animationName = "open";
            document.querySelector('#catmenu').style.animationPlayState = "running";
            document.querySelector('#catmenu').style.display = "block";
            document.querySelector('#category').innerHTML = "&#9779;";
            menuStatus = false;

        } else {

            //close menu category dropdown
            document.querySelector('#category').innerHTML = "&#9776;";
            document.querySelector('#catmenu').innerHTML = "";
            document.querySelector('#catmenu').style.display = "none";
            menuStatus = true;
        }
    };

    //search autocomplete
    document.querySelector("#search_input").addEventListener("keyup", () => {

        //compile handlebars for search engine
        const search_template = Handlebars.compile(document.querySelector('#search-template').innerHTML);
        let query = document.querySelector("#search_input").value;

        if (query.length >= 2) {

            //clear auto-complete bar
            document.querySelector('#search_auto').innerHTML = "";

            //initialize values
            const values = [];
            category_list.forEach(function (item) {
                const href = `/search/${item}/${query}`;
                const sub = {"query": query, "item": item, "href": href};
                values.push(sub);
            });

            //add content to search_auto element
            const autoserch_content = search_template({'search_catalog': values});
            document.querySelector('#search_auto').innerHTML = autoserch_content;

            //display block
            document.querySelector("#search_auto").style.display = "block";
        }
        else {
            document.querySelector("#search_auto").innerHTML = "";
            document.querySelector("#search_auto").style.display = "none";
        }
    });

    //mobile search
    let status = "closed";
    document.querySelector("#mobile_search").addEventListener("click", () => {
        if (status === "closed") {
            document.querySelector("#search").style.display = "block";
            status = "opened";
        }
        else {
            document.querySelector("#search").style.display = "none";
            status = "closed";
        }        
    });
}