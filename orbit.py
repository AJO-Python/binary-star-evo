import orbit_functions
import Integrator

#  simulate(destination_directory, continue,
#	save_suffix=, init_conds_name=, init_conds_directory=)
init_file="/init_conds.txt"
direc = "/home/ug/c1672922/results/run6"

Integrator.simulate(direc, False, init_conds_name=init_file, report_pos=100)

"""

run1 = some old test. Who knows?
run2 = Test for plotting bug. Getting diagonal line
run3 = Tweaking of x-coords
run4 = increased X x100 and y,z x10

"""
