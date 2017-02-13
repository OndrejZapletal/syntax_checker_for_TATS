re = "^\s+(public|private|const|dim|redim)"

#[Public | Private] Const constname = expression
re = "^\s*(public|private)?\s+const\s+(\w+)"

# Dim varname[([subscripts])][, varname[([subscripts])]] . . .
re = "^\s*dim\s+(\w+)"

# ReDim [Preserve] varname(subscripts) [, varname(subscripts)] . . .
re = "^\s*redim\s+(preserve)?\s+(\w+)"

# Public | Private varname[([subscripts])][, varname[([subscripts])]] . . .
re = "^\s*(public|private)\s+(\w+)"
