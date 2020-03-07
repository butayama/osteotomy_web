import flasky as app
from flask import render_template

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("/app/templates/home/index.html", index=True)


@app.route("/case")
def case():
    return render_template("app/templates/home/case.html", case=True)


@app.route("/op_planning")
def op_planning():
    return render_template("app/templates/home/op_planning.html", op_planning=True)


@app.route("/op")
def op():
    return render_template("app/templates/home/op.html", op=True)


@app.route("/post_op")
def post_op():
    return render_template("app/templates/home/post_op.html", post_op=True)


@app.route("/post_op1")
def _post_op1():
    return render_template("app/templates/home/post_op1.html", post_op1=True)


@app.route("/Log In")
def log_in():
    return render_template("login.html", log_in=True)
