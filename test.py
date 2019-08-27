import requests
from bs4 import BeautifulSoup

rvlist = []
starlist = []
datelist = []
url = "https://search.shopping.naver.com/detail/detail.nhn"
params = {
    "nvMid": "11228382728",
    "reviewSort": "registration",
    "reviewType": "all",
    "ligh": "true"
}
url = "https://search.shopping.naver.com/detail/detail.nhn?nv_mid={}".format(params["nvMid"])
res = requests.get(url)
print(res)
soup = BeautifulSoup(res.text, "html.parser")
print(soup)
a = soup.findAll("a", attrs={"data-tab-name": "review"})
review_num = a[0].findAll("em")[0].get_text().strip()
page_num = (int(review_num) // 20) + 1
print(page_num)
rvurl = "https://search.shopping.naver.com/detail/review_list.nhn"
for i in range(1, page_num + 1):
    params["page"] = i
    res = requests.post(rvurl, data=params)
    soup = BeautifulSoup(res.text, "html.parser")
    ul = soup.findAll("ul", attrs={"id": "_review_list"})
    atc_areas = ul[0].findAll("div", attrs={"class": "atc_area"})
    for j in range(len(atc_areas)):
        atc = atc_areas[j].findAll("div", attrs={"class": "atc"})
        review = atc[0].get_text().strip()
        rvlist.append(review)
        avg_area = atc_areas[j].findAll("div", attrs={"class": "avg_area"})
        date = avg_area[0].findAll("span", attrs={"class": "info_cell"})[2].text.strip()
        datelist.append(date)
        curr_avg = avg_area[0].findAll("span", attrs={"class": "curr_avg"})
        star = curr_avg[0].findAll("strong")[0].get_text().strip()
        starlist.append(star)

print(len(rvlist))
print(len(starlist))
print(len(datelist))