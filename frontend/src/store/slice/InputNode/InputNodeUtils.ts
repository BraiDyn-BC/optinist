import {
  CsvInputNode,
  ImageInputNode,
  HDF5InputNode,
  InputNodeType,
  FILE_TYPE_SET,
  MatlabInputNode,
  MicroscopeInputNode,
  NIfTIFileRefNode,
  Thorlabs2PImagingExperimentNode,
  WidefieldImagingExperimentNode,
  BrukerMRIExperimentNode,
  BrukerCTExperimentNode,
} from "store/slice/InputNode/InputNodeType"

export function isImageInputNode(
  inputNode: InputNodeType,
): inputNode is ImageInputNode {
  return inputNode.fileType === FILE_TYPE_SET.IMAGE
}

export function isCsvInputNode(
  inputNode: InputNodeType,
): inputNode is CsvInputNode {
  return inputNode.fileType === FILE_TYPE_SET.CSV
}

export function isMatlabInputNode(
  inputNode: InputNodeType,
): inputNode is MatlabInputNode {
  return inputNode.fileType === FILE_TYPE_SET.MATLAB
}

export function isHDF5InputNode(
  inputNode: InputNodeType,
): inputNode is HDF5InputNode {
  return inputNode.fileType === FILE_TYPE_SET.HDF5
}

export function isMicroscopeInputNode(
  inputNode: InputNodeType,
): inputNode is MicroscopeInputNode {
  return inputNode.fileType === FILE_TYPE_SET.MICROSCOPE
}

export function isNIfTIFileRefNode(
  inputNode: InputNodeType,
): inputNode is NIfTIFileRefNode {
  return inputNode.fileType === FILE_TYPE_SET.NIFTI
}

export function isThorlabs2PImagingExperimentNode(
  inputNode: InputNodeType,
): inputNode is Thorlabs2PImagingExperimentNode {
  return inputNode.fileType === FILE_TYPE_SET.THORLABS2P
}

export function isWidefieldImagingExperimentNode(
  inputNode: InputNodeType,
): inputNode is WidefieldImagingExperimentNode {
  return inputNode.fileType === FILE_TYPE_SET.WIDEFIELD
}

export function isBrukerMRIExperimentNode(
  inputNode: InputNodeType,
): inputNode is BrukerMRIExperimentNode {
  return inputNode.fileType === FILE_TYPE_SET.BRUKER_MRI
}

export function isBrukerCTExperimentNode(
  inputNode: InputNodeType,
): inputNode is BrukerCTExperimentNode {
  return inputNode.fileType === FILE_TYPE_SET.BRUKER_CT
}
