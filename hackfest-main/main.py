from adapters.llm_model import LLM
from models.database import Database
from llm_prompt import promptLearning
from dotenv import load_dotenv

from langchain_experimental.sql import SQLDatabaseChain

class StartEngine:
    def __init__(self):
        load_dotenv()

        # local LLM
        llm = LLM(temperature=0.2)

        # local database
        database = Database(db_path="data/dataset.db")
        database = database.get_db()

       
        prompt = promptLearning(metadata_path="data/meta_data.json",
                                prompt_path="data/prompt.txt")
        

        example_selector=prompt.get_example_selector()
        
        print(example_selector.select_examples({"Question": """Which brand grew their revenue at the slowest rate
                                   (either revenue share or absolute revenue) compared to the prior period?"""}))
        
        print(example_selector)


        # self.chain = SQLDatabaseChain.from_llm(llm, database, verbose=True, prompt=prompts)
        
        # result = self.chain("Which brand grew their revenue at the slowest rate (either revenue share or absolute revenue) compared to the prior period?")

        # print(result)
        # result = vectorstore.similarity_search('text1')
        

    def get_response(self, question):

        return self.chain.run(question)




if __name__ == "__main__":
    
    engine = StartEngine()
    # get_connection()
    


    