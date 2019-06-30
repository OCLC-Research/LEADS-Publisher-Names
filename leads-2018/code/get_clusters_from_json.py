import json
from pprint import pprint
import time

filepath = 'C:\\Users\\souvi\\Desktop\\OCLC\\connway_gold_clusters\\'

def get_clusters():
	list_of_files ={"310.json", "322.json", "333.json", "391.json", "925.json", "927.json", "1422.json"}

	for filename in list_of_files:
		if filename == "310.json":
			with open(filepath + '310.json') as f:
				data = json.load(f)
				set_MGH = set()
				for value in data["variant"]:
					set_MGH.add(value)
				#print(set_MGH)
				
		elif filename == "322.json":
			with open(filepath + '322.json') as f:
				data = json.load(f)
				set_MGHR = set()
				for value in data["variant"]:
					set_MGHR.add(value)
				#print(set_MGHR)
				
		elif filename == "333.json":
			with open(filepath + '333.json') as f:
				data = json.load(f)
				set_RH = set()
				for value in data["variant"]:
					set_RH.add(value)
				#print(set_RH)
				
		elif filename == "391.json":
			with open(filepath + '391.json') as f:
				data = json.load(f)
				set_Lerner = set()
				for value in data["variant"]:
					set_Lerner.add(value)
				#print(set_Lerner)
				
		elif filename == "925.json":
			with open(filepath + '925.json') as f:
				data = json.load(f)
				set_Lernersports = set()
				for value in data["variant"]:
					set_Lernersports.add(value)
				#print(set_Lernersports)
				
		elif filename == "927.json":
			with open(filepath + '927.json') as f:
				data = json.load(f)
				set_Elearner = set()
				for value in data["variant"]:
					set_Elearner.add(value)
				#print(set_Elearner)
				
		elif filename == "1422.json":
			with open(filepath + '1422.json') as f:
				data = json.load(f)
				set_RHNZ = set()
				for value in data["variant"]:
					set_RHNZ.add(value)
				#print(set_RHNZ)
				
		else:
			print(filename)
	return set_MGH, set_MGHR, set_RH, set_Lerner, set_Lernersports, set_Elearner, set_RHNZ

def printclusters(s):
	for entry in s:
		print(entry)

if __name__ == '__main__':
	start_time = time.time()
	input_filename = 'marc.xml'
	
	set_MGH, set_MGHR, set_RH, set_Lerner, set_Lernersports, set_Elearner, set_RHNZ = get_clusters()
	
	printclusters(set_MGH)
	print("---------------------")
	printclusters(set_MGHR)
	print("---------------------")
	printclusters(set_RH)
	print("---------------------")
	printclusters(set_Lerner)
	print("---------------------")
	printclusters(set_Lernersports)
	print("---------------------")
	printclusters(set_Elearner)
	print("---------------------")
	printclusters(set_RHNZ)
	
	elapsed_time = time.time() - start_time
	print("Elapsed Time: ", elapsed_time)			