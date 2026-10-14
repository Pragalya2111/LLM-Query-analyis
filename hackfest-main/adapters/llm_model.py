from langchain.llms import GooglePalm
import os

class LLM:
    def __init__(self,temperature=0.2):
        self.api_key = os.getenv("GOOGLEPALM_API_KEY")
        self.temperature=temperature
        
    def get_palm(self):
        return GooglePalm(google_api_key=self.api_key, temperature=self.temperature)

    
    
    
    