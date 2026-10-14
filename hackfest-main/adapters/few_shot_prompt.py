from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import json


class promptlearning:
    def __init__(self,metadata_path):
        self.metadata_path=metadata_path
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
        vectorstore = Chroma.from_texts(texts=self.get_vectors(), embedding=self.get_embeddings(), metadatas=self.get_metadata())
        return vectorstore
    def get_example_selector(self):
        example_selector = SemanticSimilarityExampleSelector(
            vectorstore=self.get_vectorstore(),
            k=2,
        )
        return example_selector
    
    def get_sql_prompt(self):
        ### my sql based instruction prompt
        mysql_prompt = """You are a SQLLITE expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
        Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
        Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
        Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
        Pay attention to use CURDATE() function to get the current date, if the question involves "today".

        Use the following format:

        Question: Question here
        SQLQuery: Query to run with no pre-amble
        SQLResult: Result of the SQLQuery
        Answer: Final answer here

        No pre-amble.
        """
        return mysql_prompt
    def few_shots(self):
        few_shot_prompt = FewShotPromptTemplate(
            example_selector=self.get_example_selector(),
            example_prompt=self.get_example_prompt(),
            prefix=self.get_sql_prompt(),
            suffix=PROMPT_SUFFIX,
            input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
        )
        return few_shot_prompt

if __name__=='__main__':

    pobj=promptlearning("data\\meta_data.json")
    print(pobj.get_metadata())