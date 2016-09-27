#!/usr/bin/env python
# Copyright (C) 2013 Shea G Craig
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

"""Flask mini-webapp for generating Wendler-based lifting programs."""


import os

from flask import (Flask, request, redirect, render_template, url_for,
                   session, flash)
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import BooleanField, IntegerField, StringField, SubmitField
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
    light =  BooleanField("Make small jumps?")
    submit = SubmitField("Get Wendlerized")


@app.route("/", methods=["GET", "POST"])
def index():
    """Extract lift info from user."""
    form = LiftForm()
    if form.validate_on_submit() and form.submit.data:
        return "<pre>{}</pre>".format(generate_program(form))

    return render_template("Wendlerizer.html", form=form)


def generate_program(form):
    """"""
    name = form.name.data
    squat = form.squat.data
    press = form.press.data
    deadlift = form.deadlift.data
    benchpress = form.bench_press.data
    light = form.light.data

    tp = TP.TrainingProgram(Name=name, Squat=int(squat), Press=int(press),
                            Deadlift=int(deadlift), BenchPress=int(benchpress),
                            light=light)

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
    app.secret_key = "TacosareTheMOSTdelicicousestOfthingsThis is forCSRFy'all"
    app.run(debug=True, port=PORT, extra_files=["templates", "static/styles"])

