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
    elif language == 'java':
        result = execute_java_code(code)
        return jsonify({'result': result})
    else:
        return jsonify({'result': 'Unsupported language'})

def execute_java_code(code):
    try:
        with open('temp.java', 'w') as file:
            file.write(code)
        
        compile_output = subprocess.check_output(['javac', 'temp.java'], stderr=subprocess.STDOUT, text=True)
        
        if compile_output:
            return compile_output
            
        run_output = subprocess.check_output(['java', '-cp', '.', 'temp'], stderr=subprocess.STDOUT, text=True)
        return run_output
    except subprocess.CalledProcessError as e:
        return e.output
    finally:
        os.remove('temp.java')
        if os.path.exists('temp.class'):
            os.remove('temp.class')








def execute_python_code(code):
    try:
        result = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output

if __name__ == '__main__':
    app.run(debug=True)
