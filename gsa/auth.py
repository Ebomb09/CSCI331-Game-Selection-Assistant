import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from gsa.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		
		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
			
		if error is None:
			try:
				db.execute(
					"INSERT INTO user (name, password) VALUES (?, ?)",
					[username, generate_password_hash(password)]
				)
				db.commit()

				user = db.execute(
					'select * from user where name = ?', 
					[username]
				).fetchone()

				if not check_password_hash(user['password'], password):
					error='Failed to create user'

			except db.IntegrityError:
				error = f"User {username} is already registered."
			else:
				session['user_id'] = user['id']
				return redirect(url_for("auth.view"))
				
		flash(error)
		
	return render_template('auth/register.html')
	

@bp.route('/login', methods=('GET', 'POST'))
def login():

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'select * from user where name = ?', 
			[username]
		).fetchone()
		
		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'
			
		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('auth.view'))
			
		flash(error)
		
	return render_template('auth/login.html')
	

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('auth.login'))


@bp.route('/view')
def view():

	if(g.user is None):
		return redirect(url_for('auth.login'))

	return render_template('auth/view.html')


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'select * from user where id=?', 
			[user_id]
		).fetchone()	