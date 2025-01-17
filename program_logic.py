import os
import json
from datetime import datetime
import shutil
import Pybind11Module

class VersionControlSystem:
    def __init__(self, repo_name):
        base_repo_path = "C:\\Repository"
        os.makedirs(base_repo_path, exist_ok=True)

        self.repo_name = repo_name
        self.repo_path = os.path.join(base_repo_path, repo_name)
        self.repo_meta = os.path.join(self.repo_path, ".vcs")
        self.files_dir = os.path.join(self.repo_meta, "files")
        self.history_dir = os.path.join(self.repo_meta, ".history")
        self.commits_file = os.path.join(self.repo_meta, "commits.json")
        self.changes_file = os.path.join(self.repo_meta, "changes.txt")
        self.tracked_files_file = os.path.join(self.repo_meta, "tracked_files.txt")

        if not os.path.exists(self.repo_meta):
            os.makedirs(self.files_dir)
            os.makedirs(self.history_dir)

            with open(self.commits_file, "w") as f:
                json.dump([], f)

            with open(self.changes_file, "w") as f:
                f.write("")

            with open(self.tracked_files_file, "w") as f:
                f.write("")

    def get_repository_name(self):
        return self.repo_name

    def add_file(self, file_path, dest_path=None):
        with open(self.tracked_files_file, "w") as f:
            f.write(file_path + "\n")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")

        if os.path.isdir(file_path):
            dest_dir = dest_path or os.path.join(self.files_dir, os.path.basename(file_path))
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(file_path, dest_dir)
            return os.path.basename(file_path)
        else:
            dest_path = dest_path or os.path.join(self.files_dir, os.path.basename(file_path))
            with open(file_path, "rb") as src, open(dest_path, "wb") as dest:
                dest.write(src.read())
            return os.path.basename(file_path)

    def delete_repo(self):
        if Pybind11Module.delete_folder(self.repo_path):
            return True

    def clone_repository(self, dest_path):
        Pybind11Module.move_folder(self.files_dir, dest_path)

    def commit(self, message, files):
        timestamp = datetime.now().isoformat()

        with open(self.commits_file, "r") as f:
            commits = json.load(f)
        version = f"v{len(commits) + 1}"
        version_dir = os.path.join(self.history_dir, version)
        os.makedirs(version_dir, exist_ok=True)
        for root, _, filenames in os.walk(self.files_dir):
            for file_name in filenames:
                relative_path = os.path.relpath(os.path.join(root, file_name), self.files_dir)
                src_file = os.path.join(self.files_dir, relative_path)
                dest_file = os.path.join(version_dir, relative_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.move(src_file, dest_file)

        with open(self.tracked_files_file, "r") as f:
            tracked_files = f.read().strip().split("\n")

        for file_path in tracked_files:
            self.add_file(file_path)
        self.compare_with_history()
        commit_data = {
            "timestamp": timestamp,
            "message": message,
            "files": files,
            "version": version
        }

        commits.append(commit_data)
        with open(self.commits_file, "w") as f:
            json.dump(commits, f, indent=4)
        return commit_data

    def compare_with_history(self):
        if not os.path.exists(self.history_dir):
            print("Error: .history folder does not exist.")
            return

        current_files_folder = self.files_dir
        output_report_path = self.changes_file

        versions = sorted(os.listdir(self.history_dir), reverse=True)
        if not versions:
            print("Error: No versions in .history.")
            return

        latest_version_folder = os.path.join(self.history_dir, versions[0])

        Pybind11Module.compare_folders(latest_version_folder, current_files_folder, output_report_path)


    def get_commits(self):
        with open(self.commits_file, "r") as f:
            return json.load(f)

