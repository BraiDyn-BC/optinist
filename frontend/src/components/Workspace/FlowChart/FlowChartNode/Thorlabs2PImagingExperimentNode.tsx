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
  selectThorlabs2PImagingExperimentNodeSelectedFilePath,
  selectInputNodeDefined,
} from "store/slice/InputNode/InputNodeSelectors"
import { FILE_TYPE_SET } from "store/slice/InputNode/InputNodeType"

export const Thorlabs2PImagingExperimentNode = memo(function MicroscopeFileNode(
  element: NodeProps,
) {
  const defined = useSelector(selectInputNodeDefined(element.id))
  if (defined) {
    return <Thorlabs2PNodeImple {...element} />
  } else {
    return null
  }
})

const Thorlabs2PNodeImple = memo(function Thorlabs2PNodeImple({
  id: nodeId,
  selected: elementSelected,
}: NodeProps) {
  const dispatch = useDispatch()
  const filePath = useSelector(
    selectThorlabs2PImagingExperimentNodeSelectedFilePath(nodeId),
  )
  const onChangeFilePath = (path: string) => {
    dispatch(setInputNodeFilePath({ nodeId, filePath: path }))
  }

  const returnType = "Thorlabs2PExperiment" // presumably Python class name
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
        fileType={FILE_TYPE_SET.THORLABS2P}
        filePath={filePath ?? ""}
      />
      <Handle
        type="source"
        position={Position.Right}
        id={toHandleId(nodeId, "thorlabs2p", returnType)}
        style={{
          ...HANDLE_STYLE,
          background: colorSetting,
        }}
        isValidConnection={isValidConnection}
      />
    </NodeContainer>
  )
})
