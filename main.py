from flask import Flask, request, jsonify
import json

app = Flask(__name__)

global data


@app.route('/add/<a>/<b>')
def add(a, b):
    try:
        result = float(a) + float(b)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numeric values.'}), 400

@app.route('/subtract/<a>/<b>')
def subtract(a, b):
    try:
        result = float(a) - float(b)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numeric values.'}), 400

@app.route('/multiply/<a>/<b>')
def multiply(a, b):
    try:
        result = float(a) * float(b)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numeric values.'}), 400

@app.route('/divide/<a>/<b>')
def divide(a, b):
    try:
        b_float = float(b)
        if b_float == 0:
            return jsonify({'error': 'Cannot divide by zero'}), 400
        result = float(a) / b_float
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numeric values.'}), 400

global data

# read data from file and store in global variable data
with open('data.json') as f:
    data = json.load(f)


@app.route('/')
def hello_world():
    return 'Hello, World!'  # return 'Hello World' in response

@app.route('/students')
def get_students():
  result = []
  pref = request.args.get('pref') # get the parameter from url
  if pref:
    for student in data: # iterate dataset
      if student['pref'] == pref: # select only the students with a given meal preference
        result.append(student) # add match student to the result
    return jsonify(result) # return filtered set if parameter is supplied
  return jsonify(data) # return entire dataset if no parameter supplied

# route variables
@app.route('/students/<id>')
def get_student(id):
  for student in data: 
    if student['id'] == id: # filter out the students without the specified id
      return jsonify(student)

@app.route('/stats')
def get_stats():
    meal_prefs = {}
    programmes = {}

    for student in data:
        pref = student['pref']
        meal_prefs[pref] = meal_prefs.get(pref, 0) + 1

        prog = student['programme']
        programmes[prog] = programmes.get(prog, 0) + 1

    return jsonify({
        'meal_preferences': meal_prefs,
        'programmes': programmes
    })


app.run(host='0.0.0.0', port=8080, debug=True)