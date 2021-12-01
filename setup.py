from setuptools import setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.txt") as changelog_file:
    changelog = changelog_file.read()

setup(
    name="lektor-chameleon",
    version="0.6.1",
    description="Chameleon support for templating in Lektor.",
    long_description=readme + "\n\n" + changelog,
    url="https://github.com/uyar/lektor-chameleon",
    author="H. Turgut Uyar",
    author_email="uyar@tekir.org",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Lektor",
        "License :: OSI Approved :: BSD License",
    ],
    keywords="lektor plugin static-site blog chameleon templating",
    py_modules=["lektor_chameleon"],
    install_requires=["chameleon"],
    entry_points={
        "lektor.plugins": ["chameleon = lektor_chameleon:ChameleonPlugin"]
    },
)
