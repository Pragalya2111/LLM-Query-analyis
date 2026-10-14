from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import LanceDB,Chroma
from langchain import SQLDatabase
import json


from models.vector_db import get_connection

from few_shots import few_shots
db_path = "C:/Gokul/hackfest/dataset.sqlite"  

# db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=3)
# llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)

# with open('data\meta_data.json', 'r') as file:
#     meta_data = json.load(file)

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
to_vectorize = [" ".join(example.values()) for example in few_shots]

vectorstore = Chroma.from_texts(texts=to_vectorize, embedding=embeddings, metadatas=few_shots)


# example_selector = SemanticSimilarityExampleSelector(
#     vectorstore=vectorstore,
#     k=2,
# )

# print(example_selector)
