# Part C - Interview Ready
# Q2: group_anagrams function
# Q3: Fix char_freq bugs

from collections import defaultdict


# ─────────────────────────────────────────────
# Q2 - group_anagrams
# Two words are anagrams if sorted characters match.
# Use sorted(word) as key in a defaultdict(list).
# ─────────────────────────────────────────────
def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    """Groups words by their anagram signature (sorted characters)."""
    anagram_map = defaultdict(list)
    for word in words:
        key = ''.join(sorted(word))   # e.g. 'eat' -> 'aet'
        anagram_map[key].append(word)
    return dict(anagram_map)


# ─────────────────────────────────────────────
# Q3 - Fixed char_freq
# Bug 1: freq[char] += 1 throws KeyError on first occurrence.
#         Fix: use freq.get(char, 0) + 1  OR  use defaultdict(int)
# Bug 2: sorted() on a dict returns only keys by default.
#         Fix: return list of (key, value) tuples by sorting freq.items()
# ─────────────────────────────────────────────
def char_freq(text: str) -> list[tuple[str, int]]:
    """Returns characters sorted by frequency (highest first) as (char, count) pairs."""
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1          # Bug 1 fixed

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)  # Bug 2 fixed
    return sorted_freq


# ─────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  PART C — INTERVIEW SOLUTIONS")
    print("=" * 50)

    print("\n[Q2] group_anagrams")
    words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
    result = group_anagrams(words)
    for key, group in result.items():
        print(f"    '{key}': {group}")

    print("\n[Q3] char_freq (fixed)")
    sample = "programming"
    freq_result = char_freq(sample)
    print(f"    Input: '{sample}'")
    print(f"    Output: {freq_result}")
