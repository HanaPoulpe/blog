import collections
from typing import Any

from . import _base as base


class DockerBuildImageAction(base.Action):
    action_name = "Build Docker Image"
    action_id = "build-docker-image"
    description = "Builds Docker image for the application."

    def get_steps(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        return [
            {
                "name": "Setup QEMU",
                "uses": "docker/setup-qemu-action@v3",
            },
            {
                "name": "Setup Buildx",
                "uses": "docker/setup-buildx-action@v3",
            },
            {
                "name": "Build docker image",
                "shell": "bash",
                "run": "docker build . -t blog --build-arg debug=1",
            },
        ]


class GithubDockerTest(base.Workflow):
    name = "github_docker_test"
    workflow_name = "Docker Tests"
    workflow_id = "docker-tests"
    description = "Creates Docker tests for github actions."

    def get_jobs(self, *args: Any, **kwargs: Any) -> collections.OrderedDict[str, Any]:
        jobs: collections.OrderedDict[str, Any] = collections.OrderedDict()
        jobs = self.get_tests(jobs, *args, **kwargs)
        jobs = self.get_tests_passed(jobs, *args, **kwargs)

        return jobs

    def get_tests(
        self,
        jobs: collections.OrderedDict[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> collections.OrderedDict[str, Any]:
        jobs["test-entrypoint"] = {
            "name": "Docker Tests: Entrypoint",
            "runs-on": "ubuntu-latest",
            "steps": [
                self.get_checkout(),
                self.get_build(),
                {
                    "name": "Run docker entrypoint tests",
                    "id": "run-entrypoint-tests",
                    "run": "docker run --env-file src/.env.example blog tests",
                },
            ],
        }
        return jobs

    def create(self, *args: Any, **kwargs: Any) -> None:
        super().create(*args, **kwargs)

        build_action = DockerBuildImageAction.as_command()
        build_action(["create"])

    @staticmethod
    def get_build() -> dict[str, Any]:
        return {
            "name": "Build",
            "uses": "./.github/actions/build-docker-image",
        }

    def get_tests_passed(
        self,
        jobs: collections.OrderedDict[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> collections.OrderedDict[str, Any]:
        all_required: list[str] = []

        for name in jobs:
            test_required = self.prompt_bool(
                f"Is {name} required for the CI?",
                default=True,
            )

            if test_required:
                all_required.append(name)

        jobs["tests-passed"] = {
            "name": "Docker test: OK",
            "runs-on": "ubuntu-latest",
            "container": "python:3.12-slim-bookworm",
            "if": "${{ always() }}",
            "needs": all_required,
            "env": {
                "RESULTS": "\n".join(
                    [f"${{{{ needs.{need}.result }}}}" for need in all_required]
                ),
            },
            "steps": [
                {
                    "id": "test-results",
                    "name": "Test results",
                    "run": "\n".join(
                        [
                            "echo $RESULTS",
                            "for r in $RESULTS",
                            "do",
                            '    if [ $r = "success" ] || [ $r = "skipped" ];',
                            "    then",
                            "        true",
                            "    else",
                            '        echo "Some tests failed"',
                            "        exit 1",
                            "    fi",
                            "done",
                            'echo "All tests passed"',
                        ],
                    ),
                },
            ],
        }

        return jobs
