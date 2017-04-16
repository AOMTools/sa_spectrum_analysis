import numpy as np

''' TO GET THE NUMBER OF CASES '''

# Function
def nof_cases():
	with open('atom_conclusion', 'r') as myfile:
		myfile.readline()
		blah = myfile.readline()
		blah = blah.split()
		result = [int(blah[1]), int(blah[3]), int(blah[5]), int(blah[7]), int(blah[9])]
	return result

# Calling the function
# print nof_cases()	# Single, long, short, multi/uncl, uncl


''' TO OBTAIN THE ARRAY OF CASES '''

# Function
def obtain_cases(verdict_report="atom_conclusion"):
	atom_conclusion=np.genfromtxt(verdict_report, dtype=str)
	'''
	verdict_cases = np.genfromtxt("atom_conclusion", dtype=str)[:,1]
	atom_number = np.genfromtxt("atom_conclusion", dtype=int)[:,0]
	atom_array = np.genfromtxt("atom_conclusion", dtype=float)[:,2:]
	'''
	verdict_cases=atom_conclusion[:,1]
	atom_number=atom_conclusion[:,0]
	atom_array=atom_conclusion[:,2:]
	atom_lifetime=atom_conclusion[:,-1]
	return atom_number, verdict_cases, atom_array,atom_lifetime

# Calling the function (example)
#no, ver, arr,lifetime = obtain_cases()
# print no, ver, arr

''' TO SELECT THE NOF ATOMS WHICH ARE XXX '''

# Defining function
def select(case = "SA",verdict_report="atom_conclusion"):
	no, ver, arr,lifetime = obtain_cases(verdict_report=verdict_report)
	selected_cases = []
	for i in range(len(ver)):
		if ver[i] == case:
			selected_cases.append(no[i])
	return selected_cases

# Calling the function (example)
#print select(no, ver)
# print select(no, ver, "MA/UC")

''' TO MASK THE ARRAY OF ATOMS with cases XXX '''

# Defining function. Note that the array has to be 2D with the zeroth axis as row and second axis as column
def mask(array, case = "SA",verdict_report='atom_conclusion'):
	no, ver, arr,lifetime = obtain_cases(verdict_report=verdict_report)
	if (len(ver) != np.size(array,axis=0)):
		print ("The length of the arrays are not same. Aborting command")
		return 0
	# Create dummy array for stacking
	compeleted_array = np.zeros(np.size(array,axis=1))
	masked_id=[]
	lifetime_array=[]
	for i in range(len(ver)):
		if ver[i] == case:
			masked_id.append(i)
			compeleted_array = np.vstack([compeleted_array, array[i]])
	# Remove the first element of dummy array
	compeleted_array = compeleted_array[1:]
	return (masked_id,compeleted_array)

#get lifetime of masked atoms
def mask_lifetime(case='SA',verdict_report='atom_conclusion'):
	no, ver, arr,lifetime = obtain_cases(verdict_report=verdict_report)
	masked_lifetime=[]
	for i in range(len(ver)):
		if ver[i]==case:
			masked_lifetime.append(float(lifetime[i]))
	return masked_lifetime



# Calling the function (example)
#print mask(arr, ver, "LG")

# Example: masking with the original raw_F array
#raw_F_array = np.genfromtxt("raw_F")[1:]	# Only obtain from the 2st row and onwards as the first row is time
#masked_array = mask(raw_F_array, ver)
#	print masked_array
