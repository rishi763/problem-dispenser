import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pickle
from train import train

number_category_map = {
    0: "A",
    1: "C",
    2: "G",
    3: "N"
}


def predict(problem):
    if os.path.exists("classifier/model.pickle"):
        with open("classifier/model.pickle", "rb") as model_file:
            (vectorizer, model, score) = pickle.load(model_file)

    else:
        (vectorizer, model, score) = train()

    problem = problem.strip().lower()

    category_number = model.predict(
        vectorizer.transform([problem]).toarray())[0]
    return number_category_map.get(category_number)


print(predict("Let $\\mathbb{Z}$ be the set of integers. Determine all functions $f: \\mathbb{Z} \\rightarrow \\mathbb{Z}$ such that, for all integers $a$ and $b$, $$f(2a)+2f(b)=f(f(a+b)).$$\\textit{Proposed by Liam Baker, South Africa}"))
vec = CountVectorizer()


#tokenize("Let $\\mathbb{Z}$ be the set of integers. Determine all functions $f: \\mathbb{Z} \\rightarrow \\mathbb{Z}$ such that, for all integers $a$ and $b$, $$f(2a)+2f(b)=f(f(a+b)).$$\\textit{Proposed by Liam Baker, South Africa}")