"""
https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html
"""

import asyncio

import importlib.metadata

import datetime as dt

from typing import Dict, Optional, Any

from nextcloud_aio.exceptions import NextCloudLoginFlowTimeout

__VERSION__ = importlib.metadata.version('nextcloud_aio')


class LoginFlowV2(object):

    async def login_flow_initiate(self, user_agent: Optional[str] = None) -> Dict[Any, Any]:
        """
        Initiate login flow v2 to obtain app token.

        https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html#login-flow-v2
        """
        response = await self.request(
            method='POST',
            url=f'{self.endpoint}/index.php/login/v2',
            headers={
                'user-agent':
                    f'nextcloud_aio/{__VERSION__}' if user_agent is None else user_agent})
        return response.json()

    async def login_flow_wait_confirm(self, token, timeout: int = 60) -> Dict:
        """Wait for user to confirm login.  Return array including new `appPassword`."""
        start_dt = dt.datetime.now()
        running_time = 0

        response = await self.request(
            method='POST',
            url=f'{self.endpoint}/login/v2/poll',
            data={'token': token})

        while response.status_code == 404 and running_time < timeout:
            response = await self.request(
                method='POST',
                url=f'{self.endpoint}/login/v2/poll',
                data={'token': token})
            running_time = (dt.datetime.now() - start_dt).seconds
            await asyncio.sleep(1)

        if response.status_code == 404:
            raise NextCloudLoginFlowTimeout(
                'Login flow timed out.  You can try again.')

        return response.json()

    async def destroy_login_token(self):
        """
        Delete an app password generated by Login Flow v2.

        The user must currently be logged in using the app password.
        """
        return await self.ocs_query(
            method='DELETE',
            sub='/ocs/v2.php/core/apppassword')
