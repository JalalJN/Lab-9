from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hardware.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class HardwarePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<HardwarePart {self.id}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        part_name = request.form['name']
        part_price = float(request.form['price'])

        new_part = HardwarePart(name=part_name, price=part_price)
        db.session.add(new_part)
        db.session.commit()
        return redirect(url_for('index'))

    parts = HardwarePart.query.order_by(HardwarePart.date_added.desc()).all()
    total = sum(part.price for part in parts)
    return render_template('index.html', parts=parts, total=total)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)