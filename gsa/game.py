from flask import Blueprint, request, session, render_template, g

from .db import get_db

bp = Blueprint('game', __name__, url_prefix='')


@bp.route('/game/<gameId>', methods=['GET', 'POST'])
def view(gameId):
	db = get_db()

	g.game = db.get_game(id=gameId)
	g.in_collection = False
	g.game_rating = 0
	g.game_completed = 0 

	if(g.user != None):

		# Try to add/remove based on the game page form selection
		if(request.method == 'POST'):

			if(request.form.get('do') == 'add'):
				db.add_user_game(g.user['id'], g.game['id'])

			elif(request.form.get('do') == 'remove'):
				db.remove_user_game(g.user['id'], g.game['id'])

			#Try to edit the user's game
			if('rate' in request.form):
				rating = int(request.form['rate'])
				db.update_user_game_rating(g.user['id'], g.game['id'], rating)

			if('completed' in request.form):
				completion = int(request.form['completed'])
				db.update_user_game_completion(g.user['id'], g.game['id'], completion)				

		# Check if game is in the user's games
		for item in db.get_user_games(userId=g.user['id']):

			if item['gameId'] == g.game['id']:
				g.in_collection = True

				if item['rating'] is not None:
					g.game_rating = item['rating']

				if item['completed'] is not None:
					g.game_completed = item['completed']
				break

	return render_template('game/view.html')