"""Run with .venv/bin/python -m unittest discover -s management/tools/tests -p test_csv_preview_links.py."""
from pathlib import Path
import unittest
from html.parser import HTMLParser

import markdown

ROOT = Path(__file__).resolve().parents[3]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs))

class CsvPreviewLinksTest(unittest.TestCase):
    def test_part3_input_links_render_preview_class_in_all_languages(self):
        count = 0
        sources = list((ROOT / 'docs/parts/part-03').rglob('*.md'))
        for part, chapter, section in [(5,7,1),(5,7,3),(5,8,1),(5,8,2),(5,8,4),(5,12,1),(6,21,3)]:
            sources.extend((ROOT / f'docs/parts/part-{part:02}/chapter-{chapter:02}').glob(f'section-{section:02}*.md'))
        for source in sources:
            parser = Links()
            parser.feed(markdown.markdown(source.read_text(), extensions=['attr_list', 'fenced_code']))
            for attrs in parser.links:
                href = attrs.get('href', '')
                if not href.endswith('.csv'):
                    continue
                with self.subTest(source=source.name, href=href):
                    asset = ROOT / 'docs' / href.removeprefix('/AiBook/') if href.startswith('/AiBook/') else source.parent / href
                    self.assertTrue(asset.is_file(), href)
                    self.assertIn('csv-preview', attrs.get('class', '').split())
                    self.assertNotIn('target', attrs)
                    count += 1
        self.assertGreater(count, 0)

if __name__ == '__main__':
    unittest.main()
