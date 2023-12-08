"""
--- Day 7: Camel Cards ---
Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!)
 It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for;
you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of
the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly
above Island Island, making it hard to even get there.

Normally, they use big machines to move the rocks and filter the sand,
but the machines have broken down because Desert Island recently stopped
receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help.
You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards.
 Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand.
A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA

    Four of a kind, where four cards have the same label and one card has a different label: AA8AA

    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332

    Three of a kind, where three cards have the same label,
    and the remaining two cards are each different from any other card in the hand: TTT98

    Two pair, where two cards share one label, two other cards share a second label,
    and the remaining card has a third label: 23432

    One pair, where two cards share one label, and the other three cards have a different label
    from the pair and each other: A23A4

    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect.
Start by comparing the first card in each hand. If these cards are different,
the hand with the stronger first card is considered stronger.
If the first card in each hand have the same label, however, then move on to considering the
second card in each hand. If they differ, the hand with the higher second card wins; otherwise,
continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger.
Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger
 (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483

This example shows five hands; each hand is followed by its bid amount.
Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1,
the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example,
the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger
(K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of
 multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
 So the total winnings in this example are 6440.

    Find the rank of every hand in your set. What are the total winnings?
"""

from __future__ import annotations


import sys
from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from operator import attrgetter
from itertools import groupby

from utils import AOCChallenge

# can be modified depending on which part is being tested
CARDS: list[str] = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")
strength: dict[str, int] = {
    card: len(CARDS) - index for index, card in enumerate(CARDS)
}


@dataclass(frozen=True)
class Hand:
    cards: tuple[str, str, str, str, str]  # a hand has five cards

    def __post_init__(self):
        def is_valid_card(card: str):
            if card not in CARDS:
                raise ValueError(f"{card} is not a valid card")

        return len(self) == 5 and all(map(is_valid_card, self))

    def __iter__(self):
        return iter(self.cards)

    def __contains__(self, item):
        return item in self.cards

    def __repr__(self):
        return f'{self.__class__.__name__}({"".join(self)})'

    def replace_joker(self, card: str):
        assert "J" in self.cards
        cards = list(self.cards)
        cards[cards.index("J")] = card
        return Hand(tuple(cards))  # type:ignore

    def remove_all_jokers(self) -> tuple[str, ...]:
        return tuple(card for card in self if card != "J")

    @staticmethod
    def from_str(cards_str: str):
        return Hand(tuple(cards_str))

    def __lt__(self, other: Hand):
        assert isinstance(other, Hand)
        for this_card, other_card in zip(self, other):
            if strength[this_card] == strength[other_card]:
                continue
            else:
                return strength[this_card] < strength[other_card]
        print("equal hands found", file=sys.stderr)
        return False

    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.cards == other.cards
        if isinstance(other, str):
            return "".join(self.cards) == other
        return False

    def __len__(self):
        return len(self.cards)


