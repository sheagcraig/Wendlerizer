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
from wtforms import (BooleanField, IntegerField, RadioField, StringField,
                     SubmitField)
from wtforms.validators import Required, NoneOf

from barbell import (Lift, WendlerSomething, JokerSomething,
                     FirstSetLastSomething, AccessoryLift, Session, Microcycle)
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
    bar_type = RadioField("Barbell size", validators=[Required()], choices=[
        (45.0, "Standard barbell"), (33.0, "Women's barbell")], default=45.0,
        coerce=float)
    submit = SubmitField("Get Wendlerized")


class Squat531Session(Session):
    """Squat session generator for 531."""
    name = "Squat"
    elements = ([WendlerSomething, "Squat"],
                [JokerSomething, "Squat"],
                [FirstSetLastSomething, "Squat"])


class Deadlift531Session(Session):
    """Deadlift session generator for 531."""
    name = "Deadlift"
    elements = ([WendlerSomething, "Deadlift"],
                [JokerSomething, "Deadlift"],
                [FirstSetLastSomething, "Deadlift"])


class Press531Session(Session):
    """Press session generator for 531."""
    name = "Press"
    elements = (
        [WendlerSomething, "Press"],
        [JokerSomething, "Press"],
        [[FirstSetLastSomething, "Press"], [AccessoryLift, "Pull Up"]],
        [AccessoryLift, "Barbell Curl"])


class BenchPress531Session(Session):
    """Bench press session generator for 531."""
    name = "Bench Press"
    elements = (
        [WendlerSomething, "Bench Press"],
        [JokerSomething, "Bench Press"],
        [[FirstSetLastSomething, "Bench Press"], [AccessoryLift, "DB Row"]],
        [AccessoryLift, "Barbell OH Tricep Extension"])


class WendlerCycle(Microcycle):
    name = "Wendler 531 Cycle"
    notes = "Three week Wendler microcycle."
    sessions = [Squat531Session, Press531Session, Deadlift531Session,
                BenchPress531Session]


@app.route("/", methods=["GET", "POST"])
def index():
    """Extract lift info from user."""
    form = LiftForm()
    if form.validate_on_submit() and form.submit.data:
        cycle = generate_program(form)
        with open("notes.html") as ifile:
            notes = ifile.read()
        meta = {"Generated from PRs": "Squat {}, Press {}, Deadlift {}, "
                "Bench press {}".format(form.squat.data, form.press.data,
                form.deadlift.data, form.bench_press.data)}
        meta["Light Program Jumps"] = str(form.light.data)
        meta["Barbell Used"] = form.bar_type.data
        return render_template("Program.html", cycles=cycle, notes=notes,
                               name=form.name.data, meta=meta)
    else:
        print form.errors

    return render_template("Wendlerizer.html", form=form)


def generate_program(form):
    """Generate a training cycle based on form data."""
    # TODO: Move up
    name = form.name.data
    initial_scale = 0.9

    # Manage the size of the jumps based on the "Light" form toggle.
    light = form.light.data
    large_increment = 5.0 if light else 10.0
    small_increment = 2.5 if light else 5.0

    # Use the correct barbell size.
    barbell_weight = form.bar_type.data

    squat = Lift("Squat", form.squat.data, initial_scale, large_increment,
                 barbell_weight)
    press = Lift("Press", form.press.data, initial_scale, small_increment,
                 barbell_weight)
    deadlift = Lift("Deadlift", form.deadlift.data, initial_scale,
                    large_increment, barbell_weight)
    bench_press = Lift("Bench Press", form.bench_press.data,
                               initial_scale, small_increment, barbell_weight)

    # Instantiate all of the Lifts used in the program.
    pull_up = Lift("Pull Up", None)
    db_row = Lift("DB Row", None)
    curl = Lift("Barbell Curl", None)
    tricep_ext = Lift("Barbell OH Tricep Extension", None)
    core = Lift("Core", None)
    lifts = [squat, press, deadlift, bench_press, pull_up, db_row, curl,
             tricep_ext, core]

    cycle = WendlerCycle(lifts)

    # TODO: It would be nice to have something to send to the template about
    # what the current TM's are per week, the user's name, the light value, etc.

    # TODO: I also need some way for people to drop-in old values and continue
    # their existing program if they want to keep going.

    cycle1 = cycle.generate_cycle()
    cycle.increase_training_maxes()
    cycle2 = cycle.generate_cycle()

    return [cycle1, cycle2]


if __name__ == "__main__":
    app.secret_key = "TacosareTheMOSTdelicicousestOfthingsThis is forCSRFy'all"
    app.run(debug=True, port=PORT, extra_files=["templates", "static/styles"])
