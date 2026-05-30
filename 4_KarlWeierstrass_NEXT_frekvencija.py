"""
4_KarlWeierstrass_NEXT_frekvencija — agregacija kombinacija iz 8 NEXT modela
i frekvencija pojavljivanja brojeva 1..39.

Citamo TXT izlaze iz svih 8 modela (NEXT1..NEXT8), vadimo svaki tuple
(a, b, c, d, e, f, g) sa 7 brojeva 1..39, brisemo duplikate unutar fajla,
izbacujemo placeholder (1,2,3,4,5,6,7) i racunamo ukupno frekvenciju.

Output:
  print u konzolu
  4_KarlWeierstrass_NEXT_frekvencija.txt
  4_KarlWeierstrass_NEXT_frekvencija.png  (tabela frekvencije)
"""

import os
import re
from collections import Counter

import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
TXT_OUT = os.path.join(HERE, "4_KarlWeierstrass_NEXT_frekvencija.txt")
PNG_OUT = os.path.join(HERE, "4_KarlWeierstrass_NEXT_frekvencija.png")

NEXT_FILES = [
    ("NEXT1", "3_KarlWeierstrass_NEXT1_2a3b.txt", 4),
    ("NEXT2", "3_KarlWeierstrass_NEXT2_2a3c.txt", 4),
    ("NEXT3", "3_KarlWeierstrass_NEXT3_2a3d.txt", 4),
    ("NEXT4", "3_KarlWeierstrass_NEXT4_2a3e.txt", 6),
    ("NEXT5", "3_KarlWeierstrass_NEXT5_2b3a.txt", 3),
    ("NEXT6", "3_KarlWeierstrass_NEXT6_2b3b.txt", 3),
    ("NEXT7", "3_KarlWeierstrass_NEXT7_2b3e.txt", 3),
    ("NEXT8", "3_KarlWeierstrass_NEXT8_2c3b.txt", 3),
]

PLACEHOLDER = (1, 2, 3, 4, 5, 6, 7)
N_MIN, N_MAX = 1, 39
K_PICK = 7

COMBO_RE = re.compile(
    r"\(\s*(\d{1,2})\s*,\s*(\d{1,2})\s*,\s*(\d{1,2})\s*,\s*(\d{1,2})\s*,"
    r"\s*(\d{1,2})\s*,\s*(\d{1,2})\s*,\s*(\d{1,2})\s*\)"
)


def extract_combos(text):
    """Vadi sve 7-tuple-ove iz teksta, vraca unique listu (po prvom pojavljivanju)."""
    seen = set()
    out = []
    for match in COMBO_RE.finditer(text):
        combo = tuple(sorted(int(x) for x in match.groups()))
        if any(v < N_MIN or v > N_MAX for v in combo):
            continue
        if len(set(combo)) != K_PICK:
            continue
        if combo == PLACEHOLDER:
            continue
        if combo in seen:
            continue
        seen.add(combo)
        out.append(combo)
    return out


all_combos = []
per_file_rows = []
mismatch_notes = []

for label, fname, expected in NEXT_FILES:
    path = os.path.join(HERE, fname)
    if not os.path.exists(path):
        mismatch_notes.append(f"  {label}: fajl ne postoji -> {path}")
        per_file_rows.append((label, fname, expected, 0, []))
        continue
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    combos = extract_combos(text)
    per_file_rows.append((label, fname, expected, len(combos), combos))
    all_combos.extend(combos)
    if len(combos) != expected:
        mismatch_notes.append(
            f"  {label}: ocekivano {expected}, pronadjeno {len(combos)}"
        )

total = len(all_combos)

counter = Counter()
for combo in all_combos:
    for num in combo:
        counter[num] += 1

# Sortiranje: count desc, pa broj desc (kad su isti, veci broj prvo)
freq_rows = sorted(counter.items(), key=lambda kv: (-kv[1], -kv[0]))

