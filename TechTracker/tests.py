from django.test import TestCase
from .core.utils import *
# Create your tests here.

class UtilsTest(TestCase):
    def test_get_files_in_dir(self):
        path = 'F:\Project\hawk\data'
        ret = Utility.get_files_in_dir(path)
        self.assertIs(ret, False)