class HandKind(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def compute_hand_kind(hand: Hand) -> HandKind:
    counter = Counter(hand)
    most_common_parity = counter.most_common()[0][1]
    second_most_common_parity = (
        counter.most_common()[1][1] if len(counter) > 1 else None
    )
    if len(counter) == 1 and most_common_parity == 5:
        return HandKind.FIVE_OF_A_KIND
    elif len(counter) == 2 and most_common_parity == 4:
        return HandKind.FOUR_OF_A_KIND
    elif (
        len(counter) == 2 and most_common_parity == 3 and second_most_common_parity == 2
    ):
        return HandKind.FULL_HOUSE
    elif len(counter) == 3 and most_common_parity == 3:
        return HandKind.THREE_OF_A_KIND
    elif (
        len(counter) == 3 and most_common_parity == 2 and second_most_common_parity == 2
    ):
        return HandKind.TWO_PAIRS
    elif len(counter) == 4 and most_common_parity == 2:
        return HandKind.ONE_PAIR
    elif most_common_parity == 1:
        return HandKind.HIGH_CARD
    raise ValueError(f"unreachable code")


@dataclass
class CamelCardBid:
    hand: Hand
    kind: HandKind
    bid: int

    def __eq__(self, other):
        return isinstance(other, CamelCardBid) and self.kind == other.kind

    def __hash__(self):
        return hash(self.kind)


def sort_by_hand_kind(
    hands: tuple[tuple[Hand, int]], kind_compute_function=compute_hand_kind
) -> tuple[CamelCardBid]:
    # start with finding the absolute ranks
    return tuple(
        sorted(
            (
                CamelCardBid(hand, kind_compute_function(hand), bid)
                for hand, bid in hands
            ),
            key=attrgetter("kind"),
        )
    )


def sort_by_relative_strength(
    bids: tuple[CamelCardBid],
) -> list[tuple[CamelCardBid, int]]:
    grouped_bids = groupby(bids)
    result, rank = [], 1

    for key, group in grouped_bids:
        sorted_group = sorted(group, key=attrgetter("hand"))
        result.extend(
            (camel_card, r) for r, camel_card in enumerate(sorted_group, start=rank)
        )
        rank += len(sorted_group)

    return result


def parse_camel_cards_bids(data: str) -> tuple[tuple[Hand, int]]:
    return tuple(
        (
            Hand.from_str(hand_str.strip()),
            int(bid_str.strip()),
        )
        for hand_str, bid_str in (line.split(" ") for line in data.splitlines())
    )


def compute_total_winnings(filename: str, kind_compute_function):
    with open(filename) as f:
        hands = parse_camel_cards_bids(f.read())
        bids = sort_by_hand_kind(hands, kind_compute_function)
        weighted_bids = sort_by_relative_strength(bids)
        sum_prod = sum(
            camel_card.bid * relative_strength
            for camel_card, relative_strength in weighted_bids
        )
        return sum_prod


def part1(filename: str) -> int:
    global CARDS, strength
    CARDS = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
    strength = {card: len(CARDS) - index for index, card in enumerate(CARDS, start=1)}
    return compute_total_winnings(filename, compute_hand_kind)


# --- Part Two ---
# To make things a little more interesting, the Elf introduces one additional rule.
# Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.
#
# To balance this, J cards are now the weakest individual cards, weaker even than 2.
# The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.
#
# J cards can pretend to be whatever card is best for the purpose of determining hand type;
# for example, QJJQ2 is now considered four of a kind.
# However, for the purpose of breaking ties between two hands of the same type,
# J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.
#
# Now, the above example goes very differently:
#
#   32T3K 765
#   T55J5 684
#   KK677 28
#   KTJJT 220
#   QQQJA 483
# 32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
# KK677 is now the only two pair, making it the second-weakest hand.
# T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
# With the new joker rule, the total winnings in this example are 5905.
#
# Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?


def get_strongest_most_common_card(hand: Hand) -> str:
    assert "J" in hand and hand != "JJJJJ"

    counter = Counter(hand.remove_all_jokers())
    results, most_common = [], counter.most_common()
    highest_count = most_common[0][1]
    for card, count in most_common:
        if count != highest_count:
            break
        results.append(card)

    results.sort(key=lambda c: strength[c], reverse=True)
    return results[0]


def compute_hand_kind_with_joker(hand: Hand) -> HandKind:
    if "J" not in hand or hand == "JJJJJ":
        return compute_hand_kind(hand)

    card = get_strongest_most_common_card(hand)
    hand = hand.replace_joker(card)
    return compute_hand_kind_with_joker(hand)


def part2(filename: str) -> int:
    global CARDS, strength
    CARDS = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")
    strength = {card: len(CARDS) - index for index, card in enumerate(CARDS, start=1)}
    return compute_total_winnings(filename, compute_hand_kind_with_joker)


day7 = AOCChallenge(7, part1, part2)
__all__ = day7
