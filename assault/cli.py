import click
from .http import assault


@click.command()
@click.option("--requests", "-r", default=5, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output JSON file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    print(f"Requests: {requests}")
    print(f"Concurrency: {concurrency}")
    print(f"JSON File: {json_file}")
    print(f"URL: {url}")
    assault(url, requests, concurrency)


if __name__ == "__main__":
    cli()
