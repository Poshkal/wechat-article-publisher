import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

class Standalone(unittest.TestCase):
    def test_structure(self):
        self.assertFalse(module('validate_skills').validate(ROOT)[1])

    def test_sensitive_gate(self):
        scan = module('scan_public')
        self.assertTrue(scan.inspect('sample.md', ('gh' + 'p_' + 'A' * 30).encode()))
        self.assertFalse(scan.inspect('sample.md', '脱敏案例'.encode()))

    def test_fake_pass(self):
        report = {'scope': 'offline', 'revision': 'fixture', 'checks': [
            {'id': 'never-run', 'status': 'PASS', 'executed': False}]}
        self.assertEqual(module('qa_gate').gate(report, ROOT)['status'], 'BLOCKED')

    def test_missing_article_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'article.html'
            p.write_text('<div id="article"><p style="color:#333">测试</p><img src="missing.png"></div>')
            self.assertEqual(module('check_article').check(p)['status'], 'NEED FIX')

if __name__ == '__main__':
    unittest.main()
