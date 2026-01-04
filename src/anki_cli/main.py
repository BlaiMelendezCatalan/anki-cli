import importlib.metadata
import sys
import traceback
from pathlib import Path

import click
from anki.collection import Collection

from anki_cli.database import DatabaseManager


def _generic_expection(e: Exception):
    click.secho(f"Error: {e}\n{traceback.format_exc()}", err=True, fg="red")
    sys.exit(1)


@click.group(invoke_without_command=True)
@click.option("-v", "--version", is_flag=True, help="Display anki-cli version")
@click.pass_context
def anki(ctx: click.Context, version: bool):
    try:
        if version:
            click.secho(f"{importlib.metadata.version('anki-cli')}", fg="cyan")
            sys.exit(0)
        elif ctx.invoked_subcommand is None:
            click.secho(ctx.get_help())
            sys.exit(0)
    except Exception as e:
        _generic_expection(e)


@anki.command()
@click.argument("collection-name", type=str, required=True)
@click.option(
    "--collection-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Specify a directory for the new collection",
)
def new(collection_name: str, collection_dir: Path):
    collection_name = (
        collection_name
        if collection_name.endswith(".anki2")
        else collection_name + ".anki2"
    )
    collection_path = (collection_dir / collection_name).resolve()
    try:
        _ = Collection(str(collection_path))
        db_manager = DatabaseManager()
        db_manager.add_collection(collection_name, collection_path)
    except Exception as e:
        _generic_expection(e)


def entry_point():
    anki(obj={})
