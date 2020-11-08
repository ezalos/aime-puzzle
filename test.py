import subprocess
import re
import time
import platform

class BinCute():
	def __init__(self, binary, leaks=False):
		self.binary = binary
		self.command = ""
		self.raw_output = None
		self.output = ""
		self.time = None
		self.leaks = leaks

	def prepare_command(self, args):
		self.command = self.binary
		if type(args) == type(""):
			self.command += " " + args
		elif type(args) == type([]):
			for arg in args:
				self.command += " " + str(arg)
		else:
			print("Wrong args tyoe: ", type(args))

	def launch(self):
		  t = time.process_time()
		  # print(self.command)
		  self.raw_output = subprocess.run(self.command, stdout=subprocess.PIPE,
										  stderr=subprocess.PIPE, shell=True)
		  self.time = time.process_time() - t
		  self.stdout = self.raw_output.stdout.decode('utf-8')
		  self.stderr = self.raw_output.stderr.decode('utf-8')

if __name__ == "__main__":
	for i in range(20):
		cmd = "python3 main.py test " + str(i)
		raw_output = subprocess.run(cmd, stdout=subprocess.PIPE,
									stderr=subprocess.PIPE, shell=True)
		stdout = raw_output.stdout.decode('utf-8')
		stderr = raw_output.stderr.decode('utf-8')
		print(i)
		print(stdout)
