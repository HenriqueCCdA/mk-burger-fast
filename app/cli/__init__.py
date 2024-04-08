import typer

from app.cli.bread import app as bread_app
from app.cli.meat import app as meat_app
from app.cli.optional import app as optional_app
from app.cli.status import app as status_app

app = typer.Typer(add_completion=False)

app.add_typer(status_app, name="status", help="Status disponiveis na plataforma.")
app.add_typer(bread_app, name="bread", help="Pães disponiveis na plataforma.")
app.add_typer(meat_app, name="meat", help="Carnes disponiveis na plataforma.")
app.add_typer(optional_app, name="optional", help="Opções disponiveis na plataforma.")
