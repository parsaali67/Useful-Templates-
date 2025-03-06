#!/usr/bin/env python3
import argparse

def read_version(file_path="VERSION.txt"):
    try:
        with open(file_path, "r") as f:
            version = f.read().strip()
            return version
    except FileNotFoundError:
        return "0.0.0"

def write_version(version, file_path="VERSION.txt"):
    with open(file_path, "w") as f:
        f.write(version + "\n")

def bump_version(version, bump_type):
    major, minor, patch = map(int, version.split("."))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError("Invalid bump type. Use 'major', 'minor', or 'patch'.")
    return f"{major}.{minor}.{patch}"

def main():
    parser = argparse.ArgumentParser(description="Automatically bump the version number.")
    parser.add_argument("bump", choices=["major", "minor", "patch"], help="Which part of the version to bump")
    args = parser.parse_args()
    
    current_version = read_version()
    new_version = bump_version(current_version, args.bump)
    write_version(new_version)
    print(f"Bumped version: {current_version} -> {new_version}")

if __name__ == "__main__":
    main()
