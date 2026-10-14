from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
import json

from langchain.vectorstores import LanceDB
from langchain.vectorstores import Chroma
from models.database import get_connection


class promptLearning:
    def __init__(self,metadata_path,prompt_path):
        self.metadata_path=metadata_path
        self.prompt_path=prompt_path
    def get_example_prompt(self):
        
        example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
        )
        return example_prompt
    def get_metadata(self):
        try:
            with open(self.metadata_path, 'r') as file:
                meta_data = json.load(file)
            return meta_data
        except Exception as e:
            return {}
    def get_vectors(self):
        return [" ".join(example.values()) for example in self.get_metadata()]
    
    def get_embeddings(self):
        return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    
    def get_vectorstore(self):
        
        embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        
        # vectorstore = LanceDB(get_connection(), embedding_function)
        vectorstore = Chroma.from_texts(texts=self.get_vectors(),
                              metadatas=self.get_metadata(),embedding=embedding_function, 
                              )

        # vectorstore = LanceDB.from_texts(cls=[],
        #                                  texts=self.get_vectors(), 
        #                                  embedding=embedding_function, 
        #                                  metadatas=self.get_metadata(),
        #                                  connection=get_connection(), 
        #                                  )
        return vectorstore
    

    def get_example_selector(self):
        example_selector = SemanticSimilarityExampleSelector(
            vectorstore=self.get_vectorstore(),
            k=2,
        )
        return example_selector
    
    def promt_reader(self):
    
        with open(self.prompt_path,'r') as f:
            mysql_prompt=f.read()
        return mysql_prompt
    
    def few_shots(self):
        few_shot_prompt = FewShotPromptTemplate(
            example_selector=self.get_example_selector(),
            example_prompt=self.get_example_prompt(),
            prefix=self.promt_reader(),
            suffix=PROMPT_SUFFIX,
            input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
        )
        return few_shot_prompt

if __name__=='__main__':

    pobj=promptLearning("data\\meta_data.json","data\\prompt.txt")
    print(pobj.get_example_selector())