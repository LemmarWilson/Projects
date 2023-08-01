import java.util.HashMap;
import java.util.Map;

public class Pantry {
    // Fields
    //private
    private HashMap<String, Integer> itemsMap;


    //METHODS

    
    // Method to add an item and its quantity to the pantry
    public void addItem(String item, int quantity) {
        itemsMap.put(item, quantity);
    }
    
    // Method to remove an item from the pantry
    public void removeItem(String item) {
        itemsMap.remove(item);
    }
    
    // Method to update the quantity of an existing item in the pantry
    public void updateItemQuantity(String item, int newQuantity) {
        itemsMap.put(item, newQuantity);
    }
    
    // Method to get the quantity of an item in the pantry
    public int getItemQuantity(String item) {
        return itemsMap.getOrDefault(item, 0);
    }
    
    // Method to get all items and their quantities in the pantry
    public Map<String, Integer> getAllItems() {
        return new HashMap<>(itemsMap); // Return a copy to prevent direct modifications to the original map
    }
    // Method to remove an item from the pantry or update its quantity
    public void removeItemQuantity(String item, int quantityToRemove) {
        int currentQuantity = itemsMap.getOrDefault(item, 0);
        // For other quantity types, subtract the specified quantity
        if (currentQuantity <= 0) {
            // Item doesn't exist or already has zero quantity, so no need to update
            return;
        }

        if (quantityToRemove <= 0) {
            // If no quantity specified, delete the entire item
            itemsMap.remove(item);
        }
        else {
            // Subtract the specified quantity from the current quantity
            int newQuantity = currentQuantity - quantityToRemove;
            if (newQuantity <= 0) {
                // If the new quantity is zero or negative, remove the item from the pantry
                itemsMap.remove(item);
            }
            else {
                // Update the quantity in the pantry
                itemsMap.put(item, newQuantity);
            }
        }
    }
    

    //CONSTRUCTORS

    // Constructor
    public Pantry() {
        itemsMap = new HashMap<>();
    }
}