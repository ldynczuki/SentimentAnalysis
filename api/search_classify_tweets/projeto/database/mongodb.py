from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId


class MongoDataBase:

    def __init__(self, url: str, database: str, collection: str):
        self._connection = MongoClient(url)  # start mongo connection

        self.connection.server_info()  # test connection

        self._database = self._connection[database]  # create mongo collection
        self._collection = self._database[collection]  # create mongo document

    @property
    def connection(self):
        return self._connection

    @property
    def database(self):
        return self._database

    @property
    def collection(self):
        return self._collection

    @property
    def database_names(self):
        return self.connection.database_names()

    @property
    def collection_names(self):
        return self.database.collection_names()

    def create(self, data: dict) -> str:
        objectid = str(self.collection.insert_one(data))
        return objectid

    def get_objectid(self, id: str) -> 'ObjectId':
        try:
            objectid = ObjectId(id)
        except InvalidId:
            raise ValueError('Identificador inválido')
        else:
            return objectid

    def read_all(self) -> list:
        data = []
        for result in self.collection.find({}):
            result['_id'] = str(result['_id'])
            data.append(result)

        return data

    def read(self, id: str) -> dict:
        result = self.collection.find_one({'_id': self.get_objectid(id)})

        if not result:
            return {}

        result['_id'] = str(result['_id'])
        return result
    
    def get_query(self, query: str) -> dict:
        result = self.collection.find_one({'query': query})

        if not result:
            return {}

        result['query'] = str(result['query'])
        return result

    def get_id(self) -> list:
        data = []
        for result in self.collection.find({}):
            result['_id'] = str(result['_id'])
            data.append(result['_id'])

        return data