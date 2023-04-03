from flask import Blueprint, request, session, render_template, g, redirect, url_for

from .db import get_db

bp = Blueprint('collection', __name__, url_prefix='')


@bp.route('/', methods=['GET'])
def view():
	db = get_db()

	g.sort = request.args.get('sort')
	g.order = request.args.get('order')

	if g.sort not in ['name', 'playtime', 'rating', 'completed']:
		g.sort = 'completed'

	if g.order not in ['ASC', 'DESC']:
		g.order = 'DESC';

	if g.user != None:
		g.collection = db.get_user_games(g.user['id'], g.sort, g.order)
		return render_template('collection/view.html')

	else:
		return redirect(url_for("auth.login"))