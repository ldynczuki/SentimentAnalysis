import time
import pandas as pd
from flask import request
from flask_restplus import Resource
from loguru import logger
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

from search_classify_tweets.projeto import settings
from search_classify_tweets.projeto.model.classificador import Classificador
from search_classify_tweets.projeto.constants import codeHttp, mensagens
from search_classify_tweets.projeto.restplus import api, objResponse
from search_classify_tweets.projeto.exceptions import SearchException
from search_classify_tweets.projeto.utils import doc_swagger
from search_classify_tweets.projeto.utils.preprocessing import preprocessing_tweets
from search_classify_tweets.projeto.search.search import search_tweets
from search_classify_tweets.projeto.restplus import objResponse
from search_classify_tweets.projeto.database import MongoDataBase


ns = api.namespace(settings.ROUTE, description=settings.DESCRIPTION_API)


@ns.route(settings.ENDPOINTS_SEARCH_CLASSIFY, methods=['POST'])
class SearchResources(Resource):

    try:
        logger.info(mensagens.INICIO_LOAD_MODEL)
        modelo_bert = Classificador()
        logger.info(mensagens.FIM_LOAD_MODEL)

    except OSError as error:
        response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_OS, status=codeHttp.ERROR_500)
        logger.error(mensagens.ERROR_OS)

    except RuntimeError as error:
        response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_RUNTIME, status=codeHttp.ERROR_500)
        logger.error(mensagens.ERROR_RUNTIME)

    except FileNotFoundError as error:
        response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_FILENOTFOUND, status=codeHttp.ERROR_500)
        logger.error(mensagens.ERROR_FILENOTFOUND)

    @api.expect(doc_swagger.INPUT_DATA_SEARCH_CLASSIFY)
    def post(self) -> dict:
        """
            Método POST para realizar a busca e classificação dos tweets coletados.
            inputs:\n
            'input_query': texto ou hashtag para coletar tweets.
            'tweets_limit': limite de tweets a serem coletados.
        """
        logger.info(mensagens.REQUEST)
        data = request.get_json()

        try:
            input_query = data["input_query"]
            tweets_limit = data['tweets_limit']

        except KeyError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_KEY, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_KEY)

        except TypeError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)

        except ValueError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_VALUE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_VALUE)
        
        try:
            logger.info(f'[+] ------ Buscando tweets ------')
            results = search_tweets(input_query, tweets_limit)
            logger.info(f'[-] ------ Fim busca de tweets ------')

        except SearchException as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_API, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_API)

        except OSError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)

        except MemoryError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.MEMORY_ERROR, status=codeHttp.ERROR_500)
            logger.error(mensagens.MEMORY_ERROR)

        except TypeError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)
        
        try:
            logger.info(f'[+] ------ Iniciando Pré-processamento dos tweets coletados ------')
            result_preprocessing = preprocessing_tweets()
            logger.info(f'[-] ------ Fim Pré-processamento dos tweets coletados ------')
        
        except SearchException as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_API, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_API)
        
        except OSError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)
        
        try:
            logger.debug(mensagens.INICIO_PREDICT)
            start_predict = time.time()

            result_predict = self.modelo_bert.get_predict(result_preprocessing, input_query)

            time_predict = time.time() - start_predict
            logger.debug(mensagens.FIM_PREDICT)
            logger.debug("Tempo gasto predict: " + str(time_predict))

        except SearchException as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_API, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_API)

        except OSError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)

        except MemoryError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.MEMORY_ERROR, status=codeHttp.ERROR_500)
            logger.error(mensagens.MEMORY_ERROR)

        except TypeError as error:
            response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
            logger.error(mensagens.ERROR_NONE_TYPE)
        
        try:
            logger.info(f'[+] ------ Iniciando conexao com MongoDB ------')
            database = MongoDataBase(settings.MONGODB_URL, settings.MONGODB_DATABASE, settings.MONGODB_COLLECTION)
            logger.info(f'[-] ------ Conexao estabelecida com MongoDB ------')

        except ServerSelectionTimeoutError as error:
            logger.error(mensagens.ERROR_CONNECTION_DB)
            response = objResponse.send_exception(objError=error,
                                                  messages=mensagens.ERROR_CONNECTION_DB, status=codeHttp.ERROR_503)

        except OperationFailure as error:
            logger.error(mensagens.ERROR_AUTENTICATION_DB)
            response = objResponse.send_exception(objError=error,
                                                  message=mensagens.ERROR_AUTENTICATION_DB, status=codeHttp.ERROR_403)

        else:

            try:
                result_insert = database.create(result_predict)
                logger.info(f'[-] ------ Objeto inserido no MongoDB com sucesso ------')
                response = objResponse.send_success(data=result_insert,
                                                    messages="Objeto inserido no MongoDB com sucesso", 
                                                    status=codeHttp.SUCCESS_200)
            except ValueError as error:
                logger.error(mensagens.ERROR_AUTENTICATION_DB)
                response = objResponse.send_exception(objError=error,
                                                      messages=mensagens.VALUE_ERROR, status=codeHttp.ERROR_401)

        return response


@ns.route(settings.ENDPOINTS_DATABASE_SEARCH_ALL, methods=['GET'])
class DatabaseGetAllResources(Resource):

    def get(self):

        try:
            logger.info(f'[+] ------ iniciando conexao com MongoDB ------')
            database = MongoDataBase(settings.MONGODB_URL, settings.MONGODB_DATABASE, settings.MONGODB_COLLECTION)
            logger.info(f'[-] ------ conexao estabelecida com MongoDB ------')

        except ServerSelectionTimeoutError as error:
            logger.error(mensagens.ERROR_CONNECTION_DB)
            response = objResponse.send_exception(objError=error,
                                                  messages=mensagens.ERROR_CONNECTION_DB, status=codeHttp.ERROR_503)

        except OperationFailure as error:
            logger.error(mensagens.ERROR_AUTENTICATION_DB)
            response = objResponse.send_exception(objError=error,
                                                  message=mensagens.ERROR_AUTENTICATION_DB, status=codeHttp.ERROR_403)

        else:
            result_all = database.read_all()
            response = objResponse.send_success(data=result_all,
                                                messages="Databases retornado com sucesso", status=codeHttp.SUCCESS_200)

        return response


@ns.route(settings.ENDPOINTS_FIND_QUERY, methods=['POST'])
class DatabaseGetQuery(Resource):

    @api.expect(doc_swagger.INPUT_GET_QUERY)
    def post(self):
        
        logger.info(mensagens.REQUEST)
        data = request.get_json()['query']
        
        try:
            logger.info(f'[+] ------ iniciando conexao com MongoDB ------')
            database = MongoDataBase(settings.MONGODB_URL, settings.MONGODB_DATABASE, settings.MONGODB_COLLECTION)
            logger.info(f'[-] ------ conexao estabelecida com MongoDB ------')

        except ServerSelectionTimeoutError as error:
            logger.error(mensagens.ERROR_CONNECTION_DB)
            response = objResponse.send_exception(objError=error,
                                                  messages=mensagens.ERROR_CONNECTION_DB, status=codeHttp.ERROR_503)

        except OperationFailure as error:
            logger.error(mensagens.ERROR_AUTENTICATION_DB)
            response = objResponse.send_exception(objError=error, message=mensagens.ERROR_AUTENTICATION_DB, status=codeHttp.ERROR_403)

        else:
            logger.info(f'[+] ------ recuperando query no MongoDB ------')
            result_lista_qury = database.get_query(data)
            response = objResponse.send_success(data=result_lista_qury, messages="Lista de objetos retornados com sucesso", status=codeHttp.SUCCESS_200)

        return response