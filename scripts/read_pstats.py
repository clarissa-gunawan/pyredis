import typer
import pstats
from pstats import SortKey


def read_pstats(filepath: str, limit: int = 20):
    p = pstats.Stats(filepath)
    p.strip_dirs().sort_stats(SortKey.CALLS).print_stats(limit)
    return p


if __name__ == "__main__":
    typer.run(read_pstats)
