# Balance Bots

This repo contains the solution to a coding challenge called "balance bots". The instructions for this challenge can be found in [assignment.txt](assignment.txt). It is written in Python because of the readability of the language, its built-in modules, and my familiarity with the language.

## Requirements

Python version 3.9+ is required in order to run the code because of the type hinting style I used. No external modules are required.

## Running the code

`python src/balance_bots.py`

Prints the answers to both questions in the assignment to your terminal. This should print 73 and 3965.

## Running tests

`python -m unittest`

Runs all tests.

## Notes

There are a few oddities in the code that you would likely not see in production code due to the nature of the assignment:

- I added type hinting only where I felt like it improved readability and clarity rather than strictly adding it everywhere (or nowhere at all).
- I went for a pragmatic approach when it comes to testing. I made isolated unit tests where feasible, but for some class methods (e.g. [Fixture.run()](tests/test_factory.py?plain=1#L61)) it was more convenient to just pass an entire fixture and verify the results.
- I think the [Factory init method](src/balance_bots.py?plain=1#L56) looks messy, but I am currently drawing a blank on how to make it better. I would ask code reviewers for suggestions here.
- In [balance_bots.py](src/balance_bots.py?plain=1#L113) I added `if __name__ == "__main__":` code so you can run the file to easily print the answers to your terminal.
- I made [test_assignment.py](tests/test_assignment.py) solely to verify the answers to the questions in the assignment. It does not test any code that is not already covered by other tests.
