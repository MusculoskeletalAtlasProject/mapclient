"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""
from os.path import join, dirname
import re, os

_SECTION_HEADER_RE = '\[(.*)\]'
_DEFAULT_ANNOTATION_FILENAME = 'annotation.rdf'
#_PHYSIOME_NAMESPACE = 'http://physiomeproject.org/workflow/1.0/rdf-schema'
_NAMESPACE_RE = '<{0}/{1}/rdf-schema#([^>]+)> <{0}/{1}/rdf-schema#([^>]+)> <{0}/{1}/rdf-schema#([^>]+)>.'
_NAMESPACE_FORMAT = '<{0}/{1}/rdf-schema#{2}>'  


class AnnotationTool(object):

    def __init__(self):
        self._vocab = Vocabulary()
        self._readVocabulary()
        self._triple_store = []
    
    def _readVocabulary(self):
        with open(join(dirname(__file__), 'annotation.voc')) as f:
            content = f.readlines()
    
        section_header_re = re.compile(_SECTION_HEADER_RE)
        
        section = ''
        for line in content:
            hash_index = line.find('#')
            line = line[:hash_index]
            if line:
                section_header = section_header_re.match(line)
                if section_header:
                    section = section_header.group(1)
                else:
                    if section == 'terms':
                        self._vocab.addTerm(line.strip())
                    else:
                        split_line = line.split(': ')
                        if len(split_line) == 2:
                            tag, value = split_line[0], split_line[1]
                            if tag == 'namespace':
                                self._vocab.setNamespace(value.strip())
                            elif tag == 'version':
                                self._vocab.setVersion(value.strip())          
    
    def getTerms(self):
        return self._vocab._terms
    
    def rdfFormOfTerm(self, term):
        t = term.strip()
        if t in self._vocab._terms:
            return _NAMESPACE_FORMAT.format(self._vocab._namespace, self._vocab._version, t)
        
        return None
    
    def serialize(self, location, rdf_file=None):
        annotation = ''#@prefix pp: <http://physiomeproject.org/workflow/1.0/>.\n'
        for triple in self._triple_store:
            annotation = annotation + _NAMESPACE_FORMAT.format(self._vocab._namespace, self._vocab._version, triple[0]) + ' ' \
                                    + _NAMESPACE_FORMAT.format(self._vocab._namespace, self._vocab._version, triple[1]) + ' ' \
                                    + _NAMESPACE_FORMAT.format(self._vocab._namespace, self._vocab._version, triple[2]) + '.\n'
            
        if rdf_file:
            annotationfile = os.path.join(location, rdf_file)
        else:
            annotationfile = os.path.join(location, _DEFAULT_ANNOTATION_FILENAME)
        f = open(annotationfile, 'w')
        f.write(annotation)
        f.close()
    
    def deserialize(self, location, rdf_file=None):
        re_string = _NAMESPACE_RE.format(self._vocab._namespace, self._vocab._version)
        s = re.compile(re_string)
        
        if rdf_file:
            annotationfile = os.path.join(location, rdf_file)
        else:
            annotationfile = os.path.join(location, _DEFAULT_ANNOTATION_FILENAME)

        if os.path.exists(annotationfile):
            f = open(annotationfile, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                r = s.match(line)
                if r:
                    self.addTriple(r.group(1), r.group(2), r.group(3))
    
    def addTriple(self, subj, pred, obj):
        self._triple_store.append((subj, pred, obj))
        
    def tripleCount(self):
        return len(self._triple_store)
    
    def getTriple(self, index):
        return self._triple_store[index]
    
    def getTriples(self):
        return self._triple_store
    
    def clear(self):
        self._triple_store = []
    
    
class Vocabulary(object):
    
    
    def __init__(self):
        self._namespace = None
        self._version = None
        self._terms = []
            
    def setNamespace(self, namespace):
        self._namespace = namespace
        
    def setVersion(self, version):
        self._version = version
        
    def addTerms(self, terms):
        self._terms.extend(terms)
        
    def addTerm(self, term):
        self._terms.append(term)
        
        
            
            
            
        
        
        