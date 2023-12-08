"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that
looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water.
Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no."
His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we
stopped getting more sand! There's a ferry leaving soon that is headed over in that direction -
it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry,
maybe you can help us with our food production problem. The latest Island Island Almanac just arrived
 and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what
type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil,
what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil,
fertilizer and so on is identified with a number, but numbers are reused by each category - that is,
soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category
into numbers in a destination category. That is, the section that starts with seed-to-soil map:
describes how to convert a seed number (the source) to a soil number (the destination).
This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer,
 and so on.

Rather than list every source number and its corresponding destination number one by one,

 the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers:
 the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2.
This line means that the source range starts at 98 and contains two values: 98 and 99.
The destination range is the same length, but it starts at 50, so its two values are 50 and 51.
With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99
corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97.
This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So,
seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number.
So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location
that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds.
 To do this, you'll need to convert each seed number through other categories until you can find its corresponding
 location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

from __future__ import annotations

import itertools
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import batched
from operator import itemgetter

from utils import extract_numbers, AOCChallenge


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

    def minimum(self):
        return min(self.map(seed) for seed in self.seeds)

    def _instance_compute_approximate_minimum(
        self, granularity: int = 100_000, to_consider: int = 3
    ) -> tuple[int, int]:
        intervals = self.gen_intervals()
        minimum = min(itertools.chain(*intervals))
        maximum = max(itertools.chain(*intervals))

        if maximum - minimum <= 1000_000:
            granularity = 1
            to_consider = 1

        ranges_granular = list(
            itertools.chain.from_iterable(
                range(start, stop + 1, granularity) for (start, stop) in intervals
            )
        )
        approx_minima = list(
            sorted(
                ((seed, self.map(seed)) for seed in ranges_granular),
                key=itemgetter(1),
            ),
        )
        approx_minima = approx_minima[:to_consider]
        absolute_minimum = approx_minima[0]
        for current_minimum_seed, _ in approx_minima:
            for seed in range(
                max(minimum, current_minimum_seed - granularity // 2),
                min(maximum, current_minimum_seed + granularity // 2),
            ):
                location = self.map(seed)
                if location < absolute_minimum[1]:
                    absolute_minimum = (seed, location)
        return absolute_minimum

    def statistical_in_quotes_best_minimum(self) -> int:
        counters: dict[int, Counter] = defaultdict(Counter)
        for granularity, to_consider in itertools.product(
            (2**p for p in range(11, 17)), (2, 10)
        ):
            seed, location = self._instance_compute_approximate_minimum(
                granularity, to_consider
            )
            print(
                f"{seed=} -> {location=} with {granularity=} & {to_consider=}",
                file=sys.stderr,
            )
            counters[seed][location] += 1
        return max((c.most_common()[0] for c in counters.values()), key=itemgetter(1))[0]  # type: ignore


def part1(filename: str) -> int:
    with open(filename) as f:
        mapping_pipeline = MappingPipeline.parse(f.read())
        return mapping_pipeline.minimum()


# --- Part Two ---
# Everyone will starve if you only plant such a small number of seeds.
# Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.
#
# The values on the initial seeds: line come in pairs. Within each pair, the first value is the start
# of the range and the second value is the length of the range. So, in the first line of the example above:
#
# seeds: 79 14 55 13
# This line describes two ranges of seed numbers to be planted in the garden.
# The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92.
# The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.
#
# Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.
#
# In the above example, the lowest location number can be obtained from seed number 82,
# which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46,
# and location 46. So, the lowest location number is 46.
#
# Consider all of the initial seed numbers listed in the ranges on the first line of the almanac.
#
# What is the lowest location number that corresponds to any of the initial seed numbers?


def part2(filename: str) -> int:
    with open(filename) as f:
        mapping_pipeline = MappingPipeline.parse(f.read())
        return mapping_pipeline.statistical_in_quotes_best_minimum()


day5 = AOCChallenge(5, part1, part2)
__all__ = [day5]
