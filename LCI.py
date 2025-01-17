from program_logic import VersionControlSystem
import json
import argparse
import os
from GUI.gui_interface import VersionControlGUI
from customtkinter import *

def LCIcommand():
    parser = argparse.ArgumentParser(description="Simple Version Control System")
    parser.add_argument("command", nargs="?", choices=["init", "add", "commit", "log", "delete", "clone"], help="Command to execute")
    parser.add_argument("--repo", help="Path to the repository")
    parser.add_argument("--file", help="File to add")
    parser.add_argument("--message", help="Commit message")
    parser.add_argument("--dest", help="Destination path for cloning the repository")

    args = parser.parse_args()

    if not args.command:
        app = CTk()
        gui = VersionControlGUI(app)
        gui.run()

    else:
        vcs = VersionControlSystem(args.repo)

        if args.command == "init":
            if not os.path.exists(args.repo):
                os.makedirs(args.repo)
            vcs = VersionControlSystem(args.repo)
            print(f"Initialized empty VCS repository in {args.repo}")

        elif args.command == "add":
            if not args.file:
                print("Error: --file argument is required for 'add' command")
            else:
                try:
                    file_hash = vcs.add_file(args.file)
                    print(f"File {args.file} added with hash: {file_hash}")
                except FileNotFoundError as e:
                    print(e)

        elif args.command == "commit":
            if not args.message:
                print("Error: --message argument is required for 'commit' command")
            else:
                with open(vcs.commits_file, "r") as f:
                    previous_commits = json.load(f)

                files = []
                if previous_commits:
                    files = [file for commit in previous_commits for file in commit["files"]]

                commit_data = vcs.commit(args.message, files)
                print(f"Commit created: {commit_data}")

        elif args.command == "log":
            commits = vcs.get_commits()
            if not commits:
                print("No commits found.")
            else:
                print("Commit log:")
                for commit in commits:
                    print(f"Timestamp: {commit['timestamp']}")
                    print(f"Message: {commit['message']}")
                    print(f"Files: {commit['files']}")
                    print("---")

        elif args.command == "delete":
            if vcs.delete_repo():
                print(f"Repository {args.repo} deleted successfully.")
            else:
                print(f"Error: Failed to delete repository {args.repo}.")

        elif args.command == "clone":
            if not args.dest:
                print("Error: --dest argument is required for 'clone' command")
            else:
                try:
                    vcs.clone_repository(args.dest)
                    print(f"Repository cloned to {args.dest}")
                except Exception as e:
                    print(f"Error: {e}")
