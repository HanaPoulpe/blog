from typing import Any

from cli import base


class DockerEntrypointTests(base.ExecCommand):
    name = "docker_entrypoint_tests"
    command_name = "./entrypoint.sh"
    description = "Runs docker entrypoint tests."
    cwd = base.PROJECT_ROOT.parent.joinpath("deployment")

    def get_args(self, *args: Any, **kwargs: Any) -> list[str]:
        return ["tests"]

    def get_env(self, *args: Any, **kwargs: Any) -> dict[str, str]:
        return {
            "ENTRYPOINT": str(self.cwd.joinpath("entrypoint.sh").absolute()),
            "DEBUG": "1",
            "DJANGO_CONFIGURATION": "BlogSite",
        }
