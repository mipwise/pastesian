"""
This module will be called when "pastesian" package is executed from the command line, with the following syntax:

>> python -m pastesian -i <input_file or input_directory> -o <output_file or output_directory>

Take a look at https://github.com/ticdat/ticdat/tree/master/examples/expert_section/diet_simple_package for an example,
as well as at standard_main function inside ticdat package. The link https://github.com/ticdat/ticdat/issues/164
contains an example for running the package and testing data integrity, from command line.
"""

from ticdat import standard_main
from pastesian import input_schema, output_schema, solve


if __name__ == "__main__":
    standard_main(input_schema, output_schema, solve)
