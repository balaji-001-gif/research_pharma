from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="pharma_rd",
    version="0.0.1",
    description="Research and Pharma Development Application for Frappe v15+",
    author="Your Company",
    author_email="admin@yourcompany.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "frappe_app": "pharma_rd=pharma_rd:get_version",
    },
)
