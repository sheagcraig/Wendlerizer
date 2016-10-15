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

from barbell import (Lift, WendlerSomething, WendlerDeloadSomething,
                     JokerSomething, FirstSetLastSomething, AccessoryLift,
                     Session, Microcycle)
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
    units = RadioField("Units", validators=[Required()], choices=[
        ("pounds", "Pounds"), ("kilograms", "Kilograms")], default="pounds")
    bar_type = RadioField("Barbell size", validators=[Required()], choices=[
        (45.0, "Standard barbell"), (33.0, "Women's barbell")], default=45.0,
        coerce=float)
    light =  BooleanField("Make small jumps?")
    submit = SubmitField("Get Wendlerized")


class AdvancedLiftForm(Form):
    """Form for getting lift 1RMs."""
    name = StringField("Name", validators=[Required()])
    squat = IntegerField("Squat")
    press = IntegerField("Press")
    bench_press = IntegerField("Bench Press")
    deadlift = IntegerField("Deadlift")
    calculate_tms =  BooleanField("Generate Training Max?", default=True)
    units = RadioField("Units", validators=[Required()], choices=[
        ("pounds", "Pounds"), ("kilograms", "Kilograms")], default="pounds")
    bar_type = RadioField("Barbell size", validators=[Required()], choices=[
        (45.0, "Standard barbell"), (33.0, "Women's barbell")], default=45.0,
        coerce=float)
    light =  BooleanField("Make small jumps?")
    program_length = IntegerField("Number of 7 week microcycles to generate")
    submit = SubmitField("Get Wendlerized")


class Squat531Session(Session):
    """Squat session generator for 531."""
    name = "Squat"
    elements = ([WendlerSomething, "Squat"],
                [JokerSomething, "Squat"],
                [FirstSetLastSomething, "Squat"],
                [AccessoryLift, "Core"])


class Deadlift531Session(Session):
    """Deadlift session generator for 531."""
    name = "Deadlift"
    elements = ([WendlerSomething, "Deadlift"],
                [JokerSomething, "Deadlift"],
                [FirstSetLastSomething, "Deadlift"],
                [AccessoryLift, "Core"])


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


class SquatDeload(Session):
    """Squat session generator for 531."""
    name = "Squat"
    elements = ([WendlerDeloadSomething, "Squat"],)


class DeadliftDeload(Session):
    """Deadlift session generator for 531."""
    name = "Deadlift"
    elements = ([WendlerDeloadSomething, "Deadlift"],)


class PressDeload(Session):
    """Press session generator for 531."""
    name = "Press"
    elements = ([WendlerDeloadSomething, "Press"],)


class BenchPressDeload(Session):
    """Bench press session generator for 531."""
    name = "Bench Press"
    elements = ([WendlerDeloadSomething, "Bench Press"],)


class WendlerCycle(Microcycle):
    name = "Wendler 531 Cycle"
    length = 3
    notes = "Three week Wendler microcycle."
    sessions = [Squat531Session, Press531Session, Deadlift531Session,
                BenchPress531Session]


class WendlerDeloadCycle(Microcycle):
    name = "Wendler 531 Deload Cycle"
    length = 1
    notes = "One week Wendler deload microcycle."
    sessions = [SquatDeload, PressDeload, DeadliftDeload,
                BenchPressDeload]


@app.route("/", methods=["GET", "POST"])
def index():
    """Extract lift info from user."""
    form = LiftForm()
    if form.validate_on_submit() and form.submit.data:
        cycle = generate_program(form)
        meta = {"Generated from PRs": "Squat {}, Press {}, Deadlift {}, "
                "Bench press {}".format(form.squat.data, form.press.data,
                form.deadlift.data, form.bench_press.data)}
        meta["Units Used"] = form.units.data
        if form.units.data == "kilograms":
            barbell = 20.0 if form.bar_type.data == 45.0 else 15.0
        else:
            barbell = form.bar_type.data
        meta["Barbell Used"] = int(barbell)
        meta["Light Program Jumps"] = str(form.light.data)
        return render_template("ProgramWithNotes.html", cycles=cycle,
                               name=form.name.data, meta=meta)
    else:
        print form.errors

    return render_template("Wendlerizer.html", form=form)


@app.route("/advanced", methods=["GET", "POST"])
def run_advanced_program():
    """Extract lift info from user."""
    form = AdvancedLiftForm()
    if form.validate_on_submit() and form.submit.data:
        cycle = generate_advanced_program(form)
        meta = {"Generated from PRs": "Squat {}, Press {}, Deadlift {}, "
                "Bench press {}".format(form.squat.data, form.press.data,
                form.deadlift.data, form.bench_press.data)}
        meta["Units Used"] = form.units.data
        if form.units.data == "kilograms":
            barbell = 20.0 if form.bar_type.data == 45.0 else 15.0
        else:
            barbell = form.bar_type.data
        meta["Barbell Used"] = int(barbell)
        meta["Light Program Jumps"] = str(form.light.data)
        return render_template("ProgramWithNotes.html", cycles=cycle,
                               name=form.name.data, meta=meta)
    else:
        print form.errors

    return render_template("Wendlerizer.html", form=form)


def generate_program(form):
    """Generate a training cycle based on form data."""
    initial_scale = 0.9
    light = form.light.data
    units = form.units.data

    # Set everything up for using the different units.
    if units == "kilograms":
        barbell_weight = 15.0 if form.bar_type.data == 33.0 else 20.0
        large_increment = 2.5 if light else 5.0
        small_increment = 1.0 if light else 2.0
    else:
        barbell_weight = form.bar_type.data
        large_increment = 5.0 if light else 10.0
        small_increment = 2.5 if light else 5.0

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


def generate_advanced_program(form):
    """Generate a training cycle based on form data."""
    initial_scale = 0.9 if form.calculate_tms.data else 1.0
    light = form.light.data
    units = form.units.data

    num_of_cycles = form.program_length.data

    # Set everything up for using the different units.
    if units == "kilograms":
        barbell_weight = 15.0 if form.bar_type.data == 33.0 else 20.0
        large_increment = 2.5 if light else 5.0
        small_increment = 1.0 if light else 2.0
    else:
        barbell_weight = form.bar_type.data
        large_increment = 5.0 if light else 10.0
        small_increment = 2.5 if light else 5.0

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
    deload_cycle = WendlerDeloadCycle(lifts)
    import pdb; pdb.set_trace()

    # TODO: It would be nice to have something to send to the template about
    # what the current TM's are per week, the user's name, the light value, etc.

    # TODO: I also need some way for people to drop-in old values and continue
    # their existing program if they want to keep going.
    result = []
    for _ in xrange(num_of_cycles):
        result.append(cycle.generate_cycle())
        cycle.increase_training_maxes()
        result.append(cycle.generate_cycle())
        result.append(deload_cycle.generate_cycle())

    return result


if __name__ == "__main__":
    app.secret_key = "TacosareTheMOSTdelicicousestOfthingsThis is forCSRFy'all"
    app.run(debug=True, port=PORT, extra_files=["templates", "static/styles"])
