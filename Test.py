import csv
import os
import subprocess

import sys
import time


def usage():
    print('Usage:')
    print('python CameraAPI.py [Folder Name of Command] [CSV file name] [Test count]')
    print('\nExample: $ python CameraAPI.py DBC831V2_Galaxy-S7 CommandOrderOfPriority.csv 100\n')
    return


def main():
    print("len=" + str(len(sys.argv)))
    if len(sys.argv) == 4:
        command_folder_name = str(sys.argv[1])
        csv_file_name = str(sys.argv[2])
        test_count = str(sys.argv[3])

        command_folder_name = os.getcwd() + '/' + command_folder_name
        if not os.path.exists(command_folder_name):
            print("\'%s\' folder not found." % (command_folder_name))
            exit()

        csv_file_name = os.getcwd() + '/' + csv_file_name
        if not os.path.isfile(csv_file_name):
            print("\'%s\' file not found." % (csv_file_name))
            exit()

        count_num = 0
        if test_count.isdigit():
            count_num = int(str(test_count))

        print("CSV File: " + csv_file_name)

        i = 1
        is_fail = False
        while i <= count_num:
            with open(csv_file_name) as csv_file:
                rows = csv.DictReader(csv_file)
                for row in rows:
                    if len(str(row['isDisabled']).strip()) == 0:
                        command = str(row['ProgramCommand']).strip() + ' ' + str(row['Argument']).strip()
                        command = command_folder_name + '/' + command
                        print("Command: " + command)
                        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

                        for line in p.stdout.readlines():
                            line = line.strip()
                            print("return_message:" + line)
                            if len(str(row['FAIL_Condition']).strip()) > 0:
                                pass

                        if is_fail:
                            break

                        if len(str(row['TakeANap']).strip()) > 0:
                            print("Take a nap: " + str(row['TakeANap']).strip() + 's')
                            time.sleep(int(str(row['TakeANap']).strip()))

                csv_file.close()
                print("Test count: " + str(i))
                print("==================================================")
                i += 1

            if is_fail:
                break

    else:
        usage()


if __name__ == '__main__':
    main()
