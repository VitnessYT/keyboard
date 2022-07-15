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


app = Flask(__name__)

"""
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
"""
D = {
"python": ['a = int(input())', 'from math import *', 'if a != 0:', 'for i in range(n):', 'for x in a:', 'while a != 0:', 'print(a, b, sep="")', 'a = [0] * n', 'a = [0 for i in range(n)]', 'a, b = map(int, input().split())', 'f = True', 'f = False', 'if a % 2 == 0:', 'if a == 0 and b == 0:', 'elif a == 0 or b == 0:', 'while i * i <= n:', 'if a ** 2 + b ** 2 == c ** 2:', 'print(sqrt(a))', 'assert a != 0', 'def add(u, v):', 'if was[i] != 0:', 'return', 'while r - l > 1:', 'def less(a, b):', 'for i in range(1, n, 2):', 'print("Hello world")', 'def max(a, b):', 'break', 'continue', 'while i <= x ** 2:', 'print(0.5 * b * h)', 'print(n // 60 % 24, n - (n // 60 * 60))', 'print(n // 60 % 24, n % 60)', 'print("The next number for the number", x, "is", x + 1)', 'print(f"The next number for the number {x} is {x + 1}")', 'print("The next number for the number " + str(x) + " is " + str(x + 1))', 'print(min(a, b))', 'return (x1 + y1 + x2 + y2) % 2 == 0', 'return year % 4 == 0 and year % 100 != 0 or year % 400 == 0', 'print(*list, sep="\n")', 'numbers = list(range(100))', 'dict = {chr(i): 0 for i in range(ord("A"), ord("B") + 1)}', 'print(((n * (n + 1)) / 2) ** 2)', 'from itertools import combinations', 'import re', 'print(string.count("333") / string.count("777"))', 'print(string[::-1])', 'print(*string, sep="&")', 'if n - j - 1 == i:', 'def swap_columns(a, i, j):', 'from time import time, sleep', 'print([i ** 2 for i in range(10)])', 'a, b, c = int(input()), int(input()), int(input())', 'print((3 * x ** 3 + 18 * x ** 2) * x + 12 * x ** 2 - 5)', 'print("{:06d}".format(a+b))', 'x = random.randint(1, 4)', 'A = [1, 2, 3]', 'window = tkinter.Tk()', 'def sum(a, b):', 'return a + b', 'file = open("input.txt", "r")', 'with open("output.txt", "w") as file:', 'print(list, file=file)', '# TODO:', 'del list[5]', 'if "*" in text:', 'A.remove(number)', 'A.extend(list)', 'for char in string:', 'print(string.isdigit())', 'A.sort(key=len, reverse=True)', 'print(sorted(A, reverse=True))', 'avg = sum(A) / len(A)', '"""This is docstring"""', '# This is comment'],
"python+": ["LATER"],
"cpp": ["int main() {", "return 0;", "cout << n << " " << m;", "#include <iostream>", "int n, m;", "cin >> n >> m;", "for (int i = 0; i < n; i++)", "vector<int> a;", "bool ok;", "long double x;", "string s;", "if (a % 2 == 0) {", "x = n / 2 + 1;", "if ((a == 0) || (b == 0))", "if ((a == 0) && (b == 0))", "} else {", "while (i * i < n) {", "while (true) {", "cout << sqrt(a);", "void add(int u, int v) ", "void dfs(int v) ", "if (was[i]) return;", "int rec(int i)", "if (l >= r) return;", "if (s[i] == ' ') d++;", "while (r - l > 1)", "bool less(point a, point b)"],
"cpp+": ["LATER"],
"java": ["LATER"],
"pascal": ["var i:integer;", "a:array[1..100] of integer;", "f:text;", "ok:boolean;", "x:extended;", "s:string;", "record x,y:integer; end;", "for i:=1 to n do begin", "read(n,m);", "write(a,' ',b);", "if a mod 2=0 then begin", "x:=n div 2 + 1;", "for i:=n downto 1 do", "if (a=0) and (b=0) then", "if (a=0) or (b=0) then", "end else begin", "while i*i<n do", "while true do begin", "repeat until false;", "var gr:array[1..100,1..100] of integer;", "assign(f,'input.txt');", "reset(f);", "rewrite(f);", "close(f);", "n:=inttostr(s);", "s:=strtoint(n);", "if sqr(a) + sqr(b) = sqr(c) then", "writeln(sqrt(a));", "if a=0 then break;", "if s='' then continue;", "assert(res=0,'Wrong res');", "procedure add(u,v:integer);", "procedure dfs(u:integer);", "if was[i]<>0 then exit;", "function rec(i:integer):integer;", "if l>=r then exit;", "if s[i]=' ' then inc(d);", "while r-l>1 do begin", "function less(a,b:tpoint):boolean;"]
}

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
    return render_template("index.html", current=current, active=not bool(runs), runs=runs, result=[len([x for x in runs if x[-1] == "ok"]), len([x for x in runs if x[-1] == "fail"]), sum(len(x[0]) for x in runs), round(sum(x[2] for x in runs), 1), round(sum(x[3] for x in runs) / numWords, 2)], best=best)

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
    serve(app, host="https://keyboardup.herokuapp.com/", port=int(os.environ.get('PORT', 8080)))
