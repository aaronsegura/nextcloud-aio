"""Nextcloud Talk Conversation Avatars API.

https://nextcloud-talk.readthedocs.io/en/latest/avatar/
"""
from typing import Optional

from nextcloud_async.driver import NextcloudTalkApi, NextcloudModule
from nextcloud_async.exceptions import NextcloudNotCapable


# TODO: Verify all return values, do things, etc...
# TODO: Add to Conversation object

class ConversationAvatars(NextcloudModule):
    """Interact with Nextcloud Talk API."""

    def __init__(
            self,
            api: NextcloudTalkApi,
            api_version: Optional[str] = '1'):
        self.stub = f'/apps/spreed/api/v{api_version}'
        self.api: NextcloudTalkApi = api

    async def set(self, room_token:str, image_file: bytes) -> None:
        if not await self.api.has_feature('avatar'):
            raise NextcloudNotCapable

        await self._post(
            path=f'/room/{room_token}/avatar',
            data={'file': image_file})

    async def set_emoji(
            self,
            room_token: str ,
            emoji: str,
            color: Optional[str] = "none") -> None:
        if not await self.api.has_feature('avatar'):
            raise NextcloudNotCapable

        await self._post(
            path=f'/room/{room_token}/avatar/emoji',
            data={
                'emoji': emoji,
                'color': color})

    async def delete(self, room_token: str):
        if not await self.api.has_feature('avatar'):
            raise NextcloudNotCapable

        await self._delete(path=f'/room/{room_token}/avatar')

    async def get(self, room_token: str, dark_mode: Optional[bool] = False) -> bytes:
        if not await self.api.has_feature('avatar'):
            raise NextcloudNotCapable

        if dark_mode:
            response = await self._get_raw(
                path=f'/room/{room_token}/avatar/dark')
        else:
            response = await self._get_raw(
                path=f'/room/{room_token}/avatar')

        return response.content

    async def get_federated(self, room_token: str, cloud_id: str, size: int, dark_mode: Optional[bool] = False) -> bytes:
        if not await self.api.has_feature('avatar') or not await self.api.has_feature('federated-v1'):
            raise NextcloudNotCapable

        if dark_mode:
            response = await self.api.client.http_client.request(
                method='GET',
                url=f'{self.api.client.endpoint}/ocs/v2.php/apps/spreed/api/v1/proxy/{room_token}/user-avatar/{size}/dark',
                data={
                    'cloudId': cloud_id,
                    'size': size})
        else:
            response = await self.api.client.http_client.request(
                method='GET',
                url=f'{self.api.client.endpoint}/ocs/v2.php/apps/spreed/api/v1/proxy/{room_token}/user-avatar/{size}',
                data={
                    'cloudId': cloud_id,
                    'size': size})

        return response.content