"""
Routes and views for the flask application.
"""

#import packages
from flask import Flask
from flask_session import Session
from tempfile import mkdtemp
import os

app = Flask(__name__)

#session configuration
app.config["DEBUG"] = True
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#create user session
Session(app)
from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify, request
import os

#models
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    stars = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    seller = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

#database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#fixed trending
with app.app_context():
    session_data = {}
    trendings = Products.query.filter(Products.reviews >= 10).order_by(Products.stars.desc()).limit(5).all()

#Routes
@app.route('/')
@app.route('/feeds')
def home():
    """Renders the feeds page."""
    #manage api error
    session["err_counter"] = 0

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
    #manage api error
    session["err_counter"] = 0

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
    #manage api error
    session["err_counter"] = 0

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
    #manage api error
    session["err_counter"] = 0

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
    #manage api error
    session["err_counter"] = 0

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
    #manage api error
    session["err_counter"] = 0
    
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
            results = Products.query.filter(Products.sku == each).all()
            if (results[0] == None):
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

    def parser(render):
        products = []
        products.append({'success': True})
        for each in render.items:
            dict_each = {}
            dict_each["name"] = each.name
            dict_each["sku"] = each.sku
            dict_each["price"] = each.price
            dict_each["stars"] = each.stars
            dict_each["original"] = int(float(each.stars) * 20)
            dict_each["link"] = each.link
            dict_each["image_url"] = each.image_url
            dict_each["reviews"] = each.reviews
            dict_each["seller"] = each.seller
            dict_each["category"] = each.category
            dict_each["description"] = each.description
            products.append(dict_each)
        return products
    try:
        #render home json route
        if session["page"] == "home":
            render = Products.query.paginate(page=page, per_page=2)
            products = parser(render)
            return jsonify(products)

        #render computing category json route
        if session["page"].lower() == "computing":
            computing_categ = session["page"].lower()
            render = Products.query.filter_by(category=computing_categ).paginate(page=page, per_page=2)
            computing_products = parser(render)
            return jsonify(computing_products)

        #render electronics category json route
        if session["page"].lower() == "electronics":
            electronics_categ = session["page"].lower()
            render = Products.query.filter_by(category=electronics_categ).paginate(page=page, per_page=2)
            electronics_products = parser(render)
            return jsonify(electronics_products)

        #render health-and-beauty category json route
        if session["page"].lower() == "health-and-beauty":
            healthbeauty_categ = session["page"].replace("-", " ").lower()
            render = Products.query.filter_by(category=healthbeauty_categ).paginate(page=page, per_page=2)
            healthbeauty_products = parser(render)
            return jsonify(healthbeauty_products)

        #render fashion category json route
        if session["page"].lower() == "fashion":
            fashion_categ = session["page"].lower()
            render = Products.query.filter_by(category=fashion_categ).paginate(page=page, per_page=2)
            fashion_products = parser(render)
            return jsonify(fashion_products)

        #render home-and-office category json route
        if session["page"].lower() == "home-and-office":
            homeoffice_categ = session["page"].replace("-", " ").lower()
            render = Products.query.filter_by(category=homeoffice_categ).paginate(page=page, per_page=2)
            homeoffice_products = parser(render)
            return jsonify(homeoffice_products)

        #render phones-and-tablets category json route
        if session["page"].lower() == "phones-and-tablets":
            phonestablets_categ = session["page"].replace("-", " ").lower()
            render = Products.query.filter_by(category=phonestablets_categ).paginate(page=page, per_page=2)
            phonestablets_products = parser(render)
            return jsonify(phonestablets_products)

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

        #render none json route
        if session["page"] == None:
            return None

    except:
        session['err_counter'] += 1
        if session['err_counter'] >= 5:
            return jsonify([{'success': False}])
        more()
        

#handle server errors
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("home"))