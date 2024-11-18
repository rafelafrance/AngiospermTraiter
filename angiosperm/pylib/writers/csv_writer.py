from collections import defaultdict

import pandas as pd


def write(pages, csv_file):
    rows = []

    for page in pages.values():
        merged = defaultdict(list)
        merged["taxon"].append(page.taxon)

        for trait in page.all_traits:
            for key, value in trait.formatted().items():
                if value:
                    merged[key].append(value)

        traits: dict[str, str] = {
            k: " | ".join(sorted(set(v))) for k, v in merged.items()
        }

        rows.append(traits)

    df = pd.DataFrame(rows)

    df.to_csv(csv_file, index=False)
