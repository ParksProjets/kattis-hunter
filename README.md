# Kattis Hunter

This project aims to hack [Duck Hunt][duck-hunt] problem (from KTH Kattis). As
validation tests from Kattis side are not random, we can try to recover them
using at best all the information that Kattis can provide. Kattis does not
provide much information on a run, but still gives CPU time (in second, with two
digits after the decimal point). This allows us to output a number between 0 and
1600 at each execution (which can hold about 10.5 bits of information).

**NOTES: Running this script without `--tos` argument may break Kattis [Terms
of Service][tos]. See section *Automated access* for more information.**


## Python dependencies

This script depends on some external Python libraries. You can find the
dependency in file `requirements.txt`. Install them by running the following
command: `python3 -m pip install -r requirements.txt`.


## How to use this script

TODO.

`python3 kattishunter`




## License

This project is released under the MIT license.  
See `LICENSE` file at the root of the project for more information.


[duck-hunt]: https://kth.kattis.com/problems/kth.ai.duckhunt
[tos]: https://kth.kattis.com/help/tos
