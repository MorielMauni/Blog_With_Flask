from flask import Flask, render_template, request
import requests
import smtplib

# ------------------- API For Blog ---------------------- #
url = "https://api.npoint.io/c3ddac6b9d573683fadd"
posts = requests.get(url=url).json()

# ------------------- Mail ---------------------- #
mail = "<your@mail.com>"
passwd = "<password>"  # It's the 'app password' from the password given by Gmail

# ------------------- Flask ---------------------- #
app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # Encrypt on the fly
            connection.login(user=mail, password=passwd)  # Log into the mail
            # Prepare the message content, encoding in utf-8
            message = f"Subject: New Message from website\n\nContact request was send on the website by {name}:\n{message}\ncontect with Email {email} / Phone number {phone}"
            connection.sendmail(from_addr=mail,
                                to_addrs="<send_to@mail.com>",
                                msg=message.encode('utf-8'))  # Explicitly encode the message as UTF-8

        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")