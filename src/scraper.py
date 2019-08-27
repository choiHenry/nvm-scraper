import pandas as pd


class Scraper:

    def __init__(self):
        self.reviewList = []
        self.scoreList = []
        self.pcodelist = []

    def getPCodeList(self, page):
        import requests
        from bs4 import BeautifulSoup

        for i in range(1, page+1):

            params = {
                "origQuery": "음성인식%20-삼성전자%20-LG전자%20-소니%20-애플%20-대우",
                "pagingIndex": i,
                "pagingSize": 80,
                "viewType": "list",
                "sort": "rel",
                "frm": "NVSHCAT",
                "cat_id": "50002322",
                "query": "음성인식",
                "xq": "삼성전자%20-LG전자%20-소니%20-애플%20-대우"
            }
            url = "https://search.shopping.naver.com/search/all.nhn"
            res = requests.post(url, data=params)
            soup = BeautifulSoup(res.text, "html.parser")
            product_info = soup.findAll("li", attrs={"class": "_itemSection"})
            for j in range(len(product_info)):
                self.pcodelist.append(product_info[j]['data-nv-mid'])

    def getRVList(self):
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd

        pclist = []
        rvlist = []
        starlist = []
        datelist = []

        for p in self.pcodelist:

            url = "https://search.shopping.naver.com/detail/detail.nhn"
            params = {
                "nvMid": p,
                "reviewSort": "registration",
                "reviewType": "all",
                "ligh": "true"
            }
            url = "https://search.shopping.naver.com/detail/detail.nhn?nv_mid={}".format(params["nvMid"])
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            a = soup.findAll("a", attrs={"data-tab-name": "review"})
            try:
                review_num = a[0].findAll("em")[0].get_text().strip()
            except:
                continue
            page_num = (locale.atoi(review_num)//20) + 1
            rvurl = "https://search.shopping.naver.com/detail/review_list.nhn"
            for i in range(1, page_num+1):
                params["page"] = i
                res = requests.post(rvurl, data=params)
                soup = BeautifulSoup(res.text, "html.parser")
                ul = soup.findAll("ul", attrs={"id": "_review_list"})
                try:
                    atc_areas = ul[0].findAll("div", attrs={"class": "atc_area"})
                except:
                    continue
                for i in range(len(atc_areas)):
                    atc = atc_areas[i].findAll("div", attrs={"class":"atc"})
                    review = atc[0].get_text().strip()
                    rvlist.append(review)
                    avg_area = atc_areas[i].findAll("div", attrs={"class":"avg_area"})
                    date = avg_area[0].findAll("span", attrs={"class":"info_cell"})[2].text.strip()
                    datelist.append(date)
                    curr_avg = avg_area[0].findAll("span", attrs={"class":"curr_avg"})
                    star = curr_avg[0].findAll("strong")[0].get_text().strip()
                    starlist.append(star)
                    pclist.append(p)
            print(len(pclist), len(rvlist), len(starlist), len(datelist))

        data = pd.DataFrame(list(zip(pclist, rvlist, datelist, starlist)))
        data.to_csv("naver-review.csv")

        return data


