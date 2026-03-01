"use client";
import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useEffect } from "react";

interface TreeNode {
  val?: unknown;
  value?: unknown;
  left?: TreeNode;
  right?: TreeNode;
  next?: TreeNode;
}

// Helper to convert recursive JSON to Nodes/Edges
const generateTreeElements = (
  node: TreeNode | null,
  x = 0,
  y = 0,
  id = "root",
  nodes: Node[] = [],
  edges: Edge[] = [],
): { nodes: Node[]; edges: Edge[] } | undefined => {
  if (!node) return undefined;

  // Create Node
  nodes.push({
    id,
    data: { label: String(node.val ?? node.value ?? "N/A") },
    position: { x, y },
    style: {
      background: "#1e1e1e",
      color: "#fff",
      border: "1px solid #6366f1",
      borderRadius: "50%",
      width: 40,
      height: 40,
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      fontSize: "12px",
    },
  });

  // Left Child
  if (node.left) {
    edges.push({ id: `${id}-left`, source: id, target: `${id}L` });
    generateTreeElements(node.left, x - 50, y + 80, `${id}L`, nodes, edges);
  } else if (node.next) {
    // Linked List Handling
    edges.push({ id: `${id}-next`, source: id, target: `${id}N` });
    generateTreeElements(node.next, x + 80, y, `${id}N`, nodes, edges);
  }

  // Right Child
  if (node.right) {
    edges.push({ id: `${id}-right`, source: id, target: `${id}R` });
    generateTreeElements(node.right, x + 50, y + 80, `${id}R`, nodes, edges);
  }

  return { nodes, edges };
};

export default function GraphVisualizer({ data }: { data: unknown }) {
  const [nodes, setNodes] = useNodesState<Node>([]);
  const [edges, setEdges] = useEdgesState<Edge>([]);

  useEffect(() => {
    const elements = generateTreeElements(data as TreeNode);
    if (elements) {
      setNodes(elements.nodes);
      setEdges(elements.edges);
    }
  }, [data, setNodes, setEdges]);

  return (
    <div className="h-75 w-full bg-[#0B0F1A] border border-white/10 rounded">
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background color="#333" gap={20} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
