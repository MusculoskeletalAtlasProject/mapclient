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
from rdflib.term import URIRef
from rdflib.graph import Graph
from rdflib.namespace import RDFS

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME


def serializeWorkflowAnnotation():
    g = Graph()

    workflow = URIRef(DEFAULT_WORKFLOW_PROJECT_FILENAME)

    #     g.add((workflow, RDF.type, URIRef("http://physiomeproject.org/workflow/1.0/rdf-schema#workflowproject")))
    g.add((workflow, RDFS.subClassOf, URIRef("http://physiomeproject.org/workflow/1.0/rdf-schema#workflowproject")))

    return g.serialize(format='xml')
