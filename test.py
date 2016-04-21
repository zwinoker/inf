# Runs tests for the inference engine. Uses input stored in the folder tests/inputs/

# Inference engine
from inferences import Inferences

# For finding input file names
import os

# Comparing test results
import filecmp

class Tester():
	def __init__(self):
		self.inputFolderName = "tests/inputs"
		self.outputFolderName = "tests/outputs"

		self.inputFiles = [inFile for inFile in os.listdir(self.inputFolderName)]
		# self.outputFiles = [outFile for outFile in os.listdir(self.outputFolderName)]

		self.resultsFileName = "test-results"

		self.testResults = []

	def runTests(self):
		for test in self.inputFiles :
			# Avoid system files
			if test[0] != "." :
				# For matching input and expected output
				whichTest = (test.split("_")[1]).replace(".txt","")

				# Read in input and solve queries
				inputPath = os.path.join(self.inputFolderName,test)
				inf = Inferences(inputPath)
				inf.readInput()
				inf.solveQueries()
				inf.cleanup()

				# Compare generated output to expected output.
				outFileName = "".join(["output_", whichTest, ".txt"])
				expectedOutputPath = os.path.join(self.outputFolderName, outFileName)
				result = filecmp.cmp(inf.outputFileName, expectedOutputPath)
				if result :
					passed = "PASSED"
				else:
					passed = "FAILED"
				self.testResults.append(passed)

		self.writeTestResults()

	def writeTestResults(self):
		results = open(self.resultsFileName,'w')
		count = 1
		for res in self.testResults :
			line = "".join(["Test ", str(count), " : ", res, '\r\n'])
			results.write(line)
			count += 1


# Main method
if __name__ == "__main__" :
	t = Tester()
	t.runTests()
