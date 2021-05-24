from flask_restplus import fields
from search_classify_tweets.projeto.restplus import api

INPUT_DATA_SEARCH_CLASSIFY = api.model('input_query',
                            {'input_query': fields.String(required=True,
                                                         description="Texto ou hashtag para buscar tweets")})

INPUT_GET_QUERY = api.model('get_query',
                            {'query': fields.String(required=True,
                                                    description="Texto ou hashtag para buscar tweets no MongoDB")})
