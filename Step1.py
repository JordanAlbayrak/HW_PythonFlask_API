import json
from flask import request, jsonify, abort
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
def home():
    return "<h1>Home Page</h1>"


@app.route("/tasks", methods=['GET'])
def getAll():
    file = open('tasks.json')
    tasks = json.load(file)
    file.close()
    return jsonify(tasks['tasks'])


@app.route('/tasks/<int:task_id>', methods=['GET'])
def getById(task_id):
    file = open('tasks.json')
    tasks = json.load(file)
    file.close()
    for task in tasks['tasks']:
        if task['id'] == int(task_id):
            return jsonify(task)
    abort(404)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def updateTask(task_id):
    indexSelected = -1
    taskSelected = []
    file = open('tasks.json')
    tasks = json.load(file)
    file.close()

    for i in range(len(tasks['tasks'])):
        if tasks['tasks'][i]['id'] == task_id:
            taskSelected = tasks['tasks'][i]
            indexSelected = i
    if taskSelected == []:
        abort(404)
    if not request.json:  # JSON BODY NOT PROVIDED
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)  # NON UNICODE DATA IN FIELD
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)  # NON UNICODE DATA IN FIELD
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)  # DONE FIELD NOT BOOLEAN EXPECTED VALUE
    if request.json:
        file = open('tasks.json', 'w')
        taskSelected['id'] = task_id
        taskSelected['title'] = request.json['title']
        taskSelected['description'] = request.json['description']
        taskSelected['done'] = request.json['done']
        tasks['tasks'][indexSelected] = taskSelected
        print(tasks)
        json.dump(tasks, file)
        file.close()
    return jsonify(taskSelected)

@app.route('/tasks', methods=['POST'])
def addTask():
    length = 0
    file = open('tasks.json')
    tasks = json.load(file)
    file.close()
    length = len(tasks['tasks'])

    if not request.json:  # JSON BODY NOT PROVIDED
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)  # NON UNICODE DATA IN FIELD
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)  # NON UNICODE DATA IN FIELD
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)  # DONE FIELD NOT BOOLEAN EXPECTED VALUE
    if request.json:
        actualArray = {}
        actualArray['id'] = int(length + 1)
        actualArray['title'] = request.json['title']
        actualArray['description'] = request.json['description']
        actualArray['done'] = request.json['done']
        tasks['tasks'].append(actualArray)
        f = open('tasks.json', 'w')
        json.dump(tasks, f)
        f.close()
    return jsonify(actualArray)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def deleteTask(task_id):
    indexSelected = -1
    taskSelected = []
    file = open('tasks.json')
    tasks = json.load(file)
    file.close()

    for i in range(len(tasks['tasks'])):
        if tasks['tasks'][i]['id'] == task_id:
            taskSelected = tasks['tasks'][i]
            indexSelected = i
    if taskSelected == []:
        abort(404)

    if not request.json:  # JSON BODY NOT PROVIDED
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)  # NON UNICODE DATA IN FIELD
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)  # NON UNICODE DATA IN FIELD
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)  # DONE FIELD NOT BOOLEAN EXPECTED VALUE
    if request.json:
        del tasks['tasks'][indexSelected]
        file = open('tasks.json', 'w')
        json.dump(tasks, file)
        file.close()
    return jsonify(taskSelected)

app.run()
