from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def index():
    return "This is default page::"

@app.route('/profile')
def users():
    return render_template("profile.html",name="Ashish")

if __name__== "__main__":
    app.run(debug=True)
    