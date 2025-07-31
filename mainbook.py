from flask import Flask, url_for ,render_template, redirect ,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, URLField, TimeField, SelectField
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)
app.secret_key = ""

#-----------------------------------------------------------------------#
#🟡 SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///.db"
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()


#-----------------------------------------------------------------------#


@app.route('/')
def main_page():
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template('index.html', books=all_books)

@app.route('/add', methods=['POST', 'GET'])
def add_page():
    if request.method == 'POST':
        new_book = Book(title=request.form['book'],
                        author=request.form['author'],
                        rate=request.form['rate'])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('main_page'))
    return render_template('add.html')


@app.route('/update', methods=['POST', 'GET'])
def update_rate():
    if request.method == "POST":
        book_id = request.form['id']
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rate = request.form['new_rate']
        db.session.commit()
        return redirect(url_for('main_page'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)

    return render_template('update.html', book=book_selected)

@app.route('/delete')
def delete_book():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("main_page"))




















app.run(debug=True)
