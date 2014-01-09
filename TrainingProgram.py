#!/usr/bin/env python
# Given input for max lifts, produce a BBC training program using Jim
# Wendler's 531 program, and specifically implementing new protocols from
# Beyond 531

import readline

class TrainingProgram(object):
    '''Represents a complete lifting program, with methods for outputting 
    it nicely.
    '''
    def __init__(self, **kwargs):
        '''Generate our plan.'''
        if len(kwargs) == 5:
            self.PRs = {'Squat': kwargs['Squat'],
                        'Press': kwargs['Press'],
                        'Deadlift': kwargs['Deadlift'],
                        'Bench Press': kwargs['BenchPress']}
            self.name = kwargs['Name']
        else:
            self.PRs = {'Squat': 0,
                        'Press': 0,
                        'Deadlift': 0,
                        'Bench Press': 0}
            self.read_PRs()

        self.TMs = {'Squat': 0,
                    'Press': 0,
                    'Deadlift': 0,
                    'Bench Press': 0}

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

    def generate_531_weights(self, tm, week):
        '''Given a training max, and a week of the cycle, return a string of
        weights to lift for reps. Week=1=5, 5, 5+; 2=3, 3, 3+; 3=5, 3, 1+.
        '''
        if week == 1:
            weights = "5, 5, 5+ @ %i, %i, %i" % (round_weight(tm * 0.65),
                                               round_weight(tm * 0.75),
                                               round_weight(tm * 0.85))
        elif week == 2:
            weights = "3, 3, 3+ @ %i, %i, %i" % (round_weight(tm * 0.7),
                                               round_weight(tm * 0.8),
                                               round_weight(tm * 0.9))
        elif week == 3:
            weights = "5, 3, 1+ @ %i, %i, %i" % (round_weight(tm * 0.75),
                                               round_weight(tm * 0.85),
                                               round_weight(tm * 0.95))
        else:
            # Rest week
            weights = "5, 5, 5 @ %i, %i, %i" % (round_weight(tm * 0.4),
                                              round_weight(tm * 0.5),
                                              round_weight(tm * 0.6))
        return weights

    def generate_training_cycle(self, week_pattern, assistance_funcs):
        '''Generate a complete training program.

        week_pattern should be a tuple of week codes where 1=3x5 week, 2=3x3
        week, 3=5, 3, 1+ week, 4=rest week, and X=increase the training maxes.

        Assistance work is included by adding in assistance functions.
        Each assistance function should conform to the Assistance class.

        assistance_funcs should be a list of assistance functions and their
        keyword arguments. 

        Supersets can be included by making a list of lists.

        '''
        ctr = 1
        for week in week_pattern:
            if week == 'X':
                self.increment_TMs()
                continue

            self.plan += "Week %i\n" % ctr
            self.plan += line() + '\n'

            for lift, tm in self.TMs.items():
                element = 'A'
                self.plan += "%s Workout\n" % lift
                self.plan += "A. %s %s\n" % (lift, self.generate_531_weights(tm, week))
                if not week == 4:
                    for superset in assistance_funcs:
                        element = chr(ord(element) + 1)

                        superset_text = []
                        for assistance in superset:
                            extra_args = assistance[1]
                            extra_args['lift'] = lift
                            output = assistance[0](tm, week, extra_args)

                            if not output == '':
                                superset_text.append(output)

                        sub = '1'
                        for temp in superset_text:
                            
                            output_string = element
                            if len(superset_text) > 1:
                               output_string += sub
                               sub = str(int(sub) + 1)

                            output_string += ". %s\n" % temp

                            self.plan += output_string

                self.plan += '\n'

            ctr += 1
            self.plan += '\n'
                
        return self.plan


    def generate_training_cycle_old(self, cycle):
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


def generate_last_set_first_weight(tm, week, extra_args):
    '''Return the last set first weight for backoff sets.'''
    if week == 1:
        weight = round_weight(tm * 0.65)
    elif week == 2:
        weight = round_weight(tm * 0.7)
    else:
        weight = round_weight(tm * 0.75)

    return "%s 3-5 sets of 5-8 reps @ %i" % (extra_args['lift'], weight)


def generate_boring_but_big_weight(tm, week, extra_args):
    '''Return the BBB weight to use. Defaults to 50%.'''
    if not 'percentage' in extra_args.keys():
        percentage = 0.5
    else:
        percentage = extra_args['percentage']

    return "%s 5 x 10 @ %i" % (extra_args['lift'], round_weight(tm * percentage))


def generate_assistance_assistance(tm, week, extra_args):
    '''Based on a lift, return an associated accessory protocol.
    Primarily for supersetting pullups with pressing assistance.

    Required keyword arguments are:
        lift = (Squat, Deadlift, Press, Bench Press)
        work = Dictionary with above lifts as key, and value should be string
                of sets and reps
    
    '''
    
    lift = extra_args['lift']
    output = "%s" % extra_args[lift]
    #if 'percentage' in kwargs['work'][lift].keys():
    #    output += " @ %i" % round_weight(tm * percentage)
    return output


def generate_jake_set(tm, week, extra_args):
    '''Just returns a jake set'''
    return "%s Jake set" % extra_args['lift']


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
    pass


if __name__ == '__main__':
    main()
