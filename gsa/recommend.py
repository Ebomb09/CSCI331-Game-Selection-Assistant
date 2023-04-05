from flask import Blueprint, request, session, render_template, g, redirect, url_for

from .db import get_db

bp = Blueprint('recommend', __name__, url_prefix='')


@bp.route('/recommend')
def view():
	db = get_db()

	games = db.get_user_games(g.user['id'])

	scoring = []
	g.results = []

	# Get scoring attributes from completed games
	for game in games:
		if game['completed']:

			for tag in game['tags'].split(','):
				tag = tag.strip()

				rating = game['rating']
				playtime = game['playtime']

				if rating is None:
					rating = 3

				scoring.append([tag, float(playtime), int(rating)])

	# Compare with the scoring to add / remove points
	for game in games:
		points = 0

		for tag in game['tags'].split(','):
			tag = tag.strip()

			for score in scoring:
				if score[0] == tag:
					playtime = float(game['playtime'])
					points += (score[2] / 3) * (1 / (pow(playtime - score[1], 2) / 50 + 1))

		if game['completed']:
			points /= 2

		g.results.append([game, round(points, 3)])

	# Sort the results before they are shown
	g.results.sort(reverse = True, key = lambda ar : ar[1])

	return render_template('recommend/view.html')