# ⛏️ Pit - A Simple Version Control System

Have you ever found yourself wondering how Git, the mystical tool every developer swears by, really works under the hood? I sure did. Inspired by a YouTube video titled "I coded Git in 1.5 hours | Make your own Version Control System 😎" by Sanket Singh, I decided to embark on a little coding adventure. Why not create my very own version control system in Python?

Enter ⛏️Pit — a whimsical, yet surprisingly functional version control system (VCS) that I whipped up for the sheer joy of coding and the challenge of seeing if I could do it. The name ‘Pit’ might evoke images of deep, dark holes, but trust me, this project is all about digging into the fascinating world of VCS. Plus, there’s something undeniably fun about saying, “I’m digging a Pit,” when initializing your repo.

## Features

Pit is designed to provide basic version control functionalities through a command-line interface. It allows users to:
- Initialize a new repository
- Add files to a staging area
- Commit changes
- View commit logs
- Check the status of the repository

## Project Structure

Before diving into the implementation details, let’s take a look at the structure of the Pit project:

```
project/
├── .pit/                 # Main repository directory (auto generated)
│   ├── objects/          # Directory for storing object (file) snapshots
│   ├── HEAD              # File storing reference to the current commit
│   ├── index             # File storing the staging area (list of staged files)
├── pit.py                # Main Python script for Pit
├── pit.cmd               # Command handler
├── other files           # Other files in project
```

## Usage

### Initializing a Repository

To begin using Pit, initialize a new repository:

```sh
pit init
```

### Adding Files

Stage changes by adding files to the staging area:

```sh
pit add <filename>
```

### Committing Changes

Commit the staged changes with a message:

```sh
pit commit "message"
```

### Viewing Commit Logs

View the commit history:

```sh
pit log
```

## Example

Here is a simple example of how to use Pit:

```sh
# Initialize a new repository
pit init

# Add files to the staging area
pit add example.txt

# Commit the changes
pit commit "Initial commit"

# View commit logs
pit log
```

## Batch Script

You can use the `pit.cmd` batch script to interact with Pit from the Windows command prompt:

```bat
@echo OFF
python -m pit %*
```

## Conclusion

In this first part of our journey with Pit, we've explored the fundamental setup and initial operations of our Python-based version control system. We started by initializing a new repository using `pit init`, which established the necessary directory structure to manage our project's history. Subsequently, we added files to the staging area with `pit add`, committed changes using `pit commit`, and examined our commit history via `pit log`.

Stay tuned for Part 2, where we will elevate our understanding and implementation of Pit to further empower our development workflows.

## Contributing

Pit is a work in progress. Contributions, forks, and stars are welcome!
