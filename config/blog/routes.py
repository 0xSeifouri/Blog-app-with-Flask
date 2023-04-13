from flask import render_template, redirect, url_for, flash, abort
from . import app, forms, db, bcrypt
from .models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        my_user = User(username=form.username.data, email=form.email.data,
                       password=hashed_pass)
        db.session.add(my_user)
        db.session.commit()
        flash('Register is Successfully')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('you Logged in Successfully', 'success')
            return redirect(url_for('home'))
        flash('Username or Password incorrect', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you logged out Successfully')
    return redirect('/')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = forms.UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account updated')
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('profile.html', form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = forms.PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.text.data, post_author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created :)')
        return redirect('/')
    return render_template('create_post.html', form=form)


@app.route('/post/detail/<int:pk>')
def post_detail(pk):
    posts = Post.query.get_or_404(pk)
    return render_template('detail_post.html', post=posts)


@app.route('/post/delete/<int:pk>')
@login_required
def delete_post(pk):
    post = Post.query.get_or_404(pk)
    if post.post_author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted')
    else:
        return abort(403)
    return redirect('/')


@app.route('/post/update/<int:pk>', methods=['GET', 'POST'])
@login_required
def update_post(pk):
    post = Post.query.get_or_404(pk)
    if post.post_author != current_user:
        return abort(403)

    form = forms.PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('post_detail', pk=post.id))
    else:
        form.title.data = post.title
        form.text.data = post.text
    return render_template('update_post.html', form=form,)
