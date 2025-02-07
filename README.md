# SMASH-analysis

The SMASH-analysis suite contains various tools and scripts useful to compute
different observables from the output generated by the
[SMASH](https://smash-transport.github.io) transport code. Most of this scripts
are written in python. The latest results
extracted by means of the SMASH-analysis suite, can be found
[here](http://theory.gsi.de/~smash/analysis_suite/current/).

Among the observables and cross-checks that are extracted with the scripts in
this repository are:
- **Energy Scan**<br/>
  Multiplicities, midrapidity yields, transverse momentum and rapidity spectra
  for the most abundant hadron species over a large range of beam energies.


## Prerequisites
Running SMASH for the above listed observables to generate the necessary data
sets is embedded in the SMASH-analysis suite. As such, the SMASH source
code (if run on a cluster), or at least the SMASH binary needs to be accessible
from where the SMASH-analysis suite is executed.
The SMASH source code as well as further instructions how to download and
compile it can be found [here](https://github.com/smash-transport/smash).

Thus, SMASH-analysis suite has been tested with the following software versions:
- SMASH version = (SMASH-analysis version)
- cmake version &ge; 3.16.3

The SMASH-analysis suite is regularly tagged (SMASH-ana-1.6 and later),
where it is ensured that the SMASH-analysis version is compatible with the
same version of the SMASH transport code. Please make sure to use compatible
versions.

Furthermore, Python 3.8.x is necessary with the following modules:

- [numpy](www.numpy.org) version &ge; 1.17.4
- [scipy](www.scipy.org) version &ge; 1.3.3
- [matplotlib](www.matplotlib.org) version &ge; 3.1.2
- [argparse](https://docs.python.org/3/library/argparse.html) version &ge; 1.1
- [pyyaml](www.pyyaml.org) version &ge; 5.3.1
- [pandas](www.pandas.pydata.org) version &ge; 0.25.3

Python 2 is not supported anymore. The versions of Python and the different
modules can be determined by running the script `version_check.py` located in
the `smash-analysis/python_scripts` directory. The versions listed above have
been verified to work. Different versions (newer or slightly older) could work
fine as well, but it is not guaranteed. Any missing python modules
(e.g. pandas) can be installed via the python package installer
[pip](https://pypi.org/project/pip/):

    pip install --user pandas

For further details, see
[here](http://pip.readthedocs.org/en/latest/reference/pip_install.html).
If the pip module itself is not available, it can be installed via

    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py --user

Then the remaining modules (e.g. pandas) can be installed via:

    python -m pip install --user pandas

In order to install a particular version of a module (e.g. version 0.14.1 of
pandas), execute:

    python -m pip install --user pandas==0.14.1

For plotting, the DejaVu font is used by default. If font problems in plots
arise, it may be downloaded [here](https://dejavu-fonts.github.io).
After downloading, the font needs to be installed on the system.
It might also be necessary to delete the local matplotlib font cache.

##### Note

Should you encounter severe difficulties installing a numpy version 1.17.3 on your
machine, you may consider using an older version. The only necessary
functionality from numpy 1.17.3 is being used for plotting the detailed balance
results. The simulations and analyses of each target can be carried out with
numpy 1.6.2 or higher. The detailed balance plots can then be created locally
from the generated analysis outputs. <br/>
Remember to adjust the required numpy version in the top level `CMakeLists.txt`
to build the SMASH-analysis suite with an older numpy version. Other adjustments
regarding the minimal version of the required modules are at the
user's own risk.

## Building the SMASH-analysis suite

Use the following commands to create all subtargets of the SMASH-analysis suite
in a separate `build` directory:

    mkdir build
    cd build
    cmake .. -DSMASH_PATH=[...]/smash/build

All subtargets of the analysis suite have been created by `cmake`.

Note though, that most of them are split into simulation targets (`sims`),
analysis targets (`analysis`) and plotting targets (`plots`). This bears the
advantage that the SMASH simulations need not be run again if the date of last
modification has changed because the files where touched unrelated to code
modifications. On the other hand, this procedure requires three
subtargets to be executed one after the other to yield the final plots. In the
example of the scattering rates (called 'elastic_box'), this means the following
commands need to be executed in the appropriate order:

    make elastic_box_sims -jN
    make elastic_box_analysis -jN
    make elastic_box_plots -jN

Where N corresponds to the number of cores, if the SMASH-analysis suite is run
in parallel.

The above described splitting applies to the following targets:
- `angular_distributions`
- `cross_sections`
- `detailed_balance`
- `elastic_box`
- `energy_scan`

In the case of FOPI Pions, there are only two subtargets:

    make FOPI_pions_sims -jN
    make FOPI_pions_plots -jN

And for the dileptons there is only one single target:

    make dileptons -jN

Note, that all dilepton data files generated during the SMASH run are
immediately removed once they have been analyzed, as they are exceptionally
large.   

In case of the afterburner target, the SMASH-analysis suite has to be compiled 
with an additional argument `-DSAMPLED_LISTS`. This has to be an URL from where
the sampled lists as an input for the afterburner target can be downloaded. 
Without this argument, the target is not available. The URL for the lists used
in the latest report is `http://theory.gsi.de/~smash/data/sampled_lists/`.

## Running the SMASH-analysis suite on a SLURM cluster

As most of the targets have a significant runtime (some of them up to several
days), it is recommended to run the SMASH-analysis on a cluster. An exemplary
slurm script, `slurm-job.sh`, is provided in the `smash-analysis`
directory. It may be used and adapted. Note that in this case, also SMASH is
compiled on the computing note.

To submit all the above mentioned targets instantaneously to the cluster, the
script `submit_to_slurm.sh` may be useful. It is currently optimized for the
kronos cluster at GSI. It can be executed via

    ./submit-to-slurm.sh [...]/smash [...]/eigen all [...]/output_dir

where the path to the SMASH directory, the path to the eigen directory, the
target (`all` in this case, such that all targets are being executed) and the
path to the output directory are being passed from the command line.

In case SMASH crashes for some reason, there will be stale lock files which
prevent SMASH to be run again in the same directory. They can be deleted via

    find [...]/output_dir -type f -name smash.lock -exec rm {} \;



## Creating the report

To interpret the generated plots at one glance, it has proven to be most
suitable to create a report in the shape of an html page. The following tools
are required in addition to those listed above:
* Python [subprocesses](https://docs.python.org/3/library/multiprocessing.html)
version &ge; 16.6.1.
* pdftoppm, embedded in [poppler](https://poppler.freedesktop.org)

The html page contains all plots created by means of the SMASH-analysis suite,
sorted by observables. It can be produced by executing the `create_report.sh`
script located in the `smash-analysis` directory:

    ./create_report.sh [...]/output_dir

Where `[...]/output_dir` is the path to the directory, that contains the
results of the SMASH-analysis runs. Note though, that this script relies on a
specific folder structure of these results. It might not work, if the output
directory was created in a different manner than described above.

Upon execution, two new directories are created in the `output_dir` directory.
The first, `PDFs_configs_{smash_version}` is a collection of all plots and
configuration files associated with the SMASH runs. The second,
`report_{smash_version}`, is the actual html report, containing the plots and
references to the configuration files.

Should you encounter difficulties installing poppler on the machine you ran the
SMASH simulations and analysis, you may want to consider copying the
`PDFs_configs_{smash_version}` directory to a different machine and execute the `generate_report_folder.sh` script located in `smash-analysis/test/report`.

## Storing the results for future comparison

Unless disabled, all generated results are compared to those of the previous
tagged SMASH version. The data files corresponding to the results of the latest
version are located in the `old_results` directory, sorted by version. This
collection can be generated by executing the `store_old_results.sh` script,
located in the `test/report` directory:

    cd test/report
    ./store_old_results.sh {smash-version} [...]/output_dir

where {smash-version} is the version of the SMASH code that is being tested and
`output_dir` the directory that contains the results. A new directory with all
data files, `old_results_{smash-version}`, is then created within the
`output_dir`. Note though that it is only useful to assemble the old results
for a newly-tagged version of SMASH. Release candidate tags are usually not
considered.
