import Integrator

#  simulate(destination_directory, continue,
#	save_suffix=, init_conds_name=, init_conds_directory=)
init_file="init_conds.txt"
#direc = "/home/ug/c1672922/results/run1"
direc = "results/test/"
#init_dir = "./results/test"

Integrator.simulate(direc,
                    CONT_PREVIOUS=False,
                    init_conds_name=init_file,
                    report_pos=100)

#Integrator.simulate(
#        destination_directory, ----> Directory to save results in
#        CONT_PREVIOUS,		----> Continue from previous data
#        save_suffix=,		----> eg "masses{save_suffix}.csv"
#        init_conds_name=,	----> Name of initial conditions file
#        init_conds_directory=,	----> Location of initial conds file
#        source_directory=,	----> Location of previous data for continuing
#        report_pos=100		----> Frequency of data saves (in time steps)


"""

run1 = some old test. Who knows?
run2 = Test for plotting bug. Getting diagonal line
run3 = Tweaking of x-coords
run4 = increased X x100 and y,z x10
run5 = 10,000 au cluster seperation
        0.1pc

"""
