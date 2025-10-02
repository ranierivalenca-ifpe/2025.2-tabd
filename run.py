import survey
import os
import subprocess

TESTS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "tests")
SCAFFOLD_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "scaffold-template"
)

cmds = ("execute", "scaffold", "seed")


def execute(path):
    subprocess.run("./run.sh {}".format(path), shell=True, check=True)


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


def select_project_directory():
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
    return options[dir_index], options


def exec():
    dir = select_project_directory()
    if dir is None:
        return
    (selected_dir, _) = dir
    directory = os.path.join(TESTS_PATH, selected_dir)
    print(f"Executing project in directory: {directory}")
    execute(directory)

def seed():
    directory = select_project_directory()
    if directory is None:
        return
    (directory, _) = directory
    path = os.path.join(TESTS_PATH, directory)
    print(f"Seeding database for project in directory: {directory}")
    subprocess.run("python3 seeder.py", shell=True, check=True, cwd=path)


def run(cmd):
    if cmd == "scaffold":
        scaffold()
    elif cmd == "execute":
        exec()
    elif cmd == "seed":
        seed()


if __name__ == "__main__":
    try:
        index = survey.routines.select("Select a command:", options=cmds)
        if index is not None:
            run(cmds[index])
    except survey._widgets.Escape:
        print("Operation cancelled by user.")
