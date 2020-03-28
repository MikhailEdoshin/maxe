from setuptools import setup

setup(
    name="maxe",
    version="0.1.8",
    description="Extensible XSLT processor",
    license="MIT",
    packages=["maxe", "maxe.ext", "maxe.ext.read"],
    package_data = {
      "": ["xslt/*.xslt"]
    },
    include_package_data=True,
    author="Mikhail Edoshin",
    author_email="mikhail@onegasoft.com",
    entry_points={"console_scripts": ["maxe = maxe.__main__:RunFromCli"]},
    install_requires=[
        "python-dateutil>=2.8.0",
        "docutils>=0.15.2",
        "lxml>=4.4.1"
    ]
)
