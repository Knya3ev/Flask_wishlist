import os

from app.__init___ import create_app, db

config_name = os.getenv('FLASK_CONFIG', default='development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
