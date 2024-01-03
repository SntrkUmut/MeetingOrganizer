from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import json
from controlFunctions import is_valid_date, is_valid_time, is_valid_datetime_format, is_valid_time_range
from datetime import datetime
import validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Bootstrap(app)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    participants = db.Column(db.String(255), nullable=False)
    platform_link = db.Column(db.String(255))

    def __repr__(self):
        return f'<Meeting {self.id}>'

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Retrieve all meetings from the database
    meetings = Meeting.query.all()
    return render_template('index_bootstrap.html', meetings=meetings)


@app.route('/add_meeting', methods=['POST'])
def add_meeting():
    # Get the form data
    topic = request.form.get('topic')
    date = request.form.get('date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    participants = request.form.get('participants')
    platform_link = request.form.get('platform_link')

    # Validate the date format
    if not is_valid_date(date):
        return "Geçersiz tarih formatı. Lütfen GG/AA/YYYY formatında bir tarih girin."

    # Checks that the meeting time is in time format.
    if not is_valid_time(start_time) or not is_valid_time(end_time):
        return "Geçersiz saat formatı. Lütfen SS:DD formatında bir saat girin."

    # Checks that the end of the meeting is not earlier than the start time.
    if not is_valid_time_range(start_time, end_time):
        return "Toplantı bitiş zamanı, başlangıç zamanından daha önce olamaz."

    today = datetime.today().strftime('%d/%m/%Y')
    if date < today:
        return "Geçmiş bir tarih giremezsiniz."
    
    # Checks that the platform link is in url format.
    if not validators.url(platform_link):
        return "Geçersiz platform linki!"

    # Create a new meeting and add it to the database
    new_meeting = Meeting(
        topic=topic,
        date=date,
        start_time=start_time,
        end_time=end_time,
        participants=participants,
        platform_link=platform_link
    )

    db.session.add(new_meeting)
    db.session.commit()

    # Redirect to the index page
    return redirect(url_for('index'))

@app.route('/update_meeting/<int:meeting_id>', methods=['GET', 'POST'])
def update_meeting(meeting_id):
    # Get the meeting from the database with the specified ID
    meeting = Meeting.query.get_or_404(meeting_id)

    # Check if the form is submitted
    if request.method == 'POST':
        meeting.topic = request.form.get('topic')
        meeting.date = request.form.get('date')
        meeting.start_time = request.form.get('start_time')
        meeting.end_time = request.form.get('end_time')
        meeting.participants = request.form.get('participants')
        meeting.platform_link = request.form.get('platform_link')

        # Commit the changes to the database
        db.session.commit()
        # Redirect to the index page
        return redirect(url_for('index'))

    # Render the update meeting page with the meeting details
    return render_template('update_meeting_bootstrap.html', meeting=meeting, meeting_id=meeting_id)

@app.route('/delete_meeting/<int:meeting_id>')
def delete_meeting(meeting_id):
    # Get the meeting from the database with the specified ID
    meeting = Meeting.query.get_or_404(meeting_id)

    # Delete the meeting from the database and commit the changes to the database.
    db.session.delete(meeting)
    db.session.commit()

    # Redirect to the index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
