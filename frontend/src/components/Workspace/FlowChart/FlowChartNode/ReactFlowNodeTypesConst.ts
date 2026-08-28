import { CustomEdge } from "components/Workspace/FlowChart/CustomEdge"
import { AlgorithmNode } from "components/Workspace/FlowChart/FlowChartNode/AlgorithmNode"
import { BehaviorFileNode } from "components/Workspace/FlowChart/FlowChartNode/BehaviorFileNode"
import { BrukerCTExperimentNode } from "components/Workspace/FlowChart/FlowChartNode/BrukerCTExperimentNode"
import { BrukerMRIExperimentNode } from "components/Workspace/FlowChart/FlowChartNode/BrukerMRIExperimentNode"
import { CsvFileNode } from "components/Workspace/FlowChart/FlowChartNode/CsvFileNode"
import { FluoFileNode } from "components/Workspace/FlowChart/FlowChartNode/FluoFileNode"
import { HDF5FileNode } from "components/Workspace/FlowChart/FlowChartNode/HDF5FileNode"
import { ImageFileNode } from "components/Workspace/FlowChart/FlowChartNode/ImageFileNode"
import { MatlabFileNode } from "components/Workspace/FlowChart/FlowChartNode/MatlabFileNode"
import { MicroscopeFileNode } from "components/Workspace/FlowChart/FlowChartNode/MicroscopeFileNode"
import { NIfTIFileRefNode } from "components/Workspace/FlowChart/FlowChartNode/NIfTIFileRefNode"
import { Thorlabs2PImagingExperimentNode } from "components/Workspace/FlowChart/FlowChartNode/Thorlabs2PImagingExperimentNode"
import { WidefieldImagingExperimentNode } from "components/Workspace/FlowChart/FlowChartNode/WidefieldImagingExperimentNode"

export const reactFlowNodeTypes = {
  ImageFileNode,
  CsvFileNode,
  MatlabFileNode,
  HDF5FileNode,
  AlgorithmNode,
  FluoFileNode,
  BehaviorFileNode,
  MicroscopeFileNode,
  NIfTIFileRefNode,
  Thorlabs2PImagingExperimentNode,
  WidefieldImagingExperimentNode,
  BrukerMRIExperimentNode,
  BrukerCTExperimentNode,
} as const

export const reactFlowEdgeTypes = {
  buttonedge: CustomEdge,
} as const
