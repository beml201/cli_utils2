suppressPackageStartupMessages({
    library(magrittr)
    library(dplyr)
    library(argparser)
})
parser <- arg_parser(paste(
    'Align a phenotype file with omic data column headers',
    '', sep='\n'))
parser %<>% add_argument('omic_file', nargs=1, help='file with headers of columns given as ids, tab separated')
parser %<>% add_argument('pheno_file', nargs=1, help='file of phenotype data, tab separated')
parser %<>% add_argument('--output', nargs=1, help='file name to write out', default='phenotypes_aligned.tsv')
parser %<>% parse_args

cat(paste(
    'Running script with the following arguments',
    paste('  - Omic File:', parser$omic_file),
    paste('  - Phenotype File:', parser$pheno_file),
    paste('  - Output:', parser$output),
    '', sep='\n')
)

# Get the order of the initial file
omics <- file(parser$omic_file) %>%
            scan(what='', nlines=1, sep='\t') %>%
            data.frame(id=.)
omics$row_number <- 1:nrow(omics)

pheno <- read.csv(parser$pheno_file, sep='\t')
out <- omics %>% left_join(pheno, by=c('id'=names(pheno)[1]))
out <- out[order(out$row_number),]
# Remove duplicates based on row number
out <- out[!duplicated(out$row_number),]
out <- subset(out, select=-row_number)
names(out) <- names(pheno)

write.table(out, parser$output, sep='\t', row.names=F, col.names=T, quote=F)