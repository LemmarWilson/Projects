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
    private Pantry pantry;
    private JTextArea displayTextArea; //Area to display the contents of the HashMap in the text area

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
           

            // Update the class-level fields with the local variables
            this.itemField = itemNameField;
            this.quantityField = quantityField;
            

            // Add labels and input fields to the input panel
            inputPanel.add(new JLabel("Item Name:"));
            inputPanel.add(itemNameField);
            inputPanel.add(new JLabel("Quantity:"));
            inputPanel.add(quantityField);

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

                // Initialize packsText to null
                String packsText = null;

                // Now you can use 'newItem', 'quantity', 'quantityType', and 'packsText' variables
                // Add the item to the pantry or perform other operations
                System.out.println("Adding item: " + newItem + ", Quantity: " + quantity  + ", Packs: " + packsText);
                
                // Call the addItem method of the Pantry class
                pantry.addItem(newItem, quantity);

                
                updateDisplayTextArea();
            }
        }
        // Handle the "Remove/Update Item" button click
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
            inputPanel.add(new JLabel("Quantity to Remove/Update:"));
            inputPanel.add(quantityToRemoveField);

            // Show the pop-up dialog to get user inputs
            int option = JOptionPane.showConfirmDialog(this, inputPanel, "Remove/Update Item",
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

                // Call the removeItemQuantity method of the Pantry class to remove the specified quantity
                pantry.removeItemQuantity(itemToRemove, quantityToRemove);

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

        // Create the main panel with BorderLayout
        mainPanel.setLayout(new BorderLayout());

        /*************/
        //  BUTTONS
        /************/

        // Create a panel for the buttons and set its layout to FlowLayout with center alignment
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 10));

        // Initialize the buttons array with the correct size
        buttons = new JButton[4];

        // Add Item button
        buttons[0] = new JButton("Add Item");
        buttons[0].addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ButtonClickHandler(e);
            }
        });
        buttonPanel.add(buttons[0]);

        // Remove Item button
        buttons[1] = new JButton("Remove/Update Item");
        buttons[1].addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ButtonClickHandler(e);
            }
        });
        buttonPanel.add(buttons[1]);

        // Search button
        buttons[2] = new JButton("Search Pantry");
        buttons[2].addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ButtonClickHandler(e);
            }
        });
        buttonPanel.add(buttons[2]);

        // Exit button
        buttons[3] = new JButton("Exit");
        buttons[3].addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ButtonClickHandler(e);
            }
        });
        buttonPanel.add(buttons[3]);

        // Add the buttonPanel to the top of the mainPanel
        mainPanel.add(buttonPanel, BorderLayout.NORTH);


        // Initialize the input panel
        inputPanel = new JPanel(new GridLayout(4, 2, 5, 5));

        

        // Create and add the text area to the main panel
        displayTextArea = new JTextArea(10, 30);
        displayTextArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(displayTextArea);
        mainPanel.add(scrollPane);
        
        // Update the text area with the initial contents of the HashMap
        updateDisplayTextArea();
    
        // Add the combo box to the input panel
        inputPanel.add(new JLabel("Quantity Type:"));

        // Setting the title and the size of the window
        setTitle("Pantry App");
        setSize(800, 500);
        setLocation(100, 100);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
    }
}
