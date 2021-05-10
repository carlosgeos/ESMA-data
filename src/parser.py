import pandas as pd
from lxml import etree

# XML namespaces ESMA uses. ISO 20022 is an universal financial
# industry message scheme defined here:
# https://www.iso20022.org/catalogue-messages/additional-content-messages/business-application-header-bah

TMP_DIR = "/tmp/"


def get_namespace(root):
    """Peeks at the Document element to check its namespace and returns
    it.

    """
    return etree.QName(next((node for node in root.find("Pyld", namespaces=root.nsmap)
                             if etree.QName(node).localname == "Document"), None)).namespace


def get_elem_1(node, ns, elem):
    try:
        res = node.find(f"{{{ns}}}{elem}").text
    except AttributeError:
        res = None
    return res


def get_elem_2(node, ns, elem1, elem2):
    try:
        res = node.find(f"{{{ns}}}{elem1}").find(f"{{{ns}}}{elem2}").text
    except AttributeError:
        res = None
    return res


def get_elem_3(node, ns, elem1, elem2, elem3):
    try:
        res = node.find(f"{{{ns}}}{elem1}") \
                  .find(f"{{{ns}}}{elem2}") \
                  .find(f"{{{ns}}}{elem3}").text
    except AttributeError:
        res = None
    return res


def parse_non_equity(instrument, file_name):
    """Given an Non-Equity Instrument as input, returns a DataFrame with
    the same data

    """
    print(f"Parsing {file_name}")
    rows = []
    tree = etree.parse(file_name)
    root = tree.getroot()
    ns = get_namespace(root)

    report_header = root.find("Pyld", namespaces=root.nsmap).find(f"{{{ns}}}Document") \
                                                            .find(f"{{{ns}}}FinInstrmRptgNonEqtyTradgActvtyRslt") \
                                                            .find(f"{{{ns}}}RptHdr")
    report_period_from = get_elem_3(report_header, ns, "RptgPrd", "FrDtToDt", "FrDt")
    report_period_to = get_elem_3(report_header, ns, "RptgPrd", "FrDtToDt", "ToDt")

    for node in root.find("Pyld", namespaces=root.nsmap).find(f"{{{ns}}}Document") \
                                                        .find(f"{{{ns}}}FinInstrmRptgNonEqtyTradgActvtyRslt") \
                                                        .findall(f"{{{ns}}}NonEqtyTrnsprncyData"):
        row = {
            "isin": get_elem_1(node, ns, "Id"),
            "instr_class": get_elem_1(node, ns, "FinInstrmClssfctn"),
            "liquidity": get_elem_1(node, ns, "Lqdty"),
            "nb_of_txns": get_elem_2(node, ns, "Sttstcs", "TtlNbOfTxsExctd"),
            "vol_of_txns": get_elem_2(node, ns, "Sttstcs", "TtlVolOfTxsExctd"),
            "pre_trade_lis": get_elem_2(node, ns, "PreTradLrgInScaleThrshld", "Amt"),
            "post_trade_lis": get_elem_2(node, ns, "PstTradLrgInScaleThrshld", "Amt"),
            "pre_trade_ssti": get_elem_2(node, ns, "PreTradInstrmSzSpcfcThrshld", "Amt"),
            "post_trade_ssti": get_elem_2(node, ns, "PstTradInstrmSzSpcfcThrshld", "Amt"),
            "period_from": get_elem_3(node, ns, "RptgPrd", "FrDtToDt", "FrDt"),
            "period_to": get_elem_3(node, ns, "RptgPrd", "FrDtToDt", "ToDt"),
            "report_period_from": report_period_from,
            "report_period_to": report_period_to,
            "file_name": file_name,
            "upload_ts": instrument["timestamp"]
        }
        rows.append(row)

    return pd.DataFrame.from_dict(rows)


def parse_equity(instrument, file_name):
    """Given an Equity Instrument as input, returns a DataFrame with the
    same data

    """
    print(f"Parsing {file_name}")
    rows = []
    tree = etree.parse(file_name)
    root = tree.getroot()
    ns = get_namespace(root)

    report_header = root.find("Pyld", namespaces=root.nsmap).find(f"{{{ns}}}Document") \
                                                            .find(f"{{{ns}}}FinInstrmRptgEqtyTradgActvtyRslt") \
                                                            .find(f"{{{ns}}}RptHdr")
    report_period_from = get_elem_3(report_header, ns, "RptgPrd", "FrDtToDt", "FrDt")
    report_period_to = get_elem_3(report_header, ns, "RptgPrd", "FrDtToDt", "ToDt")
    for node in root.find("Pyld", namespaces=root.nsmap).find(f"{{{ns}}}Document") \
                                                        .find(f"{{{ns}}}FinInstrmRptgEqtyTradgActvtyRslt") \
                                                        .findall(f"{{{ns}}}EqtyTrnsprncyData"):
        row = {
            "isin": get_elem_1(node, ns, "Id"),
            "instr_class": get_elem_1(node, ns, "FinInstrmClssfctn"),
            "liquidity": get_elem_1(node, ns, "Lqdty"),
            "methodology": get_elem_1(node, ns, "Mthdlgy"),
            "adt": get_elem_2(node, ns, "Sttstcs", "AvrgDalyTrnvr"),
            "avt": get_elem_2(node, ns, "Sttstcs", "AvrgTxVal"),
            "nb_of_txns": get_elem_2(node, ns, "Sttstcs", "TtlNbOfTxsExctd"),
            "vol_of_txns": get_elem_2(node, ns, "Sttstcs", "TtlVolOfTxsExctd"),
            "lis": get_elem_2(node, ns, "Sttstcs", "LrgInScale"),
            "sms": get_elem_2(node, ns, "Sttstcs", "StdMktSz"),
            "adnte": get_elem_2(node, ns, "Sttstcs", "AvrgDalyNbOfTxs"),
            "market": get_elem_2(node, ns, "RlvntMkt", "Id"),
            "market_adnte": get_elem_2(node, ns, "RlvntMkt", "AvrgDalyNbOfTxs"),
            "period_from": get_elem_3(node, ns, "RptgPrd", "FrDtToDt", "FrDt"),
            "period_to": get_elem_3(node, ns, "RptgPrd", "FrDtToDt", "ToDt"),
            "report_period_from": report_period_from,
            "report_period_to": report_period_to,
            "file_name": file_name,
            "upload_ts": instrument["timestamp"]
        }
        rows.append(row)

    return pd.DataFrame.from_dict(rows)
