#!/usr/bin/env python
# Given input for max lifts, produce a BBC training program using Jim
# Wendler's 531 program, and specifically implementing new protocols from
# Beyond 531

import readline

class TrainingProgram(object):
    '''Represents a complete lifting program, with methods for outputting 
    it nicely.
    '''
    def __init__(self):
        '''Generate our plan.'''
        self.PRs = {'Squat': 0,
                    'Press': 0,
                    'Deadlift': 0,
                    'Bench Press': 0}
        self.TMs = {'Squat': 0,
                    'Press': 0,
                    'Deadlift': 0,
                    'Bench Press': 0}

        self.read_PRs()
        self.generate_TMs()
        self.plan = "Training Plan for %s\n\n" % self.name

    def read_PRs(self):
        '''Enter the necessary information for generating a training plan.'''
        self.name = raw_input('Enter name: ')
        line()
        print("Input PR lift values. If a 1RM is not known, enter a rep max" \
              "like this '5x300' and it will be estimated.")
        for lift in self.PRs.keys():
            PR = raw_input('Enter %s 1RM: ' % lift)
            if 'X' in PR.upper():
                self.PRs[lift] = estimate_1RM(PR)
                print("%s 1RM: %i" % (lift, self.PRs[lift]))
            else:
                self.PRs[lift] = int(PR)

    def generate_TMs(self):
        '''Generate the training maxes.'''
        for key, value in self.PRs.items():
            self.TMs[key] = round_weight(value * 0.9)

    def increment_TMs(self):
        '''Add 5#'s to upper body lifts, and 10#'s to lower body lifts'''
        self.TMs['Squat'] += 10
        self.TMs['Deadlift'] += 10
        self.TMs['Press'] += 5
        self.TMs['Bench Press'] += 5

    def generate_531_cycle(self, tm, week):
        '''Given a training max, and a week of the cycle, return a tuple of
        weights to lift. Week=1=5, 5, 5+; 2=3, 3, 3+; 3=5, 3, 1+.
        '''
        if week == 1:
            return (round_weight(tm * 0.65), round_weight(tm * 0.75), round_weight(tm * 0.85))
        elif week == 2:
            return (round_weight(tm * 0.7), round_weight(tm * 0.8), round_weight(tm * 0.9))
        else:
            return (round_weight(tm * 0.75), round_weight(tm * 0.85), round_weight(tm * 0.95))


    def generate_training_cycle(self, cycle):
        '''Generate one cycle of training.'''
        self.plan += 'Cycle %i\n\n' % cycle
        self.plan += 'Training maxes:\n'
        self.plan += 'Squat: %s\n' % self.TMs['Squat']
        self.plan += 'Press: %s\n' % self.TMs['Press']
        self.plan += 'Deadlift: %s\n' % self.TMs['Deadlift']
        self.plan += 'Bench Press: %s\n\n' % self.TMs['Bench Press']

        week = "Week 1\n"
        week += line()
        week += "Day 1:\n"
        week += "A. Squat 5, 5, 5+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Squat'] * 0.65),
                                  round_weight(self.TMs['Squat'] * 0.75),
                                  round_weight(self.TMs['Squat'] * 0.85))
        week += "B. Squat 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Squat'] * 0.65)
        week += "C. Press 5, 5, 5+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Press'] * 0.65),
                                  round_weight(self.TMs['Press'] * 0.75),
                                  round_weight(self.TMs['Press'] * 0.85))
        week += "D1. Press 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Press'] * 0.65)
        week += "D2. Strict Pullup or DB Row or BB row 5 x 10\n"
        week += "E. Ab exercises 3-5 x 10-20\n"
        week += "F. Conditioning\n\n"

        week += line()
        week += "Day 2:\n"
        week += "A. Deadlift 5, 5, 5+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Deadlift'] * 0.65),
                                  round_weight(self.TMs['Deadlift'] * 0.75),
                                  round_weight(self.TMs['Deadlift'] * 0.85))
        week += "B. Deadlift 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Deadlift'] * 0.65)
        week += "C. Bench Press 5, 5, 5+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Bench Press'] * 0.65),
                                  round_weight(self.TMs['Bench Press'] * 0.75),
                                  round_weight(self.TMs['Bench Press'] * 0.85))
        week += "D1. Bench Press 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Bench Press'] * 0.65)
        week += "D2. Strict Pullup or DB Row or BB row 5 x 10\n"
        week += "E1. Reverse Hyper, or GH Raise or Back Extension 3-5 x\n"
        week += "E2. DB Kurlz or OH Triceps Extensions: 3-5 x 10\n"
        week += "F. Conditioning\n\n"

        self.plan += week

        week = "Week 2\n"
        week += line()
        week += "Day 1:\n"
        week += "A. Squat 3, 3, 3+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Squat'] * 0.7),
                                  round_weight(self.TMs['Squat'] * 0.8),
                                  round_weight(self.TMs['Squat'] * 0.9))
        week += "B. Squat 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Squat'] * 0.7)
        week += "C. Press 3, 3, 3+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Press'] * 0.7),
                                  round_weight(self.TMs['Press'] * 0.8),
                                  round_weight(self.TMs['Press'] * 0.9))
        week += "D1. Press 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Press'] * 0.7)
        week += "D2. Strict Pullup or DB Row or BB row 5 x 10\n"
        week += "E. Ab exercises 3-5 x 10-20\n"
        week += "F. Conditioning\n\n"

        week += line()
        week += "Day 2:\n"
        week += "A. Deadlift 3, 3, 3+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Deadlift'] * 0.7),
                                  round_weight(self.TMs['Deadlift'] * 0.8),
                                  round_weight(self.TMs['Deadlift'] * 0.9))
        week += "B. Deadlift 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Deadlift'] * 0.7)
        week += "C. Bench Press 3, 3, 3+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Bench Press'] * 0.7),
                                  round_weight(self.TMs['Bench Press'] * 0.8),
                                  round_weight(self.TMs['Bench Press'] * 0.9))
        week += "D1. Bench Press 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Bench Press'] * 0.7)
        week += "D2. Strict Pullup or DB Row or BB row 5 x 10\n"
        week += "E1. Reverse Hyper, or GH Raise or Back Extension 3-5 x\n"
        week += "E2. DB Kurlz or OH Triceps Extensions: 3-5 x 10\n"
        week += "F. Conditioning\n\n"

        self.plan += week

        week = "Week 3\n"
        week += line()
        week += "Day 1:\n"
        week += "A. Squat 5, 3, 1+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Squat'] * 0.75),
                                  round_weight(self.TMs['Squat'] * 0.85),
                                  round_weight(self.TMs['Squat'] * 0.95))
        week += "B. Squat 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Squat'] * 0.75)
        week += "C. Press 5, 3, 1+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Press'] * 0.75),
                                  round_weight(self.TMs['Press'] * 0.85),
                                  round_weight(self.TMs['Press'] * 0.95))
        week += "D1. Press 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Press'] * 0.75)
        week += "D2. Strict Pullup or DB Row or BB row 5 x 10\n"
        week += "E. Ab exercises 3-5 x 10-20\n"
        week += "F. Conditioning\n\n"

        week += line()
        week += "Day 2:\n"
        week += "A. Deadlift 5, 3, 1+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Deadlift'] * 0.75),
                                  round_weight(self.TMs['Deadlift'] * 0.85),
                                  round_weight(self.TMs['Deadlift'] * 0.95))
        week += "B. Deadlift 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Deadlift'] * 0.75)
        week += "C. Bench Press 3, 3, 3+ "\
                "@ %s, %s, %s\n" % (round_weight(self.TMs['Bench Press'] * 0.75),
                                  round_weight(self.TMs['Bench Press'] * 0.85),
                                  round_weight(self.TMs['Bench Press'] * 0.95))
        week += "D1. Bench Press 3-5 sets of 5-8 reps @ %s\n" % \
                round_weight(self.TMs['Bench Press'] * 0.75)
        week += "D2. Strict Pullup or DB Row or BB row 5 x 10\n"
        week += "E1. Reverse Hyper, or GH Raise or Back Extension 3-5 x\n"
        week += "E2. DB Kurlz or OH Triceps Extensions: 3-5 x 10\n"
        week += "F. Conditioning\n\n"

        self.plan += week

    def print_training_cycle(self):
        '''Print a nice screen output of training plan.'''
        print(self.plan + self.training_notes() + '\n' + unicorn())

    def write_training_plan(self):
        '''Output a text file with training plan.'''
        with open('%s.txt' % self.name, 'w') as f:
            f.write(self.plan + '\n\n' +  self.training_notes() + '\n\n' + 
                    unicorn())

    def training_notes(self):
        '''Return the training notes.'''
        read_data = ''
        with open('notes.txt', 'r') as f:
            read_data = f.read()

        return read_data


def estimate_1RM(rep_max):
    '''Given a rep max in the form of repsXweight, calculate an estimated 
    1RM.
    '''
    reps, x, weight = rep_max.upper().partition('X')
    est1rm = int(weight) * int(reps) * 0.0333 + int(weight)
    return int(round_weight(est1rm))
    

def round_weight(weight, precision=5.0):
    '''A simple rounding algorithm specifically for weights. You can override
    the default rounding to the nearest 5 pound plates if so desired.

    '''
    return int(weight + precision / 2 - ((weight + precision / 2) % precision))


def unicorn():
    '''Return a nice unicorn.'''
    read_data = ''
    with open('unicorn.txt', 'r') as f:
        read_data = f.read()

    return read_data


def line():
    return 79 * '*' + '\n'


def main():
    #Testing
    tp = TrainingProgram()
    print(tp.generate_531_cycle(tp.TMs['Squat'], 1))


if __name__ == '__main__':
    main()
