from library import app

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .books import books_ as books_blueprint
app.register_blueprint(books_blueprint)

from .members import members_ as members_blueprint
app.register_blueprint(members_blueprint)
