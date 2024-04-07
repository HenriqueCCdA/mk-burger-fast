import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy import select

from app.db import SessionFactory
from app.models import Bread, Meat, Status

console = Console()

app = typer.Typer(add_completion=False)

status_app = typer.Typer()
bread_app = typer.Typer()
meat_app = typer.Typer()


def generate_table(title: str, result: list) -> Table:

    table = Table(title=title)

    table.add_column("Id", justify="center", style="cyan")
    table.add_column("Tipo", justify="center", style="magenta")
    table.add_column("Created_at", justify="center", style="magenta")
    table.add_column("Updated_at", justify="center", style="magenta")

    for s in result:
        table.add_row(f"{s.id}", f"{s.tipo}", f"{s.created_at}", f"{s.updated_at}")

    return table


@status_app.command(name="list")
def list_status():
    """Listando os status disponiveis na plataforma."""

    with SessionFactory() as session:
        results = session.scalars(select(Status)).all()

    table = generate_table("Status", results)
    console.print(table)


# @status_app.command(name="list")
# def list_status():
#     """Cadastra um status novo."""

#     with SessionFactory() as session:
#         results = session.scalars(select(Status)).all()

#     table = generate_table("Status", results)
#     console.print(table)


@bread_app.command(name="list")
def list_breads():
    """Listando os tipos pães disponiveis."""

    with SessionFactory() as session:
        results = session.scalars(select(Bread)).all()

    table = generate_table("Breads", results)
    console.print(table)


@bread_app.command(name="create")
def create_bread(tipo: str):
    """Cadastra um tipo pão novo."""

    with SessionFactory() as session:
        obj = Bread(tipo=tipo)
        session.add(obj)
        session.commit()


@bread_app.command(name="delete")
def delete_bread(id: int):
    """Deleta um tipo de pão por id."""

    with SessionFactory() as session:
        if (obj := session.get(Bread, id)) is None:
            console.print(f"[red]Error: Pão com id {id} não achado[/red]")
            raise typer.Exit(1)
        session.delete(obj)
        session.commit()

    console.print(f"[green]Pão com id {id} deletado com sucesso[/green]")


@meat_app.command(name="list")
def list_meats():
    """Listando os tipos carnes disponiveis."""

    with SessionFactory() as session:
        results = session.scalars(select(Meat)).all()

    table = generate_table("Meat", results)
    console.print(table)


@meat_app.command(name="create")
def create_meat(tipo: str):
    """Cadastra um tipo carne novo."""

    with SessionFactory() as session:
        obj = Meat(tipo=tipo)
        session.add(obj)
        session.commit()


@meat_app.command(name="delete")
def delete_meat(id: int):
    """Deleta um tipo de carne por id."""

    with SessionFactory() as session:
        if (obj := session.get(Meat, id)) is None:
            console.print(f"[red]Error: Carne com id {id} não achada[/red]")
            raise typer.Exit(1)
        session.delete(obj)
        session.commit()

    console.print(f"[green]Carne com id {id} deletado com sucesso[/green]")


app.add_typer(status_app, name="status", help="Status disponiveis na plataforma.")
app.add_typer(bread_app, name="bread", help="Pães disponiveis na plataforma.")
app.add_typer(meat_app, name="meat", help="Carnes disponiveis na plataforma.")
