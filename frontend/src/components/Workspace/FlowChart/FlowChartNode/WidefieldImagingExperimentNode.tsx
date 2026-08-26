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
  selectWidefieldImagingExperimentNodeSelectedFilePath,
  selectInputNodeDefined,
} from "store/slice/InputNode/InputNodeSelectors"
import { FILE_TYPE_SET } from "store/slice/InputNode/InputNodeType"

export const WidefieldImagingExperimentNode = memo(
  function WidefieldImagingExperimentNode(element: NodeProps) {
    const defined = useSelector(selectInputNodeDefined(element.id))
    if (defined) {
      return <WidefieldNodeImple {...element} />
    } else {
      return null
    }
  },
)

const WidefieldNodeImple = memo(function WidefieldNodeImple({
  id: nodeId,
  selected: elementSelected,
}: NodeProps) {
  const dispatch = useDispatch()
  const filePath = useSelector(
    selectWidefieldImagingExperimentNodeSelectedFilePath(nodeId),
  )
  const onChangeFilePath = (path: string) => {
    dispatch(setInputNodeFilePath({ nodeId, filePath: path }))
  }

  const returnType = "WidefieldExperiment" // presumably Python class name
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
        fileType={FILE_TYPE_SET.WIDEFIELD}
        filePath={filePath ?? ""}
      />
      <Handle
        type="source"
        position={Position.Right}
        id={toHandleId(nodeId, "widefield", returnType)}
        style={{
          ...HANDLE_STYLE,
          background: colorSetting,
        }}
        isValidConnection={isValidConnection}
      />
    </NodeContainer>
  )
})
