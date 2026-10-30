from itertools import combinations
import numpy as np 
import pandas as pd 

from data_defs import (Company,LABELS,Assignment,CorrSummary,MIN_CLUSTER_SIZE,SCORING_START_MONTH, SCORING_MONTHS)

def load_universe(path) -> list[Company]:
    """ Read data/universe.csv (columns ticker,name,label) into a list of comapny 

    Data: list of company -- Self-referntial (empty/ first + rest), so the template is a loop .
    Label is an enumeration , so each row is checked. 


    >>> import io 
    >>> f = io.StringIO( "ticker,name,label\\nVRTX,Vertex,biotech\\nPFE,Pfizer,pharma\\n")
    >>> cs = load_universe(f)
    >>> len(cs),cs[0].ticker, cs[1].label
    (2, 'VRTX', 'pharma')
    >>> load_universe(io.StringIO("ticker,name,label\\n"))
    []
    >>> load_universe(io.StringIO("ticker,name,label\\nX,XCo,device\\n"))
    Traceback (most recent call last):
    ...
    ValueError: unknown label: device
    """
    df=pd.read_csv(path)
    out:list[Company]=[]
    for row in df.to_dict("records"):
        if row ["label"] not in LABELS:
            raise ValueError(f"unknown label: {row["label"]}")
        out.append(Company(str(row["ticker"]),str(row["name"]),row["label"]))
    return out    

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("doctests finished")