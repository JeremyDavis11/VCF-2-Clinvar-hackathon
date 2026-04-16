import pandas as pd

COLS = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]


def _validate_vcf_cols(df):
    missing = [col for col in COLS if col not in df.columns]

    if missing:
        raise ValueError(f"Error: Input VCF missing required columns: {missing}")


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
    cols = None

    try:
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith("##"):
                    meta.append(line.strip())
                elif line.startswith("#CHROM"):
                    cols = line.strip().lstrip("#").split("\t")
                    break

            if cols is None:
                raise ValueError("VCF file missing #CHROM header line")

            try:
                df = pd.read_csv(f, sep="\t", names=cols)
            except (ValueError, pd.errors.ParserError) as e:
                raise ValueError(f"Unable to parse file as VCF: {filepath}") from e
            _validate_vcf_cols(df)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"VCF file not found: {filepath}") from e

    df["CHROM"] = df["CHROM"].astype(str)
    try:
        df["POS"] = df["POS"].astype(int)
    except ValueError as e:
        raise ValueError("VCF column 'POS' is non-numeric") from e

    return df, meta


# For debugging
if __name__ == "__main__":
    from config import DEMO_VCF

    df, meta = parse_vcf(DEMO_VCF)
    print(f"Meta lines: {len(meta)}")
    print(f"Variants loaded: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
