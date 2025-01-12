import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query database for user's cash
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Query database for user's stocks
    stocks = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)

    # Get current stock prices and total value
    holdings = []
    total_value = cash
    for stock in stocks:
        quote = lookup(stock["symbol"])
        holdings.append({
            "symbol": stock["symbol"],
            "name": quote["name"],
            "shares": stock["shares"],
            "price": usd(quote["price"]),
            "total": usd(quote["price"] * stock["shares"])
        })
        total_value += quote["price"] * stock["shares"]

    return render_template("index.html", cash=usd(cash), holdings=holdings, total=usd(total_value))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate symbol
        if not symbol:
            return apology("must provide symbol", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        # Validate shares
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide valid number of shares", 400)
        shares = int(shares)

        # Check user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        cost = quote["price"] * shares
        if cash < cost:
            return apology("can't afford", 400)

        # Perform transaction
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
                   session["user_id"], symbol, shares, quote["price"])

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    # Fetch user's transaction history
    transactions = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ?", user_id)

    # Process each transaction for display
    for transaction in transactions:
        # Ensure price is a numeric value
        price = transaction["price"]
        shares = transaction["shares"]

        # Format the price in USD format
        transaction["price"] = usd(price)

        # Calculate the total correctly using the absolute value of shares
        total_value = abs(shares) * price
        transaction["total"] = usd(total_value)

        # Determine the transaction type and ensure shares is displayed as an absolute value
        transaction["transaction_type"] = "Buy" if shares > 0 else "Sell"
        transaction["shares"] = abs(shares)

    return render_template("history.html", transactions=transactions)









@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")

        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate submission
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must provide confirmation", 400)
        if password != confirmation:
            return apology("passwords don't match", 400)

        # Hash password
        hash = generate_password_hash(password)

        # Check if username already exists
        try:
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        except ValueError:
            return apology("username already exists", 400)

        # Log user in by remembering user id
        session["user_id"] = new_user_id

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to user account"""
    if request.method == "POST":
        amount = request.form.get("amount")

        # Validate amount
        if not amount or not amount.isdigit() or int(amount) <= 0:
            return apology("must provide valid amount", 400)
        amount = int(amount)

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])

        # Redirect to home page
        return redirect("/")
    else:
        return render_template("add_cash.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate symbol and shares
        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide valid number of shares", 400)
        shares = int(shares)

        # Check user's stock holdings
        user_id = session["user_id"]
        rows = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        if not rows or rows[0]["shares"] < shares:
            return apology("too many shares", 400)

        # Get current price of the stock
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        price = quote["price"]
        total_sale = shares * price

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, user_id)

        # Insert transaction (negative shares indicate a sale)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
                   user_id, symbol, -shares, price)

        # Redirect to home page
        return redirect("/")
    else:
        # Render sell page with available symbols
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)

