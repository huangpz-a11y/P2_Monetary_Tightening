Final Project - Monetary Tightening and US Bank Fragility
==================

### Team Members: Maxwell Dender, Peizhe Huang, Juan Ramirez, Leon Tan, and Jason Wang
# About this project


This is our Team's Data Science Tool for Finance final project. In this project we attempt to replicate the results of Table 1 found in Monetary Tightening and US Bank Fragility in 2023: Mark-To-Market Losses and Uninsured Depositor Runs, written by Erica Xuewei Jiang, Gregor Matvos,Tomasz Piskorski, and Amit Seru.

# Team Contribution

- Jason Wang - Main logic (table 1 and 2), WRDS data pulling automation and data cleaning, dodo.py (data pulling)
- Peizhe Huang - Latex document generation and dodo.py (latex and jupyter notebook automations)
- Maxwell Dender - Main logic (table 1 and 2), Data Exploration, Summary Statistics, unit tests (alternative % cushion)
- Juan Ramirez - Unit Tests, Jupyter Notebooks Data Exploration (01, 02, 03 notebooks)
- Leon Tan - GSIB preliminary analysis

# Manual Data Explanation:

1. MBS_ETF.csv
- Description: iShare MBS ETF (used for RMBs Multiplier)
- Source: https://finance.yahoo.com/quote/MBB/

2. S&P 1-3.xlsx
- Description: S&P U.S. Treasury Bond 1-3 Year Index 
- Source: https://www.spglobal.com/spdji/en/indices/fixed-income/sp-us-treasury-bond-1-3-year-index/#overview 

3. S&P 3-5.xlsx
- Description: S&P U.S. Treasury Bond 3-5 Year Index
- Source: https://www.spglobal.com/spdji/en/indices/fixed-income/sp-us-treasury-bond-3-5-year-index/ 

4. S&P 7-10.xlsx
- Description: S&P U.S. Treasury Bond 7-10 Year Index
- Source: https://www.spglobal.com/spdji/en/indices/fixed-income/sp-us-treasury-bond-7-10-year-index/#overview

5. Treasury_Index.xlsx
- Description: S&P Treasury Index (used for RMBs Multiplier)
- Source: https://www.spglobal.com/spdji/en/indices/fixed-income/sp-us-treasury-bond-index/#overview

6. cipzs5x6g2axzlhe.csv
- Description: rcfn (used for initial exploration)
- Source: https://wrds-www.wharton.upenn.edu/login/?next=/pages/get-data/bank-regulatory/call-reports/rcfn-series/

7. combined_index_df.xlsx
- Description: Combined Treasury indices for mark-to-market calculations (see 03_data_construction_JR.ipynb)
- Source: 03_data_construction_JR.ipynb

8. ddss0fpozaxonboe.csv
- Description: Series 1 of rcfd (used for unit test and initial exploration)
- Source: https://wrds-www.wharton.upenn.edu/pages/get-data/bank-regulatory/call-reports/rcfd-series-1/

9. dycfrwcdm9puanhs.csv
- Description: Series 2 of rcfd (used for unit test and initial exploration)
- Source: https://wrds-www.wharton.upenn.edu/login/?next=/pages/get-data/bank-regulatory/call-reports/rcfd-series-2/

10. hwv0m9qml6efztsi.csv
- Description: Series 2 of rcon (used for unit test and initial exploration)
- Source: https://wrds-www.wharton.upenn.edu/pages/get-data/bank-regulatory/call-reports/rcon-series-2/

11. m3pzkcjsgvk26dwa.csv
- Description: Series 1 of rcon (used for unit test and initial exploration)
- Source: https://wrds-www.wharton.upenn.edu/pages/get-data/bank-regulatory/call-reports/rcon-series-1/

12. nw5crmbtaa03thi9.csv
- Description: FR Y-9C (Used for GSIB exploration)
- Source: https://wrds-www.wharton.upenn.edu/pages/get-data/bank-regulatory/variable-metadata/variable-metadata/

# Notes for Future Reference

 - [] Insured deposits figures are far off
 - [] Uninsured deposits are quite close, but there are big differences among GSIBs
 - [] Would be nice to know what's in the "Share Other Loan" category.
 - [] Too many data sets in the "manual" folder. These should be handled automatically.

# Quick Start

