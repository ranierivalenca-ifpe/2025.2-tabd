import survey
import os
import subprocess

TESTS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "tests")
SCAFFOLD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "scaffold-template")

cmds = (
    "execute",
    "scaffold",
)

def execute(path):
    subprocess.run('./run.sh {}'.format(path), shell=True, check=True)

def scaffold():
    directory = survey.routines.input("Enter project directory name:")
    print(f"Scaffolding project in directory: {directory}")
    try:
        path = os.path.join(TESTS_PATH, directory)
        os.makedirs(path, exist_ok=False)
        subprocess.run(
            "cp -R {}/ {}".format(SCAFFOLD_PATH, path), shell=True, check=True
        )
        print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
        scaffold()  # Retry if directory exists


def exec():
    # list tests path directories sorted by creation time
    directories = os.listdir(TESTS_PATH)
    print("Available project directories:")
    options = ()
    for d in sorted(
        directories,
        key=lambda x: os.path.getctime(os.path.join(TESTS_PATH, x)),
        reverse=True,
    ):
        full_path = os.path.join(TESTS_PATH, d)
        if os.path.isdir(full_path):
            options += (d,)
    if not options:
        print("No project directories found. Please scaffold a new project first.")
        return
    dir_index = survey.routines.select(
        "Select a project directory to execute:", options=options
    )
    if dir_index is None:
        return
    directory = os.path.join(TESTS_PATH, options[dir_index])
    print(f"Executing project in directory: {directory}")
    execute(directory)


def run(cmd):
    if cmd == "scaffold":
        scaffold()
    elif cmd == "execute":
        exec()


if __name__ == "__main__":
    try:
        index = survey.routines.select("Select a command:", options=cmds)
        if index is not None:
            run(cmds[index])
    except survey._widgets.Escape:
        print("Operation cancelled by user.")
