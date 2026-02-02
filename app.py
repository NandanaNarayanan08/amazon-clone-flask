from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -----------------------
# GLOBAL CART
# -----------------------
cart = []

# -----------------------
# PRODUCTS LIST
# images must be inside /static folder
# -----------------------
products = [
    {"name": "iPhone 15", "price": 79999, "img": "images/phone.jpg"},
    {"name": "Laptop", "price": 52000, "img": "images/laptop.jpg"},
    {"name": "Headphones", "price": 1999, "img": "images/headphones.jpg"},
    {"name": "Smart Watch", "price": 2499, "img": "images/watch.jpg"},
]


# -----------------------
# HOME PAGE
# -----------------------
@app.route("/", methods=["GET", "POST"])
def home():
    search = ""

    filtered_products = products

    # search feature
    if request.method == "POST":
        search = request.form.get("search", "").lower()

        if search:
            filtered_products = [
                p for p in products if search in p["name"].lower()
            ]

    # calculate total
    prices = {p["name"]: p["price"] for p in products}
    total = sum(prices.get(item, 0) for item in cart)

    return render_template(
        "index.html",
        products=filtered_products,
        cart=cart,
        total=total,
        cart_count=len(cart)
    )


# -----------------------
# ADD TO CART
# -----------------------
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    name = request.form.get("name")

    if name:
        cart.append(name)

    return redirect(url_for("home"))


# -----------------------
# REMOVE FROM CART
# -----------------------
@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    name = request.form.get("name")

    if name in cart:
        cart.remove(name)

    return redirect(url_for("home"))


# -----------------------
# CLEAR CART
# -----------------------
@app.route("/clear-cart")
def clear_cart():
    cart.clear()
    return redirect(url_for("home"))

@app.route("/checkout")
def checkout():
    prices = {
        "iPhone 15": 79999,
        "Laptop": 52000,
        "Headphones": 1999,
        "Smart Watch": 2499
    }

    purchased_items = cart.copy()   # ✅ save first
    total = sum(prices.get(item, 0) for item in cart)  # ✅ calculate

    cart.clear()   # ✅ clear AFTER

    return render_template(
        "checkout.html",
        items=purchased_items,
        total=total
    )


# -----------------------
# RUN SERVER
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)