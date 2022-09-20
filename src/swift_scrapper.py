import os
import json
import time
import random
import argparse

from typing import List, Callable, Optional
from pathlib import Path
from functools import partial
from concurrent.futures import ThreadPoolExecutor

import bs4
import requests

base_url = "https://www.theswiftcodes.com"
user_agents = [
    # Windows 10-based PC using Edge browser
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    # Chrome OS-based laptop using Chrome browser (Chromebook)
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    # Mac OS X-based computer using a Safari browser
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    # Windows 7-based PC using a Chrome browser
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    # Linux-based PC using a Firefox browser
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
]


def parse_flags() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_path",
        type=Path,
        required=True,
        help="Where to store JSON-L file containing all scrapped data",
    )
    parser.add_argument(
        "--full_bank_info",
        action="store_true",
        help="Whether to get full bank info fields (address, postcode and connection). "
        "Will perform one more request per bank",
    )
    return parser.parse_args()


# Retrieve headers with randomized user agents
def get_headers() -> dict:
    return {"User-Agent": random.choice(user_agents)}


def wrap_request(max_retries: int) -> Callable:
    def get_url_content(url: str, headers: Optional[dict] = None) -> str:
        print(f"Requesting: {url}")
        content = None
        n_tries = 0
        while n_tries < max_retries and content is None:
            try:
                n_tries += 1
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    content = resp.content

            except Exception:
                print(f"Retrying {url} ({n_tries}/{max_retries}) in 5 seconds")
                time.sleep(5)

        return content

    return get_url_content


# Retrieve the list of all countries
def get_country_list(
    requester: Callable, url: str, headers: Optional[dict] = None
) -> dict:
    soup = bs4.BeautifulSoup(requester(url, headers), features="lxml")
    # list of lists of countries
    countries_raw = soup.find(class_="letters-ranges").find_all("ol")
    # flatten list of countries
    countries_href = [item for elem in countries_raw for item in elem.find_all("a")]
    # country data
    data = [{"href": elem["href"], "country": elem.text} for elem in countries_href]
    return data


# Retrieve the list of all banks in a country
def get_country_banks(
    requester: Callable,
    url: str,
    headers: Optional[dict] = None,
    full_bank_info: bool = True,
) -> List[dict]:
    data = []
    soup = bs4.BeautifulSoup(requester(url, headers), features="lxml")
    bank_table = soup.find(class_="swift-country")
    validate_fields = ["table-name", "table-city", "table-branch", "table-swift"]
    for bank_elem in bank_table.tbody.find_all("tr"):
        must = [bank_elem.find(class_=key) for key in validate_fields]
        if any([elem is None for elem in must]):
            continue

        swift_data = bank_elem.find(class_="table-swift").find("a")
        bank_data = {
            "name": bank_elem.find(class_="table-name").text,
            "city": bank_elem.find(class_="table-city").text,
            "branch": bank_elem.find(class_="table-branch").text,
            "swift": swift_data.text,
        }

        if full_bank_info:
            info_url = f"{base_url}/{swift_data['href']}"
            detail = get_full_swift_info(requester, info_url, headers=headers)
            bank_data.update(detail)

        data.append(bank_data)

    return data


# Retrieve extra bank information: address, postcode, connection
def get_full_swift_info(
    requester: Callable, url: str, headers: Optional[dict] = None
) -> dict:
    data = {}
    target_fields = ["address", "connection", "postcode"]
    soup = bs4.BeautifulSoup(requester(url, headers), features="lxml")
    swift_table = soup.find(class_="swift-detail")
    for swift_item in swift_table.tbody.find_all("tr"):
        key_val = swift_item.text.strip().split("\n")
        if len(key_val) == 0:
            continue

        key = key_val[0].lower()
        val = key_val[1] if len(key_val) > 1 else ""
        data[key] = val

    return {key: data.get(key, "") for key in target_fields}


def get_country_data(
    item: dict, requester: Callable, full_bank_info: bool
) -> List[dict]:
    data = []
    banks_url = f"{base_url}/{item['href']}"
    print(f"Getting data for {item['country']} from: {banks_url}")
    registry = {"country": item["country"]}
    for bank in get_country_banks(
        requester,
        banks_url,
        headers=get_headers(),
        full_bank_info=full_bank_info,
    ):
        bank.update(registry)
        data.append(bank)

    return data


def main(output_path: Path, full_bank_info: bool):
    data = []
    countries_url = f"{base_url}/browse-by-country/"
    print(f"Getting list of countries from: {countries_url}")
    requester = wrap_request(max_retries=5)
    countries_data = get_country_list(requester, countries_url, headers=get_headers())
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        getter = partial(
            get_country_data, requester=requester, full_bank_info=full_bank_info
        )
        for country_banks in executor.map(getter, countries_data):
            data.extend(country_banks)

        data = sorted(data, key=lambda registry: registry["country"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as fout:
            fout.write("\n".join(map(json.dumps, data)) + "\n")

        print(f"Written {len(data)} registries to {output_path}")


if __name__ == "__main__":
    main(**vars(parse_flags()))
