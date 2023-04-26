# Dev setup

1. Create the virtual environment by performing `poetry shell`.
2. Press `cmd+shift+p` -> `Python: Select Interpreter` -> the path from `which python` (created by poetry)

StageDirectorOperator:

1. Make it a branch operator
2. Have it use XComs to return something to be used in environment variables in the actual task
3.

TODO:
Figure out how to automatically bump pippi version, so you dont have to go in docker file and install and set the next version in pyproject.toml

Use TWINE_USERNAME=`__token__` TWINE_PASSWORD=<your token> make publish
