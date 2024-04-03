# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)
 

@app.route("/")
@app.route('/quotes')
def show_quotes():
    
    response_API = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en')
    data = response_API.text
    parse_json = json.loads(data)
    quote = parse_json['quoteText']
    
    author = parse_json['quoteAuthor']
    return render_template('quotes.html', quote=quote, author=author)

# main driver function
if __name__ == '__main__':
    app.run(debug=True)