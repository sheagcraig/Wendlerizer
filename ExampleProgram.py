#!/usr/bin/env python
# Generate a 531 program for our CrossFit Total PR Challenge
# Uses the First Set Last assistance program

import os

import TrainingProgram as TP

PROJECT_DIR = os.path.dirname(__file__)

def main():
    tp = TP.TrainingProgram()

    # These are my minor assistance exercises
    work = {'Squat': '', 'Deadlift': '',
            'Press': 'Pullup 5 x 10', 'Bench Press': 'DB Row 5 x 10'}

    # These are my abz and stuff
    extra_work = {'Squat': 'Abs 5 x 10-20', 'Deadlift': 'Abs 5 x 10-20',
            'Press': 'Kurlz 5 x 10', 'Bench Press': 'Tricepz 5 x 10'}

    # Specify assistance
    assistance = []
    assistance.append([[TP.generate_last_set_first_weight, {}],
                       [TP.generate_assistance_assistance, work]])
    assistance.append([[TP.generate_assistance_assistance, extra_work]])

    tp.generate_training_cycle((1, 2, 3, 'X', 1, 2, 3, 'X', 1, 2), assistance)
    tp.add_training_notes(os.path.join(PROJECT_DIR, 'notes.txt'))
    tp.add_training_notes(os.path.join(PROJECT_DIR, 'unicorn.txt'))
    tp.print_training_cycle()
    tp.write_training_plan()

if __name__ == '__main__':
    main()
