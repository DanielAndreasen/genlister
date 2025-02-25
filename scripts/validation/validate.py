from pathlib import Path

import typer
from core import TYPE2VALIDATOR, TypeOfListEnum
from pydantic import ValidationError


def clean_error(e: ValidationError) -> str:
    res = []
    for index, line in enumerate(str(e).split("\n")):
        match index % 3:
            case 1:
                res.append(f"* **{line}**: ")
            case 2:
                res[-1] += line[2 : line.index("[") - 1]
            case _:
                pass
    return "\n".join(res)


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
            try:
                validator.model_validate(values)
            except ValidationError as e:
                print(f"Noget er galt med rækken:\n**{row.strip()}**", end="\n")
                print(f"{clean_error(e)}\n")
                # print(e)


if __name__ == "__main__":
    app()
