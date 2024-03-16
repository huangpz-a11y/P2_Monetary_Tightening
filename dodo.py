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

# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on

env_file = ".env"
env_example_file = "env.example"

import os
import shutil

if not os.path.exists(env_file):
    shutil.copy(env_example_file, env_file)


# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


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

def copy_notebook_to_folder(notebook_stem, origin_folder, destination_folder):
    origin_path = Path(origin_folder) / f"{notebook_stem}.ipynb"
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / f"_{notebook_stem}.ipynb"
    if os_type == "nix":
        command = f"cp {origin_path} {destination_path}"
    else:
        command = f"copy  {origin_path} {destination_path}"
    return command

def copy_notebook_to_folder(notebook_stem, origin_folder, destination_folder):
    origin_path = Path(origin_folder) / f"{notebook_stem}.ipynb"
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / f"_{notebook_stem}.ipynb"
    if os_type == "nix":
        command = f"cp {origin_path} {destination_path}"
    else:
        command = f"copy  {origin_path} {destination_path}"
    return command


def task_pull_RCON_RCOA():
    """Pull RCON and RCOA from WRDS and save to disk"""
    file_dep = [
        "./src/config.py",
        "./src/load_WRDS.py",
    ]
    targets = [
        Path(DATA_DIR) / "pulled" / file
        for file in [
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
    file_dep = [
        Path("./src") / file
        for file in [
            "load_assets.py",
            "load_WRDS.py",
            "Clean_data.py",
            "Calc_table_statistic.py",
        ]
    ]
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

def task_convert_notebooks_to_scripts():
    """Preps the notebooks for presentation format.
    Execute notebooks with summary stats and plots and remove metadata.
    """
    build_dir = Path(OUTPUT_DIR)
    build_dir.mkdir(parents=True, exist_ok=True)

    notebooks = [
        "01_Final_Project_Exploration.ipynb",
        "02_Final_Updated_Analysis.ipynb",
        "03_data_construction_JR.ipynb",
    ]
    file_dep = [Path("./src") / file for file in notebooks]
    stems = [notebook.split(".")[0] for notebook in notebooks]
    targets = [build_dir / f"_{stem}.py" for stem in stems]

    actions = [
        # *[jupyter_execute_notebook(notebook) for notebook in notebooks_to_run],
        # *[jupyter_to_html(notebook) for notebook in notebooks_to_run],
        *[jupyter_clear_output(notebook) for notebook in stems],
        *[jupyter_to_python(notebook, build_dir) for notebook in stems],
    ]
    return {
        "actions": actions,
        "targets": targets,
        "task_dep": [],
        "file_dep": file_dep,
        "clean": True,
    } 


def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks with summary stats and plots and remove metadata.
    """
    notebooks = [
        "01_Final_Project_Exploration.ipynb",
        "02_Final_Updated_Analysis.ipynb",
        "03_data_construction_JR.ipynb",
    ]
    stems = [notebook.split(".")[0] for notebook in notebooks]

    file_dep = [
        # 'load_other_data.py',
        *[Path(OUTPUT_DIR) / f"_{stem}.py" for stem in stems],
    ]

    targets = [
        ## 01_example_notebook.ipynb output
        ##OUTPUT_DIR / "sine_graph.png",
        ## Notebooks converted to HTML
        *[OUTPUT_DIR / f"{stem}.html" for stem in stems],
    ]

    actions = [
        *[jupyter_execute_notebook(notebook) for notebook in stems],
        *[jupyter_to_html(notebook) for notebook in stems],
        *[copy_notebook_to_folder(notebook, Path("./src"), "./docs/_notebook_build/") for notebook in stems],
        *[jupyter_clear_output(notebook) for notebook in stems],
        # *[jupyter_to_python(notebook, build_dir) for notebook in notebooks_to_run],
    ]
    return {
        "actions": actions,
        "targets": targets,
        "task_dep": [],
        "file_dep": file_dep,
        "clean": True,
    }







notebooks_and_targets = {
    "01_Final_Project_Exploration.ipynb": [],
    "02_Final_Updated_Analysis.ipynb": [],
    "03_data_construction_JR.ipynb": [],
    # "04_final_project_exploration_jason_wang.ipynb": [],
}


def task_convert_notebooks_to_scripts():
    """Convert notebooks to script form to detect changes to source code rather
    than to the notebook's metadata.
    """
    build_dir = Path(OUTPUT_DIR)
    build_dir.mkdir(parents=True, exist_ok=True)

    stems = [notebook.split(".")[0] for notebook in notebooks_and_targets.keys()]
    for notebook in stems:
        yield {
            "name": f"{notebook}.ipynb",
            "actions": [
                # jupyter_execute_notebook(notebook),
                # jupyter_to_html(notebook),
                # copy_notebook_to_folder(notebook, Path("./src"), "./docs/_notebook_build/"),
                jupyter_clear_output(notebook),
                jupyter_to_python(notebook, build_dir),
            ],
            "file_dep": [Path("./src") / f"{notebook}.ipynb"],
            "targets": [build_dir / f"_{notebook}.py"],
            "clean": True,
            'verbosity': 0,
        }


def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks if the script version of it has been changed.
    """

    stems = [notebook.split(".")[0] for notebook in notebooks_and_targets.keys()]
    for notebook in stems:
        yield {
            "name": f"{notebook}.ipynb",
            "actions": [
                jupyter_execute_notebook(notebook),
                jupyter_to_html(notebook),
                copy_notebook_to_folder(
                    notebook, Path("./src"), "./docs/_notebook_build/"
                ),
                jupyter_clear_output(notebook),
                # jupyter_to_python(notebook, build_dir),
            ],
            "file_dep": [OUTPUT_DIR / f"_{notebook}.py"],
            "targets": [
                *notebooks_and_targets[f"{notebook}.ipynb"],
                OUTPUT_DIR / f"{notebook}.html",
            ],
            "clean": True,
            'verbosity': 0,
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
