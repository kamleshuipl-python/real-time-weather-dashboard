from app import app, db
from app import models  # noqa: F401 - ensure models are imported before create_all

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)