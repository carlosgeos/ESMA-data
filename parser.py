import pandas as pd
from lxml import etree

# XML namespaces ESMA uses. ISO 20022 is an universal financial
# industry message scheme defined here:
# https://www.iso20022.org/catalogue-messages/additional-content-messages/business-application-header-bah
ns1 = "urn:iso:std:iso:20022:tech:xsd:head.003.001.01"
ns2 = "urn:iso:std:iso:20022:tech:xsd:DRAFT5auth.045.001.01"


def get_liquidity(node):
    try:
        res = True if node.find(f"{{{ns2}}}Lqdty").text == "true" else False
    except AttributeError:
        res = None
    return res


def get_threshold(node, field):
    try:
        res = int(node.find(f"{{{ns2}}}{field}").find(f"{{{ns2}}}Amt").text)
    except AttributeError:
        res = None
    return res


def get_threshold_currency(node, field):
    try:
        res = node.find(f"{{{ns2}}}{field}").find(f"{{{ns2}}}Amt").get("Ccy")
    except AttributeError:
        res = None
    return res


def parse_non_eqty(file_name, file_type):
    """Given

    """
    rows = []
    tree = etree.parse(file_name)
    root = tree.getroot()
    for node in root.find(f"{{{ns1}}}Pyld").find(f"{{{ns2}}}Document") \
                                           .find(f"{{{ns2}}}FinInstrmRptgNonEqtyTradgActvtyRslt") \
                                           .findall(f"{{{ns2}}}NonEqtyTrnsprncyData"):
        row = {"file_type": file_type,
               "isin": node.find(f"{{{ns2}}}Id").text,
               "liquidity": get_liquidity(node),
               "pre_trade_lis_threshold": get_threshold(node, "PreTradLrgInScaleThrshld"),
               "pre_trade_lis_threshold_currency": get_threshold_currency(node, "PreTradLrgInScaleThrshld"),
               "post_trade_lis_threshold": get_threshold(node, "PstTradLrgInScaleThrshld"),
               "post_trade_lis_threshold_currency": get_threshold_currency(node, "PstTradLrgInScaleThrshld"),
               "pre_trade_ssti_threshold": get_threshold(node, "PreTradInstrmSzSpcfcThrshld"),
               "pre_trade_ssti_threshold_currency": get_threshold_currency(node, "PreTradInstrmSzSpcfcThrshld"),
               "post_trade_ssti_threshold": get_threshold(node, "PstTradInstrmSzSpcfcThrshld"),
               "post_trade_ssti_threshold_currency": get_threshold_currency(node, "PstTradInstrmSzSpcfcThrshld")}
        rows.append(row)

    return pd.DataFrame.from_dict(rows)


def parse_eqty():
    """Given an Equity Instrument - xml file - as input, it will return a
    DataFrame with the same

    """
    pass
