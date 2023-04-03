import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import click
from flask import current_app, g
from howlongtobeatpy import HowLongToBeat
import time


###
# Flask Specific Static Functions
###
def get_db():

	if 'db' not in g:
		g.db = Database(current_app.config['DATABASE'])
		
	return g.db


def close_db(exception):

	if 'db' in g:
		g.db.close()


@click.command('init-db')
def init_db_command():
	db = get_db()
	
	with current_app.open_resource('schema.sql') as file:
		db.connection.executescript(file.read().decode())
		db.connection.commit()

	click.echo('Database initialized.')
	

def register_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)


###
# Game Selection Assistant Database Helper Class
###
class Database:


	def __init__(self, url: str):
		self.connection = sqlite3.connect(url, detect_types=sqlite3.PARSE_DECLTYPES)
		self.connection.row_factory = sqlite3.Row


	def close(self):
		self.connection.close()


	def get_user(self, id: int = None, email: str = None, password: str = None):
		result = None

		if id is not None:
			result = self.connection.execute(
				'SELECT * FROM user WHERE id=?', 
				[id]
				).fetchone()

		elif email is not None and password is not None:
			result = self.connection.execute(
				'SELECT * FROM user WHERE email=?', 
				[email]
				).fetchone()			

			if result is None or not check_password_hash(result['password'], password):
				result = None

		return result


	def add_user(self, email: str, password: str, name: str):

		# Try to add user
		self.connection.execute(
			"INSERT INTO user (email, name, password) VALUES (?, ?, ?)",
			[email, name, generate_password_hash(password)]
		)
		self.connection.commit()

		# Should return the user if no errors
		return self.get_user(email=email, password=password)


	def get_game(self, name: str = None, id: int = None):

		# Search our database by id
		if id is not None:

			result = self.connection.execute(
				'SELECT * FROM game WHERE id=?',
				[id]
				).fetchone()

			if(result is None):
				result = self.add_game(id=id)

		# Search our database by name
		elif name is not None:

			result = self.connection.execute(
				'SELECT * FROM game WHERE name=?',
				[name]
				).fetchone()

			if(result is None):
				result = self.add_game(name=name)

		return result


	def add_game(self, name: str = None, id: int = None):

		result = None
		sql_result = None

		# Search by id
		if id is not None:
			result = HowLongToBeat().search_from_id(id)

		# Search by name
		elif name is not None:
			results = HowLongToBeat().search(name)

			if len(results) > 0:
				result = max(results, key=lambda r: r.similarity)

		if result is not None:

			# Try inserting the HowLongToBeat game
			self.connection.execute (
				'INSERT INTO game(id, name, image_url, playtime) VALUES(?, ?, ?, ?)',
				[result.game_id, result.game_name, result.game_image_url, result.all_styles]
				)
			self.connection.commit()

			# Check if our database has properly inserted it
			sql_result = self.connection.execute(
				'SELECT * FROM game WHERE id=?',
				[result.game_id]
				).fetchone()

		return sql_result


	def get_user_games(self, userId: int, sort: str = None, order: str = None):

		query = 'SELECT * FROM collection JOIN game 	\
			ON collection.gameId=game.id			\
			WHERE userId=? '

		if sort is not None and order is not None:
			query += f'ORDER BY {sort} {order}'

		return self.connection.execute(
			query,
			[userId]
			).fetchall()


	def remove_user_game(self, userId: int, gameId: int):
		user = self.get_user(id=userId)
		game = self.get_game(id=gameId)

		# Try to add the game if both are valid
		if game is not None and user is not None:
			self.connection.execute(
				'DELETE FROM collection WHERE userId=? AND gameId=?',
				[userId, gameId]
				)
			self.connection.commit()


	def add_user_game(self, userId: int, gameId: int):
		user = self.get_user(id=userId)
		game = self.get_game(id=gameId)

		# Try to add the game if both are valid
		if game is not None and user is not None:
			self.connection.execute(
				'INSERT INTO collection(userId, gameId, dateAdded) VALUES (?, ?, ?)',
				[userId, gameId, time.time_ns()]
				)
			self.connection.commit()


	def update_user_game_rating(self, userId: int, gameId: int, rating: int):
		user = self.get_user(id=userId)
		game = self.get_game(id=gameId)

		# Try to update rating if valid
		if game is not None and user is not None:
			self.connection.execute(
				'UPDATE collection SET rating=? WHERE userId=? AND gameId=?',
				[rating, userId, gameId]
				)
			self.connection.commit()


	def update_user_game_completion(self, userId: int, gameId: int, completion: int):
		user = self.get_user(id=userId)
		game = self.get_game(id=gameId)

		# Try to update rating if valid
		if game is not None and user is not None:
			self.connection.execute(
				'UPDATE collection SET completed=? WHERE userId=? AND gameId=?',
				[completion, userId, gameId]
				)
			self.connection.commit()