from loguru import logger
import json
import pandas as pd
from simpletransformers.classification import ClassificationModel

from search_classify_tweets.projeto import settings
from search_classify_tweets.projeto.constants import mensagens


class Classificador():

    def __init__(self):

        train_args_path = settings.TRAIN_ARGS_PATH
        weights_path = settings.WEIGHTS_PATH

        f = open(train_args_path)
        train_args = json.load(f)['train_args']

        self.model = ClassificationModel('bert', weights_path, args=train_args,
                                         num_labels=2, use_cuda=settings.USE_CUDA)

        logger.debug(mensagens.MODEL_DEVICE)
        logger.debug(self.model.device)

    def get_predict(self, df, input_query):
        '''
            Método estático para realizar o predict do modelo Bert.
        '''
        df['text'] = df['text'].astype(str)
        df["text"] = df["text"].tolist()

        predictions, raw_outputs = self.model.predict(df["text"])
        df['predict'] = pd.DataFrame(predictions)
        df['query'] = input_query
        return df
