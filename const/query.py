GET_START_DATE: str = """
    SELECT fileddate AS date FROM public.snp500_key ORDER BY fileddate ASC LIMIT 1;
    """

GET_COMPANY: str = """
    SELECT DISTINCT *
    FROM public.snp500_ticker
    ORDER BY cik ASC;
"""

GET_DATA_ALL: str = """
    SELECT a.fileddate AS date , CASE WHEN CHAR_LENGTH(b.tokenized::text) > 102
    THEN SUBSTRING(b.tokenized::TEXT,3,103)
    ELSE SUBSTRING(b.tokenized::TEXT,2,1)
    END AS "{dataType}"
    FROM public.snp500_key a
    LEFT JOIN public.snp500_tokenized b ON a.acc = b.acc
    LEFT JOIN public.snp500_ticker c ON a.cik = c.cik
    WHERE (c.ticker = UPPER('{ticker}') OR a.cik = '{cik}') AND a.fileddate BETWEEN '{startDate}' AND '{endDate}'
    ORDER BY a.fileddate DESC;
"""

GET_DATA_TYPE: str = """
    SELECT a.fileddate AS date , CASE WHEN CHAR_LENGTH(b.tokenized::text) > 102
    THEN SUBSTRING(b.tokenized::TEXT,3,103)
    ELSE SUBSTRING(b.tokenized::TEXT,2,1)
    END AS "{dataType}"
    FROM public.snp500_key a
    LEFT JOIN public.snp500_tokenized b ON a.acc = b.acc
    LEFT JOIN public.snp500_ticker c ON a.cik = c.cik
    WHERE (c.ticker = UPPER('{ticker}') OR a.cik = '{cik}') AND a.fileddate BETWEEN '{startDate}' AND '{endDate}' AND a.type = UPPER('{fileType}')
    ORDER BY a.fileddate DESC;
"""