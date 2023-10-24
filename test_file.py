import unittest
from msg_split import split_message, MAX_LEN

class TestSplitMessage(unittest.TestCase):

    def test_basic_split(self):
        msg = "<p>простой параграф</p>"
        fragments = list(split_message(msg, 10))
        self.assertEqual(len(fragments), 3)
        self.assertTrue(all(len(frag) <= 10 for frag in fragments))

    def test_with_tags(self):
        msg = "<p><b>Жирный текст</b> и обычный текст</p>"
        fragments = list(split_message(msg, 15))
        self.assertEqual(len(fragments), 4)
        self.assertTrue(all(len(frag) <= 15 for frag in fragments))
        self.assertTrue("<b>" in fragments[0])
        self.assertTrue("</b>" in fragments[1])

    def test_no_split(self):
        msg = "<p>простой параграф</p>"
        fragments = list(split_message(msg, MAX_LEN))
        self.assertEqual(len(fragments), 1)

    def test_empty_message(self):
        fragments = list(split_message("", MAX_LEN))
        self.assertEqual(len(fragments), 0)

    def test_unsplittable_message(self):
        msg = "<p>" + "a" * (MAX_LEN + 1) + "</p>"
        with self.assertRaises(ValueError):
            list(split_message(msg, MAX_LEN))

    def test_multilevel_tags(self):
        msg = """<p>
                    <b>
                        <a href="https://www.google.com/">Поиск Google</a>
                        <ul>
                            <li>Hello World</li>
                            <li>Слова на англиском</li>
                        </ul>
                    </b>
                </p>"""
        fragments = list(split_message(msg, 50))
        self.assertTrue(len(fragments) > 1)
        self.assertTrue("<ul>" in fragments[-2])
        self.assertTrue("</ul>" in fragments[-1])

if __name__ == "__main__":
    unittest.main()
