import os

from flask import Flask

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)
	
	if test_config is None: #load instance config when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)
		
	try: #ensure instance folder exists
		os.makedirs(app.instance_path)
	except OSError:
		pass
	#hello world
	@app.route('/hello')
	def hello():
		return 'Hello, World!'
	
	from . import db
	db.init_app(app)	
	
	from .import auth
	app.register_blueprint(auth.bp)
	
	return app