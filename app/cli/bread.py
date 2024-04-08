import typer
from rich.console import Console
from sqlalchemy import select

from app.cli.tables import generate_table
from app.db import SessionFactory
from app.models import Bread

console = Console()

app = typer.Typer()


@app.command(name="list")
def list_breads():
    """Listando os tipos pães disponiveis."""
    with SessionFactory() as session:
        results = session.scalars(select(Bread)).all()

    table = generate_table("Breads", results)
    console.print(table)


@app.command(name="create")
def create_bread(tipo: str):
    """Cadastra um tipo pão novo."""

    with SessionFactory() as session:
        obj = Bread(tipo=tipo)
        session.add(obj)
        session.commit()


@app.command(name="delete")
def delete_bread(id: int):
    """Deleta um tipo de pão por id."""

    with SessionFactory() as session:
        if (obj := session.get(Bread, id)) is None:
            console.print(f"[red]Error: Pão com id {id} não achado[/red]")
            raise typer.Exit(1)
        session.delete(obj)
        session.commit()

    console.print(f"[green]Pão com id {id} deletado com sucesso[/green]")
