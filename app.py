from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form['code']
    language = request.form['language']
    
    if language == 'python':
        result = execute_python_code(code)
        return jsonify({'result': result})
    
    return jsonify({'result': 'Unsupported language'})

def execute_python_code(code):
    try:
        result = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output

if __name__ == '__main__':
    app.run(debug=True)
