from setuptools import setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="lektor-chameleon",
    version="0.4",
    description="Chameleon support for templating in Lektor.",
    long_description=readme,
    url="http://github.com/uyar/lektor-chameleon",
    author="H. Turgut Uyar",
    author_email="uyar@tekir.org",
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Lektor",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    keywords="lektor chameleon templating",
    py_modules=["lektor_chameleon"],
    install_requires=["chameleon"],
    entry_points={"lektor.plugins": ["chameleon = lektor_chameleon:ChameleonPlugin"]},
)
