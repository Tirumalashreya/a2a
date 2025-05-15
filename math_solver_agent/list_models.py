import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("AIzaSyBlIOeZJqMS0ChTnxl6N5JYPXNq3DMmaq8"))

def list_models():
    models = genai.list_models()
    for model in models:
        print(model)

if __name__ == "__main__":
    list_models()
