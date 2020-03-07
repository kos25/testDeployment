from flask import Flask  , request    
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:7898994162k@localhost:5432/denmo2'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)
 
class Tasklists(db.Model):
   __tablename__ = "tasklits"
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String)
   
 
   def __init__(self, name):
    self.name = name
    print("data created")
 
 
 
 
class Tasks(db.Model):
   __tablename__ = "tasks"
   id = db.Column(db.Integer, primary_key = True)
   text = db.Column(db.String)
   Completed = db.Column(db.Boolean)
   list_id = db.Column(db.Integer)
 
   
 
   def __init__(self, text ,list_id):
    self.text = text
    self.list_id = list_id
    self.Completed = False
    
  
 
 
@app.route('/tasklits')  
def get_task_list():  
      task_lists = Tasklists.query.all()
      task_lists_list =[] 
      for task_list in task_lists:
        t={}
        t["id"] = task_list.id
        t["name"] = task_list.name    
        task_lists_list.append(t)
 
      return jsonify(list=task_lists_list) 
 
 
 
@app.route('/tasklits', methods = ['POST'])  
def create_task_list():
   data = request.get_json()
   name = data["name"]
   tl =  Tasklists(name) 
   db.session.add(tl)
   db.session.commit()
   return jsonify(message ="task list created") , 201
 
 
@app.route("/tasks")
def get_tasks():
   Task_list_id = request.args.get('task_list')
   tasks = Tasks.query.filter_by(list_id = Task_list_id)
   task_list = []
   for task in tasks:
      t={}
      t["id"]=task.id
      t["text"] = task.text
      t["Completed"] = task.Completed      
      t["task_id"] = task.list_id
      task_list.append(t)
   return jsonify(task=task_list)
 
 
@app.route('/tasks', methods = ['POST'])  
def create_task():
   data = request.get_json()
   text = data["text"]
   list_id = data["list_id"]   
   tl =  Tasks(text,list_id) 
   db.session.add(tl)
   db.session.commit()
   return jsonify(message ="task  created") , 201 
 
 
@app.route('/tasks/<id>', methods = ['PUT'])
def update_task(id):   
   task = Tasks.query.filter(id = id).first()
   task.Completed = not(task.Completed)
   db.session.add(task)
   db.session.commit()
   return jsonify(message = "task updated" , task_id = task.id, task_Completed = task.Completed)
   
    
@app.route('/')
def get_task_lists(name):
 return "hello world"
 
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)   
