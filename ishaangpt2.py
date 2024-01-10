import os
import sys

# Assuming you have Google API credentials and required libraries installed
# from google_generative_ai import GoogleGenerativeAI  # This is hypothetical, replace with actual library name

import constants
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator



os.environ["GOOGLE_API_KEY"] = constants.APIKEY  # Hypothetical, replace with actual method to set Google API key
llm = ChatGoogleGenerativeAI(model="gemini-pro")
# result = llm.invoke("who was the winner of the 2022 super bowl")
# print(result.content)

os.environ["GOOGLE_API_KEY"] = constants.APIKEY  # Hypothetical, replace with actual method to set Google API key

query = sys.argv[1]

loader = TextLoader("ishaan_f23.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

generated_text = google_ai.generate_text(query)

print(generated_text)

# # Initialize the Google Generative AI client
# google_ai = GoogleGenerativeAI(api_key=constants.APIKEY)  # Replace with actual method or class for Google's API

# # Assuming there's a similar method in Google's API for text generation
# generated_text = google_ai.generate_text(query)

# # Print or use the generated text as needed
# print(generated_text)
