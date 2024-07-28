#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import hashlib
from datetime import datetime
import json
from pprint import pp

class Pit:
    def __init__(self, repo_path=".") -> None:
        self.repo_path = Path(repo_path, ".pit")
        self.objects_path = self.repo_path / "objects"
        self.head_path = self.repo_path / "HEAD"
        self.index_path = self.repo_path / "index"
        
    def start(self):
        if self.repo_path.exists():
            print("⛏️  Pit already exists!")
            sys.exit(1)
        self.repo_path.mkdir(exist_ok=True)
        self.objects_path.mkdir(exist_ok=True)
        self.head_path.touch(exist_ok=True)
        if not self.index_path.exists():    
            with self.index_path.open("w") as index_file:
                index_file.write("[]")
        print("⛏️  Digging pit...")

    def add(self, file_path):
        print(f"⛏️  Adding {file_path} to staging area")
        file_data = self.read_file(file_path)
        file_hash = self.hash_object(file_data)
        if not file_data:
            print(f"⛏️  Error: {file_path} not found!")
            sys.exit(1)
        if self.check_hash_exists(file_hash):
            print(f"⛏️  Error: {file_path} already exists!")
            sys.exit(1)
        # print(f'⛏️  Log: file:{file_path}')
        # print(f'⛏️  Log: hash:{file_hash}')
        object_path = self.objects_path / file_hash
        self.write_file(object_path, file_data)
        self.update_staging_area(file_path, file_hash)
        # print(f'⛏️  Log: object_path:{object_path}')
        print(f"⛏️  Added {file_path} to staging area")

    def check_hash_exists(self, file_hash):
        return (self.objects_path / file_hash).exists()

    def commit(self, message):
        index = self.as_list(self.read_file(self.index_path))
        parent_commit = self.get_current_head()
        commit_data = json.dumps({
            "parent": parent_commit,
            "message": message,
            "date": datetime.now().isoformat(),
            "files": index
        })
        commit_hash = self.hash_object(str(commit_data))
        commit_path = self.objects_path / commit_hash
        self.write_file(commit_path, str(commit_data))
        self.write_file(self.head_path, commit_hash)
        self.write_file(self.index_path, "[]")
        print(f"⛏️  Committed as {commit_hash}")

    def log(self):
        current_commit_hash = self.get_current_head()
        if not current_commit_hash:
            print("⛏️  No commits yet!")
            return
        while current_commit_hash:
            commit_data = self.read_file(self.objects_path / current_commit_hash)
            commit_data = json.loads(commit_data)
            print(f"⛏️  Commit: {current_commit_hash}")
            pp(commit_data)
            current_commit_hash = commit_data.get('parent')

    def diff(self):
        pass

    def status(self):
        # if head is empty, no commits yet
        current_commit_hash = self.get_current_head()
        if not current_commit_hash:
            print("⛏️  No commits yet!")
            return
        # get the current commit data
        commit_data = self.read_file(self.objects_path / current_commit_hash)
        commit_data = json.loads(commit_data)
        # get the files in the current commit
        commit_files = commit_data.get("files")
        # get the files in the staging area
        index_files = self.as_list(self.read_file(self.index_path))
        # get the files in the working directory
        working_files = [str(file) for file in Path(".").rglob("*") if file.is_file()]
        # print the status
        print("⛏️  Working tree status:")
        for file in working_files:
            file_hash = self.hash_object(self.read_file(file))
            if file_hash in commit_files:
                print(f"    {file} - modified")
            elif file_hash in index_files:
                print(f"    {file} - staged")
            else:
                print(f"    {file} - untracked")
        print("⛏️  Staging area status:")
        for file in index_files:
            print(f"    {file['path']} - staged")

    ## Helper functions
    def hash_object(self, content):
        return hashlib.sha1(content.encode()).hexdigest()

    def update_staging_area(self, file_path, file_hash):
        index = self.as_list(self.read_file(self.index_path))
        index.append({
            "path":file_path, 
            "hash":file_hash
        })
        self.write_file(self.index_path, str(index))

    def as_list(self, str):
        if str == "[]":
            return []
        return str.replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(",")

    def get_current_head(self):
        return self.read_file(self.head_path) or None
    


    def write_file(self, file_path, content):
        try:
            with Path(file_path).open("w", encoding="utf-8") as file:
                file.write(content)
        except FileNotFoundError:
            print(f"Error: {file_path} not found!")
    
    def read_file(self, file_path):
        try:
            with Path(file_path).open("r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def show_commit_diff(self, commit_hash):
        pass

    def get_parent_file_content(self, commit_hash, file_path):
        pass

    def get_commit_data(self, commit_hash):
        pass

    def get_file_content(self, file_path):
        pass

def show_usage():
    print("⛏️  Pit - A simple version control system")
    print("Usage: pit <command> [<args>]")
    print("Commands:")
    print("  init        Create an empty pit repository")
    print("  add         Add file to staging area")
    print("  commit      Record changes to the repository")
    print("  log         Show commit logs")
    print("  status      Show the working tree status")

def main():
    ignore_files = ["pit.cmd", "pit.py", "pit.exe"]
    ignore_dirs = [".git", ".pit", "venv", "__pycache__"]
    pit = Pit()
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    command = sys.argv[1]
    if command == "init":
        pit.start()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: pit add <file_path>")
            sys.exit(1)
        file_path = sys.argv[2]
        if Path(file_path).is_dir():
            print(f"⛏️  Error: {file_path} is a directory!")
            sys.exit(1)
        if file_path in ignore_files:
            print(f"⛏️  Error: {file_path} is in the ignore list!")
            sys.exit(1)
        if not Path(".pit").exists():
            print("⛏️  Error: Not a pit repository!")
            sys.exit(1)
        if file_path == "*":
            data = Path(".").rglob("*")
            data = [file for file in data if file.is_file()]
            data = [file for file in data if not any(ignore_dir in file for ignore_dir in ignore_dirs)]
            data = [str(file) for file in data if file not in ignore_files]
            for file in data:
                print(file)


        else:            
            pit.add(file_path)
    elif command == "commit":
        if len(sys.argv) < 3:
            print("Usage: pit commit <message>")
            sys.exit(1)
        message = sys.argv[2]
        pit.commit(message)
    elif command == "log":
        pit.log()
    elif command == "status":
        pit.status()

if __name__ == "__main__":
    main()