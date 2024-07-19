from robot.api import logger
import os
import git
from robot.api.deco import keyword

class GitOperations(object):

    def __init__(self):
        # Retrieve the project name from environment variables or use a default
        self._project_name = str(os.environ.get("SCRIPTS", "default_project_name"))
        logger.console(f"DEBUG: Project Name - {self._project_name}")
        
        # Get the current working directory
        self._project_path = os.getcwd()
        logger.console(f"DEBUG: Initial Project Path - {self._project_path}")

        # Adjust the project path based on the environment
        self._adjust_project_path()

        # Define the data path relative to the project path
        self._data_path = os.path.join(self._project_path, "data/")
        logger.console(f"DEBUG: Data Path - {self._data_data_path}")

    def _adjust_project_path(self):
        # Check if the project path needs adjustment based on known structure
        expected_path = "/home/services/suite/tests"
        logger.console(f"DEBUG: Checking if project path ends with 'tests'")
        if self._project_path.endswith("tests"):
            # Adjust path to go up one level if in live testing
            self._project_path = os.path.join(self._project_path, "..", self._project_name)
            logger.console(f"DEBUG: Modified Project Path in Test Environment - {self._project_path}")
        else:
            self._project_path = os.path.join(self._project_path, self._project_name)
            logger.console(f"DEBUG: Modified Project Path in Non-Test Environment - {self._project_path}")
        
        # Normalize the path to remove any redundant separators or up-level references
        self._project_path = os.path.normpath(self._project_path)
        logger.console(f"DEBUG: Normalized Project Path - {self._project_path}")

    @keyword
    def commit_and_push(self, file_name, git_branch):
        path_to_file = os.path.join(self._data_path, file_name)
        logger.console(f"DEBUG: Path to File - {path_to_file}")

        try:
            my_repo = git.Repo(self._project_path)
            logger.console(f"DEBUG: Repository Active Branch - {my_repo.active_branch}")
            logger.console(f"DEBUG: Git Status Before Operations:\n{my_repo.git.status()}\n")

            my_repo.index.add(path_to_file)
            my_repo.index.commit(f"CRT robot committing changes to {file_name}")
            my_repo.git.push("origin", git_branch)

            logger.console(f"DEBUG: Git Status After Operations:\n{my_repo.git.status()}\n")
        except Exception as e:
            logger.console(f"ERROR: {str(e)}")
            raise
