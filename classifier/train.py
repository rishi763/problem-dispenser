import pickle
import os
import json
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier


vectorizer = CountVectorizer(stop_words='english')


category_map = {
    "A": 0,
    "C": 1,
    "G": 2,
    "N": 3
}


def gather_data():

    problem_files = []
    for root, directory, files in os.walk("data/problems"):
        for file in files:
            if file.endswith(".json"):
                problem_files.append(os.path.join(root, file))
    data = {"texts": [], "categories": []}

    for problem_file in problem_files:
        with open(problem_file, "r") as problem_json:
            json_data = json.load(problem_json)
            if json_data["category"] != "":
                data["texts"].append(json_data["latex"])
                data["categories"].append(
                    category_map.get(json_data["category"]))
    return data

def tokenize(text):
    detex_text=""
    for character in     text:




def process_data(data):

    data["texts"] = [text.strip().lower() for text in data["texts"]]

    text_train, text_test, category_train, category_test = train_test_split(
        data["texts"], data["categories"], stratify=data["categories"], test_size=0.2, random_state=42)

    text_train = vectorizer.fit_transform(text_train).toarray()
    text_test = vectorizer.transform(text_test).toarray()
    category_train = np.array(category_train)
    category_test = np.array(category_test)

    return text_train, text_test, category_train, category_test


def train():
    text_train, text_test, category_train, category_test = process_data(
        gather_data())
    model = MultinomialNB(alpha=1)
    model.fit(text_train, category_train)
    score = model.score(text_test, category_test)
    print("Score:", score)
    with open("classifier/model.pickle", "wb") as model_file:
        pickle.dump((vectorizer, model, score), model_file)
    return (vectorizer, model, score)
