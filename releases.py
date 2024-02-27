#!/usr/bin/env python3
import argparse
import subprocess
import os
from getpass import getpass
import logging
import yaml

def parse_arguments():
    parser = argparse.ArgumentParser(description='Deploy application to GHCR with optional version management.')
    parser.add_argument('--pkg', type=str, required=True, help='Package name.')
    parser.add_argument('--force', '-f', action='store_true', help='Use --no-cache option in docker build.')
    parser.add_argument('--release', type=str, help='Specify release version in the format major.minor.patch.')
    parser.add_argument('--token', type=str, help='GHCR token for authentication.')
    parser.add_argument('--ghcr-user', type=str, default='jamesainslie', help='GHCR username.')
    parser.add_argument('--install', action='store_true', help='Install this script to ~/sbin/releases.')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug logging.')
    return parser.parse_args()

def setup_logging(debug_mode):
    level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(filename='.releases/releases.log', 
                        level=level, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def docker_login(user, token, args):
    logging.debug('Attempting to login to GHCR.')
    subprocess.run(f'echo {token} | docker login ghcr.io -u {user} --password-stdin', shell=True, check=True)
    logging.debug('Logged into GHCR.')

def build_and_push_image(pkg, version, no_cache, args):
    logging.debug('Starting build and push of Docker image.')
    cache_option = '--no-cache' if no_cache else ''
    image_name = f'ghcr.io/{args.ghcr_user}/{pkg}:{version}'
    subprocess.run(f'docker build {cache_option} -t {image_name} .', shell=True, check=True)
    subprocess.run(f'docker push {image_name}', shell=True, check=True)
    logging.info(f'Successfully built and pushed {image_name}.')

def increment_version(version, increment_type, args):
    logging.debug('Incrementing version.')
    major, minor, patch = map(int, version.split('.'))
    if increment_type == 'major':
        version = f'{major + 1}.0.0'
    elif increment_type == 'minor':
        version = f'{major}.{minor + 1}.0'
    elif increment_type == 'patch':
        version = f'{major}.{minor}.{patch + 1}'
    logging.debug(f'Incremented version to {version}')
    return version

def interactive_version_update(version, args):
    logging.debug('Interactive version update.')
    update_patch = input('Increment patch version? [Y/n]: ').strip().lower() or 'y'
    if update_patch == 'y':
        version = increment_version(version, 'patch', args)
    
    update_minor = input('Increment minor version? [y/N]: ').strip().lower()
    if update_minor == 'y':
        version = increment_version(version, 'minor', args)
    
    update_major = input('Increment major version? [y/N]: ').strip().lower()
    if update_major == 'y':
        version = increment_version(version, 'major', args)
    
    return version

def main():
    args = parse_arguments()
    setup_logging(args.debug)

    if args.install:
        logging.info('Installing script')
        return

    user = args.ghcr_user
    token = args.token or getpass('GHCR Token: ')

    docker_login(user, token, args)

    version = '0.1.0'  # Default version, should ideally load from a config or last release
    if args.release:
        version = args.release
    else:
        version = interactive_version_update(version, args)

    build_and_push_image(args.pkg, version, args.force, args)

if __name__ == '__main__':
    main()
