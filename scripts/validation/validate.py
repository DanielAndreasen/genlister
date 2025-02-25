from pathlib import Path

import typer
from core import TYPE2VALIDATOR, CSVBase, TypeOfListEnum
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


def is_duplicate(genes: list[CSVBase], gene_row: CSVBase) -> bool:
    return any(gene.hugo_name == gene_row.hugo_name for gene in genes) or any(
        gene.hgnc_id == gene_row.hgnc_id for gene in genes
    )


app = typer.Typer()


@app.command(help="Validate a CSV file.")
def validate_file(type_of_list: TypeOfListEnum, fname: Path):
    if not fname.exists():
        raise IOError(f"File not found: {fname}")
    validator = TYPE2VALIDATOR[type_of_list]
    genes = []
    with open(fname, "r") as f:
        header = f.readline().strip().split(",")
        for row in f:
            values = {k: v for k, v in zip(header, row.strip().split(","))}
            try:
                gene_row = validator.model_validate(values)
            except ValidationError as e:
                print(f"Noget er galt med rækken:\n**{row.strip()}**", end="\n")
                print(f"{clean_error(e)}\n")
                continue
            if is_duplicate(genes, gene_row):
                print(f"Noget er galt med rækken:\n**{row.strip()}**", end="\n")
                print("Der er tale om en duplikat")
            else:
                genes.append(gene_row)


if __name__ == "__main__":
    app()
