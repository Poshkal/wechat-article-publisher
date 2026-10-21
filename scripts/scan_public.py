#!/usr/bin/env python3
"""Conservative public-export gate. Reports only paths/rules, never matching values.
Not a substitute for manual review of business confidentiality or provenance.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    'credential-token': re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|shp(?:at|ss|ca)_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})'),
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'jwt': re.compile(r'eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}'),
    'credential-assignment': re.compile(r'(?i)(?:appsecret|api[_-]?key|access[_-]?token|password)\s*[:=]\s*[\x22\x27]?[A-Za-z0-9_+/=-]{16,}'),
    'personal-email': re.compile(r'\b(?![A-Za-z0-9+_.-]+@users\.noreply\.github\.com\b)[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
    'local-private-path': re.compile(r'/(?:Users|Volumes)/[^\s`\x22\x27]+'),
    'phone-number': re.compile(r'(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)'),
}
EXCLUDE = {'.git', '.local-audit', '.output', '__pycache__', 'node_modules'}
ALLOW = {'.md', '.py', '.yml', '.yaml', '.json', '.txt'}


def inspect(name, data):
    issues = []
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or any(part in EXCLUDE for part in path.parts):
        return [(name, 'private/export-excluded path')]
    if path.name.startswith('.env') or path.suffix in {'.pem', '.key', '.p12', '.sqlite', '.zip'}:
        issues.append((name, 'forbidden file type'))
    if path.suffix not in ALLOW and name != '.gitignore':
        issues.append((name, 'unreviewed file type'))
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return issues + [(name, 'binary/unreviewed content')]
    for rule, pattern in RULES.items():
        if pattern.search(text):
            issues.append((name, rule))
    return issues


def scan(root, staged=False):
    issues = []
    if staged:
        raw = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMRT', '-z'], cwd=root)
        names = [n.decode() for n in raw.split(b'\0') if n]
    else:
        names = [str(p.relative_to(root)) for p in sorted(root.rglob('*'))
                 if p.is_file() and not any(x in EXCLUDE for x in p.relative_to(root).parts)]
    for name in names:
        path = root / name
        if path.is_symlink():
            issues.append((name, 'symlink not allowed in export'))
            continue
        if staged:
            mode = subprocess.check_output(['git', 'ls-files', '-s', '--', name], cwd=root).decode().split()[0]
            if mode not in {'100644', '100755'}:
                issues.append((name, 'non-regular staged file'))
                continue
            data = subprocess.check_output(['git', 'show', ':' + name], cwd=root)
        else:
            data = path.read_bytes()
        issues.extend(inspect(name, data))
    return names, issues


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    names, issues = scan(ROOT, args.staged)
    print(f'Public scan: {len(names)} files, ' + ('BLOCKED' if issues else 'PASS'))
    for name, rule in issues:
        print(f'{name}: {rule}')
    sys.exit(bool(issues))
