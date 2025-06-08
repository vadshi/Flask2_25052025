from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, DataRequired


app = Flask(__name__)
app.secret_key = "secret key example"

class MyForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=3, max=10)])


@app.route("/submit", methods=["GET", "POST"])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(f'{request.form = }')
        return redirect(url_for("done"))
    
    return render_template("index.html", **{"form": form })  # context={"form": form }


@app.route("/success")
def done():
    return jsonify(message="Well done")


if __name__ == '__main__':
    app.run(debug=True)