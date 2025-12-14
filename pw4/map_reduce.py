from collections import Counter
from multiprocessing import Pool
from pathlib import Path
import re
import sys
from typing import Iterator

if len(sys.argv) >= 2:
    filein = Path(sys.argv[1]).resolve()
else:
    filein = Path(__file__).parent / "fuckass.txt"  # demo


def stream(file: Path) -> Iterator[str]:
    with file.open("r") as f:
        yield from f


def mapper(str_stream: Iterator[str], len_limit: int) -> Iterator[str]:
    "if surpass length limit we send it. if the fist one already surpassed length limit we send it."
    counter = 0
    temp = []
    for line in str_stream:
        counter += len(line)
        temp.append(line)
        if counter >= len_limit:
            yield "".join(temp)
            temp.clear()
            counter = 0
    if temp:
        yield "".join(temp)


def process(someLines: str) -> Counter[str]:
    # fuck why concat lines when dont
    return Counter(re.findall(r"\w+", someLines))


def join(counters: list[Counter[str]]) -> Counter[str]:
    return sum(counters, Counter())


def map_reduce_word_count(
    file: Path, num_workers=4, len_limit=150
):  # sensible defaults
    this = mapper(stream(file), len_limit)
    with Pool(num_workers) as pool:
        map_results = pool.map(process, this)
    return join(map_results)


if __name__ == "__main__":
    ct = map_reduce_word_count(filein)
    for w, c in ct.most_common()[:10]:
        print(f"{w}: {c}")
