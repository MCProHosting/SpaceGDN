from flask_script import Manager
from flask_migrate import MigrateCommand

from models import *
from . import app

manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
	from gevent.pywsgi import WSGIServer

	http_server = WSGIServer(('', app.config['HTTP_PORT']), app)
	if app.config['DEBUG']:
		debugModeStr = '''Debug mode enabled!'''
	else: 
		debugModeStr = ''
	try:
		print '''===========================================================================
   __...____________________          ,
   `(\ [ ===SPACEGDN===--|__|) ___..--"_`--.._____
     `"""""""""""""""""| |""` [_""_-___________"_/
                       | |   /..../`'-._.-'`
                   ____| |__/::..'_
                  |\ ".`"` '_____//\\
                  `"'-.   """""  \\\\/
                       `""""""""""`
===========================================================================
SpaceGDN developed by pyxld.com and is OSS under the MPL-2.0 at
https://github.com/connor4312/SpaceGDN. We're lifting off... 
===========================================================================
Running on '''+app.config['HTTP_HOST']+''':'''+str(app.config['HTTP_PORT'])+'''
'''+debugModeStr+'''
==========================================================================='''
		http_server.serve_forever()
	except KeyboardInterrupt:
		http_server.stop()
		print '''
SpaceGDN has shut down. Find any bugs? Report on our Github at
https://github.com/connor4312/SpaceGDN
===========================================================================
'''
@manager.command
def debug():
	app.run(debug = app.config['DEBUG'], host=app.config['HTTP_HOST'], port=app.config['HTTP_PORT'])

@manager.command
def load():
	from loader import loader
	loader.load()
