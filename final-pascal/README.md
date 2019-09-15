# Final code in Pascal

This repository contains the final code generator for Pascal. It generates a
Pascal code that produces a target score, between 0 and 1188.


## Generate the code

For generating the Pascal code, run the following command:

```sh
make SCORES=23,10,10,0,0,0
```

The generated Pascal code is in the file `objects/finalcode.pas`.  
If you only want to generate the final Pascal code without trying to compile it,
run `make code` command like this:

```sh
make code SCORES=23,10,10,0,0,0
```
