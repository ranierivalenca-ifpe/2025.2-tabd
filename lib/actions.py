import os

from lib._constants import PROJECTS_PATH, SCAFFOLD_PATH
from lib import Logger, Input, SubCalls


net_name = lambda dir: "pg-{}".format(dir)
server_name = lambda dir: "pg-{}-server".format(dir)


class Actions:
    @staticmethod
    def scaffold():
        directory = Input.basic_input("Enter project directory name:")
        Logger.info(f"Scaffolding project in directory: {directory}")
        try:
            path = os.path.join(PROJECTS_PATH, directory)
            os.makedirs(path, exist_ok=False)
            SubCalls.run("cp -R {}/* {}".format(SCAFFOLD_PATH, path), check=True)
            Logger.done(f"Directory '{directory}' created successfully.")
        except FileExistsError:
            Logger.fail(f"Directory '{directory}' already exists.")
            Actions.scaffold()  # Retry if directory exists

    @staticmethod
    def select_project_directory():
        if not os.path.exists(PROJECTS_PATH):
            os.makedirs(PROJECTS_PATH)
        directories = os.listdir(PROJECTS_PATH)
        options = ()
        for d in sorted(
            directories,
            key=lambda x: os.path.getctime(os.path.join(PROJECTS_PATH, x)),
            reverse=True,
        ):
            full_path = os.path.join(PROJECTS_PATH, d)
            if os.path.isdir(full_path):
                options += (d,)
        if not options:
            Logger.fail(
                "No project directories found on {} directory. Please scaffold a new project first.".format(
                    PROJECTS_PATH
                )
            )
            return
        dir_index = Input.select(
            "Select a project directory to execute:", options=options
        )
        if dir_index is None:
            return
        return options[dir_index]
