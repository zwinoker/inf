# First Order Logic Query Evaluator
Python package that performs query evaluation using [backward chaining](https://en.wikipedia.org/wiki/Backward_chaining). Input files establish a knowledge base and list of queries.

# Input format
Input must be in a txt file with the following format:
1. Number of queries
2. Queries
3. Number of facts in the knowledge base
4. Knowledge base facts

Queries must be atomic facts or negations of atomic facts. EX: ```H(Jon)``` or ```~H(Jon)```
Facts in the knowledge base can be:
 * Atomic facts
 * Rules (EX: ```A(x) => H(x)```, ```D(x,y) ^ Q(y) => C(x,y)```)

Here is an example of an input file (tests/inputs/input_1.txt)
```6
F(Bob)
H(John)
~H(Alice)
~H(John)
G(Bob)
G(Tom)
14
A(x) => H(x)
D(x,y) => ~H(y)
B(x,y) ^ C(x,y) => A(x)
B(John,Alice)
B(John,Bob)
D(x,y) ^ Q(y) => C(x,y)
D(John,Alice)
Q(Bob)
D(John,Bob)
F(x) => G(x)
G(x) => H(x)
H(x) => F(x)
R(x) => H(x)
R(Tom)
```

This file outputs
```FALSE
TRUE
TRUE
FALSE
FALSE
TRUE
```

# Usage
An input file can be specified from the command line. For example : ```python inferences.py -i tests/inputs/input_0.txt```
The results for each query will be written in order to ```output.txt```. It can also be passed to the inferences constructor if the engine is used in other code (see ```test.py``` for an example).

# Tests
Input and expected output for tests are stored in the folder ```tests```. To run these : ```python test.py```
New tests can be added, be file names must be of the form ```input_n.py``` and ```output_n.py``` where n is an integer. Test results are written to the file ```test-results```