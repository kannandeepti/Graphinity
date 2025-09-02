# Add paths to PDB files to the ddG data csvs.

from pathlib import Path
import pandas as pd

def split_and_add_paths(data_path: Path, pdb_wt_path: Path, pdb_mut_path: Path):
    """
    Add paths to PDB files to the ddG data csvs.

    :param data_path: Path to the ddG data csvs.
    :param pdb_wt_path: Path to directory containingwt PDB files.
    :param pdb_mut_path: Path to directory containing mut PDB files.
    """
    df = pd.read_csv(data_path)
    wt_paths = []
    mut_paths = []
    for row in df.itertuples():
        pdb_id, mutation = row.complex.split("_")
        wt_paths.append(pdb_wt_path / f"{pdb_id}_{row.ab_chain}_{row.ag_chain}_{mutation}-wt.pdb")
        mut_paths.append(pdb_mut_path / f"{pdb_id}_{row.ab_chain}_{row.ag_chain}_{mutation}-mut.pdb")
    df['chain_prot1'] = df['ab_chain']
    df['chain_prot2'] = df['ag_chain']
    df["pdb_wt"] = wt_paths
    df["pdb_mut"] = mut_paths

    #split by train/test/val
    train_df = df[df["split"] == "train"]
    val_df = df[df["split"] == "val"]
    test_df = df[df["split"] == "test"]
    train_df.to_csv(data_path.parent / f"{data_path.stem}_train-w_paths.csv", index=False)
    val_df.to_csv(data_path.parent / f"{data_path.stem}_val-w_paths.csv", index=False)
    test_df.to_csv(data_path.parent / f"{data_path.stem}_test-w_paths.csv", index=False)

if __name__ == "__main__":
    pdb_mut_path = Path("data/ddg_synthetic/Flex_ddG/pdb_mut")
    pdb_wt_path = Path("data/ddg_synthetic/Flex_ddG/pdb_wt")
    for split_type in ["70", "90", "100", "none"]:
        data_path = Path(f"data/ddg_synthetic/Flex_ddG/cdr_seqid_cutoffs/Synthetic_FlexddG_ddG_20829-cutoff_{split_type}.csv")
        split_and_add_paths(data_path, pdb_wt_path, pdb_mut_path)