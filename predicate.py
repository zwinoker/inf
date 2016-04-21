# Predicate class. Note that arguments are 2 tuples with (variable name/order, value)

class Predicate():
	# When we use this constructor, the parsing happens in this object
	def __init__(self, predicateString):
		# The string that we parse the predicate from.
		self.predString = predicateString

		# Number of arguments
		self.numArgs = 0

		# Name of predicate (EX: B(x) has name "B" and ~H(John) has name "~H")
		self.name = ""

		# Dictionary of arguments. Arugments are just lists of values and/or variables. 
		self.args = []

		# True if the predicate is a negation. Default is false.
		self.negation = False

		# Fix attributes.
		self.parseInput()

	# For building from string.
	def parseInput(self) :
		# Make a copy of the predicate string that we can modify in order to make the predicate object.
		psCopy = self.predString

		# Check if the predicate is a negation
		psCopy = psCopy.split("~")

		if len(psCopy) == 2 :
			self.negation = True
			self.name += "~"

		# Set predicate name
		if len(psCopy) == 1 :
			self.name += psCopy[0].split("(")[0]
		else :
			self.name += psCopy[1].split("(")[0]

		# Read in variables
		psCopy = self.predString
		args = psCopy.split("(")[1].split(")")[0].split(",")
		self.args = args
		self.numArgs = len(self.args)

	# Returns true if any of the arguments are variables.
	def hasVariables(self) :
		for var in self.args :
			if not var[0].isupper() :
				return True
		return False

	# Binds a val to the given var
	def bindVar(self, val, var) :
		self.args = [val if x == var else x for x in self.args]
		
