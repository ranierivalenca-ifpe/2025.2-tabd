import subprocess


class SubCalls:
    @staticmethod
    def run(command, capture_output=False, capture_code=False, **kwargs):
        """
        Run a command in the terminal and return what is requested
        or a boolean indicating if the command was successful
        """
        if capture_output or capture_code:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, **kwargs
            )
        else:
            result = subprocess.run(command, shell=True, **kwargs)

        if capture_code and capture_output:
            return (result.stdout, result.returncode)
        if capture_output:
            return result.stdout
        if capture_code:
            return result.returncode

        return result.returncode == 0

    @staticmethod
    def docker(cmd, capture_output=False, capture_code=False, **kwargs):
        """
        Run a docker command in the terminal and return what is requested
        or a boolean indicating if the command was successful
        """
        return SubCalls.run(
            "docker {}".format(cmd),
            capture_output=capture_output,
            capture_code=capture_code,
            **kwargs,
        )

    @staticmethod
    def docker_run(
        cmd, flags=(), env={}, capture_code=True, capture_output=False, **kwargs
    ):
        if flags:
            cmd = "{} {}".format(" ".join(flags), cmd)
        if env:
            env_str = " ".join(f"-e {k}={v}" for k, v in env.items())
            cmd = "{} {}".format(env_str, cmd)
        return SubCalls.docker(
            "run {}".format(cmd),
            capture_code=capture_code,
            capture_output=capture_output,
            **kwargs,
        )
