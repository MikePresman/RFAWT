import click
from flask.cli import with_appcontext

@click.command(name="test")
@with_appcontext
def test():
    print("Hello World")
