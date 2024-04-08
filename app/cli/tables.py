from rich.table import Table


def generate_table(title: str, result: list) -> Table:

    table = Table(title=title)

    table.add_column("Id", justify="center", style="cyan")
    table.add_column("Tipo", justify="center", style="magenta")
    table.add_column("Created_at", justify="center", style="magenta")
    table.add_column("Updated_at", justify="center", style="magenta")

    for s in result:
        table.add_row(f"{s.id}", f"{s.tipo}", f"{s.created_at}", f"{s.updated_at}")

    return table
