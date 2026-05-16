import google.generativeai as genai

genai.configure(api_key="AIzaSyCuCDxsahx5UKS_EGubmV7s2bEF8VP59gI")

models = genai.list_models()

for model in models:
    print(model.name)