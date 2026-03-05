from flask import Flask, request, jsonify, render_template
import numpy as np
from scipy.stats import t
from statistics import stdev

app = Flask(__name__)   # THIS LINE IS REQUIRED

def san(a, b, alt):
    alpha = 0.05

    if len(a) < 2 or len(b) < 2:
        return {"error": "Each sample must contain at least two values"}

    n1 = len(a)
    n2 = len(b)

    x1 = np.mean(a)
    x2 = np.mean(b)

    sd1 = stdev(a)
    sd2 = stdev(b)

    df = n1 + n2 - 2
    mu = 0

    se = np.sqrt((sd1**2 / n1) + (sd2**2 / n2))
    tcal = ((x1 - x2) - mu) / se

    p_value = (1 - t.cdf(abs(tcal), df)) * 2

    return {
        "t_calculated": tcal,
        "p_value": p_value,
        "df": df
    }

@app.route("/")
def home():
    return render_template("app.html")

@app.route("/run_test", methods=["POST"])
def run_test():

    data = request.json
    a = data["a"]
    b = data["b"]
    alt = data["alt"]

    result = san(a,b,alt)

    return jsonify(result)

if __name__ == "__main__":
    app.run()

