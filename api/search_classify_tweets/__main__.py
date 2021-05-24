from search_classify_tweets.projeto.app import app
from search_classify_tweets.projeto import settings


def start():
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.FLASK_DEBUG)
    print(__package__, ' started.')


if __name__ == '__main__':
    start()
