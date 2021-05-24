from search_classify_tweets.projeto import settings

# Mensagens log API
INICIO_LOAD_MODEL = "Carregando os modelos..."
FIM_LOAD_MODEL = "Modelo carregados."
INICIO_PREDICT = "Iniciando o predict..."
FIM_PREDICT = "Fim do predict."
REQUEST = "Request recebida."
MODEL_DEVICE = "Modelo sendo inicializado em: "

ERROR_CONNECTION_DB = f'Erro durante conexão: {settings.MONGODB_URL}/{settings.MONGODB_DATABASE}/{settings.MONGODB_COLLECTION}'
ERROR_AUTENTICATION_DB = 'Erro na autentificação com o banco. Usuário ou senha incorretos.'

# Error Business #
ERROR_GENERIC = "Ocorreu um erro generico"
ERROR_NOT_TREATMENT = 'Ocorreu algo que não esperavamos e para seu conforto estaremos olhando.'
ERROR_API = "Ocorreu um erro na API."
ERROR_RUNTIME = 'Erro ao carregar o modelo'
ERROR_OS = 'Nao foi possivel identificar o objeto, verificar o caminho especificado'
ERROR_NONE_TYPE = 'Arquivo invalido. verifique o tipo do documento.'
ERROR_KEY = 'Chave incorreta'
MEMORY_ERROR = 'Ops, voce nao possui memoria suficiente para realizar essa operacao.'
VALUE_ERROR = 'Argumento incorreto ou invalido.'

# Sucess Business #
SUCESSO_GET = "Classificador OK."
SUCESSO_PREDICT = "Predict realizado com sucesso."
