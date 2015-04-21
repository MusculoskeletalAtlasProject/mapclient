'''
Created on Mar 14, 2013

@author: hsorby
'''
import os, unittest

from PySide import QtCore

from mapclient.core.workflowscene import WorkflowScene, WorkflowDependencyGraph, MetaStep, Connection

from tests import utils

test_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources', 'core_test')

class DumbManager(object):

    def location(self):
        return self._location


class DumbStep(object):

    _ports = ['one', 'two', 'three']

    def isConfigured(self):
        return True

    def getName(self):
        return self._name

    def getIdentifier(self):
        return self._identifier

    def serialize(self, location):
        pass

    def deserialize(self, location):
        pass

    def execute(self):
        pass

    def setPortData(self, index, data):
        pass

    def getPortData(self, index):
        return None


class WorkflowSceneTestCase(unittest.TestCase):


    def assertIn(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" in "b"'''
        try:
            f = super(WorkflowSceneTestCase, self).assertIn
        except AttributeError:
            self.assertTrue(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertNotIn(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" NOT in "b"'''
        try:
            f = super(WorkflowSceneTestCase, self).assertNotIn
        except AttributeError:
            self.assertFalse(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def testCreate(self):

        s = WorkflowScene(DumbManager())
        self.assertTrue(s != None)

    def testItemAPI(self):

        item = MetaStep(DumbStep())
        s = WorkflowScene(DumbManager())
        s.addItem(item)
        self.assertEqual(len(s._items), 1)
        s.setItemPos(item, QtCore.QPoint(344, 404))
        self.assertEqual(s._items[item]._pos.x(), 344)
        self.assertEqual(s._items[item]._pos.y(), 404)
        s.setItemSelected(item, False)
        self.assertFalse(s._items[item]._selected)
        s.removeItem(item)
        self.assertEqual(len(s._items), 0)

    def testSaveLoad(self):
        test_conf = os.path.join(test_path, 'test.conf')
        dm = DumbManager()
        dm._location = test_conf

        s = WorkflowScene(dm)
        ws = QtCore.QSettings(test_conf, QtCore.QSettings.IniFormat)
        ds1 = DumbStep()
        ds1._identifier = '1'
        ds1._name = 'a'
        ds2 = DumbStep()
        ds2._identifier = '2'
        ds2._name = 'b'
        item1 = MetaStep(ds1)
        item2 = MetaStep(ds2)
        s.addItem(item1)
        s.addItem(item2)
        s.saveState(ws)
        del ws

        self.assertTrue(os.path.exists(test_conf))
        file_content = open(test_conf).read()
        self.assertIn('Point(0 0)', file_content)
        self.assertIn('name=a', file_content)
        self.assertIn('name=b', file_content)
        self.assertNotIn('selected=false', file_content)

        os.remove(test_conf)


class WorkflowDependencyGraphTestCase(unittest.TestCase):


    def assertIn(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" in "b"'''
        try:
            f = super(WorkflowDependencyGraphTestCase, self).assertIn
        except AttributeError:
            self.assertTrue(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertNotIn(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" NOT in "b"'''
        try:
            f = super(WorkflowDependencyGraphTestCase, self).assertNotIn
        except AttributeError:
            self.assertFalse(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertLess(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" less "b"'''
        try:
            f = super(WorkflowDependencyGraphTestCase, self).assertLess
        except AttributeError:
            self.assertTrue(a < b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def setUp(self):
        self._s = WorkflowScene(DumbManager())
        self._nodes = []
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))

    def tearDown(self):
        self._s.clear()
        self._nodes = []

    def testCreate(self):
        g = WorkflowDependencyGraph(self._s)
        self.assertTrue(g != None)

    def testGraph1(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[1], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(c1)

        self.assertTrue(g.canExecute())
        self.assertEqual(len(g._topologicalOrder), 2)
        self.assertEqual(g._topologicalOrder[0], self._nodes[0])
        self.assertEqual(g._topologicalOrder[1], self._nodes[1])

    def testGraph2(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[1], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(c1)
        self._s.addItem(c2)

        self.assertTrue(g.canExecute())
        self.assertEqual(len(g._topologicalOrder), 3)
        self.assertEqual(g._topologicalOrder[0], self._nodes[0])
        self.assertEqual(g._topologicalOrder[1], self._nodes[1])
        self.assertEqual(g._topologicalOrder[2], self._nodes[2])

    def testGraph3(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[1], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 0)
        c3 = Connection(self._nodes[2], 0, self._nodes[3], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(c3)
        self._s.addItem(c1)
        self._s.addItem(c2)

        self.assertTrue(g.canExecute())
        self.assertEqual(len(g._topologicalOrder), 4)
        self.assertEqual(g._topologicalOrder[0], self._nodes[0])
        self.assertEqual(g._topologicalOrder[1], self._nodes[1])
        self.assertEqual(g._topologicalOrder[2], self._nodes[2])
        self.assertEqual(g._topologicalOrder[3], self._nodes[3])

    def testGraph4(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[1], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 0)
        c3 = Connection(self._nodes[2], 0, self._nodes[3], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(self._nodes[4])
        self._s.addItem(self._nodes[5])
        self._s.addItem(c3)
        self._s.addItem(c1)
        self._s.addItem(c2)

        nodes = g._findAllConnectedNodes()
        self.assertEqual(4, len(nodes))
        self.assertIn(self._nodes[0], nodes)
        self.assertIn(self._nodes[1], nodes)
        self.assertIn(self._nodes[2], nodes)
        self.assertIn(self._nodes[3], nodes)
        self.assertNotIn(self._nodes[4], nodes)
        self.assertNotIn(self._nodes[5], nodes)

    def testGraph5(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[2], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 0)
        c3 = Connection(self._nodes[2], 0, self._nodes[3], 0)
        c4 = Connection(self._nodes[2], 0, self._nodes[4], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(self._nodes[4])
        self._s.addItem(self._nodes[5])
        self._s.addItem(c1)
        self._s.addItem(c2)
        self._s.addItem(c3)
        self._s.addItem(c4)

        nodes = g._findAllConnectedNodes()
        self.assertEqual(5, len(nodes))
        self.assertIn(self._nodes[0], nodes)
        self.assertIn(self._nodes[1], nodes)
        self.assertIn(self._nodes[2], nodes)
        self.assertIn(self._nodes[3], nodes)
        self.assertIn(self._nodes[4], nodes)
        self.assertNotIn(self._nodes[5], nodes)

        graph = g._calculateDependencyGraph()
        self.assertFalse(g._nodeIsDestination(graph, self._nodes[0]))
        self.assertFalse(g._nodeIsDestination(graph, self._nodes[1]))
        self.assertTrue(g._nodeIsDestination(graph, self._nodes[2]))
        self.assertTrue(g._nodeIsDestination(graph, self._nodes[3]))
        self.assertTrue(g._nodeIsDestination(graph, self._nodes[4]))
        self.assertFalse(g._nodeIsDestination(graph, self._nodes[5]))

        starting_set = g._findStartingSet(graph, nodes)

        self.assertEqual(2, len(starting_set))
        self.assertIn(self._nodes[0], starting_set)
        self.assertIn(self._nodes[1], starting_set)
        self.assertNotIn(self._nodes[2], starting_set)
        self.assertNotIn(self._nodes[3], starting_set)
        self.assertNotIn(self._nodes[4], starting_set)
        self.assertNotIn(self._nodes[5], starting_set)

        order = g._determineTopologicalOrder(graph, starting_set)
        self.assertEqual(5, len(order))
        index0 = order.index(self._nodes[0])
        index1 = order.index(self._nodes[1])
        index2 = order.index(self._nodes[2])
        index3 = order.index(self._nodes[3])
        index4 = order.index(self._nodes[4])
        self.assertLess(index1, index2)
        self.assertLess(index0, index2)
        self.assertLess(index2, index3)
        self.assertLess(index2, index4)

    def testGraph6(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[2], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 0)
        c3 = Connection(self._nodes[2], 0, self._nodes[3], 0)
        c4 = Connection(self._nodes[2], 0, self._nodes[4], 0)
        c5 = Connection(self._nodes[6], 0, self._nodes[0], 0)
        c6 = Connection(self._nodes[6], 0, self._nodes[1], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(self._nodes[4])
        self._s.addItem(self._nodes[5])
        self._s.addItem(self._nodes[6])
        self._s.addItem(c1)
        self._s.addItem(c2)
        self._s.addItem(c3)
        self._s.addItem(c4)
        self._s.addItem(c5)
        self._s.addItem(c6)

        nodes = g._findAllConnectedNodes()
        self.assertEqual(6, len(nodes))
        graph = g._calculateDependencyGraph()
        starting_set = g._findStartingSet(graph, nodes)
        self.assertEqual(1, len(starting_set))
        order = g._determineTopologicalOrder(graph, starting_set)
        self.assertEqual(6, len(order))
        index0 = order.index(self._nodes[6])
        index1 = order.index(self._nodes[1])
        self.assertLess(index0, index1)

    def testGraph7(self):
        '''
        Testing independent graphs
        '''
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[2], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 0)
        c3 = Connection(self._nodes[2], 0, self._nodes[3], 0)
        c4 = Connection(self._nodes[2], 0, self._nodes[4], 0)
        c5 = Connection(self._nodes[6], 0, self._nodes[5], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(self._nodes[4])
        self._s.addItem(self._nodes[5])
        self._s.addItem(self._nodes[6])
        self._s.addItem(c1)
        self._s.addItem(c2)
        self._s.addItem(c3)
        self._s.addItem(c4)
        self._s.addItem(c5)

        nodes = g._findAllConnectedNodes()
        self.assertEqual(7, len(nodes))
        graph = g._calculateDependencyGraph()
        starting_set = g._findStartingSet(graph, nodes)
        self.assertEqual(3, len(starting_set))
        order = g._determineTopologicalOrder(graph, starting_set)
        self.assertEqual(7, len(order))

    def testGraph8(self):
        '''
        Testing graph with loop
        '''
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[1], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 0)
        c3 = Connection(self._nodes[2], 0, self._nodes[3], 0)
        c4 = Connection(self._nodes[3], 0, self._nodes[4], 0)
        c5 = Connection(self._nodes[3], 0, self._nodes[5], 0)
        c6 = Connection(self._nodes[5], 0, self._nodes[6], 0)
        c7 = Connection(self._nodes[6], 0, self._nodes[2], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(self._nodes[4])
        self._s.addItem(self._nodes[5])
        self._s.addItem(self._nodes[6])
        self._s.addItem(c1)
        self._s.addItem(c2)
        self._s.addItem(c3)
        self._s.addItem(c4)
        self._s.addItem(c5)
        self._s.addItem(c6)
        self._s.addItem(c7)

        nodes = g._findAllConnectedNodes()
        self.assertEqual(7, len(nodes))
        graph = g._calculateDependencyGraph()
        starting_set = g._findStartingSet(graph, nodes)
        self.assertEqual(1, len(starting_set))
        order = g._determineTopologicalOrder(graph, starting_set)
        self.assertEqual(0, len(order))

    def testExecute(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], 0, self._nodes[2], 0)
        c2 = Connection(self._nodes[1], 0, self._nodes[2], 1)
        c3 = Connection(self._nodes[1], 1, self._nodes[2], 2)
        c4 = Connection(self._nodes[2], 0, self._nodes[3], 0)
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(c1)
        self._s.addItem(c2)
        self._s.addItem(c3)
        self._s.addItem(c4)
        g.canExecute()

        for _ in range(len(g._topologicalOrder)):
            g.execute()

class DictUtilsTestCase(unittest.TestCase):


    def assertIn(self, a, b, *args, **kwargs):
        ''''Python < v2.7 compatibility.  Assert "a" in "b"'''
        try:
            f = super(DictUtilsTestCase, self).assertIn
        except AttributeError:
            self.assertTrue(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def testReverseDict(self):
        d = {'a': ['1', '2'], 'b': ['2', '3']}
#         from collections import defaultdict
        rd = {}  # defaultdict(list)
        for k, v in d.items():
            for rk in v:
                rd[rk] = rd.get(rk, [])
                rd[rk].append(k)

        self.assertIn('1', rd)
        self.assertIn('2', rd)
        self.assertIn('3', rd)
        self.assertEqual(['a'], rd['1'])
        self.assertIn('a', rd['2'])
        self.assertIn('b', rd['2'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()
