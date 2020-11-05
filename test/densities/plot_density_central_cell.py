import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)) +
    '/../../python_scripts')
from read_binary_output import *
import smash_basic_scripts as sb
import glob
import yaml

matplotlib.rcParams.update({'font.size': 16,
                            'axes.labelsize': 22,
                            'mathtext.default':'rm',
                            'legend.fontsize': 10,
                            'font.sans-serif':['Helvetica'],
                            'font.family':'sans-serif'})

PathToData = sys.argv[1]
Config = sys.argv[2]
DataOutfile = sys.argv[3]
PlotName = sys.argv[4]
try:
  comp_prev_version = sys.argv[5]
  comp_prev_version = True
except IndexError:
  comp_prev_version = False

with open(Config, 'r') as f: config_file = yaml.safe_load(f)
TimeSteps = config_file['Output']['Output_Interval']
FinalTime = config_file['General']['End_Time']
Energy = config_file['Modi']['Collider']['E_Kin']
StartTime = -3 # fm
TimeSteps = np.arange(StartTime, FinalTime, TimeSteps)
smash_analysis_version = sb.analysis_version_string()
setup ='AuAu_central_cell'

with open(PathToData + '/0/thermodynamics.dat') as f:
    smash_version = f.readline().split(' ')[1]

NFolders = 10
dirs = np.arange(0, NFolders + 1)

n_events = 0
dens_list = np.zeros(len(TimeSteps))
for dir in dirs:
    data_file = PathToData + '/{}/thermodynamics.dat'.format(dir)
    with open(data_file) as f:
        for rawline in f:
            line = rawline.split()
            # event heading
            if line[0] == "#" and line[1] == "event":
                n_events += 1
                t_counter = 0
            # data line
            if line[0] != "#":
                dens_list[t_counter] += float(line[1])
                t_counter +=1
dens_arr = np.asarray(dens_list)
dens_arr = dens_arr/(n_events*0.16)  # density in units of ground state density

header = '# AuAu @ Ekin = {}AGeV\n# smash and smash analysis version\n# {} {}\n# time[fm]  rho/rho_0\n x    y'.format(Energy, smash_version, smash_analysis_version)
np.savetxt(DataOutfile, np.c_[TimeSteps, dens_arr], header=header, comments='')

if comp_prev_version:
    import comp_to_prev_version as cpv
    processes = []
    cpv.plot_previous_results('densities', setup, '/' + DataOutfile.split('/')[-1])

# old version ?
plt.plot(TimeSteps, dens_arr, linewidth=2, linestyle="-", label='AuAu')
plt.text(0.3, 4.5, " SMASH code:      %s\n SMASH analysis: %s\n" % \
            (smash_version, smash_analysis_version), \
            color = "gray", fontsize = 7)
plt.title(r'AuAu, central cell, $E_{} = {}$ AGeV'.format('{Kin}', Energy))
plt.xlabel(r'$t\rm [fm]$')
plt.ylabel(r'$\rho_B/\rho_0$')
plt.xlim(0,40)
plt.ylim(0,5)
plt.tight_layout()
plt.legend()
plt.savefig(PlotName)
