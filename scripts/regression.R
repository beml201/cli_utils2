suppressPackageStartupMessages({
    library(magrittr)
    library(argparser)
})
parser <- arg_parser(paste(
    'Script to run regressions phenotype and omic data',
    'Phenotype data should be aligned (same order) as the omic data',
    'Phenotype data is assumed to have to form: ID Phenotype_of_interest covars',
    'Accepts tab-delimited data only',
    '', sep='\n'))
parser %<>% add_argument('omic_file', nargs=1, help='omic file, tab-delimited (columns match the rows of the phneotype file)')
parser %<>% add_argument('pheno_file', nargs=1, help='phenotype file, tab-delimited')
parser %<>% add_argument('--output', nargs=1, help='file name to write out', default='regression_results.tsv')
parser %<>% add_argument('--logistic', help='flag to run a logistic regression instead of linear', flag=TRUE)
parser %<>% parse_args
cat(paste(
    'Running script with the following arguments',
    paste('  - Omic File:', parser$omic_file),
    paste('  - Phenotype File:', parser$pheno_file),
    paste('  - Output:', parser$output),
    paste('  - Logistic Regression:', parser$logistic),
    '',
    sep='\n')
)
#parser <- list(omic_file='prot.quant', pheno_file='pheno_gender_bin.tsv', logistic=TRUE, output='tmp.txt')
# Read the data inputs
omic <- read.csv(parser$omic_file, sep='\t')
pheno <- read.csv(parser$pheno_file, sep='\t')
if('y' %in% names(pheno)){names(pheno)[which(names(pheno)=='y')] <- 'y.pheno'}
if('x' %in% names(pheno)){names(pheno)[which(names(pheno)=='x')] <- 'x.pheno'}
names(pheno)[2] <- 'y'
pheno <- pheno[,-1, drop=FALSE]

# Headers
beta_name <- ifelse(parser$logistic, 'LogOR', 'BETA')
col_names <- c('N', beta_name, 'SE', 'P')
write(paste(col_names, collapse='\t'), file=parser$output, append=FALSE)
for(row in 1:nrow(omic)){
    pheno$x <- as.vector(omic[row,]) %>% as.numeric
    n <- nrow(na.omit(pheno))
    if(n==0){
        write(paste(rep('NA',4),collapse='\t'), file=parser$output, append=TRUE)
        next
    }
    if(parser$logistic){
        results <- glm(y ~ ., data=pheno, family='binomial')
    }else{
        results <- lm(y ~ ., data=pheno)
    }
    results %<>% summary
    results <- results$coefficients['x',]
    beta <- results[1]
    se <- results[2]
    p <- results[4]
    out <- paste(n, beta, se, p, sep='\t')
    write(out, file=parser$output, append=TRUE)
}
