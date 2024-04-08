import typer
from rich.console import Console
from sqlalchemy import select

from app.cli.tables import generate_table
from app.db import SessionFactory
from app.models import Meat

console = Console()

app = typer.Typer()


@app.command(name="list")
def list_meats():
    """Listando os tipos carnes disponiveis."""

    with SessionFactory() as session:
        results = session.scalars(select(Meat)).all()

    table = generate_table("Meat", results)
    console.print(table)


@app.command(name="create")
def create_meat(tipo: str):
    """Cadastra um tipo carne novo."""

    with SessionFactory() as session:
        obj = Meat(tipo=tipo)
        session.add(obj)
        session.commit()


@app.command(name="delete")
def delete_meat(id: int):
    """Deleta um tipo de carne por id."""

    with SessionFactory() as session:
        if (obj := session.get(Meat, id)) is None:
            console.print(f"[red]Error: Carne com id {id} não achada[/red]")
            raise typer.Exit(1)
        session.delete(obj)
        session.commit()

    console.print(f"[green]Carne com id {id} deletado com sucesso[/green]")
