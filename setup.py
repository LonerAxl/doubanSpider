# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'doubanspider',
    version      = '1.0',
    packages     = find_packages(),
    package_data={
        'doubanspider': ['resourses/*.txt']
    },
    entry_points = {'scrapy': ['settings = doubanspider.settings']},
    zip_safe=False,
    include_package_data=True,
)
