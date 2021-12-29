from flask import render_template, request, redirect
from flask.helpers import url_for
from src import app
from src.models import typechecker



InputText = []
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/demo', methods=["POST", "GET"])
def demo_page():
    if request.method == "POST":
        text = request.form.get("inputtext")
        
        result = typechecker(text)
        
        return render_template('demo.html', initialtext=text ,finaltext=result)
    
    else:
        return render_template('demo.html')
