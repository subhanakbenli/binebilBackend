import requests
from bs4 import BeautifulSoup

USERNAME = "ogrenci_no"
PASSWORD = "sifre"

LOGIN_URL = "https://yks.iyte.edu.tr/Login.aspx"
DASHBOARD_URL = "https://yks.iyte.edu.tr/Default.aspx"

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Referer": LOGIN_URL,
    "Origin": "https://yks.iyte.edu.tr",
}

# Giriş sayfasını al ve form verilerini çek
response = session.get(LOGIN_URL, headers=headers)
print(response.text)
soup = BeautifulSoup(response.text, "html.parser")

viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]

payload = {
    "__VIEWSTATE": viewstate,
    "__EVENTVALIDATION": eventvalidation,
    "txtUserName": USERNAME,
    "txtPassword": PASSWORD,
    "btnLogin": "Giriş"
}

# Giriş yap
login_response = session.post(LOGIN_URL, data=payload, headers=headers)

if "Default.aspx" in login_response.url:
    print("Başarıyla giriş yapıldı!")
    dashboard_response = session.get(DASHBOARD_URL, headers=headers)
    print(dashboard_response.text[:500])
else:
    print("Giriş başarısız!")
