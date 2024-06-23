import csv
import os
import cpi

from datetime import datetime
from app.consts import DATE_FIELD
from app.parsed_report import ParsedReport
from appconfigs import AppConfigs


class RealEstateCSVReporter:
    """A class used to generate reports."""

    def __init__(self, appconfig: AppConfigs):
        self.appconfig = appconfig
        self.inflate_to = datetime(self.appconfig.get_inflation_adjustment_year(), 1, 1)

    def generate_report(self, city: str, report_data: ParsedReport):
        """A method used to generate real estate report."""
        fields = []
        for field in report_data.records.keys():
            fields.append(field)
            if field != DATE_FIELD:
                fields.append(field + " інфл.")

        report_file = os.path.abspath(os.path.join(self.appconfig.get_report_destination_folder(),
                                                   city + "-" + datetime.now().strftime('%d-%m-%Y') + ".csv"))

        with open(report_file, 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            for i in range(0, len(report_data.records[DATE_FIELD])):
                row = {}

                for district in report_data.records.keys():
                    try:
                        row[district] = report_data.records[district][i]
                        if district != DATE_FIELD:
                            district_adj = district + " інфл."
                            value_adj = cpi.inflate(report_data.records[district][i],
                                                    datetime.strptime(row[DATE_FIELD], "%Y-%m-%d"),
                                                    to=self.inflate_to)
                            row[district_adj] = round(value_adj)
                    except TypeError:
                        print("Parsing error: " + __file__)
                    except IndexError:
                        print("Parsing error: " + __file__)

                writer.writerow(row)
                csvfile.flush()

        return report_file
