import argparse
import warnings
import numpy as np
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser(
                    prog='Commandline script to rank-inverse normal transform numeric data',
                    description='\n'.join([
                        'Rank-inverse normal transforms numeric data, leaves NaNs as NaN'
                    ]))
parser.add_argument('file', help='file to mapcolumn data to')
parser.add_argument('--header', default=True, action=argparse.BooleanOptionalAction, help='use --no-header if file does not have a header')
parser.add_argument('--delim', '-d', default='\t', help='delimiter of the file input and output')
parser.add_argument('--axis', '-a', default=1, help='axis to apply transformation along (0=columns, 1=rows)')#
parser.add_argument('--output', '-o', default='file_INT.tsv', help='name of the output file')
parser = parser.parse_args()

print('Running script with the following arguments')
print(parser)

def rank_inverse_normal(x):
    # Rank the values
    # Remove warnings of pandas argsort:
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        transformed_line = x.argsort().astype(float)
    transformed_line[x.isna()] = np.nan
    transformed_line += 0.5
    transformed_line /= transformed_line.max() + 1
    # Transform them to a normal distribution
    transformed_line = transformed_line.apply(stats.norm.ppf)
    return transformed_line

if parser.header:
    df = pd.read_csv(parser.file, sep=parser.delim)
else:
    df = pd.read_csv(parser.file, sep=parser.delim, header=None)
df_transformed = df.apply(rank_inverse_normal, axis=parser.axis)

df_transformed.to_csv(parser.output, sep=parser.delim, index=False)
