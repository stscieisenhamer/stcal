"""Utility routines for Mutli-Accum Ramp Fitting
"""
import numpy as np

# Read Time in seconds
#   For Roman, the read time of the detectors is a fixed value and is currently
#   backed into code. Will need to refactor to consider the more general case.
#   Used to deconstruct the MultiAccum tables into integration times.
READ_TIME = 3.04

__all__ = ['ma_table_to_tau', 'ma_table_to_tbar']


def matable_to_readpattern(ma_table):
    """Convert read patterns to multi-accum lists

    Using Roman terminology, a "read pattern" is a list of resultants. Each element of this list
    is a list of reads that were combined, on-board, to create a resultant. An example read pattern is

    [[1], [2, 3], [4], [5, 6, 7, 8], [9, 10], [11]]

    This pattern has 6 resultants, the first consistent of the first read, the next consisting of reads 2 and 3,
    the third consists of read 4, and so on.

    A "Multi-accum table" is a short-hand version of the read pattern. It is a list of 2-tuples consisting of the following:

    (start_read, n_reads)

    For example, the above read pattern would be represented as, using lists instead of tuples:

    [[1, 1], [2, 2], [4, 1], [5, 4], [9,2], [11,1]]

    The example above, using this function, should perform as follows:
    >>> matable_to_readpattern([[1, 1], [2, 2], [4, 1], [5, 4], [9,2], [11,1]])
    [[1], [2, 3], [4], [5, 6, 7, 8], [9, 10], [11]]

    Parameters
    ----------
    ma_table : [(first_read, n_reads)[,...]]
        The multi-accum table to convert.

    Returns
    -------
    read_pattern : [[int[,...]][,...]]
        The read pattern that represents the given multi-accum table.
    """
    read_pattern = [list(range(start, start + len))
                    for start, len in ma_table]

    return read_pattern


def ma_table_to_tau(ma_table, read_time=READ_TIME):
    """Construct the tau for each resultant from an ma_table.

    .. math:: \\tau = \\overline{t} - (n - 1)(n + 1)\\delta t / 6n

    following Casertano (2022).

    Parameters
    ----------
    ma_table : list[list]
        List of lists specifying the first read and the number of reads in each
        resultant.

    Returns
    -------
    :math:`\\tau`
        A time scale appropriate for computing variances.
    """

    meantimes = ma_table_to_tbar(ma_table)
    nreads = np.array([x[1] for x in ma_table])
    return meantimes - (nreads - 1) * (nreads + 1) * read_time / 6 / nreads


def ma_table_to_tbar(ma_table, read_time=READ_TIME):
    """Construct the mean times for each resultant from an ma_table.

    Parameters
    ----------
    ma_table : list[list]
        List of lists specifying the first read and the number of reads in each
        resultant.

    Returns
    -------
    tbar : np.ndarray[n_resultant] (float)
        The mean time of the reads of each resultant.
    """
    firstreads = np.array([x[0] for x in ma_table])
    nreads = np.array([x[1] for x in ma_table])
    meantimes = read_time * firstreads + read_time * (nreads - 1) / 2
    # at some point I need to think hard about whether the first read has
    # slightly less exposure time than all other reads due to the read/reset
    # time being slightly less than the read time.
    return meantimes


def readpattern_to_matable(read_pattern):
    """Convert read patterns to multi-accum lists

    Using Roman terminology, a "read pattern" is a list of resultants. Each element of this list
    is a list of reads that were combined, on-board, to create a resultant. An example read pattern is

    [[1], [2, 3], [4], [5, 6, 7, 8], [9, 10], [11]]

    This pattern has 6 resultants, the first consistent of the first read, the next consisting of reads 2 and 3,
    the third consists of read 4, and so on.

    A "Multi-accum table" is a short-hand version of the read pattern. It is a list of 2-tuples consisting of the following:

    (start_read, n_reads)

    For example, the above read pattern would be represented as, using lists instead of tuples:

    [[1, 1], [2, 2], [4, 1], [5, 4], [9,2], [11,1]]

    The example above, using this function, should perform as follows:
    >>> readpattern_to_matable([[1], [2, 3], [4], [5, 6, 7, 8], [9, 10], [11]])
    [[1, 1], [2, 2], [4, 1], [5, 4], [9, 2], [11, 1]]

    Parameters
    ----------
    read_pattern : [[int[,...]][,...]]
        The read pattern to convert.

    Returns
    -------
    ma_table : [(first_read, n_reads)[,...]]
        The multi-accum table that represents the given read pattern.
    """
    ma_table = [[resultant[0], len(resultant)]
                for resultant in read_pattern]

    return ma_table
