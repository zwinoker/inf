 # For reading filename from command line
import argparse

# For copying rules
import copy

# For limiting time spent on a given query.
import time

# For generating lists of bindings
import itertools

# Custom logic classes
from predicate import Predicate


# Class for rules.
class Rule():
	def __init__(self, ruleString):
		# The string we parse the rule from.
		self.ruleString = ruleString

		# The predicate that is true if the rule's conjugate clauses are true.
		self.consequent = None

		# List of conjugated predicates that must be true for the rule's implication to hold.
		self.conjugates = []

		# Fix attributes
		self.parseInput()
		self.name = self.consequent.name 

	# Construct the rule from the given ruleString
	def parseInput(self) :
		# First, fix the consequent. It is the last element of the input string split by the implies character " => " (spaces intended).
		consequentString = self.ruleString.split(" => ")[-1]
		self.consequent = Predicate(consequentString)

		# Now parse the conjugates
		conjugateString = self.ruleString.split(" => ")[0]
		conjugateList = conjugateString.split(" ^ ")
		for conj in conjugateList :
			conjPred = Predicate(conj)
			self.conjugates.append(conjPred)

	# Does a variable binding for the consequent and predicates
	def bind(self, val, var) :
		self.consequent.bindVar(val, var)
		for conj in self.conjugates :
			conj.bindVar(val, var)