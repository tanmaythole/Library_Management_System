from . import app, render_template

@app.route('/')
def dashboard():
    return render_template("dashboard.html")