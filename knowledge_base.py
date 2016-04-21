

# Keeps track of rules and facts for our system.

# For copying rules
import copy

# For generating lists of bindings
import itertools

# Custom logic classes
from predicate import Predicate
from rule import Rule


class KnowledgeBase():
	def __init__(self):
		# Store rules here. Indexed by consequential predicate's name. The keyed value is a list of lists of conjugates, each corresponding to one rule.
		self.rules = {}

		# Store atomic facts here. Indexed by predicate name. The keyed value is a list of list of values for the predicate's variables.
		self.facts = {}

		# Store rule instances we've seen here when a rule's consequent has only constants. We use this for loop detection by comparing current rule against 
		#	already encountered rules in this dictionary.
		self.rulesSeen = {}

	# Add a rule to the knowledge base
	def addRule(self, rule):
		# If rule already exists, just add the new list of conjugates to it.
		if rule.name in self.rules :
			self.rules[rule.name].append(rule)
		# Otherwise, just create the list
		else :
			self.rules[rule.name] = [rule]

	# Add a fact to the knowledge base
	def addFact(self, fact):
		# If predicate already exists in the dictionary, just add the new list of values to its keyed value.
		if fact.name in self.facts :
			self.facts[fact.name].append(fact.args)
		else :
			self.facts[fact.name] = [fact.args]

	# Runs Backward Chaining Algo to see if the given query is true for this set of rules and facts.
	#	Returns a boolean. True if query is true, False otherwise
	def bcs(self, query):
		# Check if given query is explicity in the KB
		if self.isFact(query) != [] and not query.hasVariables():
			return True

		# If query not in KB we need to see if it is implied by any of our rules
		if not self.ruleExists(query) :
			return False

		# If we're here then there is at least one rule that implies the query in question, but it is not an already-established fact.
		else :
			possibleRules = self.rules[query.name]
			return (self.checkRules(query, possibleRules))

	# Given a list of rules and a query, checks recursively to see if the query is true according to any of the rules
	def checkRules(self, query, ruleList) :
		# If any rules evaluate to true after being recursively unified, then return true, else return false
		for rule in ruleList :

			q = copy.deepcopy(query)
			r = copy.deepcopy(rule)
			bindings = self.queryConsBinding(r.consequent, q)

			# Make the bindings forced by the query and consequent matching.
			for b in bindings :
				r.bind(b[0],b[1])

			# Then see if the rule evaluates to true
			if self.evalRule(r) :
				return True

		# If here, then no rules proved that the given query was true.
		return False

	# Evaluates if rule is true or false
	def evalRule(self, rule) :
		# See if we've hit a loop if the goal of the rule is all constants.
		if not rule.consequent.hasVariables() :
			if self.detectLoop(rule) :
				return False
			else :
				if rule.name in self.rulesSeen :
					self.rulesSeen[rule.name].append(rule)
				else :
					self.rulesSeen[rule.name] = [rule]

		haveVariables = [x.hasVariables() for x in rule.conjugates]
		if True in haveVariables :
			bindings = self.ruleBindings(rule)
			if bindings == [] :
				return False
			else :
				if rule.consequent.hasVariables() :
					# Unify each valid binding with the consequent and add the result to the KB
					for b in bindings :
						conscopy = copy.deepcopy(rule.consequent)
						conscopy = self.unify(b, conscopy)
						self.addFact(conscopy)
				return True
		else :
			for pred in rule.conjugates :
				if not self.bcs(pred) :
					return False
			return True

	# Detects if we hit a loop by comparing current rule to any rules with the same name stored in self.rulesSeen
	def detectLoop(self,rule) :
		if rule.name not in self.rulesSeen :
			return False
		else :
			prevRules = self.rulesSeen[rule.name]
			for oldRule in prevRules :
				if self.compareTwoRules(oldRule, rule) :
					return True
			return False

	# Tells if two rules are equal by comparing the rule name, the arg list in the consequent, and the names of the conjugates
	def compareTwoRules(self, rule1, rule2) :
		if rule1.name != rule2.name :
			return False
		if rule1.consequent.args != rule2.consequent.args :
			return False
		if len(rule1.conjugates) != len(rule2.conjugates) :
			return False
		for i in range(0, len(rule1.conjugates)) :
			if rule1.conjugates[i].name != rule2.conjugates[i].name :
				return False
		return True

	# Finds all bindings associated with a rule
	def ruleBindings(self, rule) :
		validBindings = []
		potentialBindings = []

		# First find all potential assignments
		for pred in rule.conjugates :
			fb = self.findBindings(pred)
			potentialBindings += fb
		potentialBindings = self.mergeBindings(potentialBindings)

		# Then check to see which ones are valid. Do this by querying each unified predicate in the conjugation
		for b in potentialBindings :
			rc = copy.deepcopy(rule)
			goodBinding = True
			for conj in rc.conjugates :
				ccopy = copy.deepcopy(conj)
				ccopy = self.unify(b, ccopy)

				# If the unified predicate has variables, then no binding exists which fulfills the predicate. Then return empty list, which indicates false
				if ccopy.hasVariables() :
					return []

				# If the unified predicate is not true by the KB, then this binding is not correct. Break and try the next one.	
				elif not self.bcs(ccopy) :
					goodBinding = False
					break
			# If every predicate in the conjguation is true, then this is a valid binding. 
			if goodBinding :
				validBindings.append(b)
		return validBindings


	# Merges different bindings together. Ie just subsets them into all possible assignments.
	def mergeBindings(self, bindingList) :
		bindings = []
		# First find all possible assignments for each variable and combine them into a master dictionary
		masterDict = {}
		for d in bindingList :
			for var in d :
				if var not in masterDict :
					masterDict[var] = [d[var]]
				else :
					masterDict[var] = list(set([d[var]] + masterDict[var]))
				
				

		# Then find all combinations of these different variables. This is the list of bindings we wish to return.
		# Keep record of variable names in order so we can recover the correct bindings.
		namesList = []
		valsList = []
		for var, vals in masterDict.iteritems() :
			namesList.append(var)
			valsList.append(vals)
		tupleCombinations = list(itertools.product(*valsList))

		# Now we have a list of tuples that correspond to bindings. 
		#	Just need to put them back in dictionary form so we have the variable for each value written down.
		for tup in tupleCombinations :
			newBinding = {}
			for i in range(0, len(tup)) :
				newBinding[namesList[i]] = tup[i]
			bindings.append(newBinding)

		return bindings



	# Finds bindings for a given predicate.
	def findBindings(self, pred) :
		factBind = self.bindingsFromFacts(pred)
		ruleBind = self.bindingsFromRules(pred)
		bindings = factBind + ruleBind
		return bindings

	# Finds bindings derived from facts in the KB.
	def bindingsFromFacts(self, pred) :
		# Get the facts from the KB.
		facts = self.isFact(pred)
		bindings = []
		varLocations = {}

		# Figure out which variables need binding and which argument slot they are in.
		for i in range(0, pred.numArgs) :
			if not pred.args[i][0].isupper() :
				varLocations[str(i)] = pred.args[i]

		# Generate the bindings from the variable assignments in each fact.
		for assignment in facts :
			thisBinding = {}
			for j in varLocations :
				thisBinding[varLocations[j]] = assignment[int(j)]
			bindings.append(thisBinding)
		return bindings


	# Finds bindings derived from rules in the KB.
	def bindingsFromRules(self, pred) :
		bindings = []
		if not self.ruleExists(pred) :
			return []
		else :
			rules = self.rules[pred.name]
			for r in rules:
				# Make the bindings forced by the query and consequent matching.
				rc = copy.deepcopy(r)
				pc = copy.deepcopy(pred)
				qcBinds = self.queryConsBinding(rc.consequent, pc)
				for b in bindings :
					rc.bind(b[0],b[1])
				bind = self.ruleBindings(rc)
				if bind != [] :
					bindings += (bind)
			return bindings


	# Unifies a binding with a predicate
	def unify(self, binding, pred) :
		for i in range(0,pred.numArgs) :
			for key in binding :
				if key == pred.args[i] :
					pred.args[i] = binding[key]
		return pred
			
	# Given two predicates, one with constants, identifies the bound variables. Returns a list of tuples [(val, var), ...]. pred1 is assumed to have at most the 
	#	same number of bound variables as pred2
	def queryConsBinding(self, pred1, pred2) :
		bindings = []
		for i in range(0, len(pred1.args)) :
			if not pred1.args[i][0].isupper() and pred2.args[i][0].isupper() :
				bindings.append((pred2.args[i],pred1.args[i]))
		return bindings


	# Checks if there is a rule that implies the predicate of the given query
	def ruleExists(self, query) :
		return (query.name in self.rules)

	# Just checks if a query is exactly in the knowledge base. If so, returns a list of possible bindings. Otherwise returns empty list
	def isFact(self, query) :
		# See if predicate is in KB. If not, then return false
		if query.name not in self.facts :
			return []

		# Else see if we can find a matching binding.
		else :
			trueArgs = self.facts[query.name]
			for i in range(0, query.numArgs) :
				# Eliminate arg combos that don't match the given values in the query. Ignore lowercase vars.
				if query.args[i][0].isupper() :
					trueArgs = [x for x in trueArgs if x[i] == query.args[i]]
			return trueArgs
