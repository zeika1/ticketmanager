from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from help import login_required, apology


app=Flask(__name__, template_folder="templates")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

todos = [{"task": "sample todo", "done": False}]
archives = []


@app.route("/", methods=["GET", "POST"])
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
        rows = db.execute("SELECT * FROM USER WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)


        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]

        # Redirect user to home page
        return redirect(url_for("home"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("name"):
            return apology("must provide name", 400)

        elif not request.form.get("last_name"):
            return apology("must provide Last Name", 400)

        rows = db.execute("SELECT * FROM USER WHERE username = ?", request.form.get("username"))

        if len(rows) !=0:
            return apology("username already exists", 400)

        db.execute("INSERT INTO USER (username, password_hash, name, last_name) VALUES(?, ?, ?, ?)",
                   request.form.get("username"),generate_password_hash(request.form.get("password")),request.form.get("name"), request.form.get("last_name"))

        rows = db.execute("SELECT * FROM USER WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["ID"]

        return redirect(url_for("home"))

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")


@app.route("/platform", methods=['GET', 'POST'])
@login_required
def index():
    if request.args.get('ID'):
        session["ticket_id"] = request.args.get('ID')

    if session["ticket_id"]:
        if db.execute("SELECT owner_id FROM TICKET WHERE ID = ?", session["ticket_id"])[0]["owner_id"]==session["user_id"]:
            todos = db.execute("SELECT * FROM todo_item WHERE ticket_id = ?", session["ticket_id"])

            ticket_title = db.execute("SELECT title FROM TICKET WHERE ID = ?", session["ticket_id"])[0]["title"]

            return render_template("index.html", todos=todos, ticket_title=ticket_title)
        else:
            return apology("Not allowed", 403)
    return apology("Not allowed", 500)



@app.route("/home")
@login_required
def home():
    active_usr_ticket=db.execute("SELECT * FROM TICKET WHERE owner_id = ?", session["user_id"])
    return render_template('home.html', active_usr_ticket=active_usr_ticket)



@app.route("/addticket", methods=["POST"])
@login_required
def addticket():
    if request.method == "POST":
        title = request.form.get("ticket_title")
        if len(title)>256:
            flash("title too long", 'error')
        elif len(title)==0:
            flash("Must provide title", 'error')
        else: #flash msg title too long and do not change page
            db.execute("INSERT INTO TICKET (title, owner_id) VALUES(?, ?)", title, session["user_id"])

    return redirect(url_for("home"))

@app.route("/add", methods=["POST"])
@login_required
def add():
    if request.method == "POST":
        ticket_id = session["ticket_id"]
        db.execute("INSERT INTO todo_item (ticket_id, description) VALUES(?, ?)", ticket_id, request.form.get("todo"))
    return redirect(url_for("index"))


@app.route("/change_ticket_status/<int:ticket_id>/<string:new_status>", methods=["GET"])
@login_required
def change_ticket_status(ticket_id, new_status):
    ticket_owner_id = db.execute("SELECT owner_id FROM TICKET WHERE ID = ?", ticket_id)
    if ticket_owner_id and ticket_owner_id[0]["owner_id"] == session["user_id"]:
        db.execute("UPDATE TICKET SET ticket_status = ? WHERE ID = ?", new_status, ticket_id)
        flash("Ticket status updated.", "success")
    else:
        flash("You do not have permission to change this ticket's status.", "error")
    return redirect(url_for("home"))




@app.route("/delete_ticket/<int:ticket_id>", methods=["GET"])
@login_required
def delete_ticket(ticket_id):
    # Check if the ticket belongs to the logged-in user
    ticket_owner_id = db.execute("SELECT owner_id FROM TICKET WHERE ID = ?", ticket_id)
    if ticket_owner_id and ticket_owner_id[0]["owner_id"] == session["user_id"]:
        db.execute("DELETE FROM todo_item WHERE ticket_id = ?", ticket_id)
        db.execute("DELETE FROM TICKET WHERE ID = ?", ticket_id)
        flash("Ticket and associated tasks have been deleted.", "success")
    else:
        flash("You do not have permission to delete this ticket.", "error")
    return redirect(url_for("home"))




@app.route("/edit_todo/<int:todo_id>", methods = ["GET", "POST"])
@login_required
def edit_todo(todo_id):

    if request.method == "POST":
        new_description = request.form.get("new_description")
        db.execute("UPDATE todo_item SET description = ? WHERE ID = ?", new_description, todo_id)

        return redirect(url_for("index"))
    else:
        todo = db.execute("SELECT description FROM todo_item WHERE ID = ?", todo_id)

        return render_template("edit_todo.html", todo=todo[0]["description"], todo_id=todo_id)


@app.route("/edit_ticket/<int:ticket_id>", methods = ["GET", "POST"])
@login_required
def edit_ticket(ticket_id):

    if request.method == "POST":
        new_title = request.form.get("new_title")
        db.execute("UPDATE TICKET SET title = ? WHERE ID =?", new_title, ticket_id)

        return redirect(url_for("home"))
    else:
        ticket = db.execute("SELECT title FROM TICKET WHERE ID = ?", ticket_id)

        return render_template("edit_ticket.html", ticket=ticket[0]["title"], ticket_id=ticket_id)



@app.route("/check/<int:index>")
def check(index):
    todos[index]['done'] = not todos[index]['done']
    return redirect(url_for("index"))

@app.route("/ajaxtest", methods = ["GET", "POST"])
def ajaxtest():
    if request.method == "GET":
        todo_id = request.args.get('ID')
        new_status = request.args.get('status')
        db.execute("UPDATE todo_item SET status = ? WHERE ID = ?", new_status, todo_id)
        return jsonify({"status": "success", "message": "Todo item status updated"})




@app.route("/delete/<int:todo_id>", methods=["GET"])
@login_required
def delete_todo(todo_id):
    db.execute("DELETE FROM todo_item WHERE ID = ?", todo_id)
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(debug=True)