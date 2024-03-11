"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""

import sys
sys.path.insert(1, "./src/")


import config
from pathlib import Path
from doit.tools import run_once
import platform

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)


env_file = ".env"
env_example_file = "env.example"

import os
import shutil
if not os.path.exists(env_file):
    shutil.copy(env_example_file, env_file)


def get_os():
    os_name = platform.system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Darwin":
        return "nix"
    elif os_name == "Linux":
        return "nix"
    else:
        return "unknown"

os_type = get_os()


def task_pull_RCON_RCOA():
    """Pull RCON and RCOA from WRDS and save to disk
    """
    file_dep = [
        "./src/config.py", 
        "./src/load_WRDS.py",
        ]
    targets = [
        Path(DATA_DIR) / "pulled" / file for file in 
        [
            "RCFD_Series_1.parquet", 
            "RCFD_Series_2.parquet", 
            "RCON_Series_1.parquet",
            "RCON_Series_2.parquet",
        ]
    ]

    return {
        "actions": [
            "ipython src/config.py",
            "ipython src/load_WRDS.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
        "verbosity": 2, 
        # Print everything immediately. This is important in
        # case WRDS asks for credentials.
    }

def task_run_calculation():
    """Run .py files and output replication figures"""
    file_dep = [Path("./src") / file for file in ["load_assets.py", "load_WRDS.py", "Clean_data.py", "Calc_table_statistic.py"]]
    file_output = ["Table1.tex"]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/Calc_table_statistic.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_extra_plot():
    """Extra plots"""
    file_dep = [Path("./src") / file for file in ["extra_plots.py", "data_read.py"]]
    file_output = ["Treasury_by_Maturity.png", "MBS_and_Treasury.png"]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/extra_plots.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""
    file_dep = [
        "./reports/project_report.tex",
        "./src/extra_plots.py",
        # "./src/example_table.py",
    ]
    file_output = [
        "./reports/project_report.pdf",
    ]
    targets = [file for file in file_output]

    return {
        "actions": [
            "latexmk -xelatex -cd ./reports/project_report.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/project_report.tex",  # Clean
            # "latexmk -CA -cd ../reports/",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }
