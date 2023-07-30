import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Map;


public class PantryApp extends JFrame {
    // Fields
    private JPanel mainPanel = new JPanel(); // This will hold the buttons
    private JButton[] buttons; // This will hold the buttons
    private JPanel inputPanel; // This will hold the input components
    private JTextField itemField;
    private JTextField quantityField;
    private JComboBox<QuantityType> quantityTypeComboBox;
    private JTextField packsField; // Added for "PACKS" option
    private Pantry pantry;
    private JTextArea displayTextArea; //Area to display the contents of the HashMap in the text area

    // Methods

    // Method to display the contents of the HashMap in the text area
    private void updateDisplayTextArea() {
        Map<String, Integer> itemsMap = pantry.getAllItems();
        StringBuilder displayText = new StringBuilder("Pantry Items:\n");
        for (Map.Entry<String, Integer> entry : itemsMap.entrySet()) {
            String item = entry.getKey();
            int quantity = entry.getValue();
            displayText.append(item).append(": ").append(quantity).append("\n");
        }
        displayTextArea.setText(displayText.toString());
    }

    // Method to handle the "Search Pantry" functionality
    private void searchPantry() {
        // Clear the input panel from previous components
        inputPanel.removeAll();

        // Create input field for item name to search
        JTextField itemNameField = new JTextField();

        // Add the item name input field to the input panel
        inputPanel.add(new JLabel("Item Name:"));
        inputPanel.add(itemNameField);

        // Show the pop-up dialog to get user input for searching
        int option = JOptionPane.showConfirmDialog(this, inputPanel, "Search Pantry",
                JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);

        // Process the user input (perform the search)
        if (option == JOptionPane.OK_OPTION) {
            String itemToSearch = itemNameField.getText();

            // Get the quantity of the item from the pantry (if it exists)
            int quantity = pantry.getItemQuantity(itemToSearch);

            if (quantity >= 0) {
                // Item found in the pantry
                JOptionPane.showMessageDialog(this,
                        "Item: " + itemToSearch + ", Quantity: " + quantity,
                        "Pantry Search Result", JOptionPane.INFORMATION_MESSAGE);
            } else {
                // Item not found in the pantry
                JOptionPane.showMessageDialog(this,
                        "Item not found in the pantry.",
                        "Pantry Search Result", JOptionPane.WARNING_MESSAGE);
            }
        }
    }

    //Method to handle the Exit functionality
    public void exit() {
        // Show a confirmation dialog to the user asking if they want to exit the game
        int option = JOptionPane.showConfirmDialog(this, "Are you sure you want to exit the app?", "Exit", JOptionPane.YES_NO_OPTION);

        // Check if the user selected "Yes" in the confirmation dialog
        if (option == JOptionPane.YES_OPTION) {
            // Exit the application with status code 0 (success)
            System.exit(0);
        }
        
    }


    // This method handles button clicks
    public void ButtonClickHandler(ActionEvent e) {
        JButton clickedButton = (JButton) e.getSource(); // Getting the button that was clicked

        // Handle the "Add Item" button click
        if (clickedButton.getText().equals("Add Item")) {
            // Clear the input panel from previous components
            inputPanel.removeAll();

            // Create input fields for item name, quantity, and quantity type
            JTextField itemNameField = new JTextField();
            JTextField quantityField = new JTextField();
            JComboBox<QuantityType> quantityTypeComboBox = new JComboBox<>(QuantityType.values());

            // Update the class-level fields with the local variables
            this.itemField = itemNameField;
            this.quantityField = quantityField;
            this.quantityTypeComboBox = quantityTypeComboBox;

            // Add labels and input fields to the input panel
            inputPanel.add(new JLabel("Item Name:"));
            inputPanel.add(itemNameField);
            inputPanel.add(new JLabel("Quantity:"));
            inputPanel.add(quantityField);
            inputPanel.add(new JLabel("Quantity Type:"));
            inputPanel.add(quantityTypeComboBox);

            // Show the pop-up dialog to get user inputs
            int option = JOptionPane.showConfirmDialog(this, inputPanel, "Add Item",
                    JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);

            // Process the user input (you can add it to the pantry or do something else with it)
            if (option == JOptionPane.OK_OPTION) {
                String newItem = itemNameField.getText();
                String quantityText = quantityField.getText();

                // Validate quantity input (you may want to add more checks here)
                int quantity = 0;
                try {
                    quantity = Integer.parseInt(quantityText);
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(this, "Invalid quantity. Please enter a valid number.",
                            "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                // Get the selected quantity type from the combo box
                QuantityType quantityType = (QuantityType) quantityTypeComboBox.getSelectedItem();

                // Initialize packsText to null
                String packsText = null;

                // Check if the quantity type is "PACKS"
                if (quantityType == QuantityType.PACKS) {
                    // Create another text box for "How Many Packs"
                    packsField = new JTextField();
                    inputPanel.add(new JLabel("How Many Packs:"));
                    inputPanel.add(packsField);

                    // Show the pop-up dialog again to include the "How Many Packs" text box
                    option = JOptionPane.showConfirmDialog(this, inputPanel, "Add Item", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
                    
                    // Process the user input again with the new "How Many Packs" text box
                    if (option == JOptionPane.OK_OPTION) {
                        // Get the value from the "How Many Packs" text box
                        packsText = packsField.getText();
                    } else {
                        // User canceled, so exit the method
                        return;
                    }
                }
                // Now you can use 'newItem', 'quantity', 'quantityType', and 'packsText' variables
                // Add the item to the pantry or perform other operations
                System.out.println("Adding item: " + newItem + ", Quantity: " + quantity + ", Quantity Type: " + quantityType + ", Packs: " + packsText);
                
                // Call the addItem method of the Pantry class
                pantry.addItem(newItem, quantity);

                // Call the updateItemQuantity method of the Pantry class (if needed)
                if (quantityType != QuantityType.PACKS) {
                    pantry.updateItemQuantity(newItem, quantity);
                }
                updateDisplayTextArea();
            }
        }
        //Handle the "Remove/Update Item" button click
        else if (clickedButton.getText().equals("Remove/Update Item")) {
            // Clear the input panel from previous components
            inputPanel.removeAll();
    
            // Create input fields for item name and quantity to remove
            JTextField itemNameField = new JTextField();
            JTextField quantityToRemoveField = new JTextField();
    
            // Update the class-level fields with the local variables
            this.itemField = itemNameField;
            this.quantityField = quantityToRemoveField;
    
            // Add labels and input fields to the input panel
            inputPanel.add(new JLabel("Item Name:"));
            inputPanel.add(itemNameField);
            inputPanel.add(new JLabel("Quantity to Remove:"));
            inputPanel.add(quantityToRemoveField);
    
            // Show the pop-up dialog to get user inputs
            int option = JOptionPane.showConfirmDialog(this, inputPanel, "Remove Item",
                    JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
    
            // Process the user input (you can remove the item or update the quantity with it)
            if (option == JOptionPane.OK_OPTION) {
                String itemToRemove = itemNameField.getText();
                String quantityToRemoveText = quantityToRemoveField.getText();
    
                // Validate quantity input
                int quantityToRemove = 0;
                try {
                    quantityToRemove = Integer.parseInt(quantityToRemoveText);
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(this, "Invalid quantity. Please enter a valid number.",
                            "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }
    
                // Get the selected quantity type from the combo box
                QuantityType quantityTypeToRemove = (QuantityType) quantityTypeComboBox.getSelectedItem();
    
                // Remove the item or update the quantity based on the quantity type
                pantry.removeItemOrQuantity(itemToRemove, quantityTypeToRemove, quantityToRemove);
    
                // Update the display in the text area
                updateDisplayTextArea();
            }
        }
        //Handle to "Search Pantry" button click
        else if (clickedButton.getText().equals("Search Pantry")) {
            searchPantry();
        }
        else {
            exit();
        }
    }




    // Constructor
    public PantryApp() {
        super();
        setContentPane(mainPanel); // Setting the content pane to the main panel

        // Create an instance of the Pantry class
        pantry = new Pantry();

        /*************/
        //  BUTTONS
        /************/

        // Create the button panel and set its layout to FlowLayout (horizontal alignment)
        mainPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 10, 10)); // 10px horizontal and vertical gaps

        // Building buttons
        buttons = new JButton[4]; // Creating arrays of buttons

        // Add Item button
        buttons[0] = new JButton("Add Item");
        mainPanel.add(buttons[0]); // Adding the button to the main panel

        // Remove Item button
        buttons[1] = new JButton("Remove/Update Item");
        mainPanel.add(buttons[1]); // Adding the button to the main panel


        // Search button
        buttons[2] = new JButton("Search Pantry");
        mainPanel.add(buttons[2]); // Adding the button to the main panel

        // Exit button
        buttons[3] = new JButton("Exit");
        mainPanel.add(buttons[3]); // Adding the button to the main panel

        // Adding an action listener to each button
        for (int i = 0; i < buttons.length; i++) {
            buttons[i].addActionListener(e -> ButtonClickHandler(e));
        }

        // Initialize the input panel
        inputPanel = new JPanel(new GridLayout(4, 2, 5, 5));

        // Adding a ChangeListener to the quantityTypeComboBox
        quantityTypeComboBox = new JComboBox<>(QuantityType.values());
        quantityTypeComboBox.addItemListener(new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent e) {
                // Get the selected quantity type from the combo box
                QuantityType quantityType = (QuantityType) quantityTypeComboBox.getSelectedItem();
                // Check if the quantity type is "PACKS"
                if (quantityType == QuantityType.PACKS) {
                    // Create the third text box for "How Many Packs" and add it to the input panel
                    packsField = new JTextField();
                    inputPanel.add(new JLabel("How Many Packs:"));
                    inputPanel.add(packsField);
                } 
                else {
                    // Remove the third text box from the input panel if quantity type is not "PACKS"
                    if (packsField != null) {
                        inputPanel.remove(new JLabel("How Many Packs:"));
                        inputPanel.remove(packsField);
                        packsField = null;
                    }
                }
                // Revalidate the input panel to reflect the changes
                inputPanel.revalidate();
                inputPanel.repaint();
            }
        });

        // Create and add the text area to the main panel
        displayTextArea = new JTextArea(10, 30);
        displayTextArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(displayTextArea);
        mainPanel.add(scrollPane);
        
        // Update the text area with the initial contents of the HashMap
        updateDisplayTextArea();
    
        // Add the combo box to the input panel
        inputPanel.add(new JLabel("Quantity Type:"));
        inputPanel.add(quantityTypeComboBox);

        // Setting the title and the size of the window
        setTitle("Pantry App");
        setSize(800, 500);
        setLocation(100, 100);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
    }
}
