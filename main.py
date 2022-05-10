from crypt import methods
from time import clock_getres

from requests import request
from flask import Flask, render_template, Response,request
from camera import VideoCamera

app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def index():
    global r , g , b # r g b variable for use in any function
    r , g , b = 110,5,46
    if(request.method=='POST'):
        r=request.form['r'] # change value of r
        g=request.form['g'] # change value of g
        b=request.form['b'] # change value of b
        
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame(r,g,b)
        # for continues framing for video stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
