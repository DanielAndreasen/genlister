from pathlib import Path

import typer
from core import TYPE2VALIDATOR, TypeOfListEnum

app = typer.Typer()


@app.command(help="Validate a CSV file.")
def validate_file(type_of_list: TypeOfListEnum, fname: Path):
    if not fname.exists():
        raise IOError(f"File not found: {fname}")
    validator = TYPE2VALIDATOR[type_of_list]
    with open(fname, "r") as f:
        header = f.readline().strip().split(",")
        for row in f:
            values = {k: v for k, v in zip(header, row.strip().split(","))}
            validator.model_validate(values)


if __name__ == "__main__":
    app()
