
import unicodedata
from datetime import date
import json
import requests
from bs4 import BeautifulSoup
import traceback

class historical_data(object):
    def __init__(self):
        self.base_url = "https://www.investing.com/"
        self.todays_date = (date.today()).strftime("%m/%d/%Y")
        self.start_date =  "07/22/2000"
        self.number_of_required_calls = 0
        self.curr_id = 985854
        self.smlID = 25066198
        self.country = {}
        self.boilerplate_headers = {"Host": "www.investing.com",
                                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
                                    "Accept": "text/plain, */*; q=0.01",
                                    "Accept-Language": "en-US,en;q=0.5",
                                    "Accept-Encoding": "gzip, deflate, br",
                                    "Content-Type": "application/x-www-form-urlencoded",
                                    "X-Requested-With": "XMLHttpRequest",
                                    "Origin" : "https://www.investing.com",
                                    "Connection": "keep-alive"}

    def historical_data_scrapper(self,data,link):
        data = self.unicode_to_text(data)
        soup = BeautifulSoup(data, 'html.parser')
        tables = soup.findAll('table')
        head_rows = tables[0].find('thead').find('tr').findAll('th')
        head_rows = [i.text for i in head_rows]
        ''' ['Date', 'Price', 'Open', 'High', 'Low', 'Vol.', 'Change %'] '''
        ''' ['Feb 27, 2018', '2.85', '2.85', '2.85', '2.85', '1.70K', '3.64%'] '''
        body_rows = tables[0].find('tbody').findAll('tr')

        for j in range(len(body_rows)):
            cells = body_rows[j].findAll("td")
            cell = [i.text for i in cells]
            for k in range(len(cell)):
                #print(head_rows[k] + "\t" +cell[k])
                pass

        #return (None)

    def unicode_to_text(self,data):
        return (unicodedata.normalize('NFKD', data.text).encode('ascii', 'ignore'))

    def get_historical_data (self,link,short_hand):
        url = self.base_url + "instruments/HistoricalDataAjax"
        payload = { "curr_id": str(self.curr_id),
                    "smlID": str(self.smlID),
                    "header": short_hand+"+Historical+Data",
                    "st_date": self.start_date,
                    "end_date": self.todays_date,
                    "interval_sec": "Daily",
                    "sort_col": "date",
                    "sort_ord": "DESC",
                    "action": "historical_data"}
        headers = self.boilerplate_headers
        headers["DNT"] = "1"
        headers["Content-Length"] = "173"
        headers["Referer"] = "https://www.investing.com"+link+"-historical-data"
        headers["Cookie"] = "PHPSESSID=d8gd4j3pg1ejqasrbjcsoaiesu; adBlockerNewUserDomains=1566306981; StickySession=id.23934873569.846_www.investing.com; adbBLk=1; billboardCounter_1=0; G_ENABLED_IDPS=google; r_p_s_n=1; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A4%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22941230%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A24%3A%22%2Fequities%2Fbarclays-kenya%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22941227%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fequities%2Fsafaricom%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A1%3A%221%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A14%3A%22Euro+US+Dollar%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Feur-usd%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228839%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A27%3A%22%2Findices%2Fus-spx-500-futures%22%3B%7D%7D%7D%7D; sideBlockTimeframe=max; geoC=KE; gtmFired=OK; nyxDorf=MDQ3YTFjZScxYDs3MH1hYTJjZCE%2BOzo%2F"

        response = requests.request("POST", url=url, data=payload, headers=headers)
        self.historical_data_scrapper(response,link)
        self.number_of_required_calls += 1

        print (link)

    def get_company_stocks(self,country_ID):
        url =  self.base_url + "stock-screener/Service/SearchStocks"
        #print (self.country[country_ID])
        page = 1
        payload = { "country[]":country_ID,
                    "sector": "7, 5, 12, 3, 8, 9, 1, 6, 2, 4, 10, 11",
                    "industry": "81, 56, 59, 41, 68, 67, 88, 51, 72, 47, 12, 8, 50, 2, 71, 9, 69, 45, 46, 13, 94, 102, 95, 58, 100, 101, 87, 31, 6, 38, 79, 30, 77, 28, 5, 60, 18, 26, 44, 35, 53, 48, 49, 55, 78, 7, 86, 10, 1, 34, 3, 11, 62, 16, 24, 20, 54, 33, 83, 29, 76, 37, 90, 85, 82, 22, 14, 17, 19, 43, 89, 96, 57, 84, 93, 27, 74, 97, 4, 73, 36, 42, 98, 65, 70, 40, 99, 39, 92, 75, 66, 63, 21, 25, 64, 61, 32, 91, 52, 23, 15, 80",
                    "equityType": "ORD, DRC, Preferred, Unit, ClosedEnd, REIT, ELKS, OpenEnd, Right, ParticipationShare, CapitalSecurity, PerpetualCapitalSecurity, GuaranteeCertificate, IGC, Warrant, SeniorNote, Debenture, ETF, ADR, ETC, ETN",
                    "pn": page,
                    "order[col]": "eq_market_cap",
                    "order[dir]": "d" }

        headers = self.boilerplate_headers
        headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
        headers["Content-Length"] = "872"
        headers["Cookie"] = "adBlockerNewUserDomains=1566368914; _ga=GA1.2.743399127.1566368920; G_ENABLED_IDPS=google; __qca=P0-736185115-1566368921663; r_p_s_n=1; _hjid=c815f523-6bae-42ad-9000-8a51de786167; PHPSESSID=35f195d457gnp2kufa50dpri79; StickySession=id.83344366310.465.www.investing.com; cookieConsent=was-set; editionPostpone=1566649424685; _gaexp=GAX1.2.l_phCk-tRQKz79dVNnxpag.18215.1; geoC=KE; _gid=GA1.2.1911750261.1566985341; gtmFired=OK; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A6%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228839%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A27%3A%22%2Findices%2Fus-spx-500-futures%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2237428%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A21%3A%22%2Findices%2Fkenya-nse-20%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2229071%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A26%3A%22%2Findices%2Fftse-nse-kenya-25%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22941227%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fequities%2Fsafaricom%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22941234%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fequities%2Fbamburi%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2242554%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A34%3A%22%2Fequities%2Fkenya-commercial-bank-rw%22%3B%7D%7D%7D%7D; _gat=1; _gat_allSitesTracker=1; nyxDorf=ZGVkNjF5M2cwZmx%2BYTVkYmUqNGgyPA%3D%3D; billboardCounter_1=1"
        headers["Referer"] = self.base_url +"stock-screener/?sp=country::5|sector::a|industry::a|equityType::a%3Ceq_market_cap;1"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = "same-origin"

        while True:
            response = requests.request("POST", url, data=payload, headers=headers)
            try:
                if ((json.loads(response.text)["pageNumber"]) == 1 and page != 1 ):
                    break
                historical_data = self.unicode_to_text(response)
                #print (json.loads(historical_data)["totalCount"])
                for i in range(len(json.loads(historical_data)["hits"])):
                    link = json.loads(response.text)["hits"][i]["viewData"]["link"]
                    #print (link)
                    short_hand = json.loads(response.text)["hits"][i]["viewData"]["symbol"]
                    self.get_historical_data(link=link, short_hand=short_hand)
                    self.curr_id += 1
                    self.smlID  += 1
                #print((json.loads(response.text)["pageNumber"]))
                page += 1
                payload["pn"] = page

            except Exception:
                traceback.print_exc()
                page += 1
                payload["pn"] = page
                #print (page)
                if page > 210 :
                    break

    def search(self):
        url = self.base_url + "search/service/SearchInnerPage"

        payload = {"search_text": "kenya",
                   "tab": "quotes",
                   "isFilter" : "true"
                   }

        headers = self.boilerplate_headers
        headers["Content-Length"] = "173"
        headers["Sec-Fetch-Mode"] = "same-origin"
        headers["Referer"] = "https://www.investing.com/search/?q=kenya"
        headers[
            "Cookie"] = "adBlockerNewUserDomains=1566368914; _ga=GA1.2.743399127.1566368920; G_ENABLED_IDPS=google; __qca=P0-736185115-1566368921663; r_p_s_n=1; _hjid=c815f523-6bae-42ad-9000-8a51de786167; PHPSESSID=35f195d457gnp2kufa50dpri79; geoC=GB; StickySession=id.83344366310.465.www.investing.com; _gid=GA1.2.70643849.1566649388; cookieConsent=was-set; gtmFired=OK; editionPostpone=1566649424685; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A2%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228839%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A27%3A%22%2Findices%2Fus-spx-500-futures%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2237428%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A21%3A%22%2Findices%2Fkenya-nse-20%22%3B%7D%7D%7D%7D; _gaexp=GAX1.2.l_phCk-tRQKz79dVNnxpag.18215.1; nyxDorf=YGEwYmUtYzZjNTwuMGI4Pz5sM3ZkYjIyYmQ%3D; billboardCounter_1=0; _gat=1; _gat_allSitesTracker=1"
        response = requests.request("POST", url, data=payload, headers=headers)
        country_IDs = []
        for i in range(1,(len(json.loads(response.text)["filters"]["country"]))):
            country_ID = (json.loads(response.text)["filters"]["country"][i]["country_ID"])
            self.country[(country_ID)] = (json.loads(response.text)["filters"]["country"][i]["country_name_translated"])
            country_IDs.append(country_ID)
        print(len(country_IDs))
        return({"country_IDs":country_IDs})
