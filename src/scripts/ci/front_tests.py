import collections
from typing import Any, ClassVar

from . import _base as base


class FrontEndTests(base.Workflow):
    name = "github_frontend_test"
    workflow_name: ClassVar[str] = "Frontend tests"
    workflow_id: ClassVar[str] = "frontend-tests"
    description: ClassVar[str] = "Runs frontend tests for github actions."

    def get_jobs(self, *args: Any, **kwargs: Any) -> collections.OrderedDict[str, Any]:
        jobs: collections.OrderedDict[str, Any] = collections.OrderedDict()
        jobs = self.get_css_linter(jobs, *args, **kwargs)
        jobs = self.get_tests_passed(jobs, *args, **kwargs)

        return jobs

    def get_css_linter(
        self,
        jobs: collections.OrderedDict[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> collections.OrderedDict[str, Any]:
        jobs["css-linter"] = {
            "name": "CSS linter",
            "runs-on": "ubuntu-latest",
            "steps": [
                self.get_checkout(),
                *self.get_npm_setup(),
                self.get_css_file_changed(),
                {
                    "name": "Run CSS linter",
                    "id": "run-css-linter",
                    "if": "${{ steps.file-changed.outputs.any_changed == 'true' }}",
                    "run": (
                        "npm run stylelint "
                        "${{ steps.file-changed.outputs.all_changed_files }}"
                    ),
                },
            ],
        }

        return jobs

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
            "name": "Frontend test: OK",
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

    def get_npm_setup(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "Install NPM",
                "id": "install-npm",
                "uses": "actions/setup-node@v4",
                "with": {
                    "node-version": "20",
                },
            },
            {
                "name": "Install NPM dependencies",
                "id": "install-dependencies",
                "run": "npm install",
            },
        ]

    @staticmethod
    def get_css_file_changed() -> dict[str, Any]:
        return {
            "name": "File changed",
            "id": "file-changed",
            "uses": "tj-actions/changed-files@v45",
            "with": {
                "files_yaml": "\n".join(
                    [
                        "python:",
                        "  - '**/*.css'",
                        "  - '**/*.scss'",
                    ]
                ),
            },
        }
