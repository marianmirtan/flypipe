from flypipe.node import node
from flypipe.node_graph import NodeGraph, RunStatus


class TestNodeGraph:
    def test_calculate_graph_run_status_1(self):
        @node(type="pandas")
        def t1():
            return

        @node(type="pandas")
        def t2():
            return

        @node(type="pandas")
        def t3():
            return

        @node(type="pandas", dependencies=[t1.select('c1'),
                                           t2.select('c1'),
                                           t3.select('c1')])
        def t4():
            return

        @node(type="pandas", dependencies=[t2.select('c1'),
                                           t3.select('c1')])
        def t5():
            return

        @node(type="pandas", dependencies=[t4.select('c1'),
                                           t5.select('c1')])
        def t6():
            return

        graph = NodeGraph(t6)
        graph.calculate_graph_run_status("t6", ["t4"])

        assert graph.get_node("t1")['run_status'] == RunStatus.SKIP
        assert graph.get_node("t2")['run_status'] == RunStatus.ACTIVE
        assert graph.get_node("t3")['run_status'] == RunStatus.ACTIVE
        assert graph.get_node("t4")['run_status'] == RunStatus.SKIP
        assert graph.get_node("t5")['run_status'] == RunStatus.ACTIVE
        assert graph.get_node("t6")['run_status'] == RunStatus.ACTIVE

    def test_calculate_graph_run_status_2(self):
        @node(type="pandas")
        def t1():
            return

        @node(type="pandas")
        def t2():
            return

        @node(type="pandas")
        def t3():
            return

        @node(type="pandas", dependencies=[t1.select('c1'),
                                           t2.select('c1'),
                                           t3.select('c1')])
        def t4():
            return

        @node(type="pandas", dependencies=[t2.select('c1'),
                                           t3.select('c1')])
        def t5():
            return

        @node(type="pandas", dependencies=[t5.select('c1'),
                                           t4.select('c1')])
        def t6():
            return

        graph = NodeGraph(t6)
        graph.calculate_graph_run_status("t6", ["t4"])

        assert graph.get_node("t1")['run_status']==RunStatus.SKIP
        assert graph.get_node("t2")['run_status']==RunStatus.ACTIVE
        assert graph.get_node("t3")['run_status']==RunStatus.ACTIVE
        assert graph.get_node("t4")['run_status']==RunStatus.SKIP
        assert graph.get_node("t5")['run_status']==RunStatus.ACTIVE
        assert graph.get_node("t6")['run_status']==RunStatus.ACTIVE

    def test_get_nodes_depth(self):
        """
        t1 - t3 - t5
           / |
        t2 - t4
        """
        @node(type="pandas")
        def t1():
            return

        @node(type="pandas")
        def t2():
            return

        @node(type="pandas", dependencies=[t1.select('dummy'), t2.select('dummy')])
        def t3():
            return

        @node(type="pandas", dependencies=[t3.select('dummy'), t2.select('dummy')])
        def t4():
            return

        @node(type="pandas", dependencies=[t4.select('dummy')])
        def t5():
            return

        graph = NodeGraph(t5)
        assert graph.get_depth_map() == {'t1': 0, 't2': 0, 't3': 1, 't4': 1, 't5': 2}
