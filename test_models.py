import google.generativeai as genai

genai.configure(api_key="AIzaSyBuzmzGY1hG0E-1ovCwiE0nuwSO-5pPQ_Y")

models = genai.list_models()

for model in models:
    print(model.name)