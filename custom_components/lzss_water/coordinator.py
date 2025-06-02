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

    async def _get_form_values(self) -> Dict[str, str]:
        """获取表单验证值。"""
        try:
            async with self._session.get(API_BASE_URL) as response:
                response.raise_for_status()
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            viewstate = soup.find('input', {'id': '__VIEWSTATE'})
            viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})
            eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'})

            if not all([viewstate, viewstategenerator, eventvalidation]):
                raise UpdateFailed("无法获取表单验证值")

            return {
                "__VIEWSTATE": viewstate.get('value', ''),
                "__VIEWSTATEGENERATOR": viewstategenerator.get('value', ''),
                "__EVENTVALIDATION": eventvalidation.get('value', '')
            }
        except Exception as err:
            _LOGGER.error("获取表单验证值失败: %s", str(err))
            raise UpdateFailed(f"获取表单验证值失败: {err}")

    async def _fetch_data(self) -> Dict[str, Any]:
        """获取水费数据。"""
        form_values = await self._get_form_values()
        current_date = datetime.now()
        
        data = {
            **form_values,
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

        return {
            "balance": self._extract_balance(listview),
            "unpaid_count": self._extract_unpaid_count(listview),
            "unpaid_amount": self._extract_unpaid_amount(listview)
        }

    async def _async_update_data(self) -> Dict[str, Any]:
        """从水费网站获取数据。"""
        try:
            async with async_timeout.timeout(10):
                current_date = datetime.now()
                data = await self._fetch_data()

                return {
                    "current_balance": data["balance"],
                    "current_month": f"{current_date.year}/{current_date.month}",
                    "unpaid_count": data["unpaid_count"],
                    "unpaid_amount": data["unpaid_amount"]
                }

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

    def _extract_unpaid_count(self, element: BeautifulSoup) -> int:
        """从HTML元素中提取未缴费笔数。"""
        try:
            items = element.find_all('li')
            for item in items:
                text = item.text.strip()
                if "未缴费笔数" in text:
                    value = ''.join(c for c in text if c.isdigit())
                    return int(value) if value else 0
            return 0
        except Exception as e:
            _LOGGER.error("提取未缴费笔数时出错: %s", str(e))
            return 0

    def _extract_unpaid_amount(self, element: BeautifulSoup) -> float:
        """从HTML元素中提取未缴费金额。"""
        try:
            items = element.find_all('li')
            for item in items:
                text = item.text.strip()
                if "未缴费金额" in text:
                    value = ''.join(c for c in text if c.isdigit() or c == '.')
                    return float(value) if value else 0.0
            return 0.0
        except Exception as e:
            _LOGGER.error("提取未缴费金额时出错: %s", str(e))
            return 0.0

    async def async_close(self) -> None:
        """关闭HTTP会话。"""
        await self._session.close() 