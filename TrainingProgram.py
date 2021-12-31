#!/usr/bin/env python
"""
Given input for max lifts, produce a BBC training program using Jim
Wendler's 531 program, and specifically implementing new protocols from
Beyond 531

Copyright (C) 2013 Shea G Craig <shea.craig@da.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import readline

class TrainingProgram(object):
    '''Represents a complete lifting program, with methods for outputting
    it nicely.
    '''
    def __init__(self, light=False, **kwargs):
        '''Generate our plan.'''
        self.light = light
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
        self.plan += "Based on 1RMs:\n"
        self.plan += ", ".join("{}: {}".format(lift, weight) for lift, weight in list(self.PRs.items())) + "\n\n"
        self.training_notes = []

    def read_PRs(self):
        '''Enter the necessary information for generating a training plan.'''
        self.name = input('Enter name: ')
        line()
        print("Input PR lift values. If a 1RM is not known, enter a rep max" \
              "like this '5x300' and it will be estimated.")
        for lift in list(self.PRs.keys()):
            PR = input('Enter %s 1RM: ' % lift)
            if 'X' in PR.upper():
                self.PRs[lift] = estimate_1RM(PR)
                print(("%s 1RM: %i" % (lift, self.PRs[lift])))
            else:
                self.PRs[lift] = int(PR)

    def generate_TMs(self):
        '''Generate the training maxes.'''
        for key, value in list(self.PRs.items()):
            self.TMs[key] = round_weight(value * 0.9)

    def increment_TMs(self):
        '''Add 5#'s to upper body lifts, and 10#'s to lower body lifts'''
        if self.light == True:
            self.TMs['Squat'] += 5
            self.TMs['Deadlift'] += 5
            self.TMs['Press'] += 2.5
            self.TMs['Bench Press'] += 2.5
        else:
            self.TMs['Squat'] += 10
            self.TMs['Deadlift'] += 10
            self.TMs['Press'] += 5
            self.TMs['Bench Press'] += 5

    def generate_531_weights(self, tm, week):
        '''Given a training max, and a week of the cycle, return a string of
        weights to lift for reps. Week=1=5, 5, 5+; 2=3, 3, 3+; 3=5, 3, 1+.
        '''
        if not self.light:
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
        else:
            if week == 1:
                weights = "5, 5, 5+ @ %i, %i, %i" % (round_weight(tm * 0.65, precision=2.5),
                                                round_weight(tm * 0.75, precision=2.5),
                                                round_weight(tm * 0.85, precision=2.5))
            elif week == 2:
                weights = "3, 3, 3+ @ %i, %i, %i" % (round_weight(tm * 0.7, precision=2.5),
                                                round_weight(tm * 0.8, precision=2.5),
                                                round_weight(tm * 0.9, precision=2.5))
            elif week == 3:
                weights = "5, 3, 1+ @ %i, %i, %i" % (round_weight(tm * 0.75, precision=2.5),
                                                round_weight(tm * 0.85, precision=2.5),
                                                round_weight(tm * 0.95, precision=2.5))
            else:
                # Rest week
                weights = "5, 5, 5 @ %i, %i, %i" % (round_weight(tm * 0.4, precision=2.5),
                                                round_weight(tm * 0.5, precision=2.5),
                                                round_weight(tm * 0.6, precision=2.5))

        return weights

    def generate_training_cycle(self, week_pattern, assistance_funcs):
        '''Generate a complete training program.

        week_pattern should be a tuple of week codes where 1=3x5 week, 2=3x3
        week, 3=5, 3, 1+ week, 4=rest week, and X=increase the training maxes.

        Assistance work is included by adding in assistance functions.

        assistance_funcs should be a list; each item in the list
        corresponds to one element or superset of the workout (an A., B., etc).

        Even if not supersetting, each list item needs to also be a list,
        in order, of the movement or movements to include. These items should
        also be lists, composed of the function to call, and it's extra_args.

        So all told, the assistance_funcs list will be three levels deep.

        i.e.:

        assistance_funcs = [
                                [element B stuff...
                                    [Supersetted movement 1, extra_args]
                                    [Supersetted movement 2, extra_args]
                                ]
                                [element C stuff...
                                    [Individual movement 1, extra_args]
                                ]
                            ]

        Each assistance function should accept as input tm, week, and a
        dict of extra_args, to which this method will add a key of 'lift' to.

        '''
        ctr = 1
        for week in week_pattern:
            if week == 'X':
                self.increment_TMs()
                continue

            self.plan += "Week %i\n" % ctr
            # import pdb; pdb.set_trace()
            self.plan += line() + '\n'

            self.plan += "Training Maxes:\n"
            self.plan += ", ".join("{}: {}".format(lift, weight) for lift, weight in list(self.TMs.items())) + "\n\n"

            for lift, tm in list(self.TMs.items()):
                element = 'A'
                self.plan += "%s Workout\n" % lift
                self.plan += "A. %s %s\n" % (
                    lift, self.generate_531_weights(tm, week))
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

    def print_training_cycle(self):
        '''Print a nice screen output of training plan.'''
        print((self.plan))
        for notes in self.training_notes:
            print(('\n\n%s' % notes))

    def write_training_plan(self):
        '''Output a text file with training plan.'''
        with open('%s.txt' % self.name, 'w') as f:
            output = self.plan
            for notes in self.training_notes:
                output += '\n\n%s' % notes
            f.write(output)

    def get_training_plan(self):
        """Return training plan as a string."""
        plan = self.plan
        for notes in self.training_notes:
            plan += '\n\n%s' % notes

        return plan

    def add_training_notes(self, notefile):
        '''Return the training notes.'''
        read_data = ''
        with open(notefile, 'r') as f:
            read_data = f.read()

        self.training_notes.append(read_data)


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
    if not 'percentage' in list(extra_args.keys()):
        percentage = 0.5
    else:
        percentage = extra_args['percentage']

    return "%s 5 x 10 @ %i" % (extra_args['lift'],
                               round_weight(tm * percentage))


def generate_assistance_assistance(tm, week, extra_args):
    '''Based on a lift, return an associated accessory protocol.
    Primarily for supersetting pullups with pressing assistance.

    Required keyword arguments are:
        lift = (Squat, Deadlift, Press, Bench Press)
        work = Dictionary with above lifts as key, and value should be string
                of sets and reps. If value is an empty string, that lift will
                not be supersetted.

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


def line():
    '''Return a nice line'''
    return 79 * '*' + '\n'


def main():
    pass


if __name__ == '__main__':
    main()
