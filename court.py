import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.special import erf
import os
from os import listdir
from os.path import isfile, join

def mass_judge(tar_path,judger_choice=2):
    #tarpath is the main directory of the dataset
    tar_path_F=tar_path+'/merge_norm/F'
    files= [f for f in listdir(tar_path_F) if isfile(join(tar_path_F, f)) ]
    files.sort()
    print('Model %d was chosen for Single Atoms filter' %judger_choice)
    if os.path.isdir(tar_path+'/verdict_report')==False:
        os.makedirs(tar_path+'/verdict_report')
    for f in files:
    	output_fname=tar_path+'/verdict_report/'+f
    	input_fname=tar_path_F+'/'+f
        if judger_choice==2:
            judge2(filename=input_fname,verdictreport=output_fname)
        elif judger_choice==3:
            judge3(filename=input_fname,verdictreport=output_fname)

def judge2(filename='raw_F',verdictreport='atom_conclusion'):
	MONITORING_WINDOW = 200
	WINDOW_LEAD = 10 	# Leading time to conclude whether an atom is long or short. If tc < lead -> short. If tc > window-lead -> long
	LOW_THRESHOLD = 3
	HIGH_THRESHOLD = 8
	REDCHI_CRIT = 1.25	# Upper limit for reduced chi square to conclude single atom case. For 95% confidence single tail, and (100-4) dof, the value is around 1.25
	print('JUDGING FILE %s' %filename)
	data1 = np.genfromtxt(filename)
	nof_atoms = np.size(data1, axis = 0) - 1	# Minus one because the first row contains the time information.
	result = ["#no" + "\t" + "verdict" + "\t" + "redchi" + "\t" + "low" + "\t" + "high" + "\t" + "change" ]
	cases_counter = [0, 0, 0, 0, 0]	# SA, LG, SH, MA/UC, UC

	for no in range(1, nof_atoms+1):

		# Obtaining data
		datax = data1[0]
		datay = data1[no]

		redchi = 100	# Initial value of redchi

		# Look at each bins (except first 2 and last 2)
		for i in datax[2:-2]:

			# Left and right of each bins
			index = np.where(datax == i)[0]	# Return the index where the thing is located
			left_data = datay[0:index]	# The zeroth element up to (not including index)
			right_data = datay[index+1:]	# The element after index
			# Number of data points
			n_left = np.size(left_data)
			n_right = np.size(right_data)
			# Find the mean
			left_mean = np.mean(left_data)
			right_mean = np.mean(right_data)
			# Find the variances
			left_variance = np.sum((left_data-left_mean)**2/left_mean) / (n_left - 1)
			right_variance = np.sum((right_data-right_mean)**2/right_mean) / (n_right - 1)
			# Find total residuals
			total_res = left_variance * n_left +  right_variance * n_right
			# Find estimated reduced chisquare from residuals
			est_redchi = total_res / (n_left + n_right)
			# print i, est_redchi

			# Update the parameters if the chi squared of the newest fit is better (i.e. looking for minimum chisq)
			if est_redchi < redchi:
				redchi = est_redchi
				low_est = right_mean
				high_est = left_mean
				change_est = i

		# Printing final result
		print "Final Result for case", no, ":"
		print "Reduced Chi Squared:", redchi
		print "Low/high level:", low_est, high_est
		print "Jumping (change) time:", change_est

		# Selecing cases;
		#	MA/UC - Many atoms or unconclusive
		#	LG - Long atoms
		#	SH - Short atoms
		#	SA - Single atoms
		# 	UC - Unconclusive
		if redchi > REDCHI_CRIT:
			verdict = "MA/UC"
			cases_counter[3] += 1
		elif (low_est > LOW_THRESHOLD or change_est > (MONITORING_WINDOW - WINDOW_LEAD) ) and (high_est > HIGH_THRESHOLD):
			verdict = "LG"
			cases_counter[1] += 1
		elif (high_est < HIGH_THRESHOLD or change_est < WINDOW_LEAD) and (low_est < LOW_THRESHOLD):
			verdict = "SH"
			cases_counter[2] += 1
		elif (high_est > HIGH_THRESHOLD) and (low_est < LOW_THRESHOLD) and (change_est > WINDOW_LEAD) and (change_est < (MONITORING_WINDOW - WINDOW_LEAD) ):
			verdict = "SA"
			cases_counter[0] += 1
		else:
			verdict = "UC"
			cases_counter[4] += 1


		print "Verdict:", verdict

		# # Plotting nonsense
		# dataybest = z_function(datax, low_est, step_est, change_est, resp_est)

		# plt.plot(datax, datay, marker='o')
		# plt.plot(datax, dataybest)
		# plt.ylabel("Count rate (ms$^{-1}$)")
		# plt.xlabel("Time (ms)")
		# # plt.ylim([0,20])
		# name = 'Figure ' + str(no)
		# plt.title(name)

		# plt.show()

		result_string = str(no) + "\t" + verdict + "\t" + '%.3f'%round(redchi,3) + "\t" + '%.3f'%round(low_est,3) + "\t" + '%.3f'%round(high_est,3) + "\t" + '%.3f'%round(change_est,3)
		result.append(result_string)

	# print result
	with open(verdictreport, "w") as myfile:
		myfile.write("# Sorted cases: Single atoms (SA) / Long atoms (LG) / Short atoms (SH) / Multi atoms or unconclusive (MA/UC) / Unconclusive (UC)" + '\n')
		myfile.write("# " + str(cases_counter[0]) + " / " + str(cases_counter[1]) + " / " + str(cases_counter[2]) + " / " + str(cases_counter[3]) + " / " + str(cases_counter[4]) + "\n")
		myfile.write("# Details of each cases is given below" + '\n')
		for stuffs in result:
			myfile.write(stuffs + '\n')

