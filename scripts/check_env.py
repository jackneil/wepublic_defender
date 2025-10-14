#!/usr/bin/env python
"""
Check environment readiness for wepublic_defender + Claude Code.

Verifies:
- Python version
- Required packages
- API keys
- Standard directory structure
"""

import sys
import importlib
import os
from pathlib import Path


REQUIRED_PACKAGES = [
    ("openai", None),
    ("pydantic", "__version__"),
    ("json5", None),
    ("docx", None),  # module name for python-docx
    ("rich", None),
]

STANDARD_DIRS = [
    "00_NEW_DOCUMENTS_INBOX",
    "01_CASE_OVERVIEW",
    "02_PLEADINGS",
    "03_DISCOVERY",
    "04_EVIDENCE",
    "05_CORRESPONDENCE",
    "06_RESEARCH",
    "07_DRAFTS_AND_WORK_PRODUCT",
    "08_REFERENCE",
]


def check_python():
    v = sys.version_info
    ok = v.major >= 3 and v.minor >= 9
    print(f"Python: {sys.version.split()[0]} {'OK' if ok else 'FAIL (need 3.9+)'}")
    print(f"Python exe: {sys.executable}")
    return ok


def check_packages():
    all_ok = True
    for name, attr in REQUIRED_PACKAGES:
        try:
            mod = importlib.import_module(name)
            ver = getattr(mod, attr) if attr else ""
            print(f"Package: {name} OK {ver}")
        except Exception as e:
            print(f"Package: {name} MISSING ({e})")
            all_ok = False
    return all_ok


def check_api_keys():
    keys = ["OPENAI_API_KEY", "XAI_API_KEY"]
    any_set = False
    for k in keys:
        v = os.getenv(k)
        if v:
            print(f"Env: {k} OK")
            any_set = True
        else:
            print(f"Env: {k} not set")
    if not any_set:
        print("Hint: create .env at case root or set system env vars.")
    return any_set


def check_wepublic_defender_installed():
    """Check if wepublic_defender is importable and report its location/version."""
    try:
        import wepublic_defender as wpd  # type: ignore
        path = getattr(wpd, "__file__", "?")
        version = getattr(wpd, "__version__", "?")
        print(f"WePublicDefender: INSTALLED (version {version}) @ {path}")
        return True
    except Exception as e:
        print(f"WePublicDefender: NOT INSTALLED ({e})")
        return False


def detect_env() -> str:
    """Return a short label for the current environment (conda/venv/unknown)."""
    conda_env = os.environ.get("CONDA_DEFAULT_ENV")
    if conda_env:
        return f"conda:{conda_env}"
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        return f"venv:{Path(venv).name}"
    return "system"


def check_recommended_env() -> bool:
    """Advise using 'wepublic_defender' conda env; return True if active/redundant."""
    env_label = detect_env()
    print(f"Env: {env_label}")
    if env_label.startswith("conda:wepublic_defender"):
        print("Env status: using recommended conda environment.")
        return True
    print("Env status: not in 'wepublic_defender' conda env. Recommended:")
    print("  conda create -n wepublic_defender python=3.11 -y")
    print("  conda run -n wepublic_defender python -m pip install -e wepublic_defender/")
    print("  conda run -n wepublic_defender python wepublic_defender/scripts/check_env.py")
    return False


def check_structure():
    cwd = Path.cwd()
    ok = True
    for d in STANDARD_DIRS:
        if not (cwd / d).exists():
            print(f"Dir: {d} MISSING")
            ok = False
        else:
            print(f"Dir: {d} OK")
    return ok


def main() -> int:
    print("=== Environment Check ===")
    ok_py = check_python()
    ok_pkg = check_packages()
    ok_keys = check_api_keys()
    ok_wpd = check_wepublic_defender_installed()
    ok_env = check_recommended_env()
    ok_dirs = check_structure()

    all_ok = ok_py and ok_pkg and ok_dirs
    print("=== Summary ===")
    print(
        f"Python: {'OK' if ok_py else 'FAIL'} | Packages: {'OK' if ok_pkg else 'MISSING'} | "
        f"Dirs: {'OK' if ok_dirs else 'MISSING'} | Keys: {'OK' if ok_keys else 'NOT SET'} | "
        f"WPD: {'OK' if ok_wpd else 'NOT INSTALLED'} | Env: {'OK' if ok_env else 'RECOMMEND CONDA RUN'}"
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
