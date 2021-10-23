from setuptools import setup

setup(
    name="secrets",
    version="0.1",
    py_modules=["core"],
    install_requires=[
        "Click",
        "cryptography",
    ],
    extras_require={"dev": ["black", "pylint", "isort"]},
    entry_points="""
        [console_scripts]
        secrets=main:cli
    """,
)
