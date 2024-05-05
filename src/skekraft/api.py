from HttpClient import HttpClient
from datetime import datetime, timedelta

from skekraft.const import (
    CMD_LOGIN,
    CMD_REFRESH,
    CMD_LOGOUT,
    CMD_PROFILE,
    CMD_SERVICES,
    CMD_SUBSCRIPTIONS,
    CMD_SUBSCRIPTION_DETAILS,
    CMD_MESSAGE,
    CMD_AGREEMENTS,
    CMD_ADDONS,
    CMD_OFFERS,
    CMD_CONSUMPTION,
    CMD_CURRENT,
    CMD_METERVALUES,
    CMD_BOOKINGS,
    CMD_USERS,
    USER_AGENT_TEMPLATE,
    CLIENT_HEADERS,
)

class SkekraftAPI:
    def __init__(self, base_url, ssl=True):
        self.httpclient = HttpClient(base_url)
        self.base_url = base_url
        self.useSl = False

    async def logout(self):
        await self.httpclient.logout()
        return None
    async def login(self, username, password):
        return await self.httpclient.login(username, password)
    async def refresh(self, token=None):
        return await self.httpclient.refresh(token)
    async def getUserPorfile(self):
        return await self.httpclient.run_command(CMD_PROFILE)
    async def getConsumptionsHistory(self):
        return await self.httpclient.run_command(CMD_CONSUMPTION)
    async def getOffers(self):
        return await self.httpclient.run_command(CMD_OFFERS)
    async def getUserMessage(self):
        return await self.httpclient.run_command(CMD_MESSAGE)

    async def getUser(self):
        return await self.httpclient.run_command(CMD_USERS)

    async def getSubscriptions(self, CustomerId="", source="All", utility="All"):
        payload = {
            'customerId': CustomerId,
            'source': source,
            'utility': utility,
        }
        return await self.httpclient.run_command(CMD_SUBSCRIPTIONS, payload=payload)
    async def getSubscriptionDetails(self, subscriptionNr, customerId, source="XLN", utility="EL_EXT"):
        payload = {
            'customerId': customerId,
            'subscriptionsNr': subscriptionNr,
            'source': source,
            'utility': utility,
        }
        return await self.httpclient.run_command(CMD_SUBSCRIPTION_DETAILS, payload=payload)
    async def getSubscriptions(self, customerId="", source="All", utility="All"):
        payload = {
            'customerId': customerId,
            'source': source,
            'utility': utility,
        }
        return await self.httpclient.run_command(CMD_SUBSCRIPTIONS, payload=payload)

    async def getAgreements(self, subscriptionNr,customerId, source="XLN", utility="EL_EXT"):
        payload = {
            'subscriptionsNr': subscriptionNr,
            'customerId': customerId,
            'source': source,
            'utility': utility,
        }
        return await self.httpclient.run_command(CMD_AGREEMENTS, payload=payload)

    async def getBookings(self,):
        # Get current date
        current_date = datetime.now()
        # Add one year to current date
        one_year_later = current_date + timedelta(days=365)

        payload = {
            "source": "All",
            "FromDate": current_date.strftime("%Y-%m-%d"),
            'toDate':  one_year_later.strftime("%Y-%m-%d"),
            'Utility': "All",
        }
        return await self.httpclient.run_command(CMD_BOOKINGS, payload=payload)

    async def getCustomerIifo(self, sourcerecordid):
        payload = {
            'sourcerecordid': sourcerecordid,

        }
        return await self.httpclient.run_command(CMD_CUSTOMERINFO, payload=payload)

    async def getMeterValues(self,subscriptionNr,startdate, enddate, delay=1,groupBy="Hour",unit="kWh",Source="XLN",Utility="EL_EXT"):
        # Valid groupBy: Hour, Day, Month, Year
        payload = {
            "source": Source,
            "utility": Utility,
            'subscriptionNr': subscriptionNr,
            'startdate': startdate,
            'enddate': enddate,
            'sortorder': 'ASC',
            'unit': unit,
            'delay': delay,
            'groupBy': groupBy,
        }
        return await self.httpclient.run_command(CMD_METERVALUES, payload=payload)

    async def getCurrentMonthConsumptions(self, customerId=759194):
        payload = {
            "customerId": customerId,
        }
        return await self.httpclient.run_command(CMD_CURRENT, payload=payload)

    async def getOutputServices(self, customerId=759194):
        payload = {
            "outputServiceId": "-1",
            "outputServiceTypeId": "2",
            'categoryId': "-1",
        }
        return await self.httpclient.run_command(CMD_SERVICES, payload=payload)
