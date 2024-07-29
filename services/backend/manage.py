import click
import json
import asyncio
from models.advertisment import Advertisement
from database import get_session


@click.group()
def cli():
    pass


@cli.command()
@click.option('--file', default='fixtures/ads.json', help='Path to the JSON file')
def import_data(file):
    async def import_data_async(file):
        with open(file, 'r') as f:
            data = json.load(f)

        async for session in get_session():
            async with session.begin():
                for item in data:
                    if all(item.get(key) is not None for key in ["title", "ad_id", "author", "view_count", "position"]):
                        advertisement = Advertisement(
                            title=item['title'],
                            ad_id=item['ad_id'],
                            author=item['author'],
                            view_count=item['view_count'],
                            position=item['position']
                        )
                        session.add(advertisement)
            click.echo(f"Imported {len(data)} advertisements from {file}")

    asyncio.run(import_data_async(file))


if __name__ == '__main__':
    cli()
