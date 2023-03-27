from flask import Blueprint, request, session, render_template, g, redirect, url_for
from howlongtobeatpy import HowLongToBeat

from .db import get_db

bp = Blueprint('search', __name__, url_prefix='')


@bp.route('/search')
def search():
	db = get_db()

	g.results = []
	
	# Query all games into our database
	if request.args.get('q') != None:
		results = HowLongToBeat().search(request.args['q'])

		for result in results:
			game = db.get_game(id=result.game_id)

			if game != None:
				g.results.append(game)

	return render_template('search/search.html')