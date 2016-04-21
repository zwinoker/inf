# Controler class parses input and runs the queries. Top level object.

# For reading filename from command line
import argparse

from knowledge_base import KnowledgeBase
from predicate import Predicate
from rule import Rule

class Inferences():
	def __init__(self):
		# For reading/writing input/output
		self.inputFileName = self.getInputFileName()
		self.inputFile = open(self.inputFileName, 'r')

		self.outputFileName = "output.txt"
		self.outputFile = open(self.outputFileName, 'w')

		# Num queries
		self.numQueries = 0

		# Num statements for the kb
		self.numStatements = 0

		# List of queries. Stored as predicate objects.
		self.queryList = []

		# The knowledge base for this set of queries
		self.kb = KnowledgeBase()

	def getInputFileName(self):
		# Set up input and output files
		parser = argparse.ArgumentParser()
		parser.add_argument('-i', type=str)
		args = parser.parse_args()
		inputFile = args.i
		return inputFile
		

	# Parses input file
	def readInput(self):
		try :
			# Break up by line
			lines = self.inputFile.read().split('\n')
			for line in lines :
				line = line.strip('\r\n')

			# Get number of queries to make to the KB
			self.numQueries = int(lines[0])
			
			# Read each query and store it as a predicate in self.queryList
			for i in range(1, self.numQueries + 1) :
				newQuery = Predicate(lines[i])
				self.queryList.append(newQuery)

			# Read in number of statements for the KB.
			self.numStatements = int(lines[self.numQueries + 1])

			for j in range(self.numQueries + 2, self.numQueries + 2 + self.numStatements) :
				statement = lines[j]

				# Check if statement is a rule or a fact
				if "=>" in statement :
					newRule = Rule(statement)
					self.kb.addRule(newRule)
				else :
					newFact = Predicate(statement)
					self.kb.addFact(newFact)

		except Exception as e :
			print "\nError reading input : ", e

	# Call this method to solve all queries in the queryList.
	def solveQueries(self):
		try : 
			for q in self.queryList :
				try :
					if self.kb.bcs(q) :
						self.outputFile.write("TRUE\r\n")
					else :
						self.outputFile.write("FALSE\r\n")
				except Exception as e :
					print "\nError executing specific query : ", e, "...Name = ", q.name

		except Exception as e :
			self.outputFile.write("FALSE\r\n")
			print "\nError executing queries : ", e

# Main method
if __name__ == "__main__" :
	c = Inferences()

	try :
		c.readInput()
	except Exception as e:
		print "Error reading input."

	try:
		c.solveQueries()
	except Exception as e:
		print "Error making queries"
