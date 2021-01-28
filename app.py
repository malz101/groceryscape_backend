from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/view-item', methods=["GET", "POST"])
def viewItems():
    item = 'bean'
    return "<h3> your cart has {}</h3>".format(item)

@app.route('/add-to-cart', methods=["GET", "POST"])
def addItemToCart():
    item = 'bread'
    return "<h1>{} has been added to my cart!</h1>".format(item)


if __name__ == "__main__":
    app.run(debug=True)
