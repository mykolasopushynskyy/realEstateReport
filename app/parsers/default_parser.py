import collections

collections.Callable = collections.abc.Callable
from bs4 import BeautifulSoup
from app.parsers.parsed_report import ParsedReport

HTML_PARSER = "html.parser"


class RealEstateRawInfoParser:
    """A class used to make calls to real estate source."""

    def __init__(self):
        pass

    def parse(self, html: str):
        """A class used to make calls to real estate source."""
        result = ParsedReport()
        soup = BeautifulSoup(html, HTML_PARSER)

        # Retrieve table data
        prices_table = (soup.find_all("table", class_="tHH")[0]
                        .find_all_next("tr", class_="vals"))
        date = (soup.find_all("table", class_="tHH")[0]
                        .find_all_next("tr", class_="headHH2")[0]
                .find_all_next("td")[1]).text

        # Form a finalized report
        for data in prices_table:
            string_data = data.text.strip().split("\n")
            if len(string_data) == 2 and string_data[1] != "-":
                print(string_data[0], date, string_data[1].strip("$"))
                result.append(string_data[0], date, string_data[1].strip("$"))

        return result
