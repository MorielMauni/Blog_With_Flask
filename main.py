from flask import Flask, render_template
import requests

# ------------------- API For Blog ---------------------- #
url = "https://api.npoint.io/c3ddac6b9d573683fadd"
posts = requests.get(url=url).json()


app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")