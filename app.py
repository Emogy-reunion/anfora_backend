from core import create_app
from celery import make_celery

app = create_app()
make_celery(app)



if __name__ == "__main__":
    app.run(debug=True)
