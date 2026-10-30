from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

from employee_hub import __version__ as version

setup(
    name="employee_hub",
    version=version,
    description="Employee Hub System - Comprehensive HR & Leave Management Frappe App",
    author="Sanskar Trainee",
    author_email="trainee@sanskar.io",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
