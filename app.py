from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from extensions import db
from models import Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db.init_app(app)

@app.route('/')
def index():
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    note = Note(title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.updated_at = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', note=note)

@app.route('/delete/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",debug=True)
