import subprocess
import sys
import os
import tkinter as tk
from tkinter import messagebox

def is_python_installed():
    try:
        subprocess.run(['python', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "python"
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(['python3', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return "python3"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

def is_java_installed():
    try:
        subprocess.run(['java', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_pip_command():
    try:
        subprocess.run(['pip', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "pip"
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(['pip3', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return "pip3"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

def create_venv(python_cmd):
    try:
        result = subprocess.run([python_cmd, '-m', 'venv', 'venv'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        show_error_message(f"Failed to create virtual environment.\n\n{e.stderr.decode()}", error_codes["VenvCreateFailed"])
        return False

def show_error_message(message, error_code):
    error_message = f"{message}\n\nError Code: {error_code}"
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror(f"Error {error_code}", error_message)
    root.destroy()

def activate_venv(python_cmd, pip_cmd):
    activate_script = os.path.join(script_dir, 'venv', 'bin', 'activate')
    command = f'/bin/bash -c "source \\"{activate_script}\\" && {pip_cmd} install -r \\"{os.path.join(script_dir, "requirements.txt")}\\" && {python_cmd} \\"{os.path.join(script_dir, "picodulce.py")}\\""'

    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(script_dir)
    
    error_codes = {
        "PythonMissing": 101,
        "JavaMissing": 108,
        "PipMissing": 109,
        "RequirementsMissing": 102,
        "ScriptMissing": 103,
        "VenvCreateFailed": 104,
        "VenvActivateFailed": 105,
        "DependenciesInstallFailed": 106,
        "ScriptExecutionFailed": 107
    }

    python_cmd = is_python_installed()
    if not python_cmd:
        show_error_message("Please install Python.", error_codes["PythonMissing"])
    elif not is_java_installed():
        show_error_message("Please install Java.", error_codes["JavaMissing"])
    else:
        pip_cmd = get_pip_command()
        if not pip_cmd:
            show_error_message("Please install pip.", error_codes["PipMissing"])
        elif not os.path.exists(os.path.join(script_dir, 'requirements.txt')):
            show_error_message("requirements.txt not found.", error_codes["RequirementsMissing"])
        elif not os.path.exists(os.path.join(script_dir, 'picodulce.py')):
            show_error_message("picodulce.py not found.", error_codes["ScriptMissing"])
        else:
            if os.path.exists(os.path.join(script_dir, 'venv')):
                print("Virtual environment 'venv' already exists.")
                if not activate_venv(python_cmd, pip_cmd):
                    show_error_message("Failed to activate the existing virtual environment, install dependencies, or run picodulce.py.", error_codes["VenvActivateFailed"])
                else:
                    print("Existing virtual environment activated, dependencies installed, and picodulce.py executed successfully.")
            else:
                if not create_venv(python_cmd):
                    print("Virtual environment creation failed. Error message shown.")
                else:
                    print("Virtual environment created successfully.")
                    if not activate_venv(python_cmd, pip_cmd):
                        show_error_message("Failed to activate the virtual environment, install dependencies, or run picodulce.py.", error_codes["VenvActivateFailed"])
                    else:
                        print("Virtual environment activated, dependencies installed, and picodulce.py executed successfully.")
