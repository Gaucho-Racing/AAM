poetry install
poetry run pre-commit install
poetry run pre-commit run --all-files
poetry run ruff check aam/
poetry run black --check aam/