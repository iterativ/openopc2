from unittest import TestCase
from openopc2.opc_types import TagProperties


class TestPropertiesClass(TestCase):
    def test_to_dict(self):
        props = TagProperties()
        props.quality = 'Good'
        test_dict = props.class_to_dict()
        self.assertTrue(test_dict['quality'], 'Good')

    def test_from_dict(self):
        test_dict = {'tag_name': None,
         'data_type': 'VT12',
         'value': 3.1415,
         'quality': 'Good',
         'timestamp': None,
         'access_rights': 'Read',
         'server_scan_rate': 100.0,
         'eu_type': 'None',
         'eu_info': 'None',
         'description': "Unknown tag",
        '__class__': 'test'}

        props = TagProperties.dict_to_class('test', test_dict)
        self.assertTrue(props.value, 3.1415)
        self.assertTrue(props.server_scan_rate, 100)
