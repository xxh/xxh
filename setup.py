import setuptools
from xonssh_xxh.settings import global_settings

setuptools.setup(
    name="xonssh-xxh", # Replace with your own username
    version=global_settings['XXH_VERSION'],
    description="xxh is for using portable xonsh shell wherever you go through the ssh",
    url="https://github.com/xonssh/xxh",
    python_requires='>=3.6',
    install_requires=['xonsh'],
    platforms='Unix-like',
    scripts=['xxh'],
    package_data={'xonssh_xxh':['*.xsh', '*.sh']},
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
    license="BSD",
    author="xonssh",
    author_email="author@example.com"
)