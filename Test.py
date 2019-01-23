import csv
import logging
import logging.config
import os
import subprocess

import datetime
import sys
import time


def genLogger():
    global logger
    STR_DATETIME = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    logger = logging.getLogger(__name__)
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(levelname)s - %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "./log/Test_" + STR_DATETIME + ".log",
                "maxBytes": 3145728,
                "backupCount": 10,
                "encoding": "utf8"
            }
        },

        "loggers": {
            "my_module": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        "root": {
            "level": "DEBUG",
            "handlers": ["console", "info_file_handler"]
        }
    })


def usage():
    print('Usage:')
    print('python CameraAPI.py [Folder Name of Command] [CSV file name] [Test count]')
    print('\nExample: $ python CameraAPI.py DBC831V2_Galaxy-S7 CommandOrderOfPriority.csv 100\n')
    return


def main():
    try:
        logger.debug("len=" + str(len(sys.argv)))
        if len(sys.argv) == 4:
            command_folder_name = str(sys.argv[1])
            csv_file_name = str(sys.argv[2])
            test_count = str(sys.argv[3])

            command_folder_name = os.getcwd() + '/' + command_folder_name
            if not os.path.exists(command_folder_name):
                logger.debug("\'%s\' folder not found." % (command_folder_name))
                exit()

            csv_file_name = os.getcwd() + '/' + csv_file_name
            if not os.path.isfile(csv_file_name):
                logger.debug("\'%s\' file not found." % (csv_file_name))
                exit()

            count_num = 100
            if test_count.isdigit():
                count_num = int(str(test_count))

            logger.debug("CSV File: " + csv_file_name)

            i = 1
            is_fail = False
            while i <= count_num:
                with open(csv_file_name) as csv_file:
                    rows = csv.DictReader(csv_file)
                    for row in rows:
                        if len(str(row['isDisabled']).strip()) == 0:
                            command = str(row['ProgramCommand']).strip() + ' ' + str(row['Argument']).strip()
                            command = command_folder_name + '/' + command
                            logger.debug("Command: " + command)
                            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

                            for line in p.stdout.readlines():
                                line = line.strip()
                                logger.debug("return_message:" + line)
                                if len(str(row['PASS_Condition']).strip()) > 0:
                                    pass

                            if is_fail:
                                break

                            if len(str(row['TakeANap']).strip()) > 0:
                                logger.debug("Take a nap: " + str(row['TakeANap']).strip() + 's')
                                time.sleep(int(str(row['TakeANap']).strip()))

                    csv_file.close()
                    logger.debug("Test count: " + str(i))
                    logger.debug("==================================================")
                    i += 1

                if is_fail:
                    break

        else:
            usage()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error("An exception occurred:" + str(e))


if __name__ == '__main__':
    genLogger()
    main()
