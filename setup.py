"""
Setup for cfgmgr
"""

from setuptools import setup

setup(
    name="cfgmgr",
    version="002",
    packages=[
        "cfgmgr",
    ],
    install_requires=[
        "Click",
        "cryptography",
    ],
    extras_require={"dev": ["black", "pylint", "isort", "ipython"]},
    entry_points="""
        [console_scripts]
        cfgmgr=cfgmgr.cli:cli
    """,
)
