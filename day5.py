from __future__ import annotations

import itertools
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import batched
from operator import itemgetter
from pprint import pprint


@dataclass(frozen=True, slots=True)
class RangeMap:
    source_start: int
    destination_start: int
    range_length: int


@dataclass
class Mapping(list[RangeMap]):
    src_name: str
    dest_name: str

    def map(self, value: int) -> int:
        for range_map in self:
            if (
                range_map.source_start
                <= value
                < range_map.source_start + range_map.range_length
            ):
                return range_map.destination_start + (value - range_map.source_start)
        return value

    def start(self):
        return min(range_map.source_start for range_map in self)

    def end(self):
        return max(
            range_map.source_start + range_map.range_length for range_map in self
        )

    def __str__(self):
        s = ""
        for source_value in range(self.end()):
            s += f"{source_value} -> {self.map(source_value)}\n"
        return s


def extract_numbers(seeds_str: str, syntax=re.compile(r"(\d+)")):
    return tuple(map(int, syntax.findall(seeds_str) or []))


@dataclass
class MappingPipeline:
    seeds: tuple[int]
    mappings: list[Mapping]

    def map(self, value: int) -> int:
        assert self.mappings[0].src_name == "seed", self.mappings[0].src_name
        for current_mapping in self.mappings:
            value = current_mapping.map(value)
            if current_mapping.src_name == "location":
                break
        return value

    def start(self):
        return self.mappings[0].start()

    def end(self):
        return self.mappings[-1].end()

    @staticmethod
    def parse(data: str) -> MappingPipeline:
        seeds_line, *rest = data.strip().splitlines()
        mappings = []
        current_mapping = None

        for line in (line.strip() for line in rest):
            if not line:
                if current_mapping:
                    mappings.append(current_mapping)
            elif line.endswith("map:"):
                src_name, dest_name = line[:-5].split("-to-")
                current_mapping = Mapping(src_name, dest_name)
            else:
                res = extract_numbers(line)
                dst, src, range_length = res
                current_mapping.append(RangeMap(src, dst, range_length))
        if current_mapping is not None and mappings[-1] != current_mapping:
            mappings.append(current_mapping)

        seeds = extract_numbers(seeds_line)

        return MappingPipeline(seeds, mappings)

    def gen_intervals(self) -> list[tuple[int, int]]:
        return list(
            sorted((start, start + extent) for start, extent in batched(self.seeds, 2))
        )

    def _instance_compute_approximate_minimum(
        self, granularity: int = 100_000, to_consider: int = 3
    ) -> tuple[int, int]:
        intervals = self.gen_intervals()
        ranges_granular = list(
            itertools.chain.from_iterable(
                range(start, stop, granularity) for (start, stop) in intervals
            )
        )
        approx_minima = list(
            sorted(
                ((seed, mapping_pipeline.map(seed)) for seed in ranges_granular),
                key=itemgetter(1),
            ),
        )
        approx_minima = approx_minima[:to_consider]
        absolute_minimum = approx_minima[0]
        for current_minimum_seed, _ in approx_minima:
            for seed in range(
                current_minimum_seed - granularity, current_minimum_seed + granularity
            ):
                location = mapping_pipeline.map(seed)
                if location < absolute_minimum[1]:
                    absolute_minimum = (seed, location)
        return absolute_minimum

    def statistical_in_quotes_best_minimum(self) -> int:
        # from playing around, G geometric dist i.e. 1024 to 2048 to 4096 to 8192
        #            to_consider = (0 to 10) -> dist of 1
        counters: dict[int, Counter] = defaultdict(Counter)
        for granularity, to_consider in itertools.product(
            (2**p for p in range(11, 17)), (2, 10, 20)
        ):
            seed, location = self._instance_compute_approximate_minimum(
                granularity, to_consider
            )
            print(f"{seed=} -> {location=} with {granularity=} & {to_consider=}")
            counters[seed][location] += 1
        pprint(counters)
        return max(c.most_common() for c in counters.values())  # type: ignore


if __name__ == "__main__":
    # 284_352_702
    # 219_529_182
    # 219_529_182
    # 219_533_664
    with open("input/day5.txt") as f:
        mapping_pipeline = MappingPipeline.parse(f.read())
        print(mapping_pipeline.statistical_in_quotes_best_minimum())
