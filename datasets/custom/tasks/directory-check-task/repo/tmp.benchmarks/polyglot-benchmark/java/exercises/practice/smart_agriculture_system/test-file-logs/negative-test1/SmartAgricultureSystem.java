import java.util.*;

public class SmartAgricultureSystem {

    static class Zone {
        String name;
        int moisture;
        int nutrient;
        List<Zone> children;

        Zone(String name, int moisture, int nutrient) {
            this.name = name;
            this.moisture = moisture;
            this.nutrient = nutrient;
            this.children = new ArrayList<>();
        }
    }

    public static Map<String, Object> analyzeFarmland(int N, String[][] farmlandTree) {
        Map<String, Zone> zoneMap = new HashMap<>();
        Zone root = null;

        for (String[] zoneData : farmlandTree) {
            String name = zoneData[0];
            String parentName = zoneData[1];
            int moisture = Integer.parseInt(zoneData[2]);
            int nutrient = Integer.parseInt(zoneData[3]);

            Zone zone = new Zone(name, moisture, nutrient);
            zoneMap.put(name, zone);

            if (parentName.equals("ROOT")) {
                root = zone;
            } else {
                zoneMap.get(parentName).children.add(zone);
            }
        }

        List<String> preorder = new ArrayList<>();
        List<String> inorder = new ArrayList<>();
        List<String> postorder = new ArrayList<>();

        traverse(root, preorder, inorder, postorder);

        String driestZone = findDriestZone(root, zoneMap);
        String mostFertileZone = findMostFertileZone(root, zoneMap);

        Map<String, Object> result = new HashMap<>();
        result.put("Preorder Traversal", preorder);
        result.put("Inorder Traversal", inorder);
        result.put("Postorder Traversal", postorder);
        result.put("Driest Zone", driestZone);
        result.put("Most Fertile Zone", mostFertileZone);

        return result;
    }

    private static void traverse(Zone zone, List<String> preorder, List<String> inorder, List<String> postorder) {
        if (zone == null) return;

        preorder.add(zone.name);

        if (!zone.children.isEmpty()) {
            traverse(zone.children.get(0), preorder, inorder, postorder);
        }

        inorder.add(zone.name);
        // BUG FOR LOGICAL ERROR : updated for loop termination to zone.children.size() - 1 from zone.children.size()
        for (int i = 1; i < zone.children.size() - 1; i++) {
            traverse(zone.children.get(i), preorder, inorder, postorder);
        }

        postorder.add(zone.name);
    }

    private static String findDriestZone(Zone zone, Map<String, Zone> zoneMap) {
        String driest = zone.name;
        int minMoisture = zone.moisture;

        for (Zone child : zone.children) {
            String childDriest = findDriestZone(child, zoneMap);
            Zone childZone = zoneMap.get(childDriest);
            if (childZone.moisture < minMoisture) {
                driest = childDriest;
                minMoisture = childZone.moisture;
            }
        }

        return driest;
    }

