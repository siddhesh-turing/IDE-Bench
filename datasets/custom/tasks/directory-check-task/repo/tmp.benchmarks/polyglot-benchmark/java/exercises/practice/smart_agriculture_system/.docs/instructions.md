Solve the following Problem Solving task in Java 8 while strictly adhering to the given class and method contract. Just output the code, don't include any explanation or examples. Provide the code within Markdown.

Problem description:
A precision farming system is being developed to monitor and optimize crop growth using a hierarchical tree structure. The farmland is divided into zones, each represented as a node in a tree, where:

Each node represents a field section (Zone A, Zone B, etc.).
Each zone has subzones representing smaller sections of the field.
Leaf nodes contain real-time data on soil moisture, temperature, and crop health.
Your task is to:

Traverse the entire farmland tree to collect real-time data.
Identify the driest zone that requires immediate irrigation.
Find the most fertile zone based on soil nutrient levels.
Generate a structured report showing health metrics for each zone.
Optimize traversal efficiency for large farms.
Input:
int N → Number of zones (nodes) in the tree.
String[][] farmlandTree → A N x 4 matrix where each row contains:
farmlandTree[i][0] → Zone name (e.g., "Zone A").
farmlandTree[i][1] → Parent zone (or "ROOT" for top-level zones).
farmlandTree[i][2] → Soil moisture percentage (int).
farmlandTree[i][3] → Soil nutrient level (int).
Output:
A List<String> representing preorder, inorder, and postorder traversals of the farmland.
The driest zone name based on the lowest moisture percentage.
The most fertile zone name based on the highest nutrient level.
A structured report of zone health.
Example:
Input:

N = 5  
farmlandTree = [  
  ["Zone A", "ROOT", 60, 40],  
  ["Zone B", "Zone A", 50, 45],  
  ["Zone C", "Zone A", 30, 50],  
  ["Zone D", "Zone C", 20, 55],  
  ["Zone E", "Zone C", 40, 35]  
]  
Output:

Preorder Traversal: ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E"]  
Inorder Traversal: ["Zone B", "Zone A", "Zone D", "Zone C", "Zone E"]  
Postorder Traversal: ["Zone B", "Zone D", "Zone E", "Zone C", "Zone A"]  
Driest Zone: "Zone D"  
Most Fertile Zone: "Zone D"  
Implementation:
Implement a method inside the class SmartAgricultureSystem:

public static Map<String, Object> analyzeFarmland(int N, String[][] farmlandTree)  
Hints:
Use tree traversal algorithms (preorder, inorder, postorder) for data collection.
Sort moisture values to determine the driest zone.
Find the max soil nutrient value for the most fertile zone.
Ensure scalability for large farms with thousands of zones.