To quickest way to run code in this repo is to use the following steps. First, note that you must have TexLive installed on your computer and available in your path.
You can do this by downloading and installing it from here ([windows](https://tug.org/texlive/windows.html#install) and [mac](https://tug.org/mactex/mactex-download.html) installers).
Having installed LaTeX, open a terminal and navigate to the root directory of the project and create a conda environment using the following command:
```
conda create -n blank python=3.12
conda activate blank
```
and then install the dependencies with pip
```
pip install -r requirements.txt
```
You can then navigate to the `src` directory and then run 
```
doit
```

## Other commands

You can run the unit test, including doctests, with the following command:
```
pytest --doctest-modules
```
You can build the documentation with:
```
rm ./src/.pytest_cache/README.md 
jupyter-book build -W ./
```
Use `del` instead of rm on Windows


# General Directory Structure

 - The `assets` folder is used for things like hand-drawn figures or other pictures that were not generated from code. These things cannot be easily recreated if they are deleted.

 - The `output` folder, on the other hand, contains tables and figures that are generated from code. The entire folder should be able to be deleted, because the code can be run again, which would again generate all of the contents.

 - I'm using the `doit` Python module as a task runner. It works like `make` and the associated `Makefile`s. To rerun the code, install `doit` (https://pydoit.org/) and execute the command `doit` from the `src` directory. Note that doit is very flexible and can be used to run code commands from the command prompt, thus making it suitable for projects that use scripts written in multiple different programming languages.

 - I'm using the `.env` file as a container for absolute paths that are private to each collaborator in the project. You can also use it for private credentials, if needed. It should not be tracked in Git.

# Data and Output Storage

I'll often use a separate folder for storing data. I usually write code that will pull the data and save it to a directory in the data folder called "pulled"  to let the reader know that anything in the "pulled" folder could hypothetically be deleted and recreated by rerunning the PyDoit command (the pulls are in the dodo.py file).

I'll usually store manually created data in the "assets" folder if the data is small enough. Because of the risk of manually data getting changed or lost, I prefer to keep it under version control if I can.

Output is stored in the "output" directory. This includes tables, charts, and rendered notebooks. When the output is small enough, I'll keep this under version control. I like this because I can keep track of how tables change as my analysis progresses, for example.

Of course, the data directory and output directory can be kept elsewhere on the machine. To make this easy, I always include the ability to customize these locations by defining the path to these directories in environment variables, which I intend to be defined in the `.env` file, though they can also simply be defined on the command line or elsewhere. The `config.py` is reponsible for loading these environment variables and doing some like preprocessing on them. The `config.py` file is the entry point for all other scripts to these definitions. That is, all code that references these variables and others are loading by importing `config`.


# Dependencies and Virtual Environments

## Working with `pip` requirements

`conda` allows for a lot of flexibility, but can often be slow. `pip`, however, is fast for what it does.  You can install the requirements for this project using the `requirements.txt` file specified here. Do this with the following command:
```
pip install -r requirements.txt
```

The requirements file can be created like this:
```
pip list --format=freeze
```

## Working with `conda` environments

The dependencies used in this environment (along with many other environments commonly used in data science) are stored in the conda environment called `blank` which is saved in the file called `environment.yml`. To create the environment from the file (as a prerequisite to loading the environment), use the following command:

```
conda env create -f environment.yml
```

Now, to load the environment, use

```
conda activate blank
```

Note that an environment file can be created with the following command:

```
conda env export > environment.yml
```

However, it's often preferable to create an environment file manually, as was done with the file in this project.

Also, these dependencies are also saved in `requirements.txt` for those that would rather use pip. Also, GitHub actions work better with pip, so it's nice to also have the dependencies listed here. This file is created with the following command:

```
pip freeze > requirements.txt
```

### Alternative Quickstart using Conda
Another way to  run code in this repo is to use the following steps.
First, open a terminal and navigate to the root directory of the project and create a conda environment using the following command:
```
conda env create -f environment.yml
```
Now, load the environment with
```
conda activate blank
```
Now, navigate to the directory called `src`
and run
```
doit
```
That should be it!



**Other helpful `conda` commands**

- Create conda environment from file: `conda env create -f environment.yml`
- Activate environment for this project: `conda activate blank`
- Remove conda environment: `conda remove --name blank --all`
- Create blank conda environment: `conda create --name myenv --no-default-packages`
- Create blank conda environment with different version of Python: `conda create --name myenv --no-default-packages python` Note that the addition of "python" will install the most up-to-date version of Python. Without this, it may use the system version of Python, which will likely have some packages installed already.

## `mamba` and `conda` performance issues

Since `conda` has so many performance issues, it's recommended to use `mamba` instead. I recommend installing the `miniforge` distribution. See here: https://github.com/conda-forge/miniforge

