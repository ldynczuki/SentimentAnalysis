import os

"""
    Variaveis booleanas e objetos nao poderao ser definidas nas variaveis de ambiente,
    pois todas serao convertidas para string.
    Para as variaveis definidas com "os.environ.get()" o primeiro valor é referente
    a variavel que está buscando, o segundo valor será usado como valor padrão caso
    não encontre nas variaveis de ambiente.
"""
API_NAME = "Buscador e classificador de tweets"
VERSION_API = '1.0.0'
TITLE_API = "TCC PUC-MG"
DESCRIPTION_API = f"Buscador e Classificador de tweets"

# Flask settings
FLASK_SERVER_NAME = None
FLASK_HOST = os.environ.get('FLASK_HOST', "0.0.0.0")
FLASK_PORT = os.environ.get('FLASK_PORT', "5000")
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

OUTPUT_TWEETS_CSV = "/code/search_classify_tweets/projeto/search/output/tweets.csv"

# database settings
MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb://mongo:27017')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', 'tcc_puc')
MONGODB_COLLECTION = os.environ.get('MONGODB_COLLECTION', 'documentos')

URL_PREFIX = os.environ.get('URL_PREFIX', '/api')
ROUTE = os.environ.get("ROUTE", "")

# Enpoints
ENDPOINTS_SEARCH_CLASSIFY = os.environ.get("ENDPOINTS", "/search_classify_tweets")

ENDPOINTS_DATABASE_SEARCH_ALL = os.environ.get("ENDPOINTS_DATABASE_SEARCH_ALL", "/database/search_all")
ENDPOINTS_FIND_QUERY = os.environ.get("ENDPOINTS_FIND_QUERY", "/database/find_query")

ROUTE_GET_ID = os.environ.get("ROUTE", "/get_id/<string:id>")
ROUTE_DATABASES = os.environ.get("ROUTE", "/databases")
ROUTE_COLLECTIONS = os.environ.get("ROUTE", "/collections")
ROUTE_UPDATE = os.environ.get("ROUTE", "/update")
ROUTE_DELETE = os.environ.get("ROUTE", "/delete/<string:id>")

PATH_LOG = os.environ.get("PATH_LOG", "./log_project_name")

# MODEL_WEIGHTS_PATH
TRAIN_ARGS_PATH = '/code/search_classify_tweets/projeto/model/train_args.json'
WEIGHTS_PATH = '/code/search_classify_tweets/projeto/model/weights/'

USE_CUDA = os.environ.get("USE_CUDA", False)