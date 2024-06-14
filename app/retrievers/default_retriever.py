import requests

from appconfigs import AppConfigs


class RealEstateRawInfoRetriever:
    """A class used to make calls to real estate source."""

    REGION = "0"

    def __init__(self, appconfig: AppConfigs):
        self.appconfigs = appconfig

    def retrieve(self, city: str, year: int, month: int):
        """A class used to make calls to real estate source."""
        url = "http://www.svdevelopment.com/ua/web/flat_costs/"

        date = "%s-%02d-01" % (year, month)

        city_reg = self.appconfigs.get_cities()[city]

        payload = (
                "st%5Bact%5D=stat&st%5Boblast%5D=" + city_reg + (
                "&st%5Bregion%5D=" + RealEstateRawInfoRetriever.REGION +
                ("&st%5Bdate1%5D=" + date + ("&st%5Bdate2%5D=" + date))))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text


if __name__ == '__main__':
    """Main method of application"""
    appconfig = AppConfigs()
    retriever = RealEstateRawInfoRetriever(appconfig)

    retriever.retrieve('львів', 2024, 5)
