
#!/usr/bin/env python3
import argparse
import subprocess
import os
import subprocess
import sys
from getpass import getpass
import logging
import yaml
import shutil

# Logging setup
logging.basicConfig(filename='.releases/releases.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Deploy application to GHCR with optional version management.')
    parser.add_argument('--force', '-f', action='store_true', help='Use --no-cache option in docker build.')
    parser.add_argument('--release', type=str, help='Specify release version in the format major.minor.patch.')
    parser.add_argument('--token', type=str, help='GHCR token for authentication.')
    parser.add_argument('--ghcr-user', type=str, default='jamesainslie', help='GHCR username.')
    parser.add_argument('--install', action='store_true', help='Install this script to ~/sbin/releases.')
    return parser.parse_args()

def docker_login(user, token):
    subprocess.run(f'echo {token} | docker login ghcr.io -u {user} --password-stdin', shell=True, check=True)

def build_and_push_image(version, no_cache):
    cache_option = '--no-cache' if no_cache else ''
    image_name = f'ghcr.io/{args.ghcr_user}/barnowl:{version}'
    subprocess.run(f'docker build {cache_option} -t {image_name} -t ghcr.io/{args.ghcr_user}/barnowl:latest .', shell=True, check=True)
    subprocess.run(f'docker push {image_name}', shell=True, check=True)
    subprocess.run(f'docker push ghcr.io/{args.ghcr_user}/barnowl:latest', shell=True, check=True)

def increment_version(version, increment_type):
    major, minor, patch = map(int, version.split('.'))
    if increment_type == 'major':
        return f'{major + 1}.0.0'
    elif increment_type == 'minor':
        return f'{major}.{minor + 1}.0'
    elif increment_type == 'patch':
        return f'{major}.{minor}.{patch + 1}'
    return version

def interactive_version_update(version):
    update_patch = input('Increment patch version? [Y/n]: ').strip().lower() or 'y'
    if update_patch == 'y':
        version = increment_version(version, 'patch')
    
    update_minor = input('Increment minor version? [y/N]: ').strip().lower()
    if update_minor == 'y':
        version = increment_version(version, 'minor')
    
    update_major = input('Increment major version? [y/N]: ').strip().lower()
    if update_major == 'y':
        version = increment_version(version, 'major')
    
    return version

def install_requirements():
    requirements_path = 'requirements.txt'
    if os.path.exists(requirements_path):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
    else:
        print("No requirements.txt found, skipping Python dependencies installation.")

def install_script():
    install_path = os.path.expanduser('~/sbin')
    script_name = 'releases'  # Name of the script without .py suffix
    target_path = os.path.join(install_path, script_name)
    
    if not os.path.exists(install_path):
        os.makedirs(install_path)
    
    shutil.copy(__file__, target_path)
    os.chmod(target_path, 0o755)  # Set the script as executable
    
    # Install Python requirements
    install_requirements()
    
    print(f'Script installed to {target_path}. Please ensure {install_path} is in your PATH.')

def create_default_config():
    config_path = '.releases'
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    with open(os.path.join(config_path, 'releases.yaml'), 'w') as config_file:
        yaml.dump({'ghcr_user': 'jamesainslie', 'token': ''}, config_file)

def main():
    global args
    args = parse_arguments()
    if args.install:
        install_script()
        create_default_config()
        return

    user = args.ghcr_user
    token = args.token or getpass('GHCR Token: ')

    docker_login(user, token)

    version = '0.2.12'  # Default version, should ideally load from a config or last release
    if args.release:
        version = args.release
    else:
        version = interactive_version_update(version)

    build_and_push_image(version, args.force)

if __name__ == '__main__':
    main()

