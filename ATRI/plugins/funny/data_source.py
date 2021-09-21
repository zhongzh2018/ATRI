import re
import os

from pathlib import Path
from random import choice, randint
from nonebot.adapters.cqhttp.utils import unescape

from ATRI.service import Service
from ATRI.log import logger
from ATRI.exceptions import RequestError
from ATRI.utils import request
from ATRI.utils import request, Translate
from ATRI.rule import is_in_service


FUNNY_DIR = Path(".") / "data"
os.makedirs(FUNNY_DIR, exist_ok=True)


__doc__ = """
乐1乐，莫当真
"""


class Funny(Service):
    def __init__(self):
        Service.__init__(self, "乐", __doc__, rule=is_in_service("乐"))

    @staticmethod
    async def idk_laugh(name: str) -> str:
        laugh_list = list()

        file_name = "laugh.txt"
        path = FUNNY_DIR / file_name
        if not path.is_file():
            logger.warning("未发现笑话相关数据，正在下载并保存...")
            url = (
                "https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/laugh.txt"
            )
            res = await request.get(url)
            context = await res.text()  # type: ignore
            with open(path, "w", encoding="utf-8") as w:
                w.write(context)
            logger.warning("完成")

        with open(path, "r", encoding="utf-8") as r:
            for line in r:
                laugh_list.append(line.strip("\n"))

        rd: str = choice(laugh_list)
        result = rd.replace("%name", name)
        return result

    @staticmethod
    def me_re_you(msg: str) -> tuple:
        if "我" in msg and "[CQ" not in msg:
            return msg.replace("我", "你"), True
        else:
            return msg, False

    @staticmethod
    def fake_msg(text: str) -> list:
        arg = text.split(" ")
        node = list()

        for i in arg:
            args = i.split("-")
            qq = args[0]
            name = unescape(args[1])
            repo = unescape(args[2])
            dic = {"type": "node", "data": {"name": name, "uin": qq, "content": repo}}
            node.append(dic)
        return node

    @staticmethod
    async def eat_what(name: str, msg: str) -> str:
        EAT_URL = "https://wtf.hiigara.net/api/run/"
        params = {"event": "ManualRun"}
        pattern_0 = r"大?[今明后]天(.*?)吃[什啥]么?"
        pattern_1 = r"(今|明|后|大后)天"
        arg = re.findall(pattern_0, msg)[0]
        day = re.match(pattern_1, msg).group(0)  # type: ignore

        if arg == "中午":
            a = f"LdS4K6/{randint(0, 1145141919810)}"
            url = EAT_URL + a
            try:
                data = await request.post(url, params=params)
                data = await data.json()
            except RequestError:
                raise RequestError("Request failed!")

            text = Translate(data["text"]).to_simple().replace("今天", day)
            get_a = re.search(r"非常(.*?)的", text).group(0)  # type: ignore
            result = text.replace(get_a, "")

        elif arg == "晚上":
            a = f"KaTMS/{randint(0, 1145141919810)}"
            url = EAT_URL + a
            try:
                data = await request.post(url, params=params)
                data = await data.json()
            except RequestError:
                raise RequestError("Request failed!")

            result = Translate(data["text"]).to_simple().replace("今天", day)

        else:
            rd = randint(1, 10)
            if rd == 5:
                result = ["吃我吧", "吃屎吧你","吔屎啦你"]
                return choice(result)
            else:
                a = f"JJr1hJ/{randint(0, 1145141919810)}"
                url = EAT_URL + a
                try:
                    data = await request.post(url, params=params)
                    data = await data.json()
                except RequestError:
                    raise RequestError("Request failed!")

                text = Translate(data["text"]).to_simple().replace("今天", day)
                get_a = re.match(r"(.*?)的智商", text).group(0)  # type: ignore
                result = text.replace(get_a, f"{name}的智商")

        return result
