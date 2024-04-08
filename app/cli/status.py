import typer
from rich.console import Console
from sqlalchemy import select

from app.cli.tables import generate_table
from app.db import SessionFactory
from app.models import Status

console = Console()

app = typer.Typer()


@app.command(name="list")
def list_status():
    """Listando os status disponiveis na plataforma."""

    with SessionFactory() as session:
        results = session.scalars(select(Status)).all()

    table = generate_table("Status", results)
    console.print(table)


@app.command(name="create")
def create_status(tipo: str):
    """Cadastra um status pão novo."""

    with SessionFactory() as session:
        obj = Status(tipo=tipo)
        session.add(obj)
        session.commit()


@app.command(name="delete")
def delete_status(id: int):
    """Deleta um tipo de status por id."""

    with SessionFactory() as session:
        if (obj := session.get(Status, id)) is None:
            console.print(f"[red]Error: Pão com id {id} não achado[/red]")
            raise typer.Exit(1)
        session.delete(obj)
        session.commit()

    console.print(f"[green]Status com id {id} deletado com sucesso[/green]")
