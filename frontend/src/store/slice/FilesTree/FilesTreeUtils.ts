import { TreeNodeTypeDTO } from "api/files/Files"
import { TreeNodeType } from "store/slice/FilesTree/FilesTreeType"

export function convertToTreeNodeType(dto: TreeNodeTypeDTO[]): TreeNodeType[] {
  return dto.map((node) =>
    node.isdir
      ? {
          path: node.path,
          name: node.name,
          isDir: true,
          nodes: convertToTreeNodeType(node.nodes),
          shape: node.shape,
        }
      : {
          path: node.path,
          name: node.name,
          isDir: false,
          shape: node.shape,
        },
  )
}

export function updateDirectoryContents(
  path: string,
  tree: TreeNodeType[],
  children: TreeNodeTypeDTO[],
): TreeNodeType[] {
  return tree.map((node) => {
    if (node.path == path) {
      return {
        path: node.path,
        name: node.name,
        isDir: true,
        nodes: convertToTreeNodeType(children),
        shape: node.shape,
      }
    } else if (node.isDir) {
      return {
        path: node.path,
        name: node.name,
        isDir: true,
        nodes: updateDirectoryContents(path, node.nodes, children),
        shape: node.shape,
      }
    } else {
      return node
    }
  })
}

export function isDirNodeByPath(path: string, tree: TreeNodeType[]): boolean {
  const node = getNodeByPath(path, tree)
  if (node != null) {
    return node.isDir
  } else {
    throw new Error(`failed to get node: ${path}`)
  }
}

export function getNodeByPath(
  path: string,
  tree: TreeNodeType[],
): TreeNodeType | null {
  let targetNode: TreeNodeType | null = null
  for (const node of tree) {
    if (path === node.path) {
      targetNode = node
      break
    } else {
      if (node.isDir) {
        targetNode = getNodeByPath(path, node.nodes)
        if (targetNode != null) {
          break
        }
      }
    }
  }
  return targetNode
}

export function hasDirectoryBeenRetrieved(
  path: string,
  tree: TreeNodeType[],
): boolean {
  const node = getNodeByPath(path, tree)
  if (node != null && node.isDir) {
    return node.nodes.filter((node) => node.name == ".lazy_loaded").length == 0
  } else {
    throw new Error(`failed to get node: ${path}`)
  }
}
