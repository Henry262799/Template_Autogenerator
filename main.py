from inspect import getsource
from flask import Flask, render_template, request
from template_app import Builder, Template
#import sys
import json
from dill.source import getsource

app=Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    templ=request.form['template']
    #print(type(templ))
    cont=str(request.form['context'])
    #value=json.loads(cont)
    new_value=eval(cont)
    #return new_value
    obj=Template(templ,new_value)

    

    return render_template("submit.html",result=obj.function_str)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

