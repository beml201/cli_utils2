# Reference commands

Often a completely separate script isn't actually necessary to manipulate your data. In these cases, a single bash line can do what you want. For these, I've created this file for you to copy, paste and alter the commands to suit your needs. Remember, a lot of these outputs can be piped (|) together to make things clearer.
For usability, files in or out are written like bash variables (ie `${file.in}, ${file.out}`)

### Split a file
The following will take only the first 5 columns (inclusive) of a file (tab delimited)
`cut -f-5 ${file.in} > ${file.out}`
Similarly, we can take columns 6 onwards using the following
`cut -f6- ${file.in} > ${file.out}`

### Take certain columns of a file
For this we can use awk. The following takes the field separator `tab` and the output field separator (OFS) `tab` and prints the first and fourth column
`awk -F '\t' -v OFS='\t' '{ print $1, $4 }' ${file.in} > ${file.out}`

### Paste columns together
To paste columsn together we use the following
`paste -d '\t' ${file1.in} ${file2.in} > ${file.out}`

### Remove a header
To remove everything but the top line
`tail -n +1 ${file.in} > ${file.out}`

To get just the header
`head -n1 ${file.in} > ${file.out}`