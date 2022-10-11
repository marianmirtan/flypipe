from abc import ABC
from flypipe.exceptions import ErrorDependencyNoSelectedColumns, ErrorNodeTypeInvalid
from flypipe.utils import DataFrameType


class Transformation:
    TYPE_MAP = {
        'pyspark': DataFrameType.PYSPARK,
        'pandas': DataFrameType.PANDAS,
        'pandas_on_spark': DataFrameType.PANDAS_ON_SPARK,
    }

    def __init__(self,
                 function,
                 type: str,
                 description=None,
                 tags=None,
                 dependencies=None,
                 output=None,
                 spark_context=False):
        self.function = function
        try:
            self.type = self.TYPE_MAP[type]
        except KeyError:
            raise ErrorNodeTypeInvalid(f'Invalid type {type}, expected one of {",".join(self.TYPE_MAP.keys())}')
        self.description = description or "No description"
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.dependencies_selected_columns = {}

        if self.dependencies:
            self.dependencies = sorted(self.dependencies, key=lambda d: d.__name__)
            for dependency in self.dependencies:
                if not dependency.selected_columns:
                    raise ErrorDependencyNoSelectedColumns(f'Selected columns of dependency {dependency.__name__} not specified')
                self.dependencies_selected_columns[dependency.__name__] = dependency.selected_columns

        self._provided_inputs = {}
        self.output_schema = output
        self.spark_context = spark_context
        self.selected_columns = []
        self.node_graph = None

    @property
    def __name__(self):
        """Return the name of the wrapped transformation rather than the name of the decorator object"""
        # TODO: replace with regex only a-z and 0-9 digits
        return self.varname.replace(".", "_")

    @property
    def varname(self):
        """Return the variable name of the wrapped transformation rather than the name of the decorator object"""
        return self.function.__name__

    @property
    def __doc__(self):
        """Return the docstring of the wrapped transformation rather than the docstring of the decorator object"""
        return self.function.__doc__