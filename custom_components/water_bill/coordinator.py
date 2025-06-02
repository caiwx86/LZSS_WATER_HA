"""水费查询集成数据更新协调器。"""
from __future__ import annotations

import logging
from datetime import timedelta, datetime
from typing import Any, Dict

import aiohttp
import async_timeout
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class WaterBillDataUpdateCoordinator(DataUpdateCoordinator):
    """水费数据更新协调器类。"""

    def __init__(
        self,
        hass: HomeAssistant,
        account_number: str,
        update_interval: timedelta = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """初始化协调器。"""
        super().__init__(
            hass,
            _LOGGER,
            name="兴泸水务",
            update_interval=update_interval,
        )
        self._account_number = account_number
        self._session = aiohttp.ClientSession()

    @property
    def account_number(self) -> str:
        """返回账号。"""
        return self._account_number

    async def _async_update_data(self) -> Dict[str, Any]:
        """从水费网站获取数据。"""
        try:
            async with async_timeout.timeout(10):
                current_date = datetime.now()
                data = {
                    "__VIEWSTATE": "/wEPDwUJMTMwNTkwMjI4ZGRzSpW4QQXIKjbNWAPa1WXtaK/mwTcYmTjvG8fbktlMgQ==",
                    "__VIEWSTATEGENERATOR": "51114EE5",
                    "__EVENTVALIDATION": "/wEdAAWVO/3fmRx9gZB/eBewQB4qEZwElK9JgTzgWgAz/ShB8JIQMpM+ZLBNEKe/ZRcwNE5BgGO2cbZoYVVlrl5IIMvpoJf8A5tkF8NhvUx0nVlv69wrY/UMNK+Bf+CULI/mm2zt8ewA6VuleufMKQ9TL/CN",
                    "startMonth": f"{current_date.year}/{current_date.month}",
                    "endMonth": f"{current_date.year}/{current_date.month}",
                    "userCode": self._account_number,
                    "userName": "",
                    "vaCode": "",
                    "btnSender": "提交"
                }

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://wt.lzss.com",
                    "Referer": "https://wt.lzss.com/fee/waterfee.aspx"
                }

                async with self._session.post(API_BASE_URL, data=data, headers=headers) as response:
                    response.raise_for_status()
                    html = await response.text()

                soup = BeautifulSoup(html, 'html.parser')
                listview = soup.find('ul', {'id': 'listview'})
                
                if not listview:
                    raise UpdateFailed("未找到数据列表")

                return {"balance": self._extract_balance(listview)}

        except Exception as err:
            _LOGGER.error("获取数据失败: %s", str(err))
            raise UpdateFailed(f"Error: {err}")

    def _extract_balance(self, element: BeautifulSoup) -> float:
        """从HTML元素中提取余额。"""
        try:
            items = element.find_all('li')
            for item in items:
                text = item.text.strip()
                if "余额" in text:
                    value = ''.join(c for c in text if c.isdigit() or c == '.')
                    return float(value) if value else 0.0
            return 0.0
        except Exception as e:
            _LOGGER.error("提取余额时出错: %s", str(e))
            return 0.0

    async def async_close(self) -> None:
        """关闭HTTP会话。"""
        await self._session.close() 