import random
from time import time
from flask import Flask, render_template, request, redirect, url_for
import os

def checkLine(sample, line, start):
    if sample.split() == line.split():
        return [sample, [["sample", sample]], round(time() - start, 2), round(len(line) / (time() - start) * 60, 2), "ok"]
    result = [sample, [], round(time() - start, 2), round(len(line) / (time() - start) * 60, 2), "fail"]
    i = 0
    for i in range(len(line)):
        if len(sample) <= i:
            result[1].append(["bad", line[i:]])
            break
        elif sample[i] == line[i]:
            result[1].append(["sample", line[i]])
        else:
            result[1].append(["bad", line[i]])
    else:
        if i < len(sample):
            result[4] = "fail"
            result[1].append(["bad", " " * (len(sample) - i)])
    return result


app = Flask(__name__, template_folder=os.getcwd())

D = {}
with open("dictionaries/python.txt") as file:
    D["python"] = file.read().splitlines()
with open("dictionaries/python+.txt") as file:
    D["python+"] = file.read().splitlines()
with open("dictionaries/cpp.txt") as file:
    D["cpp"] = file.read().splitlines()
with open("dictionaries/cpp+.txt") as file:
    D["cpp+"] = file.read().splitlines()
with open("dictionaries/java.txt") as file:
    D["java"] = file.read().splitlines()
with open("dictionaries/pascal.txt") as file:
    D["pascal"] = file.read().splitlines()

best = [0, 0, 0, 0, 0]
redirected = False
runs = []
current = ""
start = 0
numWords = 10
fName = "python"


@app.route("/")
@app.route("/index")
def index():
    global runs, current, start, numWords, fName, best, redirected
    if not redirected:
        runs = []
        current = ""
        start = 0
        numWords = 10
        fName = "python"
    redirected = False
    return render_template("index.html", d=fName, n=numWords, current=current, active=not bool(runs), runs=runs, result=[len([x for x in runs if x[-1] == "ok"]), len([x for x in runs if x[-1] == "fail"]), sum(len(x[0]) for x in runs), round(sum(x[2] for x in runs), 1), round(sum(x[3] for x in runs) / numWords, 2)], best=best)

@app.route("/data", methods=["POST"])
def data():
    global runs, current, start, numWords, fName, best, redirected
    if request.method == 'POST':
        if "fName" in request.form:
            runs = []
            numWords = int(request.form["numWords"])
            fName = request.form["fName"]
        elif not request.form:
            runs = []
        if "input" in request.form:
            runs.append(checkLine(current, request.form.get("input").rstrip(" "), start))
        if len(runs) < numWords:
            current = random.choice(D[fName])
            start = time()
            redirected = True
            return redirect(url_for('index'))
        current=""
        result = [len([x for x in runs if x[-1] == "ok"])]
        result.append(len(runs) - result[0])
        result.append(sum(len(x[0]) for x in runs))
        result.append(round(sum(x[2] for x in runs), 1))
        result.append(round(sum(x[3] for x in runs) / numWords, 2))
        if result[4] > best[4]:
            best = result
        redirected = True
        return redirect(url_for('index'))

if __name__ == "__main__":
    from waitress import serve
    print("http://localhost:5000/")
    serve(app, host="0.0.0.0", port=5000)