import subprocess
import os
def install_modules(module_list_file):
    '''
    Install modules from new_added.txt
    '''
    try:
        for root, dirs, files in os.walk("."):
            for file in sorted(files, key=lambda x: os.stat(x).st_mtime):
                if file.endswith(".whl"):
                    print(os.path.join(root, file))
                    install_command = ['pip', 'install'] + [file]
                    subprocess.check_call(install_command)
                    print(f"Successfully installed {file}")

    except Exception as e:
        print(f"Error installing modules: {str(e)}")

if __name__ == "__main__":
    module_list_file = 'modules/new_added.txt'  # Change this to the actual path of your new_added.txt file
    install_modules(module_list_file)