# ─── ispis ─────────────────────────────────────────────────────────
lines = []
lines.append("4_KarlWeierstrass_NEXT_frekvencija")
lines.append("=" * 60)
lines.append("")
lines.append("Izvor: 8 NEXT TXT fajlova (placeholder (1,2,3,4,5,6,7) izbacen).")
lines.append("")
lines.append("Kombinacije po fajlu:")
lines.append("-" * 60)
for label, fname, expected, got, combos in per_file_rows:
    status = "OK" if got == expected else f"MISMATCH (ocekivano {expected})"
    lines.append(f"{label}  [{fname}]  combos: {got}  {status}")
    for combo in combos:
        lines.append(f"    {combo}")
    lines.append("")

lines.append("-" * 60)
lines.append(f"UKUPNO jedinstvenih kombinacija (bez placeholder-a): {total}")
lines.append("")

if mismatch_notes:
    lines.append("Napomena - razlika u broju kombinacija:")
    lines.extend(mismatch_notes)
    lines.append("")

lines.append("Frekvencija pojavljivanja brojeva 1..39 (sort: count desc, broj desc):")
lines.append("-" * 60)
lines.append(f"  {'rang':<6}{'broj':>6}{'count':>10}")
for rank, (num, cnt) in enumerate(freq_rows, start=1):
    lines.append(f"  {rank:<6}{num:>6}{cnt:>10}")

# Brojevi koji se nikad nisu pojavili
missing = [n for n in range(N_MIN, N_MAX + 1) if n not in counter]
if missing:
    lines.append("")
    lines.append(f"Brojevi bez pojavljivanja ({len(missing)}): {missing}")

text = "\n".join(lines) + "\n"
print(text)

with open(TXT_OUT, "w", encoding="utf-8") as f:
    f.write(text)

print(f"TXT saved -> {TXT_OUT}")
print()


# ─── tabela frekvencije kao PNG ──────────────────────────────────────
table_headers = ["rang", "broj", "count"]
table_rows = [[str(rank), str(num), str(cnt)]
              for rank, (num, cnt) in enumerate(freq_rows, start=1)]

max_count = max((cnt for _, cnt in freq_rows), default=1)

fig, ax = plt.subplots(figsize=(7, 12))
ax.axis("off")
ax.set_title(
    f"Frekvencija pojavljivanja brojeva 1..39\n"
    f"(8 NEXT modela, {total} jedinstvenih kombinacija)",
    fontsize=13,
    fontweight="bold",
    pad=14,
)

table = ax.table(
    cellText=table_rows,
    colLabels=table_headers,
    colWidths=[0.18, 0.20, 0.22],
    cellLoc="center",
    loc="center",
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.0, 1.25)

for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor("#444444")
    cell.set_linewidth(0.5)
    if row == 0:
        cell.set_facecolor("#1f2937")
        cell.set_text_props(color="white", weight="bold")
        cell.set_height(cell.get_height() * 1.1)
    else:
        cnt = int(table_rows[row - 1][2])
        shade = 0.25 + 0.60 * (cnt / max_count)
        cell.set_facecolor((1.0 - 0.55 * shade, 1.0 - 0.20 * shade, 1.0 - 0.05 * shade))
        if col == 2:
            cell.set_text_props(weight="bold")

fig.tight_layout()
plt.show()
fig.savefig(PNG_OUT, dpi=200, bbox_inches="tight")
print(f"PNG saved -> {PNG_OUT}")
print()


"""
čita svih 8 TXT fajlova 3_KarlWeierstrass_NEXT*_*.txt
regex-om vadi sve (a, b, c, d, e, f, g) tuple-ove
skida duplikate unutar fajla (npr. glavna prognoza koja se ponavlja kao z=0 kandidat)
izbacuje placeholder (1, 2, 3, 4, 5, 6, 7)
proverava broj kombinacija po fajlu i obeležava OK / MISMATCH
ispisuje sve kombinacije, pa frekvenciju brojeva 1..39 sortirano count↓, tie-break veći broj prvo
snima izlaz i u 4_KarlWeierstrass_NEXT_frekvencija.txt
"""



