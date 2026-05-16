from langchain_community.chat_models import ChatTongyi
from langchain_core import documents
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from rag_src.file_history_store import get_history
from rag_src.vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.chat_models import init_chat_model
from rag_src.utils.pormptLoader import promptloaderservice
import config_data as config

def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt

class RagService:
    def __init__(self):

        self.vertor_service = VectorStoreService(
            embedding=DashScopeEmbeddings(
                model=config.embedding_model_name,
                dashscope_api_key=config.DASHSCOPE_API_KEY
            )
        )

        systen_prompt = promptloaderservice()
        self.prompt_template = ChatPromptTemplate(
            [
                ("system", systen_prompt),
                ("system","并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                (
                    "user","请回答用户提问：{input}"
                )
            ]
        )

        self.chat_model =   init_chat_model(
            model=config.chat_model_name,
            model_provider="openai",
            base_url = config.OPENAI_BASE_URL,
            api_key=config.OPENAI_API_KEY
        )

        self.chain = self._get_chain()


    def _get_chain(self):
        """获取最终的执行链"""
        retriever = self.vertor_service.get_retriever()

        def format_document(docs:list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        def format_for_prompt_template(value):
            # {input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        from langchain_core.runnables import RunnableLambda
        chain = (
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(format_for_retriever) | retriever | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt |self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )

        return conversation_chain

if __name__ == '__main__':
    # session id 配置
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }

    res = RagService().chain.invoke({"input": "针织毛衣如何保养？如果没有参考资料，请根据通用常识回答"}, session_config)
    print(res)



