"""
The following RegEx pertains to the 7 main PLOS journals and the defunct PLOS Clinical Trials, as well as PLOS Currents.
"""

import re
import os

from . import get_corpus_dir

regex_match_prefix = r"^10\.1371/"
regex_body_match = (r"((journal\.p[a-zA-Z]{3}\.[\d]{7})"
                    r"|(annotation/[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$))")
regex_suffix_match = r"(\.[rs][0-9]{3})?"   # matches reviews and supplementary materials
regex_body_search = (r"((journal\.p[a-zA-Z]{3}\.[\d]{7})"
                     r"|(annotation/[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}))")
regex_body_currents = (r"((currents\.[a-zA-Z]{2,9}\.[a-zA-Z0-9]{32}$)"
                       r"|(currents\.RRN[\d]{4}$)"
                       r"|([a-zA-Z0-9]{13}$)"
                       r"|([a-zA-Z0-9]{32}$))")
regex_file_search = (r"((journal\.p[a-zA-Z]{3}\.[\d]{7})"
                     r"|(plos\.correction\.[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}))")
full_doi_regex_match = re.compile(regex_match_prefix+regex_body_match+regex_suffix_match)
full_doi_regex_search = re.compile(r"10\.1371/journal\.p[a-zA-Z]{3}\.[\d]{7}"
                                   "|10\.1371/annotation/[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}")
currents_doi_regex = re.compile(regex_match_prefix+regex_body_currents)
file_regex_match = re.compile(regex_file_search+r"\.xml")
regex_type_match = r"(article)|(peerReview)"
regex_file_suffix = r"&type=((manuscript)|(supplementary))"

BASE_URL = 'https://journals.plos.org/plosone/'
external_url_regex_match = re.compile(re.escape(BASE_URL) + re.escape("article/file?id=10.1371/") +
                                      regex_body_search + regex_suffix_match + regex_file_suffix)
plos_url_regex_match = re.compile(re.escape("https://journals.plos.org/") + r"[a-z]+/" +
                                  regex_type_match + re.escape("?id=10.1371/") +
                                  regex_body_search + regex_suffix_match)


def validate_doi(doi):
    """
    For an individual string, tests whether the full string is in a valid PLOS DOI format or not
    Example: '10.1371/journal.pbio.2000777' is True, but '10.1371/journal.pbio.2000777 ' is False
    :return: True if string is in valid PLOS DOI format; False if not
    """
    return bool(full_doi_regex_match.search(doi))


def validate_filename(filename):
    """
    For an individual string, tests whether the full string is in a valid article file. This can take two forms.
    
    TODO: Officially document these two forms and give them names. Also, Explain the example below.
    
    Example: 'allofplos_xml/journal.pbio.2000777.xml' is True, but 'allofplos_xml/journal.pbio.20007779.xml' is False
    :filename: A string with a file name
    :return: True if string is in a valid PLOS corpus article format; False if not
    """
    if file_regex_match.search(filename):
        return True
    else:
        return False


def validate_file_url(url):
    """
    For an individual string, tests whether the full string is in a valid article (manuscript) url format or not
    Example: 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pcbi.0020147&type=manuscript' is True,
    but 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pcbi.0020147' is False

    Urls leading to files containing supplementary material are valid.
    example: 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0222522.s002&type=supplementary' is True

    :return: True if string is in a valid PLOS file url; False if not
    """
    return bool(external_url_regex_match.match(url))


def validate_plos_url(url):
    """
    Tests whether the given `url` string is a valid PLOS website format.

    :return True if string is in a valid PLOS url; False otherwise
    """
    return bool(plos_url_regex_match.search(url))


def find_valid_dois(doi):
    """
    For an individual string, searches for any valid PLOS DOIs within it and returns them
    :return: list of valid PLOS DOIs contained within string
    """
    return full_doi_regex_search.findall(doi)


def show_invalid_dois(doi_list):
    """
    Checks to see whether a list of PLOS DOIs follow the correct format. Used mainly to determine
    if linked DOI fields in other articles (such as retractions and corrections) are correct.
    :return: list of DOI candidates that don't match PLOS's pattern
    """
    return list(filter(lambda x: not validate_doi(x), doi_list))


def currents_doi_filter(doi_list):
    """
    Checks to see whether a list of PLOS Currents DOIs follow the correct format. Used mainly to determine
    if linked DOI fields in PMC articles are correct.
    :return: list of DOI candidates that don't match Currents' pattern
    """
    return list(filter(lambda x: not bool(currents_doi_regex.search(x)), doi_list))
