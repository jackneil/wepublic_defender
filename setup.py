"""
Setup script for wepublic_defender package.

Install with:
    pip install -e .  (for development)
    pip install .     (for normal installation)
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="wepublic_defender",
    version="0.1.0",
    description="Adversarial Legal Review System using multiple AI providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jack",
    author_email="",
    url="https://github.com/jackneil/wepublic_defender",
    packages=find_packages(exclude=["tests", "scripts", ".claude"]),
    package_data={
        "wepublic_defender": [
            "config/*.json",
        ],
    },
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        "openai>=1.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "json5>=0.9.0",
        "rich>=13.0.0",
        "python-docx>=0.8.11",
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.10.0",
        "aiofiles>=23.0.0",
        "typing-extensions>=4.0.0",
        "xai-sdk>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "wpd-run-agent=wepublic_defender.cli.run_agent:main",
            "wpd-usage-summary=wepublic_defender.cli.usage_summary:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Legal Industry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="legal review ai adversarial gpt grok openai",
)
