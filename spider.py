#!/usr/bin/python3

import asyncio
import aiohttp
import html5lib

from bs4 import BeautifulSoup

from models import Crypto

class Spider:
    def __init__(self,url,loop):
        self.url = url
        self.loop = loop

    async def run(self):
        site_soup = await self.get_site_contect()
        crypto_data = await self.get_crypto_data(site_soup)
    
        for crypto in crypto_data:
            name = crypto.find('a', class_='currency-name-container').text
            price = crypto.find('a', class_='price').text.replace("$","")
            await Crypto(name,price).save()

    async def get_site_contect(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as site_data:
                data = await site_data.read()
        
        return BeautifulSoup(data.decode('utf-8'),'html5lib')

    async def get_crypto_data(self,html):
        data = html.find('tr', id="id-bitcoin").find_parent().find_all('tr')
        return data

if __name__ == '__main__':
    url = "https://coinmarketcap.com/"
    loop = asyncio.get_event_loop()
    spider = Spider(url, loop)
    loop.run_until_complete(spider.run())
    loop.close()