import unittest

from DownloadANDAI import Profile

test_string = "Test"
profile = None

class DownloadANDAITest(unittest.TestCase):
    def __init__(self):
        super(DownloadANDAITest, self).__init__()

    @classmethod
    def setUpClass(cls):
        global profile
        profile = Profile("1.7.10")

    def testDownloadFile(self):
        global profile
        source_file = open("source.txt", "w+")
        source_file.write(test_string)
        source_file.close()
        profile.downloadFile("test.txt", "source.txt")
        downloaded_file = open("test.txt")
        output = downloaded_file.readline().strip()
        downloaded_file.close()
        self.assertEqual(test_string, output)
