__doc__ = """
Functions for write sequence data to sequence files.
"""

# Import pandas
import pandas as pd
import pandas_flavor as pf


# Import Biopython
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import Bio.Alphabet


def _write(dataframe, filename=None, schema='fasta', sequence_col='sequence',
           id_col='id', id_only=False, alphabet=None, **kwargs):
    """Write a PhyloPandas DataFrame to a sequence file.
    """
    # Check Alphabet if given
    if alphabet is None:
        alphabet = Bio.Alphabet.Alphabet()
    elif alphabet in ['dna', 'rna', 'protein', 'nucleotide']:
        alphabet = getattr(Bio.Alphabet, 'generic_{}'.format(alphabet))
    else:
        raise Exception(
            "The alphabet is not recognized. Must be 'dna', 'rna', "
            "'nucleotide', or 'protein'.")

    seq_records = []
    # Iterate through dataframe rows
    for i, row in dataframe.iterrows():
        seq = Seq(row[sequence_col], alphabet)
        # Create a SeqRecord and append to list.
        if id_only:
            record = SeqRecord(seq, id=row[id_col], name='', description='')
        else:
            record = SeqRecord(seq, id=row[id_col], name=row['name'],
                               description=row['description'])
        seq_records.append(record)

    # Write to disk or return string
    if filename is not None:
        SeqIO.write(seq_records, filename, format=schema, **kwargs)
    else:
        return "".join([s.format(schema) for s in seq_records])


@pf.register_dataframe_method
def to_fasta(df, filename=None, sequence_col='sequence',
             id_col='id', id_only=False, alphabet=None, **kwargs):
    """Write to fasta format.

    Parameters
    ----------
    filename : str
        File to write fasta string to. If no filename is given, a fasta string
        will be returned.
    sequence_col : str (default='sequence')
        Sequence column name in DataFrame.
    id_col : str (default='id')
        ID column name in DataFrame
    id_only : bool (default=False)
        If True, use only the ID column to label sequences in fasta.
    """
    return _write(df, filename=filename, schema='fasta',
                  sequence_col=sequence_col, id_col=id_col, id_only=id_only,
                  alphabet=None, **kwargs)


@pf.register_dataframe_method
def to_phylip(df, filename=None, sequence_col='sequence',
             id_col='id', alphabet=None, **kwargs):
    """Write to phylip format.

    Parameters
    ----------
    filename : str
        File to write phylip string to. If no filename is given, a fasta string
        will be returned.
    sequence_col : str (default='sequence')
        Sequence column name in DataFrame.
    """
    return _write(df, filename=filename, schema='phylip',
                  sequence_col=sequence_col, id_col=id_col, id_only=True,
                  alphabet=None, **kwargs)


@pf.register_dataframe_method
def to_clustal(df, filename=None, sequence_col='sequence',
             id_col='id', alphabet=None, **kwargs):
    """Write to CLUSTAL format.

    Parameters
    ----------
    filename : str
        File to write CLUSTAL string to. If no filename is given, a fasta string
        will be returned.
    sequence_col : str (default='sequence')
        Sequence column name in DataFrame.
    """
    return _write(df, filename=filename, schema='clustal',
                  sequence_col=sequence_col, id_col=id_col, id_only=True,
                  alphabet=None, **kwargs)

@pf.register_dataframe_method
def to_embl(df, alphabet, filename=None, sequence_col='sequence',
             id_col='id', **kwargs):
    """Write to EMBL format.

    Parameters
    ----------
    filename : str
        File to write EMBL string to. If no filename is given, a fasta string
        will be returned.
    sequence_col : str (default='sequence')
        Sequence column name in DataFrame.
    """
    return _write(df, filename=filename, schema='embl', sequence_col=sequence_col,
                  id_col=id_col, id_only=True, alphabet=alphabet, **kwargs)


@pf.register_dataframe_method
def to_nexus(df, alphabet, filename=None, sequence_col='sequence',
             id_col='id', id_only=False, **kwargs):
    """Write to NEXUS format.

    Parameters
    ----------
    filename : str
        File to write nexus string to. If no filename is given, a fasta string
        will be returned.
    sequence_col : str (default='sequence')
        Sequence column name in DataFrame.
    """
    return _write(df, alphabet=alphabet, filename=filename, schema='nexus',
                  sequence_col=sequence_col, id_col='id',
                  id_only=True, **kwargs)


@pf.register_dataframe_method
def to_swiss(df, filename=None, sequence_col='sequence',
             id_col='id', id_only=False, alphabet=None, **kwargs):
    """Write to SWISS format.

    Parameters
    ----------
    filename : str
        File to write SWISS string to. If no filename is given, a fasta string
        will be returned.
    sequence_col : str (default='sequence')
        Sequence column name in DataFrame.
    """
    return _write(df, alphabet=alphabet, filename=filename, schema='swiss',
                  sequence_col=sequence_col, id_col='id', id_only=True,
                  **kwargs)


@pf.register_dataframe_method
def to_fastq(df, filename=None, sequence_col='sequence',
             id_col='id', id_only=False, alphabet=None, **kwargs):
    """Write to FASTQ format.

    Parameters
    ----------
    filename : str
        File to write FASTQ string to. If no filename is given, a fasta string
        will be returned.
    sequence_col : str (default='sequence')
        Sequence column name in DataFrame.
    """
    return _write(df, filename=filename, schema='fastq',
                  sequence_col=sequence_col, id_col='id', id_only=True,
                  alphabet=None, **kwargs)
