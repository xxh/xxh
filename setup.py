import setuptools
from xonssh_xxh.settings import global_settings

setuptools.setup(
    name="xonssh-xxh",
    version=global_settings['XXH_VERSION'],
    description="xxh is for using portable xonsh shell wherever you go through the ssh",
    url="https://github.com/xonssh/xxh",
    project_urls={
        "Documentation": "https://github.com/xonssh/xxh/blob/master/README.md",
        "Code": "https://github.com/xonssh/xxh",
        "Issue tracker": "https://github.com/xonssh/xxh/issues",
    },
    python_requires='>=3.6',
    install_requires=[
        'xonsh >= 0.9.13'
    ],
    platforms='Unix-like',
    scripts=['xxh'],
    package_data={'xonssh_xxh':['*.xsh', '*.sh']},
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
    author="xonssh",
    author_email="author@example.com"
)