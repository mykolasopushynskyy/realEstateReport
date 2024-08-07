"""
This module contains application configuration class and various additional util methods. It reads properties from
config file and merges it with some commandline configs which have bigger priority.
"""

import configparser
import os
import argparse
from datetime import datetime

SOURCE = "source"
SOURCE_URL = "url"
CITIES = "cities"
START_YEAR = "start_year"
REPORT = "report"
HIDE_DISTRICTS = "hide_districts"
DESTINATION_FOLDER = "destination_folder"
INFLATION_ADJUSTMENT_YEAR = "inflation_adjustment_year"

PROJECT_DIR = os.path.dirname(__file__)

DATE_FIELD = "Date"
CSV_DATE_FORMAT = "%Y-%m-%d"
HTML_PARSER = "html.parser"


def obfuscate_path(file_path: str):
    """
    Obfuscates the absolute path of project directory

    :param file_path: file path to obfuscate project absolute path
    :return:
    """
    return file_path.replace(PROJECT_DIR, "<project_path>")


def is_true_config(value: str):
    """
    Check if the string configs value is true

    :param value: value to check
    :rtype: bool
    """
    return (not (value is None) and
            "true".casefold() == value.casefold() or
            "yes".casefold() == value.casefold() or
            "y".casefold() == value.casefold())


def empty_or_else(value, or_else):
    """
    Return property value. If it is not present return or_else property

    :param value: value to return
    :param or_else: another value to return
    :return:
    """
    if value is None:
        return or_else
    if isinstance(value, list) and len(value) == 0:
        return or_else
    return value


class AppConfigs:
    """
    A class used to read project properties. Reads properties from config file and merges it with commandline
    properties.
    """

    def __init__(self, cl_args: argparse.Namespace):
        """
        Init method of :class:`AppConfigs` class. Reads config file and initializes config parser

        :param cl_args: command-line arguments
        """
        configfile = os.path.abspath(os.path.join(PROJECT_DIR, 'resources', 'properties.ini'))

        self.cl_args = cl_args
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

    def get_source_url(self):
        """
        Get the real estate source url

        :return: real estate source url
        :rtype: str
        """

        return self.config.get(SOURCE, SOURCE_URL)

    def get_cities_mappings(self):
        """
        Get the real estate available cities

        :return: mapping between cities and retriever url city id
        :rtype: dict
        """
        cities = {}
        for city in self.config.options(CITIES):
            cities[city] = self.config.get(CITIES, city)

        return cities

    def get_cities(self):
        """
        Get the real estate cities to generate report for

        :return: mapping between cities and retriever url city id
        :rtype: dict
        """
        return empty_or_else([city.lower() for city in self.cl_args.cities],
                             [city for city in self.config.options(CITIES)])

    def get_start_year(self):
        """
        Get the reports start year

        :return: start year of report generation
        :rtype: int
        """

        return int(self.config.get(SOURCE, START_YEAR))

    def get_inflation_adjustment_year(self):
        """Get the year for inflation adjustment
        :rtype: int
        """

        return int(self.config.get(SOURCE, INFLATION_ADJUSTMENT_YEAR))

    def hide_districts(self):
        """
        Hide city districts on final diagram

        :return: config to show/hide districts on final diagram
        :rtype: bool
        """

        return is_true_config(empty_or_else(self.cl_args.hide_districts,
                                            self.config.get(REPORT, HIDE_DISTRICTS)))

    def get_report_destination_folder(self):
        """
        Get the reports folder

        :return: absolute path reports folder
        :rtype: str
        """

        return os.path.join(os.path.dirname(__file__), self.config.get(REPORT, DESTINATION_FOLDER))

    @staticmethod
    def get_current_year():
        """Return current year for reports. Made as separate method for test simplification."""
        return datetime.now().year

    @staticmethod
    def get_current_month():
        """Return current month for reports. Made as separate method for test simplification."""
        return datetime.now().month
