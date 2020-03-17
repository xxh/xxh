import setuptools
from xxh_xxh.settings import global_settings

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xxh-xxh",
    version=global_settings['XXH_VERSION'],
    description="Bring your favorite shell wherever you go through the ssh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xxh/xxh",
    project_urls={
        "Documentation": "https://github.com/xxh/xxh/blob/master/README.md",
        "Code": "https://github.com/xxh/xxh",
        "Issue tracker": "https://github.com/xxh/xxh/issues",
    },
    python_requires='>=3.6',
    install_requires=[
        'xonsh >= 0.9.13',
        'pexpect >= 4.8.0',
        'pyyaml'
    ],
    platforms='Unix-like',
    scripts=['xxh','xxhp','xxh.zsh','xxh.xsh'],
    package_data={'xxh_xxh':['*.py', '*.sh', '*.xxhc']},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Unix Shell",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: BSD License"
    ],
    license="BSD",
    author="xxh",
    author_email="author@example.com"
)
