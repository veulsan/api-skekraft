from api import SkekraftAPI
import asyncio
from datetime import datetime, timedelta


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def is_agreement_about_to_end(enddate, warningDays = 30):
    if enddate == '9999-12-31T23:59:59.9999999':
        # If AgreementEnd is set to a future date, return False
        return False
    # Convert AgreementEnd string to datetime object
    agreement_end = datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%S")


    # Get current date
    current_date = datetime.now()
    # Calculate the difference in days between current date and AgreementEnd date
    days_until_end = (agreement_end - current_date).days
    # Check if the agreement is about to end (within the next warningDays (default=30))
    return days_until_end <= warningDays

async def main():
    yesterday = datetime.now() - timedelta(days=2)
    base_url = "https://externalapi.skekraft.se/api/MySkekraft"

    skekraft_api = SkekraftAPI(base_url)

    # Påslag 7.50 öre/kWh
    # Månadsavgift 45 kr/månad Rabatt: -45
    # Elcertifikatsavgift 0.75 öre / kWh

    # Login
    token = "your-token-here"
    login_response = await skekraft_api.login("username", "password")
    if login_response is not None and int(login_response['ErrNumber']) == 1:
        log(f"Login successful. Token: {login_response['Dst']}")
        token = login_response['Dst']
    else:
        log(f"Login Failed: {login_response['ErrDescription']}")
        await skekraft_api.logout()
        exit(-1)

    token = await skekraft_api.refresh(token)
    log(f"token={token}")
    if (token == "False"):
        log(f"Invalid token {token}")
        exit(-1)
    else:
        log(f"Login successful. Token: {token}")

    if token == "true":
        log(f"Login successful. Token: {token}")
        # Get user profile
        user_profile = await skekraft_api.getUserPorfile()
        log(f"Name: {user_profile['Name']} Username: {user_profile['Username']} Email: {user_profile['Email']} Customertype: {user_profile['Customertype']}")
        user = await skekraft_api.getUser()
        log(f"UserId: {user['UserInfo']['UserId']} Username: {user['UserInfo']['Username']} Email: {user['UserInfo']['Email']} Name: {user['UserInfo']['Name']}")
        consumptions = await skekraft_api.getCurrentMonthConsumptions()
        for meterreading in consumptions['MeterReading']:
            log(f"Consumption for {meterreading['Anladress']},{meterreading['Anlpostnr']},{meterreading['Anlort']}: DeliveryCategory: {meterreading['DeliveryCategory']} ReadingDate: {meterreading['ReadingDate']} Consumption: {meterreading['Consumption']}{meterreading['Unit']} ")

        bookings = await skekraft_api.getBookings()
        log(f"Bookings: {bookings}")
        subscription_number = ""
        customerid=""
        subscriptions = await skekraft_api.getSubscriptions()
        for subscription in subscriptions['SubscriptionInfo']:
            invidid = subscription['IndividId']
            netArea = subscription['NetArea']
            customerName = subscription['CustomerName']
            source = subscription['Source']
            utility = subscription['Utility']
            customerId = subscription['CustomerId']
            subscriptionNr = subscription['SubscriptionNr']
            subscriptionAddress = subscription['SubscriptionAddress']
            altNr = subscription['AltNr']
            subscriptiondetails = await skekraft_api.getSubscriptionDetails(subscriptionNr, customerId, source, utility)
            elAreaCode = subscriptiondetails['ElAreaCode']
            zipCode = subscriptiondetails['SubscriptionZipCode']
            city = subscriptiondetails['SubscriptionCity']
            deliveredFrom = subscriptiondetails['DeliveredFrom']
            gs1 = subscriptiondetails['Gs1']
            year1 = subscriptiondetails['YearConsumption1']
            year2 = subscriptiondetails['YearConsumption2']
            isHourMeasured = subscriptiondetails['IsHourMeasured']
            log(
                f"Subscription CustomerName: {customerName} CustomerId: {customerId} SubscriptionNr: {subscriptionNr} Address: {subscriptionAddress} City: {city} ZipCode: {zipCode} DeliveredFrom : {deliveredFrom} NetArea: {netArea} Elområde: {elAreaCode } AltNr: {altNr} Year1: {year1} Year2: {year2} Source: {source} Utility: {utility} ")
            subscription_number = subscriptionNr
            customerid=customerId

        agreements = await skekraft_api.getAgreements(subscription_number,customerid)
        for agreement in agreements['AgreementInfo']:
            produkt = agreement['Produkt']
            agreementId = agreement['AgreementId']
            agreementBegin = agreement['AgreementBegin']
            agreementEnd  = agreement['AgreementEnd']
            description = agreement['Descriptions']
            if (is_agreement_about_to_end(agreementEnd)):
                log(f"Agreement about to end: AgreementId: {agreementId} Description: {description} AgreementEnd: {agreementEnd}")
            article_info = agreement['ArticleInfoItems']['ArticleInfo']
            if isinstance(article_info, list):
                for article in agreement['ArticleInfoItems']['ArticleInfo']:
                    articleName = article['ArticleName']
                    articleUnit = article['ArticleUnit']
                    articleValue = article['ArticleValue']

                    log(f"Produkt: {produkt} AgreementId: {agreementId} AgreementBegin:{agreementBegin} AgreementEnd: {agreementEnd} Description: {description} ArticleName: {articleName} ArticleUnit: {articleUnit} ArticleValue: {articleValue}")
            else:
                articleName = article_info['ArticleName']
                articleUnit = article_info['ArticleUnit']
                articleValue = article_info['ArticleValue']
                log(f"Produkt: {produkt} AgreementId: {agreementId} AgreementBegin:{agreementBegin} AgreementEnd: {agreementEnd} Description: {description} ArticleName: {articleName} ArticleUnit: {articleUnit} ArticleValue: {articleValue}")

        await skekraft_api.refresh()
        subscription_number = "2507435"
        log("Period: " + yesterday.strftime("%Y-%m-%d") + " - " + yesterday.strftime("%Y-%m-%d"))
        meter_values = await skekraft_api.getMeterValues(subscription_number, yesterday.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"),groupBy="Day")
        log(f"Meter values for {subscription_number}: {meter_values}")
        # Pause execution for 1 hour (3600 seconds)
        currentMonth = await skekraft_api.getCurrentMonthConsumptions()
        log(f"currentMonth {currentMonth}")

        await skekraft_api.logout()
        # Get meter values
        # meter_values = await skekraft_api.get_meter_values()
        # print("Meter values:", meter_values)
    else:
        log(f"Login failed")
        await skekraft_api.logout()


# Run the async functions
asyncio.run(main())
