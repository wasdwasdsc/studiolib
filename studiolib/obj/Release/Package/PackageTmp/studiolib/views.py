from studiolib import app, db, models, lm
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import login_user , logout_user , current_user , login_required
from .forms import LoginForm, RegisterForm, AddForm, SearchForm, EditForm

# index view function suppressed for brevity

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.e_mail.data
        pw = form.pw.data
        registered_user = models.User.query.filter_by(e_mail=username,pw=pw).first()
        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        login_user(registered_user)
        flash('Logged in succesfully')
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = current_user.e_mail
    else: user = "Not logged in"
    return render_template("index.html",
                           title='Home',
                           user=user)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        if len(models.User.query.filter_by(e_mail=form.e_mail.data).all()) == 0:
            user = models.User(form.pw.data, form.e_mail.data)
            db.session.add(user)
            db.session.commit()
            flash('Registred in succesfully')
            return redirect('/index')
        else:
            flash('Such e-mail already registred')
            return redirect('/index')
    return render_template('register.html',
                           title='Register',
                           form=form)



@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add',methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        if len(models.Author.query.filter_by(name=form.a_name.data).all()) != 0:
            author = models.Author.query.filter_by(name=form.a_name.data).first()
        else:
            author = models.Author(form.a_name.data)
        if len(models.Book.query.filter_by(name=form.a_name.data).all()) != 0:
            book = models.Book.query.filter_by(name=form.b_name.data).first()
        else:
            book = models.Book(form.b_name.data)
        author.books.append(book)
        db.session.add(author)
        db.session.commit()
        flash('Added successfully')
        return redirect('/index')
    return render_template('Add.html',
                           title='Add',
                           form=form)

@app.route('/init',methods=['GET', 'POST'])
@login_required
def init():
    a = models.Author.query.all()
    b = models.Book.query.all()
    for c in a:
        db.session.delete(c)
        db.session.commit()
    for c in b:
        db.session.delete(c)
        db.session.commit()
    a1 = models.Author('author1')
    a2 = models.Author('author2')
    a3 = models.Author('author3')
    a4 = models.Author('author4')
    b1 = models.Book('book1')
    b2 = models.Book('book2')
    b3 = models.Book('book3')
    b4 = models.Book('book4')
    a1.books.append(b1)
    a1.books.append(b2)
    a2.books.append(b2)
    a3.books.append(b2)
    a3.books.append(b3)
    a4.books.append(b1)
    a4.books.append(b2)
    a4.books.append(b3)
    a4.books.append(b4)
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    db.session.add(a4)
    db.session.commit()
    flash('Database was reinitiated')
    return redirect('/index')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    eform = EditForm()
    if form.validate_on_submit():
        if form.by_author.data == form.by_book.data == False:
            flash('Choose at least one search option')
            return redirect('/search')
        if form.by_author.data == form.by_book.data == True:
            a = models.Author.query.filter_by(name=form.text.data).all()
            b = models.Book.query.filter_by(name=form.text.data).all()
            data = []
            if len(a) != 0:
                data.append(form.text.data + ' wrote ' + str(models.Author.query.filter_by(name=form.text.data).first().books.all())[1:-1])
            if len(b) != 0:
                data.append(form.text.data + ' is written by ' + str(models.Book.query.filter_by(name=form.text.data).first().authors.all())[1:-1])
            if len(data) == 0:
                data.append("Nothing was found")
            return render_template('display.html',
                                    title='Display books',
                                    data=data,
                                   form=eform)
        if form.by_author.data:
            a = models.Author.query.filter_by(name=form.text.data).all()
            data = []
            if len(a) != 0:
                data.append(form.text.data + ' wrote ' + str(models.Author.query.filter_by(name=form.text.data).first().books.all())[1:-1])
            else: data.append('No such author')
            return render_template('display.html',
                                   title='Display books',
                                   data=data,
                                   form=eform)
        if form.by_book.data:
            b = models.Book.query.filter_by(name=form.text.data).all()
            data = []
            if len(b) != 0:
                data.append(form.text.data + ' is written by ' + str(models.Book.query.filter_by(name=form.text.data).first().authors.all())[1:-1])
            else: data.append('No such book name')
            return render_template('display.html',
                                   title='Display books',
                                   data=data,
                                   form=eform)
    return render_template('search.html',
                           title='Search',
                           form=form)

@app.route('/display_all')
def show_all():
    a = models.Author.query.all()
    form = EditForm()
    data = []
    for b in a:
        data.append(str(b) + ' wrote ' + str(models.Author.query.filter_by(name=str(b)).first().books.all())[1:-1])
    return render_template('display.html',
                                   title='Display books',
                                   data=data,
                                   form=form)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = SearchForm()
    if form.validate_on_submit():
        if form.by_author.data == form.by_book.data == False:
            flash('Choose at least one delete option')
            return redirect('/delete')
        if form.by_author.data == form.by_book.data == True:
            if len(models.Author.query.filter_by(name=form.text.data).all()) != 0:
                a = models.Author.query.filter_by(name=form.text.data).first()
                db.session.delete(a)
            if len(models.Book.query.filter_by(name=form.text.data).all()) != 0:
                b = models.Book.query.filter_by(name=form.text.data).first()
                db.session.delete(b)
            db.session.commit()
            flash('Deleted successfully')
            return redirect('/index')
        if form.by_author.data:
            if len(models.Author.query.filter_by(name=form.text.data).all()) != 0:
                a = models.Author.query.filter_by(name=form.text.data).first()
                db.session.delete(a)
                flash('Deleted successfully')
            else: flash('Invalid input information')
            db.session.commit()
            return redirect('/index')
        if form.by_book.data:
            if len(models.Book.query.filter_by(name=form.text.data).all()) != 0:
                b = models.Book.query.filter_by(name=form.text.data).first()
                db.session.delete(b)
                flash('Deleted successfully')
            else: flash('Invalid input information')
            db.session.commit()
            return redirect('/index')
    return render_template('delete.html',
                           title='Search',
                           form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        if form.by_author.data == form.by_book.data == False:
            flash('Choose one of options')
            return redirect('/edit')
        if form.by_author.data == form.by_book.data == True:
            flash('You can only choose one option')
            return redirect('/edit')
        if form.by_author.data:
            if len(models.Author.query.filter_by(name=form.text.data).all()) != 0:
                a = models.Author.query.filter_by(name=form.text.data).first()
                a.name = form.new_text.data
                db.session.commit()
                flash('Edited successfully')
                return redirect('/index')
            else:
                flash('No such author')
                return redirect('/edit')
        if form.by_book.data:
            if len(models.Book.query.filter_by(name=form.text.data).all()) != 0:
                a = models.Book.query.filter_by(name=form.text.data).first()
                a.name = form.new_text.data
                db.session.commit()
                flash('Edited successfully')
                return redirect('/index')
            else:
                flash('No such book')
                return redirect('/edit')
    return render_template('edit.html',
                           title='Edit',
                           form=form)

