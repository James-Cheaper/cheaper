from setuptools import setup, find_packages

setup(
    name='cheaper',
    version='0.1',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "flask",
        "pandas",
        "numpy",
        "requests",
        "gunicorn",
    ],
    entry_points={
        'console_scripts': [
            'cheaper=webscraper.main:main',
        ],
    },
    
    description='cheaper for now',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
