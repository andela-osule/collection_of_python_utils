import asyncio
import argparse
from aiohttp import ClientSession, BasicAuth

parser = argparse.ArgumentParser(description='Load test a URL')
parser.add_argument('num', type=int,
                    help='num of times to request URL')
parser.add_argument('url', type=str,
                    help='URL to load test')
parser.add_argument('--username', type=str, help='username for HTTP Basic Auth')
parser.add_argument('--password', type=str, help='password for HTTP Basic Auth')

args = parser.parse_args()

auth = BasicAuth(args.username, password=args.password) if args.username else None


async def get_page(url):
    """Retrieve content at a url"""
    async with ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            response = await response.read()
            print('.', end='')

loop = asyncio.get_event_loop()
tasks = []

for _ in range(args.num):
    task = asyncio.ensure_future(get_page(args.url))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))
