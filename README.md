# The Wendlerizer

I love Jim Wendler's 5/3/1 program, and my appreciation has grown the longer I
do it and use it to coach athletes. In an attempt to help spread the love, I
wrote this quick and kind of crappy class to help me crank out the numbers for
members of the Barbell Club, mostly just because it's a lot cooler than using a
spreadsheet (see unicorn.txt).

The Wendlerizer ended up getting recycled into generating programs for the
[CrossFit Local](http://crossfitlocal.com) CrossFit Total Challenge. It was
updated to be runnable as a mod_python wsgi script to alleviate the need
for me to manually enter numbers for all of my athletes. It has since
been updated again as a Flask app.

Be warned! It has been in service for three years with very few changes to the
actual core functionality; most of the changes have been to reskin the input
into different web formats. It is in dire need of "modernization" to my
professional coding standards. At this point a complete rewrite is probably in
order!

## What's Here
- TrainingProgram.py is the actual class.
- ExampleProgram.py is an example of putting it to use.
- Wendlerizer is a Flask app for generating the programming CrossFitLocal
  uses for its annual strength challenge.
  - Wendlerizer.py: App code.
  - notes.txt and unicorn.txt: text files added at the end of the program.
  - static, templates: Flask support files.
  - requirements.txt: Pip requirements file for use in a Virtualenv.


## TODO
- Complete rewrite of TrainingProgram.
- Include mod_python code, potentially as a dead branch.
- Output was originally supposed to be beautifully old school. I'm kind of over
  it. Do a new design on output.


