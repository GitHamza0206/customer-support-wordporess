
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

import os 

class Rag:
    def __init__(self):
        self.gpt4o = ChatOpenAI(model_name="gpt-4o", temperature=0)
        self.groq = ChatGroq(model_name="mixtral-8x7b-32768")
        self.openai_embeddings = OpenAIEmbeddings() 
        current_path = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.dirname(current_path)
        self.assets_path = os.path.join(parent_folder, "assets")

        self.retriever = self.retrieve_document()


    

    def load_and_split_documents(self):  

        loader = PyPDFLoader(os.path.join(self.assets_path, "kb.pdf"))
        pages = loader.load_and_split()

        docs= []
        for markdown_file in os.listdir(self.assets_path):
            if markdown_file.endswith(".md"):
                markdown_path = os.path.join(self.assets_path, markdown_file)
                loader = UnstructuredMarkdownLoader(markdown_path)
                docs.append(loader.load()[0])
                print(f"✅ added document {markdown_file}")
            

        
        
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=200
        )
        doc_splits = text_splitter.split_documents(docs)
        doc_splits.extend(pages)

        return doc_splits
    
    def retrieve_document(self):
        splits = self.load_and_split_documents()
        vectorstore = FAISS.from_documents(documents=splits, embedding=self.openai_embeddings)
        return vectorstore.as_retriever()

    def make_rag_chain(self):
    # We will use a prompt template from langchain hub.
        # Prompt
        #prompt = hub.pull("rlm/rag-prompt")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                            You are a useful assistant that can help with questions about dakshampoo-shop.nl.
                            You can provide information about the products, the company, the website, etc.
                            You can also provide general information about the domain.
                            Your goal is to provide helpful information to the user.
                            You can suggest useful links to the user. the links should be relevant to the user's question.
                            You can base your response on kb.pdf 
                            Your response should be in the same language as the user's question.
                 
                        """),
                ("human", """
                            You are an assistant for question-answering tasks. 
                            Use the following pieces of retrieved context to answer 
                            the question.
                            If you don't know the answer, 
                            just say that you don't know. Use three sentences maximum 
                            and keep the answer concise.
                            Question: {input} 
                            Context: {context} 
                            Answer:
                    """),
            ]
        )
        # LLM
        llm = self.gpt4o
        # Chain
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        chain = create_retrieval_chain(self.retriever, question_answer_chain)

        return chain


    def run(self, question, st_callback=None):
        # Run
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        
        rag_chain = self.make_rag_chain()
        #{"callbacks":[st_callback]}
        if st_callback:
            return rag_chain.invoke( {"input": question, "callbacks":[st_callback]})
        
        return rag_chain.invoke( {"input": question})



if __name__ == "__main__":
    rag = Rag()
    
    response = rag.run("wat verkoop je?")
    print(response)