import logging
from concurrent.futures import ThreadPoolExecutor, wait
from flypipe.node_graph import NodeGraph
from collections import namedtuple
from abc import ABC, abstractmethod
from types import FunctionType

logger = logging.getLogger(__name__)


NodeInput = namedtuple('NodeInput', ['node', 'schema'])


class Node(ABC):

    TYPES = {}
    TYPE = None

    def __init__(self, transformation, inputs=None, output=None):
        self.transformation = transformation
        self.inputs = []
        if inputs:
            for input_def in inputs:
                if isinstance(input_def, tuple):
                    node, schema = input_def
                    self.inputs.append(NodeInput(node, schema))
                elif isinstance(input_def, Node):
                    self.inputs.append(NodeInput(input_def, None))
                else:
                    raise TypeError(
                        f'Input {input_def} is {type(input_def)} but expected it to be either a tuple or an instance/subinstance of Node')
        self.output_schema = output
        self.node_graph = NodeGraph(self)

    @classmethod
    def get_class(cls, node_type):
        try:
            return cls.TYPES[node_type]
        except KeyError:
            raise ValueError(f'Invalid node type {node_type} specified, provide type must be one of {cls.TYPES.keys()}')

    @classmethod
    def register_node_type(cls, node_type_class):
        cls.TYPES[node_type_class.TYPE] = node_type_class

    @property
    def __name__(self):
        """Return the name of the wrapped transformation rather than the name of the decorator object"""
        return self.transformation.__name__

    @property
    def __doc__(self):
        """Return the docstring of the wrapped transformation rather than the docstring of the decorator object"""
        return self.transformation.__doc__

    def __call__(self, *args, **kwargs):
        return self.transformation(*args, **kwargs)

    @classmethod
    @abstractmethod
    def convert_dataframe(cls, df, destination_type):
        # TODO- is there a better place to put this? It seems a little out of place here
        pass

    def run(self):
        outputs = {}
        dependency_chain = self.node_graph.get_dependency_chain()

        def process_and_cache_node(node_obj, **inputs):
            outputs[node_obj.__name__] = self.process_node(node_obj, **inputs)
            try:
                self.validate_dataframe(node_obj.output_schema, outputs[node_obj.__name__])
            except TypeError as ex:
                raise TypeError(
                    f'Validation failure on node {node_name} when checking output schema: \n{str(ex)}')

        with ThreadPoolExecutor() as executor:
            for node_group in dependency_chain:
                logger.debug(f'Started processing group of nodes {node_group}')
                result_futures = []
                for node_name in node_group:
                    node_obj = self.node_graph.get_node(node_name)
                    try:
                        node_inputs = {}
                        for input_node, input_schema in node_obj.inputs:
                            # We need to ensure that the result of each input is converted to the same type as the node
                            # that's processing it.
                            input_value = input_node.convert_dataframe(outputs[input_node.__name__], node_obj.TYPE)
                            if input_schema:
                                try:
                                    input_value = self.validate_dataframe(input_schema, input_value)
                                except TypeError as ex:
                                    raise TypeError(
                                        f'Validation failure on node {node_name} when checking input node '
                                        f'{input_node.__name__}: \n{str(ex)}')
                            node_inputs[input_node.__name__] = input_value
                    except KeyError as ex:
                        raise ValueError(f'Unable to process transformation {node_obj.__name__}, missing input {ex.args[0]}')

                    logger.debug(f'Processing node {node_obj.__name__}')
                    result_futures.append(executor.submit(process_and_cache_node, node_obj, **node_inputs))
                logger.debug('Waiting for group of nodes to finish...')
                wait(result_futures)
                # This is not actually a no-op- if any exceptions occur during node processing they get re-raised when
                # calling result()
                [future.result() for future in result_futures]
                logger.debug('Finished processing group of nodes')
        return outputs[self.transformation.__name__]

    @classmethod
    def validate_dataframe(cls, schema, df):
        pass

    def process_node(self, node_obj, **inputs):
        return node_obj(**inputs)

    def plot(self):
        self.node_graph.plot()


def node(*args, **kwargs):
    """
    Decorator factory that returns the given function wrapped inside a Node class
    """
    def decorator(func):
        try:
            node_type = kwargs.pop('type')
        except KeyError:
            node_type = None
        return Node.get_class(node_type)(func, *args, **kwargs)
    return decorator
