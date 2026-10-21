#!/usr/bin/env python3
"""Offline HTML packaging check, not a WeChat compatibility guarantee."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.article_count = 0
        self.images = 0
        self.errors = []
        self.text = []
        self.inline = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        starts = attrs.get('id') == 'article'
        inside = bool(self.stack) or starts
        if starts:
            self.article_count += 1
        if inside:
            if tag not in {'img', 'br', 'hr', 'meta', 'link', 'input', 'source', 'wbr', 'area', 'base', 'embed', 'param', 'track', 'col'}:
                self.stack.append(tag)
            if tag in {'script', 'style', 'iframe', 'object', 'form', 'link', 'button', 'input'}:
                self.errors.append('active content or external style in article')
            if any(key.startswith('on') for key in attrs):
                self.errors.append('event handler in article')
            if attrs.get('style'):
                self.inline += 1
            if tag == 'img':
                self.images += 1
                src = attrs.get('src', '')
                if not src.startswith('data:image/'):
                    self.errors.append('image is not embedded; dependency needs review')
            for key in ('href', 'src'):
                if attrs.get(key, '').strip().lower().startswith(('javascript:', 'file:')):
                    self.errors.append('unsafe local or executable reference')
            if re_unsafe_style(attrs.get('style', '')):
                self.errors.append('CSS external resource/expression needs review')

    def handle_endtag(self, tag):
        if self.stack:
            if self.stack[-1] == tag:
                self.stack.pop()
            else:
                self.errors.append('unbalanced article markup')

    def handle_data(self, data):
        if self.stack:
            self.text.append(data)


def re_unsafe_style(style):
    import re
    return bool(re.search(r'url\s*\(|expression\s*\(', style, re.I))


def check(path):
    parser = ArticleParser()
    parser.feed(Path(path).read_text(encoding='utf-8'))
    if parser.article_count != 1:
        parser.errors.append('expected one id=article container')
    if parser.stack:
        parser.errors.append('article not closed')
    if not ''.join(parser.text).strip():
        parser.errors.append('empty article text')
    if not parser.inline:
        parser.errors.append('no inline styles found')
    return {'status': 'NEED FIX' if parser.errors else 'PASS', 'scope': 'local HTML packaging only',
            'images': parser.images, 'errors': sorted(set(parser.errors))}


if __name__ == '__main__':
    result = check(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(result['status'] != 'PASS')
