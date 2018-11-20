from setuptools import setup


setup(
    name="lektor-chameleon",
    description="Chameleon support for templating.",
    version="0.1",
    author="H. Turgut Uyar",
    author_email="uyar@tekir.org",
    url="http://github.com/uyar/lektor-chameleon",
    license="LGPL",
    install_requires=["chameleon"],
    py_modules=["lektor_chameleon"],
    entry_points={"lektor.plugins": ["chameleon = lektor_chameleon:ChameleonPlugin"]},
)
