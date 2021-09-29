import os
import argparse
import logging
import sys
import pytz
import traceback
import json
from datetime import datetime
from process_image_files import ProcessImageFilesByDate
from utils import Logging

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--path', type=str, help="Absolute directory path containing Camera image files",
                            required=True)
        operation_help = "Operation to perform" \
                         " 1.Return Date Range of image files present in the path" \
                         " 2.Return List of Dict with files by timezone-aware date"
        parser.add_argument('-o', '--operation', type=int, help=operation_help, required=True)
        parser.add_argument('-t', '--timeZone', type=str, help="Timezone to list the files",
                            required=False)
        parser.add_argument('-l', '--logFilePath', type=str, help="File path to Log the information",
                            required=False)
        args = parser.parse_args()

        if not args.logFilePath:
            log_file_path = os.path.join(os.getcwd(), "{0}.log".format(datetime.now().strftime('%Y%m%d')))
        else:
            log_file_path = args.logFilePath

        logger = Logging(log_file_path)
        logger.set_logging()

        if not os.path.exists(args.path):
            logging.error("Directory {0} doesn't exists".format(args.path))
            sys.exit(1)

        if str(args.operation) not in ("1", "2"):
            logging.error("{0} is not a valid operation. Valid operations - ('1', '2)".format(args.operation))
            sys.exit(1)

        if args.operation is str(2) and (not args.timeZone or args.timeZone not in pytz.all_timezones):
            logging.error("{0} is not a valid timezone.")
            sys.exit(1)

        process_image_files = ProcessImageFilesByDate(args.path)
        if str(args.operation) == "1":
            logging.info("File names in the path {0} are of date range - ".format(args.path))
            logging.info(process_image_files.get_date_range_of_image_files())
        elif str(args.operation) == "2":
            logging.info("List of Dictionaries with files by timezone-aware date")
            file_dict_list = process_image_files.list_files_by_time_zone_date(args.timeZone)
            logging.info(json.dumps(file_dict_list, indent=4, sort_keys=True))
        sys.exit(0)
    except Exception as exc:
        logging.warn("traceback is {}".format(traceback.format_exc()))
        logging.error("Execution failed with the exception {0}".format(str(exc)))

