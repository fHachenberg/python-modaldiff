Modal Diff
==========

Motivation
----------

Software tests using text diff normally follow the procedure

* system under test creates output file
* output file is compared to an accepted reference state using text diff

This approach is very simple but has a few shortcomings:

* if user names or file system locations are present in the output,
  the reference state is dependant of the user and os environment
  the test runs under. This limits transferability of a test which
  is a basic quality of software tests.
* numerical calculations introduce rounding errors which can as well
  complicate the management of reference states because normally even
  in the exact same environment results of numerical calculations differ
  between Debug and Release builds.

One popular approach to handle problems of transferability are diff ignores.
Using regular expressions, lines are scanned for patterns and -if found- the
line is ignored in calculating the textual difference between output and reference.

Modal diff aims to solve the problem by introducing "diff modes". By enriching
the output using pseudo-xml-Tags, the file is splitted into ranges of lines.
For each range, another method can be used to compare it to the reference state.

Examples of modes
-----------------

numdiff ===

    <tio:numdiff expr="
    (skip 2 lines)
        (n times
            (int>0)(s+)(real 0.69315~0.00001)(s+)(real 0.69315~0.00001)(s+)(real 6.93147E-01~1E-3)(s+)(real 693.14718E-03~1E-3))" skip_emptylines="true">

                 1    1    2    2    3    3    4    4    5    5    6    6    7    7
        ....5....0....5....0....5....0....5....0....5....0....5....0....5....0....5
          1   2.00000    0.69315E+00   0.69315E+000    6.93147E-01  693.14718E-03
          2   1.80000    0.58779E+00   0.58779E+000    5.87787E-01  587.78661E-03
          3   1.60000    0.47000E+00   0.47000E+000    4.70004E-01  470.00358E-03
          4   1.40000    0.33647E+00   0.33647E+000    3.36472E-01  336.47212E-03
          5   1.20000    0.18232E+00   0.18232E+000    1.82321E-01  182.32140E-03
          6   1.00000   -0.17881E-06  -0.17881E-006   -1.78814E-07 -178.81395E-09
          7   0.80000   -0.22314E+00  -0.22314E+000   -2.23144E-01 -223.14376E-03
          8   0.60000   -0.51083E+00  -0.51083E+000   -5.10826E-01 -510.82587E-03
          9   0.40000   -0.91629E+00  -0.91629E+000   -9.16291E-01 -916.29112E-03
         10   0.20000   -0.16094E+01  -0.16094E+001   -1.60944E+00   -1.60944E+00

    </tio:numdiff>

numdiff-Ranges are compared using numerical tolerances ... TO BE CONTINUED
