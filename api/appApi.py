from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
class Language(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(180))
    def __repr__(self):
        return f"{self.name} - {self.description}"
db.create_all()
@app.route('/')
def index():
    return 'Hello!'

@app.route('/languages')
def get_languages():
    languages = Language.query.all()
    output = []
    for language in languages:
        language_data = {'name' : language.name, 'description' : language.description}
        output.append(language_data)
    return {"Programming Language" : output}
@app.route('/languages/<id>')
def get_language(id):
    language = Language.query.get_or_404(id)
    return {'name': language.name, 'description':language.description} 
@app.route('/languages', methods=['POST'])
def add_language():
    language = Language(name=request.json['name'], description=request.json['description'])
    db.session.add(language)
    db.session.commit()
    return {'id': language.id}
@app.route('/languages/<id>',methods=['DELETE'])
def delete_language(id):
    language= Language.query.get(id)
    if language is None:
        return {'error' : 'not found'}
    db.session.delete(language)
    db.session.commit()
    return {'message' : 'Deleted successfully'}
