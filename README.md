hanabi_json
==========
## Usage

## Development
* install git, python3.12, poetry, poethepoet.
* git clone this repo
* create a venv using `poetry env use python3.12; poetry install`
* enable pre-commit checks with `poetry run pre-commit install`
* use `poe check` to verify code quality

## Build
* install poetry-dynamic-versioning[plugin]
* use `poe version` to see the current version
* use `poe tag new_version_number` to add a git tag
* use `poetry build` to build
