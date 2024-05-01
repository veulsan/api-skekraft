# Commands
#cmd=login
CMD_LOGIN="Login"
#cmd=login
#Not implemented ??
CMD_LOGOUT="Logout"
# RefreshDST refreshes DST
CMD_REFRESH="RefreshDST"
# GetUserProfile
CMD_PROFILE="GetUserProfile"
# GetSubscriptions
CMD_SUBSCRIPTIONS="GetSubscriptions"
# GetSubscriptionDetails
CMD_SUBSCRIPTION_DETAILS="GetSubscriptionDetails"
# GetOutputServices
CMD_SERVICES="GetOutputServices"
# GetAddOnProducts
CMD_ADDONS="GetAddOnProducts"
# GetAgreements
CMD_AGREEMENTS="GetAgreements"
# GetBookings
CMD_BOOKINGS="GetBookings"
# GetConsumptionsHistory
CMD_CONSUMPTION="GetConsumptionsHistory"
# GetCurrentMonthConsumptions
CMD_CURRENT="GetCurrentMonthConsumptions"
# GetExtCustomerInfo
CMD_CUSTOMERINFO="GetExtCustomerInfo"
# GetIndividUsers
CMD_USERS="GetIndividUsers"
# GetMeterValues
CMD_METERVALUES="GetMeterValues"
# GetOffers
CMD_OFFERS="GetOffers"
# GetUserMessage
CMD_MESSAGE="GetUserMessage"
# PreCacheAllInvoicesWithPageing
CMD_CACHE="PreCacheAllInvoicesWithPageing"
# GetHanStatus
CMD_HANSTATUS="GetHanStatus"

USER_AGENT_TEMPLATE = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/85.0.{BUILD}.{REV} Safari/537.36"
)
CLIENT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}
