#!/usr/bin/env python
# Generate a 531 program
# Uses the First Set Last assistance program

import TrainingProgram as TP


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
    tp.print_training_cycle()
    tp.write_training_plan()

if __name__ == '__main__':
    main()