    private static String findMostFertileZone(Zone zone, Map<String, Zone> zoneMap) {
        String mostFertile = zone.name;
        int maxNutrient = zone.nutrient;

        for (Zone child : zone.children) {
            String childFertile = findMostFertileZone(child, zoneMap);
            Zone childZone = zoneMap.get(childFertile);
            if (childZone.nutrient > maxNutrient) {
                mostFertile = childFertile;
                maxNutrient = childZone.nutrient;
            }
        }

        return mostFertile;
    }
}

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class SmartAgricultureSystemTest {

    @Test
    void testAnalyzeFarmland_SingleZone() {
        int N = 1;
        String[][] farmlandTree = {{"Zone A", "ROOT", "60", "40"}};

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals(List.of("Zone A"), result.get("Preorder Traversal"));
        assertEquals(List.of("Zone A"), result.get("Inorder Traversal"));
        assertEquals(List.of("Zone A"), result.get("Postorder Traversal"));
        assertEquals("Zone A", result.get("Driest Zone"));
        assertEquals("Zone A", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_TwoLevels() {
        int N = 3;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "30", "50"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals(List.of("Zone A", "Zone B", "Zone C"), result.get("Preorder Traversal"));
        assertEquals(List.of("Zone B", "Zone A", "Zone C"), result.get("Inorder Traversal"));
        assertEquals(List.of("Zone B", "Zone C", "Zone A"), result.get("Postorder Traversal"));
        assertEquals("Zone C", result.get("Driest Zone"));
        assertEquals("Zone C", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_ThreeLevels() {
        int N = 5;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "30", "50"},
                {"Zone D", "Zone C", "20", "55"},
                {"Zone E", "Zone C", "40", "35"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals(List.of("Zone A", "Zone B", "Zone C", "Zone D", "Zone E"), result.get("Preorder Traversal"));
        assertEquals(List.of("Zone B", "Zone A", "Zone D", "Zone C", "Zone E"), result.get("Inorder Traversal"));
        assertEquals(List.of("Zone B", "Zone D", "Zone E", "Zone C", "Zone A"), result.get("Postorder Traversal"));
        assertEquals("Zone D", result.get("Driest Zone"));
        assertEquals("Zone D", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_AllEqualMoisture() {
        int N = 3;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "50", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "50", "50"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals("Zone A", result.get("Driest Zone")); // First zone in traversal
    }

    @Test
    void testAnalyzeFarmland_AllEqualNutrient() {
        int N = 3;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "50"},
                {"Zone B", "Zone A", "50", "50"},
                {"Zone C", "Zone A", "30", "50"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals("Zone A", result.get("Most Fertile Zone")); // First zone in traversal
    }

    @Test
    void testAnalyzeFarmland_InvalidInput() {
        int N = 2;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "InvalidParent", "50", "45"}
        };

        assertThrows(NullPointerException.class, () -> SmartAgricultureSystem.analyzeFarmland(N, farmlandTree));
    }

    @Test
    void testAnalyzeFarmland_LargeTree() {
        int N = 7;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "30", "50"},
                {"Zone D", "Zone C", "20", "55"},
                {"Zone E", "Zone C", "40", "35"},
                {"Zone F", "Zone B", "10", "60"},
                {"Zone G", "Zone B", "70", "30"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals(List.of("Zone A", "Zone B", "Zone F", "Zone G", "Zone C", "Zone D", "Zone E"), result.get("Preorder Traversal"));
        assertEquals(List.of("Zone F", "Zone B", "Zone G", "Zone A", "Zone D", "Zone C", "Zone E"), result.get("Inorder Traversal"));
        assertEquals(List.of("Zone F", "Zone G", "Zone B", "Zone D", "Zone E", "Zone C", "Zone A"), result.get("Postorder Traversal"));
        assertEquals("Zone F", result.get("Driest Zone"));
        assertEquals("Zone F", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_DriestZoneAtLeaf() {
        int N = 4;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "30", "50"},
                {"Zone D", "Zone C", "10", "55"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals("Zone D", result.get("Driest Zone"));
    }

    @Test
    void testAnalyzeFarmland_MostFertileZoneAtLeaf() {
        int N = 4;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "30", "50"},
                {"Zone D", "Zone C", "20", "60"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals("Zone D", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_DriestAndFertileSameZone() {
        int N = 3;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "10", "60"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals("Zone C", result.get("Driest Zone"));
        assertEquals("Zone C", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_DriestAndFertileDifferentZones() {
        int N = 4;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "10", "50"},
                {"Zone D", "Zone C", "20", "60"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals("Zone C", result.get("Driest Zone"));
        assertEquals("Zone D", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_ComplexTree() {
        int N = 6;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "60", "40"},
                {"Zone B", "Zone A", "50", "45"},
                {"Zone C", "Zone A", "30", "50"},
                {"Zone D", "Zone C", "20", "55"},
                {"Zone E", "Zone C", "40", "35"},
                {"Zone F", "Zone B", "10", "60"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals(List.of("Zone A", "Zone B", "Zone F", "Zone C", "Zone D", "Zone E"), result.get("Preorder Traversal"));
        assertEquals(List.of("Zone F", "Zone B", "Zone A", "Zone D", "Zone C", "Zone E"), result.get("Inorder Traversal"));
        assertEquals(List.of("Zone F", "Zone B", "Zone D", "Zone E", "Zone C", "Zone A"), result.get("Postorder Traversal"));
        assertEquals("Zone F", result.get("Driest Zone"));
        assertEquals("Zone F", result.get("Most Fertile Zone"));
    }

    @Test
    void testAnalyzeFarmland_AllZonesEqual() {
        int N = 3;
        String[][] farmlandTree = {
                {"Zone A", "ROOT", "50", "50"},
                {"Zone B", "Zone A", "50", "50"},
                {"Zone C", "Zone A", "50", "50"}
        };

        Map<String, Object> result = SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        assertEquals("Zone A", result.get("Driest Zone"));
        assertEquals("Zone A", result.get("Most Fertile Zone"));
    }

    @Test
    @Timeout(120) // Fail if the test runs longer than 2 minutes
    void testAnalyzeFarmlandPerformance() {
        int N = 10000; // large number of zones
        String[][] farmlandTree = new String[N][4];

        // Root zone
        farmlandTree[0][0] = "Zone0";
        farmlandTree[0][1] = "ROOT";
        farmlandTree[0][2] = "50"; // moisture
        farmlandTree[0][3] = "50"; // nutrient

        // Generate a chain/tree structure
        for (int i = 1; i < N; i++) {
            farmlandTree[i][0] = "Zone" + i;
            farmlandTree[i][1] = "Zone" + (i - 1); // parent is previous zone
            farmlandTree[i][2] = String.valueOf((i % 100) + 1); // moisture
            farmlandTree[i][3] = String.valueOf((i % 200) + 1); // nutrient
        }

        long startTime = System.currentTimeMillis();

        Map<String, Object> result =
                SmartAgricultureSystem.analyzeFarmland(N, farmlandTree);

        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;

        System.out.println("Execution time (ms): " + duration);

        // Basic sanity checks
        assertNotNull(result);
        assertTrue(result.containsKey("Preorder Traversal"));
        assertTrue(result.containsKey("Inorder Traversal"));
        assertTrue(result.containsKey("Postorder Traversal"));
        assertTrue(result.containsKey("Driest Zone"));
        assertTrue(result.containsKey("Most Fertile Zone"));

        // Ensure traversals covered all nodes
        List<String> preorder = (List<String>) result.get("Preorder Traversal");
        assertEquals(N, preorder.size());
    }
}