from flask_restplus import Api
from loguru import logger

from search_classify_tweets.projeto import settings
from search_classify_tweets.projeto.constants import codeHttp, mensagens
from search_classify_tweets.projeto.responses.responses import ControllResponse


# Objeto para resposta
objResponse = ControllResponse()

api = Api(version=settings.VERSION_API, title=settings.TITLE_API,
          description=settings.DESCRIPTION_API)


@api.errorhandler
def default_error_handler(e):
    logger.exception(mensagens.ERROR_NOT_TREATMENT)

    if not settings.FLASK_DEBUG:
        return {'mensagem': mensagens.ERROR_NOT_TREATMENT}, codeHttp.ERROR_500
