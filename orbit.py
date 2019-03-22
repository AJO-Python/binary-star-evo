import orbit_functions
import Integrator

#  simulate(destination_directory, continue,
#	save_suffix=, init_conds_name=, init_conds_directory=)
init_file="/init_conds.txt"
direc = "/home/ug/c1672922/results/run3"
Integrator.simulate(direc, False, init_conds_name=init_file)
