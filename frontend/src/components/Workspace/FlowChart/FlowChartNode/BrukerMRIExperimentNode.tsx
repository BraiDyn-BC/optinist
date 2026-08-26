import { memo } from "react"
import { useSelector, useDispatch } from "react-redux"
import { Handle, Position, NodeProps } from "reactflow"

import { FileSelect } from "components/Workspace/FlowChart/FlowChartNode/FileSelect"
import {
  toHandleId,
  isValidConnection,
} from "components/Workspace/FlowChart/FlowChartNode/FlowChartUtils"
import { useHandleColor } from "components/Workspace/FlowChart/FlowChartNode/HandleColorHook"
import { NodeContainer } from "components/Workspace/FlowChart/FlowChartNode/NodeContainer"
import { HANDLE_STYLE } from "const/flowchart"
import { deleteFlowNodeById } from "store/slice/FlowElement/FlowElementSlice"
import { setInputNodeFilePath } from "store/slice/InputNode/InputNodeActions"
import {
  selectBrukerMRIExperimentNodeSelectedFilePath,
  selectInputNodeDefined,
} from "store/slice/InputNode/InputNodeSelectors"
import { FILE_TYPE_SET } from "store/slice/InputNode/InputNodeType"

export const BrukerMRIExperimentNode = memo(function BrukerMRIExperimentNode(
  element: NodeProps,
) {
  const defined = useSelector(selectInputNodeDefined(element.id))
  if (defined) {
    return <BrukerMRINodeImple {...element} />
  } else {
    return null
  }
})

const BrukerMRINodeImple = memo(function BrukerMRINodeImple({
  id: nodeId,
  selected: elementSelected,
}: NodeProps) {
  const dispatch = useDispatch()
  const filePath = useSelector(
    selectBrukerMRIExperimentNodeSelectedFilePath(nodeId),
  )
  const onChangeFilePath = (path: string) => {
    dispatch(setInputNodeFilePath({ nodeId, filePath: path }))
  }

  // returnType: presumably Python class name
  // also supposed to correspond to the HandleTypeColor settings
  const returnType = "BrukerMRIExperiment"
  const colorSetting = useHandleColor(returnType)

  const onClickDeleteIcon = () => {
    dispatch(deleteFlowNodeById(nodeId))
  }

  return (
    <NodeContainer nodeId={nodeId} selected={elementSelected}>
      <button
        className="flowbutton"
        onClick={onClickDeleteIcon}
        style={{ color: "black", position: "absolute", top: -10, right: 10 }}
      >
        ×
      </button>
      <FileSelect
        nodeId={nodeId}
        onChangeFilePath={(path) => {
          if (!Array.isArray(path)) {
            onChangeFilePath(path)
          }
        }}
        fileType={FILE_TYPE_SET.BRUKER_MRI}
        filePath={filePath ?? ""}
      />
      <Handle
        type="source"
        position={Position.Right}
        id={toHandleId(nodeId, "brukerMRI", returnType)}
        style={{
          ...HANDLE_STYLE,
          background: colorSetting,
        }}
        isValidConnection={isValidConnection}
      />
    </NodeContainer>
  )
})
