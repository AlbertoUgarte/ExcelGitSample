from robot.api import logger
import os
import git
from robot.api.deco import keyword

class GitOperations(object):

    def __init__(self):
        self._project_name = str(os.environ.get("SCRIPTS"))
        logger.console(f"DEBUG: Project Name - {self._project_name}")
        
        self._project_path = os.getcwd()
        logger.console(f"DEBUG: Initial Project Path - {self._project_path}")

        if self._project_name != "None":
            if self._project_path == "/home/services/suite/tests":
                self._project_path = os.path.join("/home/services/suite/")
            else:
                self._project_path = os.path.join(self._project_path, self._project_name)

        logger.console(f"DEBUG: Adjusted Project Path - {self._project_path}")
        self._data_path = os.path.join(self._project_path, "data/")
        logger.console(f"DEBUG: Data Path - {self._data_path}")

    @keyword
    def commit_and_push(self, file_name, git_branch):
        path_to_file = os.path.join(self._data_path, file_name)
        logger.console(f"DEBUG: Path to File - {path_to_file}")  # Log the full path to the file

        my_repo = git.Repo(self._project_path)
        logger.console(f"DEBUG: Repository Active Branch - {my_repo.active_branch}")  # Log the active branch of the repo

        # Print git status to console for visibility
        logger.console(f"DEBUG: Git Status Before Operations:\n{my_repo.git.status()}\n")

        # Add, commit and push to git
        my_repo.index.add(path_to_file)
        my_repo.index.commit(f"CRT robot committing changes to {file_name}")
        my_repo.git.push("origin", git_branch)

        # Optionally, you can log the git status after the operations
        logger.console(f"DEBUG: Git Status After Operations:\n{my_repo.git.status()}\n")