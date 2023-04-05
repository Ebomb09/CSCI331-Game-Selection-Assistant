import os
from flask import Flask, session

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE= os.path.join(app.instance_path, 'gsa.db'),
	)
		
	try: #ensure instance folder exists
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	from . import db
	db.register_app(app)	
	
	from . import auth
	app.register_blueprint(auth.bp)

	from . import game
	app.register_blueprint(game.bp)
	
	from . import search
	app.register_blueprint(search.bp)

	from . import recommend
	app.register_blueprint(recommend.bp)

	from . import collection
	app.register_blueprint(collection.bp)

	return app
