import typer
from rich.console import Console
from sqlalchemy import select

from app.cli.tables import generate_table
from app.db import SessionFactory
from app.models import Optional

console = Console()

app = typer.Typer()


@app.command(name="list")
def list_optionals():
    """Listando os opcionais carnes disponiveis."""

    with SessionFactory() as session:
        results = session.scalars(select(Optional)).all()

    table = generate_table("Meat", results)
    console.print(table)


@app.command(name="create")
def create_optional(tipo: str):
    """Cadastra um tipo opção novo."""

    with SessionFactory() as session:
        obj = Optional(tipo=tipo)
        session.add(obj)
        session.commit()


@app.command(name="delete")
def delete_optional(id: int):
    """Deleta um tipo de opção por id."""

    with SessionFactory() as session:
        if (obj := session.get(Optional, id)) is None:
            console.print(f"[red]Error: Opção com id {id} não achada[/red]")
            raise typer.Exit(1)
        session.delete(obj)
        session.commit()

    console.print(f"[green]Opção com id {id} deletado com sucesso[/green]")
