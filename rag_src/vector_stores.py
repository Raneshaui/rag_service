from idlelib.searchengine import search_reverse

import config_data as config
from langchain_chroma import Chroma

"""
向量检索器：可以优化
"""
class VectorStoreService(object):
    def __init__(self,embedding):
        """
           :param embedding:嵌入模型的传入
        """
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config.collection_name, #数据库的表名
            embedding_function=embedding,
            #DashScopeEmbeddings(model="text-embedding-v4"
             #                                      ,dashscope_api_key=config.DASHSCOPE_API_KEY), #向量模型
            persist_directory=config.persist_directory
        )

    def get_retriever(self):
        """返回向量检索器，方便加入chain"""
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})

