import random
from time import time
from flask import Flask, render_template, request

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


app = Flask(__name__)
runs = []
current = ""
start = 0
numWords = 10
fName = ""
D = {}
best = [0, 0, 0, 0, 0]
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


@app.route("/", methods=["GET", "POST"])
def index():
    global runs, current, start, numWords, fName, best
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
            return render_template("index.html", active=False, runs=runs, current=current)
        result = [len([x for x in runs if x[-1] == "ok"])]
        result.append(len(runs) - result[0])
        result.append(sum(len(x[0]) for x in runs))
        result.append(round(sum(x[2] for x in runs), 1))
        result.append(round(sum(x[3] for x in runs) / numWords, 2))
        if result[4] > best[4]:
            best = result
        return render_template("index.html", active=False, runs=runs, result=[len([x for x in runs if x[-1] == "ok"]), len([x for x in runs if x[-1] == "fail"]), sum(len(x[0]) for x in runs), round(sum(x[2] for x in runs), 1), round(sum(x[3] for x in runs) / numWords, 2)], best=best)
    return render_template("index.html", active=True)


app.run()
