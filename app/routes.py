from __future__ import print_function
import sys
from flask import Blueprint,render_template, flash, redirect, url_for, request

from app import db
from app.forms import CourseForm, TAForm
from app.models import Course, Room, TeachingAssistant

app_blueprint = Blueprint('app', __name__)


@app_blueprint.route('/', methods=['GET', 'POST'])
@app_blueprint.route('/index', methods=['GET', 'POST'])
def index():  
    form = CourseForm()
    if form.validate_on_submit():
        if (form.major.data is not None) and (form.coursenum.data is not None):
            #check if course already exists
            _coursecount = Course.query.filter_by(major=form.major.data).filter_by(coursenum=form.coursenum.data).count()
            if _coursecount < 1:
                newcourse = Course(major = form.major.data,coursenum = form.coursenum.data,title = form.title.data, roomid = form.classroom.data.id)
                db.session.add(newcourse)
                db.session.commit()
                return redirect(url_for('app.course', courseid = newcourse.id) )
    # display existing courses
    _courses = Course.query.order_by(Course.coursenum).order_by(Course.major). all()
    return render_template('index.html', form=form, courses = _courses)

@app_blueprint.route('/course/<courseid>/assignta', methods = ['GET', 'POST'])
def course(courseid):
    form = TAForm()
    if form.validate_on_submit():
        if (form.ta_name.data is not None) :
                new_ta = TeachingAssistant(ta_name = form.ta_name.data, ta_email = form.ta_email.data)
                db.session.add(new_ta)
                thecourse = Course.query.session.get(Course,courseid)
                thecourse.add_ta(new_ta)
                db.session.commit()
                return redirect(url_for('app.course', courseid = thecourse.id) )
    thecourse = Course.query.session.get(Course,courseid)
    return render_template('course.html', form = form, current_course = thecourse)
