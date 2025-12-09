from flask import Flask, render_template
import socket

app = Flask(__name__)

@app.route('/')
def home():
    nom_machine = socket.gethostname()
    return render_template('index.html', name_pc=nom_machine)

if __name__ == '__main__':
    app.run(debug=True)