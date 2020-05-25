import click
from flask.cli import with_appcontext
from config import Config
from app import app

@app.cli.command("REG_KEY")
@click.argument("key")
def set_reg_key(key):
    app.config["REGISTER_KEY"] = key
    print("The Registration Key is Now Set To ...  " + key)
