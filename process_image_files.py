import os
import pytz
from datetime import datetime
import logging


class ProcessImageFilesByDate:

    _IMAGE_TYPE = ['.png', '.jpg']
    _FARM_NAME = ['farm-xxx']

    def __init__(self, dir_path):
        """
        :param dir_path: Absolute Directory path containing the images captured by Camera
        """
        self._image_dir_path = dir_path

    @staticmethod
    def _parse_date_from_file_name(file_name):
        """
        :param file_name: Parse file name for datetime
        :return: datetime
        """
        file_date_str = file_name.split('_')[-1].split('.')[0]
        file_date = datetime.strptime(file_date_str, '%Y-%m-%dT%Hh%Mm%Ss+0000')
        return file_date

    @staticmethod
    def _get_file_date_by_timezone_in_str(file_date, time_zone_info):
        """
        :param file_date: UTC file_date extracted from the file_name
        :param time_zone_info: Time zone to convert the file_date
        :return: timezone date string (YY-MM-DD)
        """
        file_date_by_timezone = file_date.replace(tzinfo=pytz.utc).astimezone(time_zone_info)
        file_date_by_timezone_str = file_date_by_timezone.strftime("%Y-%m-%d")
        return file_date_by_timezone_str

    def _is_valid_file(self, file_name):
        """
        :param file_name: file_names in the directory
        :return: True/False depending on whether file_name is camera image from farm
        """
        if file_name.startswith(tuple(self._FARM_NAME)) and file_name.endswith(tuple(self._IMAGE_TYPE)):
            return True
        return False

    def get_date_range_of_image_files(self):
        """
        :return: Str - Date range of image file names
        """
        start_date = None
        end_date = None
        for root, dirs, files in os.walk(self._image_dir_path):
            for file_name in files:
                if self._is_valid_file(file_name):
                    file_date = self._parse_date_from_file_name(file_name)
                    if not start_date or start_date > file_date:
                        start_date = file_date
                    if not end_date or end_date < file_date:
                        end_date = file_date
        if not start_date or not end_date:
            return 'Failed to find the range for the file set. Start Date or End Date is Not available'
        else:
            return 'Date Range: {0} - {1}'.format(start_date.strftime("%Y%m%d%H%M%S"), end_date.strftime("%Y%m%d%H%M%S"))

    def list_files_by_time_zone_date(self, timezone_tz):
        """
        :param timezone_tz: timezone in format US/Eastern, US/Central..
        :return: List of Dictionaries with files by timezone-aware date
        """
        time_zone_info = pytz.timezone(timezone_tz)
        files_by_date_dict = {}
        result_file_by_date_list = []
        for root, dirs, files in os.walk(self._image_dir_path):
            for file_name in files:
                if self._is_valid_file(file_name):
                    file_date = self._parse_date_from_file_name(file_name)
                    file_date_by_timezone_str = self._get_file_date_by_timezone_in_str(file_date, time_zone_info)
                    cur_file_list = files_by_date_dict.get(file_date_by_timezone_str, [])
                    cur_file_list.append(os.path.join(root, file_name))
                    files_by_date_dict.update({file_date_by_timezone_str: cur_file_list})
        for file_date, file_list in files_by_date_dict.items():
            result_file_by_date_list.append({'date_tz': file_date, 'files': file_list})
        return result_file_by_date_list
