import feedgenerator
import requests
from bs4 import BeautifulSoup

def get_latest_scp_number():
    try:
        url = "https://scp-wiki.wikidot.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        newest_pages = soup.select_one(".new-pages-list")
        if newest_pages:
            latest_scp_link = newest_pages.select_one("a[href^='/scp-']")
            parts = latest_scp_link["href"].split("-")
            if len(parts) >= 3:
                latest_scp_num = int(parts[2])
                return latest_scp_num
    except Exception as e:
        print(f"Error fetching latest SCP number: {e}")
    return 8999

seasons = [
    (1, 0, 999),
    (2, 1000, 1999),
    (3, 2000, 2999),
    (4, 3000, 3999),
    (5, 4000, 4999),
    (6, 5000, 5999),
    (7, 6000, 6999),
    (8, 7000, 7999),
    (9, 8000, 8999),
]

def get_title_from_file(scp_num, season_num):
    filename = f"titles/season{season_num}.txt"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(f"SCP-{scp_num:03d} - "):
                return line.strip().replace(f"SCP-{scp_num:03d} - ", "")
    return None

def generate_feed_for_range(season_num, start, end, latest_scp):
    current_start = start
    while current_start <= end:
        current_end = min(current_start + 99, end)
        feed = feedgenerator.Rss201rev2Feed(
            title=f"SCP Season {season_num} ({current_start:04d}-{current_end:04d})",
            link="https://scp-wiki.wikidot.com",
            description=f"RSS feed for SCPs {current_start:04d} to {current_end:04d}"
        )

        for scp_num in range(current_start, current_end + 1):
            if scp_num > latest_scp:
                continue
            url = f"https://scp-wiki.wikidot.com/scp-{scp_num:03d}"
            title = get_title_from_file(scp_num, season_num)
            if title is None:
                title = f"SCP-{scp_num:03d}"
            feed.add_item(
                title=title,
                link=url,
                description=f"Updates for {url}"
            )

        filename = f"scp_s{season_num}_{current_start:03d}-{current_end:03d}.xml"
        with open(filename, "w", encoding="utf-8") as f:
            feed.write(f, "utf-8")
        print(f"Saved {filename}")
        current_start = current_end + 1

def main():
    latest_scp = get_latest_scp_number()
    print(f"Latest SCP number: {latest_scp}")

    for season_num, start, end in seasons:
        generate_feed_for_range(season_num, start, end, latest_scp)

if __name__ == "__main__":
    main()