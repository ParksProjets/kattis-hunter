# Kattis Hunter

This project aims to hack [Duck Hunt][duck-hunt] problem (from KTH Kattis). As
validation tests from Kattis side are not random, we can try to recover them
using at best all the information that Kattis can provide. Kattis does not
provide much information on a run, but still gives CPU time (in second, with two
digits after the decimal point). This allows us to output a number between 0 and
1600 at each execution (which can hold about 10.6 bits of information).

**Please note the following:**

- For KTH students who have not read [EECS code of honour][coh], this repository
  does not contain solutions for the [Duck Hunt][duck-hunt] problem (at least
  not directly).

- Running this script without `--tos` argument may break Kattis [Terms of
  Service][tos]. See section *Automated access* for more information.


## Python dependencies

This script depends on some external Python libraries. You can find the
dependency in file `requirements.txt`. Install them by running the following
command: `python3 -m pip install -r requirements.txt`.


## How to use this script

The script has 3 sub-commands: `run`, `results` and `answer`.

The `run` sub-command run the script for the given nulber of steps. For example,
use `python3 kattishunter run 1` for running Kattis Hunter for one step. The
current step will be saved in file `cache.json`.

The `results` sub-command show current results (from `cache.json` file).

The `answer` sub-command generates a C++ that will make your target score when
ran on Kattis. Use it like this: `python3 kattishunter answer 10,20,30,40,50,60`
(with the target score for each environment).


## License

This project is released under the MIT license.  
See `LICENSE` file at the root of the project for more information.


[duck-hunt]: https://kth.kattis.com/problems/kth.ai.duckhunt
[coh]: https://www.kth.se/en/eecs/utbildning/hederskodex/inledning-1.17237
[tos]: https://kth.kattis.com/help/tos
