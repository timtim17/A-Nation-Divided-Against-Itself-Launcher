import unittest
import os
import threading

from ANDAI.DownloadANDAI import Profile

test_string = "Test"
profile = None

class DownloadANDAITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global profile
        if profile is None:
            profile = Profile("1.7.10")

    def test_download_file(self):
        global profile
        source_file = open("source.txt", "w+")
        source_file.write(test_string)
        source_file.close()
        thread = threading.Thread(target=profile.downloadFile, args=(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/" + "test.txt", "source.txt"))
        thread.start()
        thread.join()
        # profile.downloadFile(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/" + "test.txt", "source.txt")
        downloaded_file = open("test.txt")
        output = downloaded_file.readline().strip()
        downloaded_file.close()
        self.assertEqual(test_string, output)
        os.remove("source.txt")
        os.remove("test.txt")

if __name__ == "__main__":
    unittest.main()
