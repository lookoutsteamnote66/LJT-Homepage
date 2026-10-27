"""Check the rendered site without third-party Python dependencies."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json

ROOT = Path('_site')
SITE = 'https://lookoutsteamnote66.github.io'
BASE = '/LJT-Homepage'
HOME = SITE + BASE + '/'


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.resources = []
        self.text = []
        self.canonical = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in {'img', 'script'} and attrs.get('src'):
            self.resources.append(attrs['src'])
        if tag == 'link' and attrs.get('href'):
            if attrs.get('rel') == 'canonical':
                self.canonical = attrs['href']
            else:
                self.resources.append(attrs['href'])

    def handle_data(self, data):
        self.text.append(data)


html_files = {str(path.relative_to(ROOT)) for path in ROOT.rglob('*.html')}
assert html_files == {'index.html'}, f'Unexpected pages: {sorted(html_files)}'
assert not list(ROOT.rglob('*.md')), 'Source/demo Markdown was published'
html = (ROOT / 'index.html').read_text(encoding='utf-8')
page = Page()
page.feed(html)
text = ' '.join(' '.join(page.text).split())

required = [
    'Junteng Liu', 'first-year PhD candidate', 'HKUST NLP Group',
    'Professor Junxian He', 'Ph.D. in Computer Science',
    'Hong Kong University of Science and Technology', '2024–Present',
    'B.Eng.', 'Shanghai Jiao Tong University', '2020–2024', 'June 2024',
    'Research Intern — MINIMAX', 'February 2025–Present',
    'Research Intern — Tencent WXG', 'June 2024–September 2024', 'Zifei Shan',
    'Research Intern — Shanghai AI Lab', 'June 2023–December 2023', 'Prof. Yu Cheng',
    'natural language processing', 'machine learning',
    'LLM Reasoning and Reinforcement Learning',
    'Hallucination in Vision-Language Models (VLM)',
    'LLM Truthfulness and Interpretability', 'Zhiyuan Honor Scholarship',
    'Vision4Chart', 'Universal_Truthfulness_Hyperplane',
]
for value in required:
    assert value in text, f'Missing remembered detail: {value}'

publications = [
    'SynLogic: Synthesizing Verifiable Reasoning Data at Scale for Learning Logical Reasoning and Beyond',
    'On the Perception Bottleneck of VLMs for Chart Understanding',
    'On the Universal Truthfulness Hyperplane Inside LLMs',
    'In-Context Sharpness as Alerts: An Inner Representation Perspective for Hallucination Mitigation',
    'C-Eval: A Multi-Level Multi-Discipline Chinese Evaluation Suite for Foundation Models',
    'Composing Parameter-Efficient Modules with Arithmetic Operations',
]
publication_html = html.split('id="publications"', 1)[1].split('id="skills"', 1)[0]
publication_page = Page()
publication_page.feed(publication_html)
publication_text = ' '.join(' '.join(publication_page.text).split())
for title in publications:
    assert publication_text.count(title) == 1, f'Publication missing/duplicated on About: {title}'
assert publication_text.count('First author.') == 3
assert publication_text.count('arXiv, 2025.') == 2
assert publication_text.count('EMNLP 2024.') == 1
assert publication_text.count('ICML 2024.') == 1
assert publication_text.count('NeurIPS 2023.') == 2

for value in [
    'Your Name', 'Your Sidebar Name', 'none@example.org', 'Red Brick University',
    'PS_CX0AAAAAJ', 'yourorcidurl', 'john+snow', 'bsky.app',
    'profile.png', 'og-image.png',
]:
    assert value not in html, f'Template placeholder remains: {value}'

contacts = {
    'mailto:jliugi@connect.ust.hk',
    'https://github.com/Vicent0205',
    'https://scholar.google.com/citations?hl=en&user=tbK9jl4AAAAJ&view_op=list_works&sortby=pubdate',
    'https://x.com/junteng88716710',
}
assert contacts <= set(page.links), f'Missing contacts: {contacts - set(page.links)}'
assert page.canonical == HOME, f'Incorrect project-site canonical URL: {page.canonical}'
assert {'academic-background', 'research-experience', 'publications', 'skills', 'honors', 'contact'} <= page.ids


def local_path(url):
    parsed = urlsplit(url)
    if parsed.scheme and parsed.scheme not in {'http', 'https'}:
        return None
    if parsed.netloc and parsed.netloc != urlsplit(SITE).netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return '', parsed.fragment
    assert path.startswith(BASE + '/'), f'URL is missing the project baseurl: {url}'
    return path[len(BASE) + 1:], parsed.fragment


for url in page.links:
    local = local_path(url)
    if local is None:
        continue
    path, fragment = local
    assert path in {'', 'index.html'}, f'Unexpected local page link: {url}'
    assert not fragment or fragment in page.ids, f'Broken section link: {url}'

for url in page.resources:
    local = local_path(url)
    if local is not None:
        path, _ = local
        assert (ROOT / path).is_file(), f'Missing local resource: {url}'

manifest = json.loads((ROOT / 'images/manifest.json').read_text(encoding='utf-8'))
assert manifest['name'] == 'Junteng Liu'
assert manifest['start_url'] == BASE + '/'
for icon in manifest['icons']:
    path, _ = local_path(icon['src'])
    assert (ROOT / path).is_file(), f'Missing manifest icon: {path}'

print('Verified: one About page, six publications, remembered details, contacts, anchors, and project-site assets.')
