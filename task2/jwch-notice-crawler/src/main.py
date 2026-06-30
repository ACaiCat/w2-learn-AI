import json
import re

from concurrent.futures import ThreadPoolExecutor
from datetime import date
from typing import Optional, Any
import httpx
import pandas
from bs4 import BeautifulSoup, Tag, ResultSet
from attach import Attach
from constants import BASE_URL, HEADERS
from notice import Notice
from notice_group import NoticeGroup
from pathlib import Path

import os


client: httpx.Client = httpx.Client(base_url=BASE_URL, headers=HEADERS)


def get_download_times(wbnewsid: str, owner: str) -> int:
    parms: dict[str, Any] = {
        "wbnewsid": wbnewsid,
        "owner": owner,
        "type": "wbnewsfile",
        "randomid": "nattach",
    }

    response_json: httpx.Response = client.get(
        "system/resource/code/news/click/clicktimes.jsp", params=parms, timeout=10
    ).json()

    return response_json["wbshowtimes"]  # type: ignore


def get_notice(notice: Notice) -> None:
    print(f"Get: {notice.path}")

    response: httpx.Response = client.get(notice.path, timeout=10)
    notice_soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    notice.body = notice_soup.find("div", class_="v_news_content")  # type: ignore
    attach_ul_tag: Optional[Tag] = notice_soup.find("ul", style="list-style-type:none;")  # type: ignore

    if attach_ul_tag is not None:
        for attach_tag in attach_ul_tag:
            link_tag: Tag = attach_tag.find_next("a")  # type: ignore

            name: str = link_tag.get_text()

            if name == "加入收藏" or not name:
                continue

            path: str = link_tag.get("href")  # type: ignore

            download_time_tag: Tag = attach_tag.find_next("script")  # type: ignore

            download_time_parms: list[str] = (
                download_time_tag.get_text()
                .replace("getClickTimes(", "")
                .replace(',"wbnewsfile","attach")', "")
                .split(",")
            )

            download_times: int = get_download_times(*download_time_parms)
            notice.attaches.append(
                Attach(name=name, path=path, download_times=download_times)
            )
        notice.attaches = list(
            {attach.name: attach for attach in notice.attaches}.values()
        )


def get_notice_list(notices: list[Notice], path: str) -> None:
    response: httpx.Response = client.get(path)

    jxtz_soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    jxtz_tags: ResultSet[Tag] = jxtz_soup.find("ul", class_="list-gl").find_all("li")  # type: ignore

    for tag in jxtz_tags:
        title = tag.find("a").get("title")  # type: ignore
        assert title is not None
        # “ 是为了匹配标题
        keywords = ["转专业", "“嘉锡化学", "“数智", "“数理综合", "“数理金融"]

        if not any(keyword in title for keyword in keywords):
            continue
        notices.append(
            Notice(
                author=re.search(r"【(.*)】", tag.get_text()).group(1),  # type: ignore
                title=tag.find("a").get("title"),  # type: ignore
                date=date.fromisoformat(tag.find("span").text.strip()),  # type: ignore
                path=tag.find("a").get("href").replace("../", ""),  # type: ignore
                body="",
                attaches=[],
            )
        )


def export_notices_csv(notices: list[Notice], filename: str):
    detailed_data = []
    for notice in notices:
        row = {
            "title": notice.title,
            "author": notice.author,
            "date": notice.date.isoformat(),
            "url": notice.url,
            "body": notice.body,
            "attaches": json.dumps(
                [attach.to_dict() for attach in notice.attaches], ensure_ascii=False
            ),
        }

        detailed_data.append(row)

    df = pandas.DataFrame(detailed_data)

    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"成功导出 {len(detailed_data)} 条记录到 {filename}")


def export_notices_files(notices: list[Notice], path: Path):
    os.makedirs(path, exist_ok=True)

    notice_groups: dict[int, NoticeGroup] = {}

    notices.sort(key=lambda n: n.date, reverse=True)
    for notice in notices:
        if notice.date.year not in notice_groups:
            notice_groups[notice.date.year] = NoticeGroup(notice.date.year, [notice])
        else:
            notice_groups[notice.date.year].notices.append(notice)

    with open(path / "README.md", mode="wt", encoding="utf-8") as f:
        f.write("# 转专业教务通知\n")
        for group in notice_groups.values():
            f.write(f"## {group.year} 年\n")
            for notice in group.notices:
                f.write(
                    f"#### 【{notice.date.strftime('%m月%d日')}】[{notice.title}]({notice.url})\n"
                )
                for attach in notice.attaches:
                    f.write(f"- [📄 {attach.name}]({attach.url})\n")
                    response = client.get(attach.path)

                    file_dir = "其他"
                    target_text = notice.title + " " + attach.name

                    if "细则" in target_text:
                        file_dir = "转专业细则"
                    elif "名单" in target_text:
                        file_dir = "转专业拟同意名单"
                    elif "实施办法" in target_text:
                        file_dir = "转专业实施办法"
                    elif "嘉锡化学" in target_text:
                        file_dir = "实验班/嘉锡化学实验班"
                    elif "数智" in target_text:
                        file_dir = "实验班/数智实验班"
                    elif "数理综合" in target_text:
                        file_dir = "实验班/数理综合实验班"
                    elif "数理金融" in target_text:
                        file_dir = "实验班/数理金融实验班"

                    os.makedirs(path / file_dir / str(group.year), exist_ok=True)
                    with open(
                        path / file_dir / str(group.year) / attach.name, "wb"
                    ) as file:
                        file.write(response.read())


def main() -> None:
    jxtz_response: httpx.Response = client.get("jxtz.htm")
    jxtz_max_page: int = int(re.search(r"jxtz/(\d*).htm", jxtz_response.text).group(1))  # type: ignore

    gsgg_response: httpx.Response = client.get("gsgg.htm")
    gsgg_max_page: int = int(re.search(r"gsgg/(\d*).htm", gsgg_response.text).group(1))

    notice_list_paths: list[str] = [
        f"jxtz/{page}.htm" for page in range(2, jxtz_max_page)
    ]
    notice_list_paths += [f"gsgg/{page}.htm" for page in range(2, gsgg_max_page)]
    notice_list_paths.append("gsgg.htm")
    notice_list_paths.append("jxtz.htm")

    notices: list[Notice] = []

    with ThreadPoolExecutor(max_workers=30) as pool:
        pool.map(lambda path: get_notice_list(notices, path), notice_list_paths)

    with ThreadPoolExecutor(max_workers=50) as pool:
        pool.map(lambda notice: get_notice(notice), notices)

    export_notices_files(notices, Path("./转专业"))


if __name__ == "__main__":
    main()
