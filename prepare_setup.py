import subprocess

def download_modules(module_list_file):
    '''
    Download modules from new_added.txt
    '''
    try:
        with open(module_list_file, 'r') as file:
            module_list = [line.strip() for line in file.readlines()]

        if module_list:
            download_command = ['pip', 'download', '-r']+ [module_list_file]+['--only-binary', ':all:', '--dest'] + ['./modules/.'] + ['--no-cache'] 
            subprocess.check_call(download_command)
            print("Successfully downloaded modules from new_added.txt.")
        else:
            print("No modules to download from new_added.txt.")

    except Exception as e:
        print(f"Error download modules: {str(e)}")

if __name__ == "__main__":
    module_list_file = 'modules/new_added.txt'  # Change this to the actual path of your new_added.txt file
    download_modules(module_list_file)

