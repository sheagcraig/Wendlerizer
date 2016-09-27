#!/usr/bin/env python
# Copyright (C) 2016 Shea G Craig
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details. #
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
"""
import os

from flask import (Flask, request, redirect, render_template, url_for,
                   session, flash)
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import Required, NoneOf

import TrainingProgram as TP

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Flask Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080

PROJECT_DIR = os.path.dirname(__file__)


class LiftForm(Form):
    """Form for getting lift 1RMs."""
    name = StringField("Name", validators=[Required()])
    squat = IntegerField("Squat")
    press = IntegerField("Press")
    bench_press = IntegerField("Bench Press")
    deadlift = IntegerField("Deadlift")

class StandardLiftForm(LiftForm):
    submit = SubmitField("Get Wendlerized")

class SmallJumpLiftForm(LiftForm):
    generate = SubmitField("Get Wendlerized")
    


@app.route("/", methods=["GET", "POST"])
def index():
    """Extract lift info from user."""
    form = StandardLiftForm()
    small_form = SmallJumpLiftForm()
    if form.validate_on_submit() and form.submit.data:
        #redirect(url_for("generate_program"))
        return "<pre>{}</pre>".format(generate_program(form))
    elif small_form.validate_on_submit() and small_form.generate.data:
        return "<pre>{}</pre>".format(generate_small_jumps(small_form))

    return render_template("Wendlerizer.html", form=form, form2=small_form)


#@app.route("/generate_program")
def generate_program(form):
    """"""
    name = form.name.data
    squat = form.squat.data
    press = form.press.data
    deadlift = form.deadlift.data
    benchpress = form.bench_press.data

    tp = TP.TrainingProgram(Name=name, Squat=int(squat), Press=int(press), Deadlift=int(deadlift), BenchPress=int(benchpress))

    # These are my minor assistance exercises
    work = {'Squat': '',
            'Deadlift': '',
            'Press': 'Pullup 5 x 10',
            'Bench Press': 'DB Row 5 x 10'}

    # These are my abz and stuff
    extra_work = {'Squat': 'Abs 5 x 10-20',
                  'Deadlift': 'Abs 5 x 10-20',
                  'Press': 'Kurlz 5 x 10',
                  'Bench Press': 'Tricepz 5 x 10'}

    # Specify assistance
    assistance = []
    assistance.append([[TP.generate_last_set_first_weight, {}],
                       [TP.generate_assistance_assistance, work]])
    assistance.append([[TP.generate_assistance_assistance, extra_work]])

    tp.generate_training_cycle((1, 2, 3, 'X', 1, 2, 3, 'X', 1, 2), assistance)
    tp.add_training_notes(os.path.join(PROJECT_DIR, 'notes.txt'))
    tp.add_training_notes(os.path.join(PROJECT_DIR, 'unicorn.txt'))
    return tp.get_training_plan()


def generate_small_jumps(form):
    name = form.name.data
    squat = form.squat.data
    press = form.press.data
    deadlift = form.deadlift.data
    benchpress = form.bench_press.data
    tp = TP.TrainingProgram(light=True, Name=name, Squat=int(squat), Press=int(press), Deadlift=int(deadlift), BenchPress=int(benchpress))

    # These are my minor assistance exercises
    work = {'Squat': '',
            'Deadlift': '',
            'Press': 'Pullup 5 x 10',
            'Bench Press': 'DB Row 5 x 10'}

    # These are my abz and stuff
    extra_work = {'Squat': 'Abs 5 x 10-20',
                  'Deadlift': 'Abs 5 x 10-20',
                  'Press': 'Kurlz 5 x 10',
                  'Bench Press': 'Tricepz 5 x 10'}

    # Specify assistance
    assistance = []
    assistance.append([[TP.generate_last_set_first_weight, {}],
                       [TP.generate_assistance_assistance, work]])
    assistance.append([[TP.generate_assistance_assistance, extra_work]])

    tp.generate_training_cycle((1, 2, 3, 'X', 1, 2, 3, 'X', 1, 2), assistance)
    tp.add_training_notes(os.path.join(PROJECT_DIR, 'notes.txt'))
    tp.add_training_notes(os.path.join(PROJECT_DIR, 'unicorn.txt'))
    return tp.get_training_plan()


if __name__ == "__main__":
    app.run(debug=True, port=PORT)

