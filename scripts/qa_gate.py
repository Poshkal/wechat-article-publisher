#!/usr/bin/env python3
"""Aggregate an evidence-backed offline QA report. Does not execute tests."""
import json
import sys
from pathlib import Path


def gate(report, base):
    issues = []
    failed = False
    checks = report.get('checks', [])
    if not checks or not report.get('scope') or not report.get('revision'):
        issues.append('missing scope, revision or checks')
    for item in checks:
        name = item.get('id', 'unnamed')
        status = item.get('status')
        if status not in {'PASS', 'NEED FIX', 'BLOCKED', 'NOT VERIFIED'}:
            issues.append(f'{name}: invalid status')
        if status == 'NEED FIX':
            failed = True
        if status == 'PASS':
            evidence = (base / item.get('evidence', '')).resolve()
            if (not item.get('executed') or type(item.get('exit_code')) is not int or item.get('exit_code') != 0
                    or not item.get('command') or not item.get('environment')
                    or not evidence.is_relative_to(base.resolve()) or not evidence.is_file()
                    or not evidence.stat().st_size):
                issues.append(f'{name}: PASS without valid execution evidence')
        elif item.get('required', True):
            issues.append(f'{name}: required check not passed')
    return {'status': 'NEED FIX' if failed else 'BLOCKED' if issues else 'PASS',
            'scope': report.get('scope'), 'issues': issues}


if __name__ == '__main__':
    path = Path(sys.argv[1]).resolve()
    result = gate(json.loads(path.read_text()), path.parent)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(result['status'] != 'PASS')
