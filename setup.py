from setuptools import setup, find_packages

setup(
    name='Real estate parser',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'start=application.application:main',
        ]
    },
    install_requires=[
        "webcolors~=24.6.0",
        "setuptools~=65.5.1",
        "requests~=2.32.3",
        "pandas~=2.2.2",
        "beautifulsoup4~=4.4.1",
        "plotly~=5.22.0",
        "packaging~=24.1",
        "progressbar~=2.5",
        "typing_extensions~=4.12.2",
        "cpi~=1.1.6",
        "click~=8.1.7",
        "python-dateutil~=2.9.0.post0",
        "pip~=23.3.2",
        "pytz~=2024.1",
        "numpy~=1.26.4",
        "certifi~=2024.6.2",
        "urllib3~=2.2.1",
        "six~=1.16.0",
        "idna~=3.7"
    ]
)