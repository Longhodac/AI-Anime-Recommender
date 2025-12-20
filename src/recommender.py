from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.prompt_template import get_anime_prompt

class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
        self.llm = ChatGroq(api_key=api_key, model=model_name, temperature=0)
        self.retriever = retriever
        self.prompt = get_anime_prompt()

        # Create RAG chain using LCEL (LangChain Expression Language)
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.qa_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_recommendation(self, query: str):
        result = self.qa_chain.invoke(query)
        return result
    