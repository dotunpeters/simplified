"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify, request
from simplified.helpers import parser
from simplified import app, session_data, trendings
from simplified.model import *
import os

#Routes
@app.route('/')
@app.route('/feeds')
def home():
    """Renders the feeds page."""
    year = datetime.now().year
    title="Feeds"
    keywords = "original, jumia, konga"
    description = "Surf through online products from popular eCommerce site in Nigeria with ease."

    #session condition
    if "home" not in session_data:
        session_data["home"] = Products.query.paginate(page=1, per_page=5)

    session["page"] = "home"

    #set products
    products = session_data["home"]
    for each_item in products.items:
        each_item.original = int(float(each_item.stars) * 20)

    #return index template
    return render_template("index.html", year=year, title=title, feeds=products, trends=trendings, keywords=keywords, description=description)


@app.route('/category/<string:cat>')
def category(cat):
    """Renders the category route."""
    year = datetime.now().year
    title = cat.replace("-", " ").capitalize()
    keywords = f"original, {cat}"
    description = f"All original {cat} products on jumia and konga | Surf through online products from popular eCommerce site in Nigeria with ease."

    #get target list category
    cat_checks = title.lower()

    #session condition
    if cat not in session_data:
        session_data[cat] = Products.query.filter_by(category=cat_checks).paginate(page=1, per_page=5)

    session["page"] = cat
    #set products
    products = session_data[cat]
    for each_item in products.items:
        each_item.original = int(float(each_item.stars) * 20)

    #return index template
    return render_template("index.html", year=year, title=title, feeds=products, trends=trendings, keywords=keywords, description=description)


@app.route('/search/<string:category>/<string:query>')
def search(category, query):
    """Renders the search complete route."""
    year = datetime.now().year
    title = f"Search result for '{query}'"
    keywords = f"original, {category}, {query}"
    description = f"All original {query} in {category} on jumia and konga | Surf through online products from popular eCommerce site in Nigeria with ease."

    #query in category
    cat_checks = category.lower()

    #session condition
    if f"{cat_checks}-{query}" not in session_data:
        session_data[f"{cat_checks}-{query}"] = Products.query.filter_by(category=cat_checks).filter(Products.name.ilike(f"%{query}%")).paginate(page=1, per_page=5)

    session["page"] = f"cat-search"
    session_data["query"] = [query, cat_checks]

    #set products
    products = session_data[f"{cat_checks}-{query}"]
    for each_item in products.items:
        each_item.original = int(float(each_item.stars) * 20)

    #return index template
    return render_template("index.html", year=year, title=title, feeds=products, trends=trendings, keywords=keywords, description=description)


@app.route('/search', methods=["GET"])
def search_query():
    """Renders the search complete route."""
    year = datetime.now().year

    #get query
    query = request.args.get("query")
    title = f"Search result for '{query}'"
    keywords = f"original, {query}"
    description = f"All original {query} on jumia and konga | Surf through online products from popular eCommerce site in Nigeria with ease."

    #session condition
    if query not in session_data:
        session_data[query] = Products.query.filter(Products.name.ilike(f"%{query}%")).paginate(page=1, per_page=5)
        
    session["page"] = "search"
    session_data["query"] = query

    #set products
    products = session_data[query]
    for each_item in products.items:
        each_item.original = int(float(each_item.stars) * 20)

    #render template
    return render_template("index.html", year=year, title=title, feeds=products, trends=trendings, keywords=keywords, description=description)


@app.route('/share/<string:sku>')
def share(sku):
    """Renders the category api."""
    year = datetime.now().year

    #get target product
    try:
        products = Products.query.filter(Products.sku == sku).all()
        for each in products:
            title = each.name
            keywords = f"original, {each.name}"
            description = f"Original {each.name} on simplified | Surf through online products from popular eCommerce site in Nigeria with ease."
            break
    except:
        title = "Item not found"
        keywords = f"original"
        description = f"Original product on simplified | Surf through online products from popular eCommerce site in Nigeria with ease."
    
    session["page"] = None

    for each_item in products:
        each_item.original = int(float(each_item.stars) * 20)

    #render template
    return render_template("indexparse.html", year=year, title=title, feeds=products, trends=trendings, keywords=keywords, description=description)


@app.route('/favourites/<string:favlist>', methods=["GET"])
def favourites(favlist):
    """Renders the favourites template."""
    year = datetime.now().year
    title="Favourite items"
    keywords = f"favourite, products, original, jumia, konga"
    description = f"Original product on simplified | Surf through online products from popular eCommerce site in Nigeria with ease."

    #session condition
    if session["page"] != "favourite":
        favlist = favlist.split(",")
        favlist = favlist[1:]

        #get each sku from feeds
        products = []
        for each in favlist:
            try:
                results = Products.query.filter(Products.sku == each).all()
            except:
                continue
            try:
                if (results[0] == None):
                    continue
            except:
                continue
            products.append(results[0])

        session["page"] = None

    for each_item in products:
        each_item.original = int(float(each_item.stars) * 20)

    #render template
    return render_template("indexparse.html", year=year, title=title, feeds=products, trends=trendings, keywords=keywords, description=description)

#route for more...
@app.route('/more', methods=["POST"])
def more():
    page = int(request.form.get("page"))

    #testing
    if request.form.get("test"):
        session["page"] = request.form.get("test")
        if request.form.get("query"):
            if request.form.get("test") == "search":
                session_data["query"] = request.form.get("query")   
            if request.form.get("test") == "cat-search":
                session_data["query"] = request.form.get("query").split(",")

    try:
        #render home json route
        if session["page"] == "home":
            render = Products.query.paginate(page=page, per_page=2)
            products = parser(render)
            return jsonify(products)

        #render category json route
        if session["page"] in ["computing", "electronics", "fashion", "health-and-beauty", "home-and-office", "phones-and-tablets"]:
            categ = session["page"].replace("-", " ").lower()
            render = Products.query.filter_by(category=categ).paginate(page=page, per_page=2)
            products = parser(render)
            categ = categ.replace(" ", "-").lower()
            return jsonify(products)

        #render search json route
        if session["page"] == "search":
            query = session_data["query"]
            render = Products.query.filter(Products.name.ilike(f"%{query}%")).paginate(page=page, per_page=2)
            products = parser(render)
            return jsonify(products)

        #render category search json route
        if session["page"] == "cat-search":
            query = session_data["query"][0]
            cat_checks = session_data["query"][1]
            render = Products.query.filter_by(category=cat_checks).filter(Products.name.ilike(f"%{query}%")).paginate(page=page, per_page=2)
            products = parser(render)
            return jsonify(products)

    except Exception as e:
        return jsonify([{'success': False}])

    return jsonify([{'success': False}])
        

#handle server errors
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)