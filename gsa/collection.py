from flask import Blueprint, request, session, render_template, g, redirect, url_for

from .db import get_db

bp = Blueprint('collection', __name__, url_prefix='')


@bp.route('/', methods=['GET', 'POST'])
def view():
	db = get_db()

	if g.user != None:
		g.collection = db.get_user_games(g.user['id'])
		return render_template('collection/view.html')

	else:
		return redirect(url_for("auth.login"))