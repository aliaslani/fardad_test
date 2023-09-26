import os
import shutil
import difflib

# Define the paths to the current and new repository directories
current_repo_dir = 'current_repo'
new_repo_dir = 'new_repo'
setup_file = 'setup.py'
new_added_file = 'modules/new_added.txt' 
# Define the path to the specific folder for changed files
server_dir = 'server'
def read_requirements(file_path):
    with open(file_path, 'r') as file:
        return {line.strip() for line in file.readlines()}

# Paths to the two requirements.txt files
current_requirements_file = 'current_repo/requirements.txt'
new_requirements_file = 'new_repo/requirements.txt'

# Read the requirements from both files
current_requirements = read_requirements(current_requirements_file)
new_requirements = read_requirements(new_requirements_file)
# Calculate the added modules (present in new_requirements but not in current_requirements)
added_modules = new_requirements - current_requirements

# Calculate the updated modules (present in both but with different versions)
updated_modules = {
    module: (current_versions, new_versions)
    for module, current_versions in (
        module.split('==') if '==' in module else (module, '')
        for module in current_requirements
    )
    for new_module, new_versions in (
        module.split('==') if '==' in module else (module, '')
        for module in new_requirements
    )
    if module == new_module and current_versions != new_versions
}

with open(new_added_file, 'a') as new_added_txt:
    for module in added_modules:
        new_added_txt.write(module + "\n")
    for module, (current_versions, new_versions) in updated_modules.items():
        new_added_txt.write(f"{module}=={new_versions}\n")

# Print a message indicating that the modules have been appended to 'new_added.txt'
print("Newly added and updated modules have been appended to 'new_added.txt'")

# Create the server directory if it doesn't exist
if not os.path.exists(server_dir):
    os.makedirs(server_dir)

# Function to compare two files and return the differences
def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    
    return list(difflib.unified_diff(lines1, lines2))

# Function to copy changed files to the 'server' directory
def copy_changed_files(current_dir, new_dir, server_dir):
    for root, _, files in os.walk(new_dir):
        for file in files:
            for root2,_2, files2 in os.walk(current_dir):
                if file in files2 and file != 'requirements.txt':
                    current_file = os.path.join(root2, file)
                    new_file = os.path.join(root, file)
                    diff = compare_files(current_file, new_file)
                    if diff:
                        print(f'Changes found in {file}')
                        shutil.copy(new_file, server_dir)
                        break
                else:
                    new_file = os.path.join(root, file)
                    print(f'New file found: {file}')
                    shutil.copy(new_file, server_dir)
                    break
            

copy_changed_files(current_repo_dir, new_repo_dir, server_dir)