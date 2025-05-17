from fastapi import FastAPI, Query
import json

app = FastAPI()

with open("data/knowledge_base.json", "r") as f:
    kb = json.load(f)

@app.get("/faq")
def get_faq(city: str, location: str, question: str):
    try:
        faqs = kb[city][location]["faq"]
        for q in faqs:
            if question.lower() in q.lower():
                return {"answer": faqs[q]}
        return {"answer": "Sorry, I couldn't find that."}
    except:
        return {"answer": "Invalid city or location."}
