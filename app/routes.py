from app import app
from app.forms import BookForm
from app.recommend import recommend
from flask import render_template, redirect, request


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = BookForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            id = form.data['gr_id']
            num_books = form.data['num_books']
            recs = recommend(id, num_books)
            return render_template('results.html', books=recs)
    return render_template('get_recs.html',  form=form)


