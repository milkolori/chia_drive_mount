import pathlib
import logging
from system_logging import setup_logging
from system_logging import read_config
import sys
from glob import glob
from os.path import ismount, abspath, exists
import string
import subprocess
import os


__author__ = 'Milko Lorinkov'
VERSION = "0.1 (2021-05-24)"


TRANSFER_FILE_PREFIX = 'copyFrom'
RECEIVE_FILE_PREFIX = 'copyTo'


config_file_name = sys.argv[1:]
is_simulation = read_config(config_file_name, 'env_params', 'simulate')

setup_logging(config_file_name)
level = read_config(config_file_name, 'system_logging', 'log_level')
level = logging._checkLevel(level)
logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)
log.setLevel(level)


red = '\033[0;31m'
yellow = '\033[0;33m'
green = '\033[0;32m'
white = '\033[0;37m'
blue = '\033[0;34m'
nc = '\033[0m'


def check_chia_config_file():
    chia_config_file = read_config(
        config_file_name, 'env_params', 'chia_config_file')
    if exists(chia_config_file):
        return
    else:
        log.error(f'{red}ERROR{nc} opening {yellow}{chia_config_file}{nc}! Please check your {yellow}filepath{nc} and try again!')
        exit()


def get_all_mounted_drives():
    mount = subprocess.getoutput('mount -v')
    mntlines = mount.split('\n')
    drives = [mount.split()[0] for mount in mntlines if os.path.ismount(mount.split()[2])]
    return drives

def get_new_drive():
    all_drives = sorted(glob('/dev/sd*'))#sd - TODO change
    mounted_drives = get_all_mounted_drives()
    unmounted_drives = list(filter(lambda drive: drive not in mounted_drives, all_drives))
    if unmounted_drives:
        return sorted(unmounted_drives)[0]
    else:
        return False

def mount_new_drive():
    log.debug(f'Check for new drives to be mounted.')
    #TODO check_chia_config_file()
    new_drive = get_new_drive()
    if new_drive:
        log.debug(f'New drive found {new_drive}')
    else:
        log.debug(f'No new drives found. Will check again soon!')


def main():
    mount_new_drive()


if __name__ == '__main__':
    main()