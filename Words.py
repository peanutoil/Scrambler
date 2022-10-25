from flask import *
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId
import random


fl = Flask("run")
fl.config['MONGO_URI'] = "mongodb://localhost:27017/jumbled-words-db"
mongo = PyMongo(fl)
Bootstrap(fl)


@fl.route("/", methods=["GET", "POST"])
def route():
    if request.method == "GET":
        return render_template("jumbled.html")
    elif request.method == 'POST':
        return redirect("/")


@fl.route("/jumble", methods=["GET", "POST"])
def jumbling():
    if request.method == "GET":
        return render_template("jumbling.html")
    elif request.method == 'POST':
        word = request.form['word'].strip().upper()
        document = {'word': word}
        duplicate = mongo.db.JumbledWords.find_one({'word': word})
        # special type None
        if (duplicate is None):
            mongo.db.JumbledWords.insert_one(document)
        else:
            return redirect("/jumble")
        return redirect("/")


@fl.route("/figureout", methods=["GET", "POST"])
def figuring():
    if request.method == "GET":
        allWords = list(mongo.db.JumbledWords.find({}))
        print(allWords)
        wordList = []
        for i in allWords:
            listword = list(i['word'])
            random.shuffle(listword)
            word = "".join(listword)
            i['word'] = word
        return render_template("figuring.html", allWords=allWords)
    elif request.method == 'POST':
        score = 0
        allWords = mongo.db.JumbledWords.find({})
        for i in allWords:
            idNum = str(i['_id'])
            answer = request.form[idNum].strip().upper()
            if answer==i['word']:
                score+=1
        return render_template("results.html",score=score)


fl.run(debug=True)
