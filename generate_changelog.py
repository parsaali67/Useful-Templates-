#!/usr/bin/env python3
import subprocess
import os


def get_last_tag():
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"]
        ).strip().decode('utf-8')
        return tag
    except subprocess.CalledProcessError:
        return None


def get_commit_messages(since_tag):
    if since_tag:
        cmd = ["git", "log", f"{since_tag}..HEAD", "--pretty=format:%s"]
    else:
        cmd = ["git", "log", "--pretty=format:%s"]
    commits = subprocess.check_output(cmd).decode('utf-8').splitlines()
    return commits


def generate_changelog():
    last_tag = get_last_tag()
    commits = get_commit_messages(last_tag)
    if not commits:
        print("No new commits to add to changelog.")
        return

    # Create a simple header and format the commit messages as bullet points
    header = "## Changelog\n\n"
    changelog_entries = "\n".join(f"- {commit}" for commit in commits)
    changelog_content = header + changelog_entries + "\n\n"

    changelog_file = "CHANGELOG.md"
    if os.path.exists(changelog_file):
        with open(changelog_file, "a") as f:
            f.write(changelog_content)
    else:
        with open(changelog_file, "w") as f:
            f.write("# Changelog\n\n" + changelog_entries + "\n")
    print("CHANGELOG.md updated.")


if __name__ == "__main__":
    generate_changelog()
