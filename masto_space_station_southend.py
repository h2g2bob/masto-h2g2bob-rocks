# pylint: disable=line-too-long,missing-module-docstring,missing-function-docstring,invalid-name
import datetime
import re
from os import environ

import requests
from mastodon import Mastodon

LOCATE="51.55,0.71"

ISS_LOC="United_Kingdom_England_Canvey_Island"
ISS_URL="https://spotthestation.nasa.gov/sightings/view.cfm?country=United_Kingdom&region=England&city=Canvey_Island"

def weather_api_key():
    with open("weatherapi.com.secret", "r", encoding="ascii") as secretf:
        return secretf.read().strip()

def weather(iso_date: str, hour: int):
    resp = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key()}&q={LOCATE}&dt={iso_date}&hour={hour}",
        timeout=60.0,
    )
    return resp.json()

def cloud_is_ok(iso_date: str, hour: int):
    data = weather(iso_date, hour)
    cloud = data["forecast"]["forecastday"][0]["hour"][0]["cloud"]
    log(f"cloud={cloud!r}")
    return cloud <= 40

def iss_rss(iso_date: str):
    resp = requests.get(
        f"https://spotthestation.nasa.gov/sightings/xml_files.cfm?filename={ISS_LOC}.xml",
        timeout=60.0,
    )
    for block in re.compile(r"<item>(.*?)</item>", re.DOTALL).findall(resp.text):
        m = re.compile(r"<title>(.*?)</title>").search(block)
        assert m, block
        title = m.group(1)
        if iso_date in title:
            m = re.compile(r"Duration: (\d+) minutes").search(block)
            assert m, block
            if int(m.group(1)) >= 4:
                m = re.compile(r"<description>(.*?)</description>", re.DOTALL).search(block)
                assert m, block
                describe = m.group(1)
                if " PM" in describe:
                    return "\n".join(
                        line.strip()
                        for line in describe.split("&lt;br/&gt;")
                    ).replace("&#176;", "°")
    return None

def toot(msg):
    mastodon = Mastodon(access_token="spacestationsouthend_mastodon_me_uk_login_cred.secret")
    mastodon.toot(msg)

def log(msg):
    if environ.get("LOGLOG", ""):
        print(msg)

def main():
    iso_date = datetime.date.today().isoformat()
    iss_description = iss_rss(iso_date)
    log(f"describe={iss_description!r}")
    if iss_description:
        if cloud_is_ok(iso_date, 20):
            msg = f"You can see the #InternationalSpaceStation in #Southend tonight\n{iss_description}\n{ISS_URL}"
            if environ.get("TOOT", ""):
                toot(msg)
            else:
                print("Would toot: {msg}")


if __name__ == "__main__":
    main()
