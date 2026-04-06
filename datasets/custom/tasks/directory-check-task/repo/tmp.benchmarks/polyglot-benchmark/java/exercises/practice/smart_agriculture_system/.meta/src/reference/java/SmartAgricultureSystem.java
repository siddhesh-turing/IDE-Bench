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

        for (int i = 1; i < zone.children.size(); i++) {
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