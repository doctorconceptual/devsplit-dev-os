import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]

def test_cli_scaffold_smoke():
    result = subprocess.run([sys.executable, str(CODE / 'audit.py'), '--smoke'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'scaffold ready' in result.stdout
