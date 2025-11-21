#! /usr/bin/env python3

import argparse, os, subprocess
from pathlib import Path
from zipfile import ZipFile

# Create the parser for an easier time dealing with the input arguments
parser = argparse.ArgumentParser(
    description='automatically setup a sln project with proper nvim setup')

# Adding the arguments the parser should look for
group = parser.add_mutually_exclusive_group(required=True)
_ = group.add_argument('-z','--zip_path', type=str, help='The location of the zip with the given files for the project')
_ = group.add_argument('-n','--project_name', type=str, help='The location of the zip with the given files for the project')
_ = parser.add_argument('class_name', type=str, help='The class name for the project folder')

args = parser.parse_args()

# Collecting the arguments
using_zip = (args.zip_path is not None)

zip_path = os.path.abspath(str(args.zip_path))
project_name = str(args.project_name)

class_name = str(args.class_name).upper()

directory_path = Path.home().joinpath("./OneDrive/Documents/Digipen").joinpath("./" + class_name)

# Processing the strings to create the folder
file_name = str()
if(using_zip):
    file_name = str(os.path.basename(zip_path)).removesuffix(".zip").removesuffix("-files")
else:
    file_name = project_name

# Checking that we are getting a zip file that exists
if(using_zip and (not zip_path.endswith(".zip") or not os.path.isfile(zip_path))):
    print("zip path does not evaluate to existing zip file")
    exit()

folder_path = str(directory_path) + "\\" + file_name

# Cloning the github template
repo_name = class_name + "-" + file_name

repo_creation_output = subprocess.run(["gh","repo", "create", repo_name, "--private", "-p", "CrispyTonkatsu/sln-template"])

if(repo_creation_output.returncode != 0):
    exit()

repo_cloning_output = subprocess.run(["gh", "repo", "clone", repo_name, folder_path])

if(repo_cloning_output.returncode != 0):
    exit()

repo_pull_output = subprocess.run(["git", "-C", folder_path, "pull"])

# Actually placing the files there
if(using_zip):
    ZipFile(zip_path).extractall(folder_path)
