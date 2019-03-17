import unittest
from winthingies.win32.wevtapi import *
from winthingies.win32.wevtapi_helpers import get_keyword_mapping


class TestProvider(unittest.TestCase):
    def test_get_providers(self):
        publisher_list_handle = EvtOpenPublisherEnum()

        publisher_list = []
        while True:
            publisher_name = EvtNextPublisherId(publisher_list_handle)
            if publisher_name is not None:
                publisher_list.append(
                    publisher_name
                )
            else:
                break

        self.assertEqual(True, bool("Microsoft-Windows-Kernel-File" in publisher_list))
        self.assertEqual(True, bool("Microsoft-Windows-Kernel-Registry" in publisher_list))

        for publisher_name in sorted(publisher_list):
            print(publisher_name)

        wevtapi.EvtClose(
            publisher_list_handle
        )

    def test_get_metadata(self):
        """PublisherMetadata is needed to map keyword descriptions to their flag.

        :return:
        """
        # This function opens up a metadata handle to a given local publisher
        metadata_handle = EvtOpenPublisherMetadata(
            "Microsoft-Windows-Kernel-Process"
        )

        mapping = get_keyword_mapping(
            metadata_handle
        )

        self.assertEqual(11, len(mapping))
        self.assertEqual("WINEVENT_KEYWORD_PROCESS", mapping[16]["name"])
        self.assertEqual("WINEVENT_KEYWORD_THREAD", mapping[32]["name"])
        self.assertEqual("WINEVENT_KEYWORD_IMAGE", mapping[64]["name"])
        self.assertEqual("WINEVENT_KEYWORD_CPU_PRIORITY", mapping[128]["name"])
        self.assertEqual("WINEVENT_KEYWORD_OTHER_PRIORITY", mapping[256]["name"])
        self.assertEqual("WINEVENT_KEYWORD_PROCESS_FREEZE", mapping[512]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB", mapping[1024]["name"])
        self.assertEqual("WINEVENT_KEYWORD_ENABLE_PROCESS_TRACING_CALLBACKS", mapping[2048]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB_IO", mapping[4096]["name"])
        self.assertEqual("WINEVENT_KEYWORD_WORK_ON_BEHALF", mapping[8192]["name"])
        self.assertEqual("WINEVENT_KEYWORD_JOB_SILO", mapping[16384]["name"])

        wevtapi.EvtClose(
            metadata_handle
        )


if __name__ == '__main__':
    unittest.main()