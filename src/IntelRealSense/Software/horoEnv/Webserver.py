from flask import Flask, escape, request,render_template, Response

global test

app = Flask(__name__)

@app.route('/') 
def index():
    """Video streaming home page."""
    return render_template("index.html")
   
def gen():
    global test
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + test + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
#if __name__ == '__main__':
#    app.run()

def start():
    app.run()

def setFoto(_image):
    global test
    test = _image
