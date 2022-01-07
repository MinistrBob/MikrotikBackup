import csv
import datetime
import os
import shutil

from mikrotik import Mikrotik


def compare_files(f1, f2):
    """
    Compare two text files. Ignore lines with '#'.
    :param f1: current_file
    :param f2: previous_file
    :return: True - if files identical, otherwise - False. If previous_file doesn't exist return False.
    """
    if not os.path.exists(f2):
        return False
    with open(f1, 'r') as fp1, open(f2, 'r') as fp2:
        while True:
            # b1 = fp1.readline().rstrip()
            # b2 = fp2.readline().rstrip()
            b1 = fp1.readline()
            b2 = fp2.readline()
            # print(b1)
            # print(b2)
            # print("--------------------------------")
            if b1.startswith('#') or b2.startswith('#'):
                continue
            if b1 != b2:
                return False
            if not b1:
                return True


def backup_mikrotik(curr_date, base_path, line):
    # Work with mikrotik
    print(f"Work with {line[0]} mikrotik")
    mk = Mikrotik(line[0], line[1], line[2])
    # Create export backup. Compare with previous.
    # If exist differences, additionally create binary backup and store both.
    # Binary backup restore: /system backup load name=<file_name>
    mk.backup_export("current.rsc")
    backup_folder = os.path.join(base_path, line[0])
    # Create folder for backup
    if not os.path.exists(backup_folder):
        print(f"Create folder for backup {backup_folder}")
        try:
            os.mkdir(backup_folder)
        except OSError as e:
            print(f"ERROR: Can't create folder {backup_folder}:\n{e}")
    # Copy local current.rsc file to previous.rsc
    current_file = os.path.join(backup_folder, "current.rsc")
    previous_file = os.path.join(backup_folder, "previous.rsc")
    if os.path.exists(current_file):
        try:
            os.replace(current_file, previous_file)
        except OSError as e:
            print(f"ERROR: Can't rename current.rsc to previous.rsc:\n{e}")
    # Download current.rsc locally
    mk.download_file("current.rsc", current_file)
    # Compare current and previous files
    result = compare_files(current_file, previous_file)
    # If exist differences, additionally create binary backup and store both
    if result:
        print(f"No changes. Nothing to work")
    else:
        print(f"There are changes. Making a backup")
        backup_name = f"{line[0]}-{curr_date}"
        # Copy local current.rsc to <backup_name>.rsc
        backup_file = os.path.join(backup_folder, f"{backup_name}.rsc")
        print(f"Copy {current_file} to {backup_file}")
        try:
            shutil.copy(current_file, backup_file)
        except Error as e:
            print(f"ERROR: Can't copy current.rsc:\n{e}")
        # Create binary backup additionally
        mk.backup_backup("current")
        # Download current.backup locally
        binary_backup_file = os.path.join(backup_folder, f"{backup_name}.backup")
        mk.download_file("current.backup", binary_backup_file)
    print()


if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    curr_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_path = os.getenv('MIKROTIK_BACKUP_PATH')

    # Get MIKROTIK_BACKUP_PATH env
    try:
        if base_path is None:
            raise EnvironmentError("ERROR: Environment variable MIKROTIK_BACKUP_PATH not defined")
    except EnvironmentError as e:
        exit(1)

    with open('config.conf', newline='', encoding='utf-8') as f:
        config = csv.reader(f, delimiter=';')
        # headers = next(reader, None)
        for line in config:  # ['192.168.2.1', 'admin', '']
            # print(line)
            if line[0].startswith('#'):
                continue
            backup_mikrotik(curr_date, base_path, line)

    print(f"Program completed")
    print(f"Total time spent: {datetime.datetime.now() - begin_time} sec.")