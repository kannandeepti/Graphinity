""" Parse pdb files to parquet files. """

from pathlib import Path
from multiprocessing import Pool
import os
import sys
from tqdm import tqdm

sys.path.append(os.getcwd())

from src.ddg_regression.base import utils


def parse_pdb_to_parquet(pdb_file: Path):
    parquet_path = pdb_file.with_suffix('.parquet')
    if parquet_path.exists():
        try:
            pdb_df = pd.read_parquet(parquet_path)
            return
        except:
            pass
    pdb_df = utils.parse_pdb_to_parquet(pdb_file, parquet_path, lmg_typed=True, ca=False)

if __name__ == "__main__":
    pdb_wt = Path("data/ddg_synthetic/Flex_ddG/pdb_wt")
    pdb_mut = Path("data/ddg_synthetic/Flex_ddG/pdb_mut")
    pdb_files_to_parse = list(pdb_wt.glob("*.pdb")) + list(pdb_mut.glob("*.pdb"))
    #put the following for loop in a multiprocessing pool
    with Pool() as pool:
        for _ in tqdm(pool.imap(parse_pdb_to_parquet, pdb_files_to_parse), total=len(pdb_files_to_parse)):
            pass