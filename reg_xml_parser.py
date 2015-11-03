#!/usr/bin/env python

__author__ = 'vinokurovy'

import argparse
import sys
import os
import json
import codecs

from lxml import etree
from pprint import pprint

from regulation.tree import *

import settings

reload(sys)
sys.setdefaultencoding('UTF8')


def write_layer(layer_object, reg_number, notice, layer_type):

    layer_path = os.path.join(settings.JSON_ROOT, layer_type, reg_number)
    if not os.path.exists(layer_path):
        os.mkdir(layer_path)
    layer_file = os.path.join(layer_path, notice)
    json.dump(layer_object, open(layer_file, 'w'), indent=4, separators=(',', ':'))


def parser_driver(regulation_file, notice_doc_numbers=[]):

    with open(regulation_file, 'r') as f:
        reg_xml = f.read()
    xml_tree = etree.fromstring(reg_xml)
    reg_tree = build_reg_tree(xml_tree)
    reg_number = reg_tree.label[0]

    paragraph_markers = build_paragraph_marker_layer(xml_tree)
    internal_citations = build_internal_citations_layer(xml_tree)
    external_citations = build_external_citations_layer(xml_tree)
    terms = build_terms_layer(xml_tree)
    meta = build_meta_layer(xml_tree)
    toc = build_toc_layer(xml_tree)
    keyterms = build_keyterm_layer(xml_tree)

    reg_tree.include_children = True
    reg_json = reg_tree.to_json()

    notice = notice_doc_numbers[0]

    write_layer(reg_json, reg_number, notice, 'regulation')
    write_layer(meta, reg_number, notice, 'layer/meta')
    write_layer(paragraph_markers, reg_number, notice, 'layer/paragraph-markers')
    write_layer(internal_citations, reg_number, notice, 'layer/internal-citations')
    write_layer(external_citations, reg_number, notice, 'layer/external-citations')
    write_layer(terms, reg_number, notice, 'layer/terms')
    write_layer(toc, reg_number, notice, 'layer/toc')
    write_layer(keyterms, reg_number, notice, 'layer/keyterms')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', dest='operation', action='store')
    parser.add_argument('regulation-file', nargs='?')
    parser.add_argument('notice-doc-numbers', nargs='*')

    args = vars(parser.parse_args())

    if args['regulation-file'] is not None:
        parser_driver(args['regulation-file'], args['notice-doc-numbers'])