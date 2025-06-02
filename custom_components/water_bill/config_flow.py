"""水费查询集成配置流程。"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_ACCOUNT_NUMBER

_LOGGER = logging.getLogger(__name__)

class WaterBillConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理水费查询集成的配置流程。"""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """处理用户配置步骤。"""
        errors = {}

        if user_input is not None:
            account_number = user_input[CONF_ACCOUNT_NUMBER]
            
            # 设置唯一ID
            await self.async_set_unique_id(account_number)
            self._abort_if_unique_id_configured()

            # 创建配置条目
            return self.async_create_entry(
                title=f"水费账户 {account_number}",
                data={
                    CONF_ACCOUNT_NUMBER: account_number
                }
            )

        # 显示配置表单
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ACCOUNT_NUMBER): str
                }
            ),
            errors=errors
        ) 