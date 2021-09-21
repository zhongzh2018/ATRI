import time
import psutil
import random
import platform
from datetime import datetime

from ATRI.service import Service
from ATRI.log import logger as log
from ATRI.rule import is_in_service
from ATRI.exceptions import GetStatusError


__doc__ = """
检查咱自身状态
"""


class IsSurvive(Service):
    def __init__(self):
        Service.__init__(self, "状态", __doc__, rule=is_in_service("状态"))

    @staticmethod
    def ping() -> str:
        #return "I'm fine."
        ping_msg = ["当然，我是高性能的嘛",
        "小事一桩，我是高性能的嘛", "不愧是高性能的我，可以卖个让人满意的好价钱呢",
        "哼哼，我才是高性能的呢",
        "是吧！我是高性能的嘛，哼哼",
        "我会像人类一样犯错，从某种意义上来说也证明了我是高性能机器人",
        "因为我是高性能的嘛！嗯哼！",
        "毕竟我可是高性能的",
        "哼哼,毕竟我是高性能的呢"]
        return random.choice(ping_msg)

    @staticmethod
    def get_status():
        log.info("开始检查资源消耗...")
        try:
            system_info = platform.system()
            node_info = platform.uname().node
            kernel_info = platform.release()
            cpu = psutil.cpu_percent(interval=1)
            mem_used = int(psutil.virtual_memory().used / 1048576)
            mem_total = int(psutil.virtual_memory().total / 1048576)
            mem = psutil.virtual_memory().percent
            disk_used = round(psutil.disk_usage("/").used / 1073741824, 2)
            disk_total = round(psutil.disk_usage("/").total / 1073741824, 2)
            disk = psutil.disk_usage("/").percent
            tempture= open("/sys/class/thermal/thermal_zone0/temp", "r")
            cpu_temp = round(float(tempture.readline().strip())/1000, 2)
            '''
            inteSENT = round(psutil.net_io_counters().bytes_sent / 1000000, 2)  # type: ignore
            inteRECV = round(psutil.net_io_counters().bytes_recv / 1000000, 2)  # type: ignore
            '''
            now = time.time()
            boot = psutil.boot_time()
            up_time = str(
                datetime.utcfromtimestamp(now).replace(microsecond=0)
                - datetime.utcfromtimestamp(boot).replace(microsecond=0)
            )

        except GetStatusError:
            raise GetStatusError("Failed to get status.")

        msg = "アトリは、高性能ですから！"
        if cpu > 90:  # type: ignore
            msg = "处理器占用高哦..."
            is_ok = False
            if mem > 90:
                msg = "处理器和内存占用高哦..."
                is_ok = False
        elif mem > 90:
            msg = "内存占用高哦..."
            is_ok = False
        elif disk > 90:
            msg = "硬盘快要装满了..."
            is_ok = False
        else:
            log.info("资源占用正常")
            is_ok = True

        msg0 = (
            "看起来很高性能呢:"
            f"\n操作系统: {system_info}"
            f"\n设备名称: {node_info}"
            f"\n内核版本: {kernel_info}"
            f"\n处理器: {cpu}%"
            f"\n内存: {mem_used}MB/{mem_total}MB"
            f"\n硬盘: {disk_used}GB/{disk_total}GB"
            f"\n温度: {cpu_temp}℃"
            #f"\n数据发送量: {inteSENT}MB\n"
            #f"\n数据接收量: {inteRECV}MB\n"
            f"\n系统运行时间: {up_time}"
        )

        return msg0, is_ok
