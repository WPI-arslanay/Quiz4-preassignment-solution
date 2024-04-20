from app import create_app, db
from app.models import Course, Room
from config  import Config
from flask_sqlalchemy import SQLAlchemy


app = create_app(Config)


def init_database():
    # create the rooms 
    allrooms = [{'building' : 'Fuller', 'roomNumber' : 'B46', 'capacity' : 60}, 
                {'building' : 'UnityHall', 'roomNumber' : '175', 'capacity' : 100},
                {'building' : 'UnityHall', 'roomNumber' : '150', 'capacity' : 80},
                {'building' : 'Goddard', 'roomNumber' : '227', 'capacity' : 56}]
    if Room.query.count() == 0:
        for room in allrooms:
            theroom = Room (building = room['building'],roomNumber=room['roomNumber'], capacity = room['capacity'] ) 
            db.session.add(theroom)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_database()
        app.run(debug=True)