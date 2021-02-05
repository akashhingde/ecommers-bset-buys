from flask import Flask, send_file, request, render_template
from flask_cors import CORS, cross_origin
import json
import time
import pandas as pd
import xlsxwriter
import openpyxl
import os
from scraper import start_parsing

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
cors = CORS(app, resources={r"*": {"origins": "*"}})


# process data based on input
@cross_origin()
@app.route("/download", methods=["GET", "POST"])
def process():
    dirname = os.path.dirname(__file__)
    if os.path.exists(os.path.join(dirname, "betterbuys.xlsx")):
        os.remove(os.path.join(dirname, "betterbuys.xlsx"))

    if request.method == "POST":
        input_dict = request.form
        input_dict = {
            "product_name": input_dict.get("product_name"),
            "size": int(input_dict.get("size")),
            "sort_by": input_dict.get("sort_by"),
            "price_range_from": input_dict.get("price_range_from"),
            "price_range_to": input_dict.get("price_range_to")
        }
        start_parsing(input_dict)
        excel_filename = os.path.join(dirname, "betterbuys.xlsx")
        return send_file(
            excel_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True)

@cross_origin()
@app.route("/hello", methods=["GET"])
def start():
    return "Hello World"

@cross_origin()
@app.route("/", methods=["GET"])
def get_data():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.",port=5000, debug=True)
