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


def parse_arguments():
    logging.info('Parsing command line arguments')
    parser = argparse.ArgumentParser(description='Deploy application to GHCR with optional version management.')
    parser.add_argument('--pkg', type=str, required=True, help='Package name.')
    parser.add_argument('--force', '-f', action='store_true', help='Use --no-cache option in docker build.')
    parser.add_argument('--release', type=str, help='Specify release version in the format major.minor.patch.')
    parser.add_argument('--token', type=str, help='GHCR token for authentication.')
    parser.add_argument('--ghcr-user', type=str, default='jamesainslie', help='GHCR username.')
    parser.add_argument('--install', action='store_true', help='Install this script to ~/sbin/releases.')
    return parser.parse_args()

def docker_login(user, token):
    logging.info('Logging into GHCR')
    subprocess.run(f'echo {token} | docker login ghcr.io -u {user} --password-stdin', shell=True, check=True)

def build_and_push_image(pkg, version, no_cache):
    logging.info('Building and pushing Docker image')
    cache_option = '--no-cache' if no_cache else ''
    image_name = f'ghcr.io/{args.ghcr_user}/{pkg}:{version}'
    subprocess.run(f'docker build {cache_option} -t {image_name} -t ghcr.io/{args.ghcr_user}/{pkg}:latest .', shell=True, check=True)
    subprocess.run(f'docker push {image_name}', shell=True, check=True)
    subprocess.run(f'docker push ghcr.io/{args.ghcr_user}/{pkg}:latest', shell=True, check=True)

def increment_version(version, increment_type):
    logging.info('Incrementing version')
    major, minor, patch = map(int, version.split('.'))
    if increment_type == 'major':
        return f'{major + 1}.0.0'
    elif increment_type == 'minor':
        return f'{major}.{minor + 1}.0'
    elif increment_type == 'patch':
        return f'{major}.{minor}.{patch + 1}'
    logging.info(f'Incremented version to {version}')
    return version

def interactive_version_update(version):
    logging.info('Performing interactive version update')
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

def create_default_config():
    logging.info('Creating default config')
    config_path = os.path.join(os.getcwd(), '.releases')
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    with open(os.path.join(config_path, 'releases.yaml'), 'w') as config_file:
        yaml.dump({'ghcr_user': 'jamesainslie', 'token': ''}, config_file)

# Logging setup
create_default_config()
logging.basicConfig(filename='.releases/releases.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
def main():
    logging.info('Starting script')
    global args
    args = parse_arguments()
    if args.install:
        logging.info('Installing script')
        return

    user = args.ghcr_user
    token = args.token or getpass('GHCR Token: ')

    docker_login(user, token)

    version = '0.1.0'  # Default version, should ideally load from a config or last release
    if args.release:
        version = args.release
    else:
        version = interactive_version_update(version)

    build_and_push_image(args.pkg, version, args.force)

if __name__ == '__main__':
    main()
