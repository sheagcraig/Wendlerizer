#!/usr/bin/env python
# Generate a 531 program
# Uses the First Set Last assistance program

import TrainingProgram as TP


def main():
    tp = TP.TrainingProgram()
    tp.generate_training_cycle(1)
    tp.increment_TMs()
    tp.generate_training_cycle(2)
    tp.increment_TMs()
    tp.generate_training_cycle(3)
    tp.print_training_cycle()
    tp.write_training_plan()


if __name__ == '__main__':
    main()
