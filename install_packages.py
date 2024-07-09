import subprocess
import sys

def install_packages(requirements_file='requirements.txt'):
    try:
        with open(requirements_file, 'r') as file:
            packages = file.readlines()
            packages = [pkg.strip() for pkg in packages if pkg.strip() and not pkg.startswith('#')]

            for package in packages:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

        print("All packages installed successfully.")

    except FileNotFoundError:
        print(f"The file {requirements_file} does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing the package: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    install_packages()
