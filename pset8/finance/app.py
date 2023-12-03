from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import sqlite3
from update import get_data
import threading


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Open cursor database for users data
finance_con = sqlite3.connect(r"/home/recep/CS50/pset8/finance/Finance.db",check_same_thread=False)
finance_cur = finance_con.cursor()

# Open database for show tickers
Tickers_con = sqlite3.connect(r"/home/recep/CS50/pset8/finance/Tickers.db", check_same_thread=False)
Tickers_cur = Tickers_con.cursor()


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get data from database for stock
    data = finance_cur.execute("SELECT symbol,SUM(shares) FROM history WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0", str(session["user_id"]))
    symbols = []
    shares = []
    prices = []
    total = []
    total2 = []
    for stock in data:
        symbols.append(stock["symbol"])
        share = stock["SUM(shares)"]
        price = lookup(stock["symbol"])["price"]
        shares.append(share)
        prices.append(usd(price))
        total.append(price*share)
        total2.append(usd(price*share))

    # Merge data for stock
    stock = list(zip(symbols,symbols,shares,prices,total2))

    # Get cash from database
    cash = finance_cur.execute("SELECT cash FROM users WHERE id=?",[session["user_id"]]).fetchone()[0]

    # Render homepage with data
    return render_template("index.html", rows = stock, cash = usd(cash), total = usd(cash + sum(total)))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL",400)
        
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("MISSING SHARES",400)
        
        # Ensure username was valid
        elif not request.form.get("shares").isdecimal():
            return apology("INVALID SHARES",400)
        elif int(request.form.get("shares"))<=0:
            return apology("INVALID SHARES",400)
        
        # TRY to buy shares
        else:

            # Get data from lookup
            data = lookup(request.form.get("symbol"));

            # Get user cash from database
            cash = finance_cur.execute("SELECT cash FROM users WHERE id=?", str(session["user_id"]))[0]

            # Ensure symbol was valid
            if data is None:
                return apology("INVALID SYMBOL",400)
            
            # Ensure user can afford price of shares
            elif float(data["price"])*float(request.form.get("shares"))>=cash:
                return apology("CAN'T AFFORD")
            
            # Get and update user cash after bougt shares
            cash = cash-float(data["price"])*float(request.form.get("shares"))
            finance_cur.execute("UPDATE users SET cash = ? WHERE id = ?",cash,str(session["user_id"]))

            # Set user history
            finance_cur.execute("INSERT INTO history VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)", session["user_id"], data["symbol"], request.form.get("shares"), usd(data["price"]))

            # Redirect user to homepage
            return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Ensure username was submitted
    if not request.args.get("username"):
        return apology("must provide username", 400)

    # Ensure that username is available
    if finance_cur.execute("SELECT * FROM users WHERE username = ?",[request.args.get("username")]):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get history data from database
    data = finance_cur.execute("SELECT * FROM history WHERE id = ?",[session["user_id"]])
    return render_template("history.html",rows = data)


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
        rows = finance_cur.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")]).fetchone()
        
        # Ensure username exists and password is correct
        if rows is None or not check_password_hash(rows[2], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]

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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get symbol data from lookup 
        data = lookup(str(request.form.get("symbol")))
        
        #Check symbol is valid or not
        if data:
            return render_template("quoted.html",name = data["name"], symbol = data["symbol"], price = usd(data["price"]))
        else:
            return apology("INVALID SYMBOL",400)
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        # Ensure second password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password again", 400)
        
        # Ensure passwords was confirmed
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("must passwords confirm", 400)
        
        # Check username is available
        elif finance_cur.execute("SELECT username FROM users WHERE username = ?", [request.form.get("username")]).fetchone() is not None:
            return apology("USERNAME ALREADY TAKEN", 400)
        
        # Insert user
        else:
            # Log in user
            finance_cur.execute("INSERT INTO users(username, hash, cash) VALUES (?, ?,10000)",[request.form.get("username"),generate_password_hash(request.form.get("password"))])
            finance_con.commit()

            # Redirect user to homepage
            return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:  
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (expoas by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if request.form.get("symbol") == "symbol":
            return apology("MISSING SYMBOL",400)
        
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("MISSIN SHARES",400)
        
        # Get data from database for stock
        data = finance_cur.execute("SELECT symbol,SUM(shares) FROM history WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0",str(session["user_id"]))

        # Add data of stock to a list
        stocks = []
        for stock in data:
            dict = {stock["symbol"] : stock["SUM(shares)"]}
            stocks.append(dict)

        # Return the list to a dict
        dicts = {}
        for dict in stocks:
            dicts.update(dict)

        if request.form.get("symbol") is None:
            return apology("PLEASE SELECT A SYMBOL",400)

        # Check the requested shares from stock
        if dicts[request.form.get("symbol")] < int(request.form.get("shares")):
            return apology("TOO MANY SHARES",400)
        
        # Sell shares and redirect user to homepage
        else:
            cash = (finance_cur.execute("SELECT cash FROM users WHERE id = ?", session["user_id"]))[0]["cash"]
            price = (lookup(request.form.get("symbol")))["price"]
            finance_cur.execute("INSERT INTO history VALUES (?, ?, -?, ?, CURRENT_TIMESTAMP)",session["user_id"],request.form.get("symbol"),request.form.get("shares"),usd(price))
            finance_cur.execute("UPDATE users SET cash = ? WHERE id = ?", cash + price * int(request.form.get("shares")),session["user_id"])
            return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Get symbols from database for options menu
        data = finance_cur.execute("SELECT symbol,SUM(shares) FROM history WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0",str(session["user_id"]))
        symbols = []
        for stock in data:
            symbols.append(stock["symbol"])
        
        return render_template("sell.html",options = symbols)


@app.route("/password", methods=["GET","POST"])
@login_required
def password():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get user password hash
        password = finance_cur.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]

        # Check user input for match current password
        if check_password_hash(password,request.form.get("CurrentPassword")):

            # Check passwords are match or not
            if request.form.get("NewPassword") == request.form.get("ConfirmPassword"):
                
                # Check new password is same with current password
                if check_password_hash(password,request.form.get("NewPassword")):
                    flash("New password cannot be the same as the current one !!!")
                    return redirect("/password")
                
                #Change password
                else:
                    finance_cur.execute("UPDATE users SET hash = ? WHERE id = ?",generate_password_hash(request.form.get("NewPassword")),session["user_id"])
                    flash("PASSWORD CHANGED")
                    return redirect("/")
            else:
                flash("Passwords are not match !!!")
                return redirect("/password")
        else:
            flash("Current password is wrong !!!")
            return redirect("/password")

        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")



@app.route("/cash", methods=["GET","POST"])
@login_required
def cash():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Update cash
        finance_cur.execute("UPDATE users SET cash = ? WHERE id = ?", [request.form.get("cash"), session["user_id"]])
        finance_con.commit()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cash.html")


@app.route("/live", methods=["GET", "POST"])
def live():
    # Get all data from the database
    data = Tickers_cur.execute("SELECT * FROM tickers").fetchall()  
    
    return  render_template("live.html",rows = data)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

threading.Thread(target=get_data,).start()
