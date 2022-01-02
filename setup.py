DESCRIPTION = "yiri-be is backend for yiri-mirai."

with open("Readme.md", "r") as f:
    LONG_DESCRIPTION = f.read()


CLASSIFIERS = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Developers
License :: OSI Approved :: AGPL-3.0 License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Typing :: Typed
"""

INSTALL_REQUIREMENTS = """\
yiri-mirai>=0.2.6, <0.3
flask[async]>=2.0.0
marshmallow>=3.14
"""


def setup_pkg():
    import setuptools

    metadata = dict(
        name="yiri-be",
        version="0.0.1",
        author="Rebuild",
        author_email="admin@rebuild.moe",
        license="AGPL-3.0",
        license_files=("LICENSE",),
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        classifiers=[_f for _f in CLASSIFIERS.split("\n") if _f],
        python_requires=">=3.7",
        install_requires=[_f for _f in INSTALL_REQUIREMENTS.split("\n") if _f],
        packages="yiri_be",
    )

    setuptools.setup(**metadata)


if __name__ == "__main__":
    setup_pkg()
