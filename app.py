from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Get the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        msg = request.form.get("message")

        if name and msg:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("INSERT INTO contact (name, message) VALUES (%s, %s)", (name, msg))
            conn.commit()
            cur.close()
            conn.close()
            message = "Message received!"
        else:
            message = "Please fill in all fields."

    return render_template("index.html", message=message)
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    app.run(debug=True)