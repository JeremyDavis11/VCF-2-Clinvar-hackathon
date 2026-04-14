import pandas as pd


def parse_vcf(filepath):
    """
    Parse a VCF file into a pandas DataFrame.

    Args:
        filepath: Path to the VCF file (str or Path)

    Returns:
        df   -- DataFrame with columns: CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO (+ sample columns if present)
        meta -- List of ## header lines
    """
    meta = []

    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("##"):
                meta.append(line.strip())
            elif line.startswith("#CHROM"):
                cols = line.strip().lstrip("#").split("\t")
                break

        df = pd.read_csv(f, sep="\t", names=cols)

    df["CHROM"] = df["CHROM"].astype(str)
    df["POS"] = df["POS"].astype(int)

    return df, meta


if __name__ == "__main__":
    from config import DEMO_VCF

    df, meta = parse_vcf(DEMO_VCF)
    print(f"Meta lines: {len(meta)}")
    print(f"Variants loaded: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
