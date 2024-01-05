import argparse

parser = argparse.ArgumentParser(
                    prog='Commandline dictionary mapper',
                    description='\n'.join([
                        'Python script to map a column of a given file to columns based on a given alternate file',
                        'Ignores missing values'
                    ]))
parser.add_argument('file', help='file to mapcolumn data to')
parser.add_argument('dict', help='file containing the old and new names for the column')
parser.add_argument('--output', '-o', default='mapped_file', help='name of the output file')
parser.add_argument('--file-delim', '-fd', default='\t', help='delimiter of the file')
parser.add_argument('--dict-delim', '-dd', default='\t', help='set delim as "excel" to read an excel file instead, requires the pandas module')
parser.add_argument('--file-ncol', default=0, type=int, help='index of column to modify')
parser.add_argument('--dict-ncols', nargs=2, type=int, default=[0,1], help='indices of key,value pairs for the dictionary')
parser.add_argument('--file-col', help='name of the column to modify (overrules -ncol)')
parser.add_argument('--dict-cols', nargs=2, help='names of the columns of key,value pairs (overrules -ncols)')
parser.add_argument('--file-header', default=True, action=argparse.BooleanOptionalAction, help='use --no-file-header if the main file does not have a header')
parser.add_argument('--dict-header', default=True, action=argparse.BooleanOptionalAction, help='use --no-dict-header if the dictionary file does not have a header')
parser = parser.parse_args()

print('Running script with the following arguments')
print(parser)

if parser.dict_delim == 'excel':
    import pandas as pd
    # Set the column indices based on the names given
    if parser.dict_cols is not None:
        col_names = pd.read_excel(parser.dict, nrows=1).columns.to_list()
        parser.dict_ncols[0] = col_names.index(parser.dict_cols[0])
        parser.dict_ncols[1] = col_names.index(parser.dict_cols[1])
    if parser.dict_header == False:
        mapper = pd.read_excel(parser.dict, header=None)
    else:
        mapper = pd.read_excel(parser.dict)
    mapper.index = mapper.iloc[:, parser.dict_ncols[0]]
    mapper = mapper.iloc[:, parser.dict_ncols[1]].to_dict()
else:
    mapper = dict()
    with open(parser.dict) as f:
        if parser.dict_cols is not None:
            col_names = next(f).strip().split(parser.dict_delim)
            parser.dict_ncols[0] = col_names.index(parser.dict_cols[0])
            parser.dict_ncols[1] = col_names.index(parser.dict_cols[1])
        if parser.dict_header == True and parser.dict_cols is not None:
            next(f)
        for line in f:
            line = line.strip().split(parser.dict_delim)
            mapper[line[parser.dict_ncols[0]]] = line[parser.dict_ncols[1]]

with open(parser.file, 'r') as f:
    with open(parser.output, 'w') as f_out:
        if parser.file_header == True:
            line = next(f)
            f_out.write(line)
            if parser.file_col is not None:
                line = line.strip().split(parser.file_delim)
                parser.file_ncol = line.index(parser.file_col)
        for line in f:
            line = line.strip().split(parser.file_delim)
            try:
                line[parser.file_ncol] = mapper[line[parser.file_ncol]]
                f_out.write(parser.file_delim.join(line))
                f_out.write('\n')
            except:
                pass