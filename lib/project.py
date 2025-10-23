from lib.actions import net_name, server_name
from lib._constants import PROJECTS_PATH, EXPOSED_PORT, DB_USER, DB_PASS
from lib._sub_calls import SubCalls
from lib.input import Input
from lib.logger import Logger


import os
import time
import threading


class Project:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        pass

    def is_server_up(self):
        return (
            SubCalls.docker_run(
                "postgres /bin/bash -c 'pg_isready -h {} -U {}'".format(
                    server_name(self.project_dir), DB_USER
                ),
                flags=(
                    "--rm",
                    "--network {}".format(net_name(self.project_dir)),
                ),
                env={"PGPASSWORD": DB_PASS},
                capture_code=True,
            )
            == 0
        )

    def server_thread(self, output):
        directory = os.path.join(PROJECTS_PATH, self.project_dir)
        output.append(
            SubCalls.docker_run(
                "postgres",
                flags=(
                    "--rm",
                    "--name {}".format(server_name(self.project_dir)),
                    "--network {}".format(net_name(self.project_dir)),
                    "-p {}:5432".format(EXPOSED_PORT),
                    "-v {}/sql:/docker-entrypoint-initdb.d/:ro".format(directory),
                ),
                env={
                    "PGDATA": "/var/lib/postgresql/data/pgdata",
                    "POSTGRES_USER": DB_USER,
                    "POSTGRES_PASSWORD": DB_PASS,
                },
                capture_output=True,
                capture_code=False,
                # check=True,
            )
        )

    def start_server(self):

        # Create project network
        if (
            SubCalls.docker(
                "network create {}".format(net_name(self.project_dir)),
                capture_code=True,
            )
            == 0
        ):
            Logger.done("Network {} created.".format(net_name(self.project_dir)))

        output = []
        thread = threading.Thread(target=self.server_thread, args=(output,))
        thread.start()

        Logger.info("Waiting for PostgreSQL server to be ready...")
        while not self.is_server_up() and thread.is_alive():
            time.sleep(1)
        if not thread.is_alive():
            Logger.fail("Failed to start PostgreSQL server.")
            Logger.text("".join(output))
            return
        Logger.done("PostgreSQL server is running.")

    def stop_server(self):
        if (
            SubCalls.docker(
                "stop {}".format(server_name(self.project_dir)), capture_code=True
            )
            == 0
        ):
            Logger.done("PostgreSQL server stopped.")
        if (
            SubCalls.docker(
                "network rm {}".format(net_name(self.project_dir)), capture_code=True
            )
            == 0
        ):
            Logger.done("Network {} removed.".format(net_name(self.project_dir)))

    def shell_into_server(self):
        if not self.is_server_up():
            Logger.fail("PostgreSQL server is not running.")
            return
        SubCalls.docker(
            "exec -it {} /bin/bash".format(server_name(self.project_dir)),
            capture_code=False,
            capture_output=False,
            check=True,
        )

    def connect_db(self):
        SubCalls.docker_run(
            "postgres psql -h {} -U {}".format(server_name(self.project_dir), DB_USER),
            flags=(
                "--rm",
                "--network {}".format(net_name(self.project_dir)),
                "-it",
            ),
            env={"PGPASSWORD": DB_PASS},
            capture_code=False,
            capture_output=False,
            check=True,
        )

    def seed_db(self):
        SubCalls.run(
            "python3 {}/seeder.py".format(
                os.path.join(PROJECTS_PATH, self.project_dir)
            ),
            # check=True,
        )
