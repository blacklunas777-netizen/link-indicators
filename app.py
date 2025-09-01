from flask import Flask, render_template
from stream import signal_cache, launch_streams

app = Flask(__name__)
launch_streams()

@app.route("/")
def dashboard():
    return render_template("dashboard.html", signal_cache=signal_cache)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
