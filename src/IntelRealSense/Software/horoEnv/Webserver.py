from flask import Flask, escape, request

global test

app = Flask(__name__)

@app.route('/') 
def hello():
    return "Hello World"
   

#if __name__ == '__main__':
#    app.run()

def start():
    app.run()

def setFoto(_image):
    test = _image