"""
4_KarlWeierstrass_NEXT_frekvencija
============================================================

Izvor: 8 NEXT TXT fajlova (placeholder (1,2,3,4,5,6,7) izbacen).

Kombinacije po fajlu:
------------------------------------------------------------
NEXT1  [3_KarlWeierstrass_NEXT1_2a3b.txt]  combos: 4  OK
    (1, 6, 13, 24, 31, 37, 39)
    (2, 6, 14, 20, 25, 38, 39)
    (3, 8, 9, 17, 23, 30, 37)
    (4, 16, 19, 20, 23, 28, 32)

NEXT2  [3_KarlWeierstrass_NEXT2_2a3c.txt]  combos: 4  OK
    (1, 10, 12, 15, 16, 32, 39)
    (1, 8, 11, 21, 22, 25, 32)
    (3, 13, 23, 24, 29, 30, 37)
    (5, 13, 16, 28, 29, 35, 37)

NEXT3  [3_KarlWeierstrass_NEXT3_2a3d.txt]  combos: 4  OK
    (2, 3, 4, 7, 11, 21, 25)
    (2, 3, 5, 10, 20, 23, 26)
    (4, 6, 13, 18, 22, 32, 34)
    (6, 11, 17, 19, 21, 27, 34)

NEXT4  [3_KarlWeierstrass_NEXT4_2a3e.txt]  combos: 6  OK
    (3, 20, 21, 25, 26, 29, 33)
    (1, 6, 15, 17, 18, 25, 37)
    (2, 5, 12, 19, 21, 33, 38)
    (4, 5, 6, 15, 24, 29, 31)
    (6, 7, 11, 17, 23, 25, 26)
    (7, 19, 20, 23, 24, 25, 32)

NEXT5  [3_KarlWeierstrass_NEXT5_2b3a.txt]  combos: 3  OK
    (1, 4, 6, 21, 27, 35, 38)
    (1, 22, 23, 24, 25, 31, 38)
    (2, 12, 13, 25, 28, 31, 38)

NEXT6  [3_KarlWeierstrass_NEXT6_2b3b.txt]  combos: 3  OK
    (1, 4, 6, 10, 15, 20, 27)
    (1, 19, 25, 28, 31, 32, 34)
    (2, 11, 21, 28, 34, 35, 36)

NEXT7  [3_KarlWeierstrass_NEXT7_2b3e.txt]  combos: 3  OK
    (1, 7, 16, 18, 21, 24, 36)
    (2, 9, 11, 16, 27, 34, 36)
    (4, 5, 9, 10, 14, 21, 25)

NEXT8  [3_KarlWeierstrass_NEXT8_2c3b.txt]  combos: 3  OK
    (1, 10, 14, 16, 18, 20, 26)
    (2, 15, 19, 22, 29, 32, 37)
    (4, 8, 13, 15, 16, 25, 35)

------------------------------------------------------------
UKUPNO jedinstvenih kombinacija (bez placeholder-a): 30

Frekvencija pojavljivanja brojeva 1..39 (sort: count desc, broj desc):
------------------------------------------------------------
  rang    broj     count
  1         25        12
  2          1        10
  3         21         9
  4          6         9
  5          4         8
  6          2         8
  7         32         7
  8         23         7
  9         20         7
  10        16         7
  11        37         6
  12        24         6
  13        19         6
  14        15         6
  15        13         6
  16        11         6
  17        38         5
  18        34         5
  19        31         5
  20        29         5
  21        28         5
  22        10         5
  23         5         5
  24         3         5
  25        35         4
  26        27         4
  27        26         4
  28        22         4
  29        18         4
  30        17         4
  31         7         4
  32        39         3
  33        36         3
  34        14         3
  35        12         3
  36         9         3
  37         8         3
  38        33         2
  39        30         2

TXT saved -> /4_KarlWeierstrass_NEXT_frekvencija.txt

PNG saved -> /4_KarlWeierstrass_NEXT_frekvencija.png
"""
