from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    if not os.path.exists('notes.db'):
        db.create_all()

with app.app_context():
    init_db()

@app.route('/')
def index():
    query = request.args.get('q', '')
    if query:
        notes = Note.query.filter(Note.content.contains(query)).order_by(Note.updated_at.desc()).all()
    else:
        notes = Note.query.order_by(Note.updated_at.desc()).all()
    return render_template('index.html', notes=notes, query=query)

@app.route('/note/new', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            note = Note(content=content)
            db.session.add(note)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('note_form.html', note=None)

@app.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            note.content = content
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('note_form.html', note=note)

@app.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 