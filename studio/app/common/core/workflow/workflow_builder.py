from typing_extensions import Self

from studio.app.common.schemas.workflow import WorkflowConfig


class WorkflowConfigBuilder:
    def __init__(self):
        self._nodeDict = None
        self._edgeDict = None

    def set_config(self, config: WorkflowConfig) -> Self:
        self._nodeDict = config.nodeDict
        self._edgeDict = config.edgeDict
        return self

    def set_node_dict(self, nodeDict) -> Self:
        self._nodeDict = nodeDict
        return self

    def set_edge_dict(self, edgeDict) -> Self:
        self._edgeDict = edgeDict
        return self

    def build(self) -> WorkflowConfig:
        return WorkflowConfig(self._nodeDict, self._edgeDict)
