#!/usr/bin/env python3
"""Validate this library's deliberately small, single-line YAML frontmatter contract."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = ('When to use', 'Preconditions', 'Procedure', 'Tool permissions',
            'Failure handling', 'Deliverables', 'Acceptance criteria',
            'Hard boundaries', 'Response contract', 'Evidence and examples')


def validate(root):
    errors = []
    standalone = (root / 'SKILL.md').is_file()
    expected = 1 if standalone else 12
    files = [root / 'SKILL.md'] if standalone else sorted((root / 'skills').glob('*/SKILL.md'))
    if len(files) != expected:
        errors.append(f'expected {expected} skills, found {len(files)}')
    names = set()
    for path in files:
        label = str(path.relative_to(root))
        text = path.read_text(encoding='utf-8')
        front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        fields = {}
        if not front:
            errors.append(f'{label}: invalid frontmatter')
            continue
        for line in front[1].splitlines():
            match = re.fullmatch(r'(name|description): (.+)', line)
            if not match or match[1] in fields:
                errors.append(f'{label}: invalid/duplicate frontmatter field')
                continue
            value = match[2].strip()
            if value.startswith('"'):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    errors.append(f'{label}: invalid quoted scalar')
                    continue
            elif ': ' in value or value.startswith(('[', '{', '&', '*', '|', '>')):
                errors.append(f'{label}: unsupported YAML scalar')
                continue
            fields[match[1]] = value
        name = fields.get('name', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) >= 64:
            errors.append(f'{label}: invalid name')
        if name != path.parent.name or name in names:
            errors.append(f'{label}: name mismatch/duplicate')
        names.add(name)
        if not isinstance(fields.get('description'), str) or not fields.get('description', '').strip():
            errors.append(f'{label}: missing description')
        body = text[front.end():]
        for heading in HEADINGS:
            section = re.search(r'^## ' + re.escape(heading) + r'\n+(.*?)(?=^## |\Z)', body, re.M | re.S)
            if not section or not section[1].strip():
                errors.append(f'{label}: missing/empty {heading}')
        if 'Use when the user asks for work matching this skill' in body or re.search(r'\b(?:TODO|TBD)\b', body):
            errors.append(f'{label}: unfinished generic scaffold')
        if len(body.splitlines()) > 500:
            errors.append(f'{label}: entrypoint too long')
    for path in sorted(root.rglob('*.md')):
        if any(part in {'.git', '.local-audit', 'node_modules'} for part in path.relative_to(root).parts):
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in target or target.startswith(('#', 'mailto:')):
                continue
            resolved = (path.parent / target.split('#')[0]).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f'{path.relative_to(root)}: broken/escaping link')
    return files, errors


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    files, errors = validate(root)
    print(f'Checked {len(files)} skills: ' + ('NEED FIX' if errors else 'PASS'))
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
