from unittest import TestCase, mock, main
from process_image_files import ProcessImageFilesByDate


class TestProcessImageFilesByDate(TestCase):

    @staticmethod
    @mock.patch('os.walk')
    def test_get_date_range_of_image_files_1(mock_os_walk):
        mock_os_walk.return_value = (('parent', ('child1', 'child2', 'child3'), ()),
                                     ('parent/child1', (), ('farm-xxx_barn-3_camera-1_2020-11-02T00h00m00s+0000.png',)),
                                     ('parent/child2', (), ('farm-xxx_barn-3_camera-1_2020-09-02T00h00m00s+0000.png',)),
                                     ('parent/child3', (), ('farm-xxx_barn-3_camera-1_2020-12-02T00h00m00s+0000.png',)))

        process_image_files = ProcessImageFilesByDate('DIR1')
        assert process_image_files.get_date_range_of_image_files() == "Date Range: 20200902000000 - 20201202000000"

    @staticmethod
    @mock.patch('os.walk')
    def test_get_date_range_of_image_files_2(mock_os_walk):
        mock_os_walk.return_value = (('parent', ('child1', 'child2', 'child3'), ()),
                                     ('parent/child1', (), ()),
                                     ('parent/child2', (), ()),
                                     ('parent/child3', (), ()))

        process_image_files = ProcessImageFilesByDate('DIR1')
        assert process_image_files.get_date_range_of_image_files() == \
               "Failed to find the range for the file set. Start Date or End Date is Not available"

    @staticmethod
    @mock.patch('os.walk')
    def test_get_date_range_of_image_files_3(mock_os_walk):
        mock_os_walk.return_value = (('parent', ('child1', 'child2', 'child3'), ()),
                                     ('parent/child1', (), ()),
                                     ('parent/child2', (), ()),
                                     ('parent/child3', (), ('farm-xxx_barn-3_camera-1_2020-12-02T00h00m00s+0000.png',)))

        process_image_files = ProcessImageFilesByDate('DIR1')
        assert process_image_files.get_date_range_of_image_files() == "Date Range: 20201202000000 - 20201202000000"

    @staticmethod
    @mock.patch('os.walk')
    def test_list_files_by_time_zone_date_1(mock_os_walk):
        flag = True
        mock_os_walk.return_value = (('parent', ('child1', 'child2', 'child3'), ()),
                                     ('parent/child1', (), ('farm-xxx_barn-3_camera-1_2020-11-02T00h00m00s+0000.png',)),
                                     ('parent/child2', (), ('farm-xxx_barn-3_camera-1_2020-09-02T00h00m00s+0000.png',)),
                                     ('parent/child3', (), ('farm-xxx_barn-3_camera-1_2020-12-02T13h00m00s+0000.png',)))
        process_image_files = ProcessImageFilesByDate('DIR1')
        expected_output = [{'date_tz': '2020-09-02',
                            'files': ['parent/child2/farm-xxx_barn-3_camera-1_2020-09-02T00h00m00s+0000.png']},
                           {'date_tz': '2020-12-03',
                            'files': ['parent/child3/farm-xxx_barn-3_camera-1_2020-12-02T13h00m00s+0000.png']},
                           {'date_tz': '2020-11-02',
                            'files': ['parent/child1/farm-xxx_barn-3_camera-1_2020-11-02T00h00m00s+0000.png']}]
        actual_output = process_image_files.list_files_by_time_zone_date("Pacific/Enderbury")
        if len(expected_output) != len(actual_output) or any(item not in actual_output for item in expected_output):
            flag = False
        assert flag is True

    @staticmethod
    @mock.patch('os.walk')
    def test_list_files_by_time_zone_date_2(mock_os_walk):
        flag = True
        mock_os_walk.return_value = (('parent', ('child1', 'child2', 'child3'), ()),
                                     ('parent/child1', (), ()),
                                     ('parent/child2', (), ()),
                                     ('parent/child3', (), ()))
        process_image_files = ProcessImageFilesByDate('DIR1')
        expected_output = []
        actual_output = process_image_files.list_files_by_time_zone_date("Pacific/Enderbury")
        if len(expected_output) != len(actual_output) or any(item not in actual_output for item in expected_output):
            flag = False
        assert flag is True


if __name__ == '__main__':
    main()