def judge3(filename='raw_R',verdictreport='atom_conclusion'):
	MONITORING_WINDOW = 200
	WINDOW_LEAD = 10 	# Leading time to conclude whether an atom is long or short. If tc < lead -> short. If tc > window-lead -> long
	LOW_THRESHOLD = 3
	HIGH_THRESHOLD = 8
	REDCHI_CRIT = 1.25	# Upper limit for reduced chi square to conclude single atom case. For 95% confidence single tail, and (100-4) dof, the value is around 1.25
	print('JUDGING FILE %s' %filename)
	data1 = np.genfromtxt(filename)
	nof_atoms = np.size(data1, axis = 0) - 1	# Minus one because the first row contains the time information.
	result = ["#no" + "\t" + "verdict" + "\t" + "redchi" + "\t" + "low" + "\t" + "high" + "\t" + "change" + "\t" + "vet_sepratio"]
	cases_counter = [0, 0, 0, 0, 0, 0]	# SA/SA, LG, SH, MA/UC, UC, SA/MA

	for no in range(1, nof_atoms+1):

		# Obtaining data
		datax = data1[0]
		datay = data1[no]

		redchi = 100	# Initial value of redchi

		# Look at each bins (except first 2 and last 2)
		for i in datax[2:-2]:

			# Left and right of each bins
			index = np.where(datax == i)[0][0]	# Return the index where the thing is located
			left_data = datay[0:index]	# The zeroth element up to (not including index)
			right_data = datay[index+1:]	# The element after index
			# Number of data points
			n_left = np.size(left_data)
			n_right = np.size(right_data)
			# Find the mean
			left_mean = np.mean(left_data)
			right_mean = np.mean(right_data)
			# Find the normalised variances (usually called mean residuals I think)
			if left_mean != 0:	# Handles zero division error
				left_variance = np.sum((left_data-left_mean)**2/left_mean) / (n_left - 1)
			else:
				left_variance = 0
			if right_mean != 0: # Handles zero division error
				right_variance = np.sum((right_data-right_mean)**2/right_mean) / (n_right - 1)
			else:
				right_variance = 0
			# Find total residuals
			total_res = left_variance * n_left +  right_variance * n_right
			# Find estimated reduced chisquare from residuals
			est_redchi = total_res / (n_left + n_right)
			# print i, est_redchi

			# Update the parameters if the chi squared of the newest fit is better (i.e. looking for minimum chisq)
			if est_redchi < redchi:
				redchi = est_redchi
				low_est = right_mean
				high_est = left_mean
				change_est = i

		# Printing final result
		print "Final Result for case", no, ":"
		print "Reduced Chi Squared:", redchi
		print "Low/high level:", low_est, high_est
		print "Jumping (change) time:", change_est

		# Setting vet_sep_ratio to undefined (-1), except single atom cases (will be modified during second vetting process)
		vet_sepratio = -1

		# Selecing cases;
		#	MA/UC - Many atoms or unconclusive
		#	LG - Long atoms
		#	SH - Short atoms
		#	SA - Single atoms
		# 	UC - Unconclusive
		if redchi > REDCHI_CRIT:
			verdict = "MA/UC"
			cases_counter[3] += 1
		elif (low_est > LOW_THRESHOLD or change_est >= (MONITORING_WINDOW - WINDOW_LEAD) ) and (high_est > HIGH_THRESHOLD):
			verdict = "LG"
			cases_counter[1] += 1
		elif (high_est < HIGH_THRESHOLD or change_est <= WINDOW_LEAD) and (low_est < LOW_THRESHOLD):
			verdict = "SH"
			cases_counter[2] += 1
		elif (high_est > HIGH_THRESHOLD) and (low_est < LOW_THRESHOLD) and (change_est > WINDOW_LEAD) and (change_est < (MONITORING_WINDOW - WINDOW_LEAD) ):
			verdict = "SA"
			# Cases counter is performed in the second vetting process
		else:
			verdict = "UC"
			cases_counter[4] += 1

		print "Verdict:", verdict

		# Second vetting process
		if verdict == "SA":
			print "ADDDIIONAL PROCESSING: Vetting the SA cases"
			# Get the data before the atom escapes (btae)
			btae_index = np.where(datax == change_est)[0][0]
			print btae_index
			btae_data = datay[0:btae_index]
			sepratio = 0
			# Scanning each bins in btae (find where std error of mean is unexpected)
			for i in datax[2:btae_index-2]:
				# Get lefty and righty (similar procedure as previously)
				scan_index = np.where(datax == i)[0][0]	# Return the index where the thing is located
				lefty_data = btae_data[0:scan_index]	# The zeroth element up to (not including index)
				righty_data = btae_data[scan_index+1:]	# The element after index
				# Number of data points
				n_lefty = np.size(lefty_data)
				n_righty = np.size(righty_data)
				# Find the data mean
				lefty_mean = np.mean(lefty_data)
				righty_mean = np.mean(righty_data)
				# Expected value of mean and stderr_mean
				exp_mean = high_est
				lefty_stderr = exp_mean / np.sqrt(exp_mean * n_lefty)
				righty_stderr = exp_mean / np.sqrt(exp_mean * n_righty)
				# Comparison
				lefty_sepratio = abs(lefty_mean - exp_mean) / lefty_stderr
				righty_sepratio = abs(righty_mean - exp_mean) / righty_stderr
				sepratio = max(sepratio, lefty_sepratio, righty_sepratio)
			print "Separation ratio:", sepratio
			vet_sepratio = sepratio
			if sepratio > 3:	# 3 sigma away from expected value: 0.3% type I error only >> actually quite a lax criteria, but it works nicely here
				verdict = "MA/VT"
				cases_counter[5] += 1
			else:
				verdict = "SA"	# Single atom filtered by two methods of checking
				cases_counter[0] += 1
			print "Final verdict:", verdict

		result_string = str(no) + "\t" + verdict + "\t" + '%.3f'%round(redchi,3) + "\t" + '%.3f'%round(low_est,3) + "\t" + '%.3f'%round(high_est,3) + "\t" + '%.3f'%round(change_est,3) + "\t" + '%.3f'%round(vet_sepratio,3)
		result.append(result_string)
		print "-"*60

	# print result
	with open(verdictreport, "w") as myfile:
		myfile.write("# Sorted cases: True single atoms (SA) / Long atoms (LG) / Short atoms (SH) / Multi atoms or unconclusive (MA/UC) / Unconclusive (UC) / Vetted as multi atom (MA/VT)" + '\n')
		myfile.write("# " + str(cases_counter[0]) + " / " + str(cases_counter[1]) + " / " + str(cases_counter[2]) + " / " + str(cases_counter[3]) + " / " + str(cases_counter[4]) + " / " + str(cases_counter[5]) + '\n')
		myfile.write("# Details of each cases is given below" + '\n')
		for stuffs in result:
			myfile.write(stuffs + '\n')
'''
if __name__ == '__main__':
#judge(filename='F/264.dat',verdictreport='264_vd')
	tar_path='merge_norm/F'
	mass_judge(tar_path)
'''
