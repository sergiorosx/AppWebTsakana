import os

from flask import Flask

from commerceretail.database import db_session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'#,
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    #if test_config is None:
        # load the instance config, if it exists, when not testing
        #app.config.from_pyfile('config.py', silent=True)
    #else:
        # load the test config if passed in
        #app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    #@app.route('/hello')
    #def hello():
    #    return 'Hello, World!'

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from . import client
    app.register_blueprint(client.bp)

    from . import product
    app.register_blueprint(product.bp)

    from . import bill
    app.register_blueprint(bill.bp)

    return app