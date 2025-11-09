from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
import numpy as np
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

FILETYPES = [".png", ".jpg"]

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap5(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        f = request.files["file"]
        if f.filename.split(".")[-1] in FILETYPES:
            f.save(f"static/assets/img/{f.filename}")
            top_n_c = process_img(f.filename)
            return render_template("index.html", name=f.filename, colors=top_n_c)
        elif f.filename == "standard.jpg":
            flash("Filename clashes with preassigned File. Please rename your file.")
            return redirect(url_for("home"))
        else:
            flash("Wrong filetype!")
            return redirect(url_for("home"))
    if request.method == "GET":
        top_n_c = process_img("standard.jpg")
        return render_template("index.html", name="standard.jpg", colors=top_n_c)


def process_img(file: str) -> dict:
    image = Image.open(f"./static/assets/img/{file}").convert("RGB")
    np_img = np.asarray(image)
    np_img_reshaped = np_img.reshape(-1, 3)
    unique_colors, counts = np.unique(np_img_reshaped, axis=0, return_counts=True)
    size_test = True
    n = 10
    while size_test:
        try:
            top_n_colors_pos = np.argpartition(counts, -n)[-n:]
            size_test = False
        except ValueError:
            n -= 1
    top_n_colors_tuples = [
        tuple(color) for color in unique_colors[top_n_colors_pos].tolist()
    ]
    top_n_colors_dict = {
        k: v for (k, v) in zip(top_n_colors_tuples, counts[top_n_colors_pos].tolist())
    }

    return top_n_colors_dict


if __name__ == "__main__":
    app.run(debug=True)
