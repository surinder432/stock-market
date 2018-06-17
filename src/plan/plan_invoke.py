#!/usr/bin/python

import sys
import re
import csv
import traceback
import plan

from operator import itemgetter


# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 3 :
   print "usage: " + program_name + " <debug_level : 1-4> <plan.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
in_filename = sys.argv[2]
out_filename_phase2 = sys.argv[3]
out_filename_phase3 = sys.argv[4]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

indu_comp = 'comp'
ic_name = 'all'

if len(sys.argv) == 7 :
	indu_comp = sys.argv[5]
	ic_name = sys.argv[6]
	ic_name = ic_name.capitalize()

plan = plan.Plan()

plan.set_debug_level(debug_level)

plan.load_plan_data(in_filename)

plan.print_phase2(out_filename_phase2)
plan.print_phase3(out_filename_phase3)

if len(sys.argv) == 7 :
	if indu_comp.lower() == "comp":
		print 'companies count : ', plan.size_comp_data()
		if ic_name == "All":
			plan.print_comp_data()
		else:
			print plan.get_comp_units(ic_name)
	else:
		print 'industries count : ', plan.size_indu_data()
		if ic_name == "All":
			plan.print_indu_data()
		else:
			print plan.get_indu_units(ic_name)