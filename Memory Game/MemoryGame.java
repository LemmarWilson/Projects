import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class MemoryGame extends JFrame {
    private int score = 0; // Initialize score
    private JPanel mainContents = new JPanel(); // Create a panel for main contents
    private JPanel buttonPanel = new JPanel(); // Create a panel for buttons
    private JLabel mainLabel = new JLabel("Welcome new player. Your current score is: " + score); // Create a label with initial score
    private final int rows = 3; // Specify number of rows in the grid
    private final int columns = 4; // Specify number of columns in the grid
    private final int totalRounds = (rows * columns) / 2; // Calculate total number of rounds
    private ArrayList<JButton> buttons = new ArrayList<>(); // Create a list to store buttons
    private ArrayList<Color> colors = new ArrayList<>(); // Create a list to store colors
    private JButton lastClickedButton = null; // Initialize last clicked button as null
    private int totalMatched = 0; // Initialize total matched count
    private Set<Integer> matchedIndices = new HashSet<>(); // Create a set to store matched button indices

    public MemoryGame() {
        super("Memory Game"); // Set frame title

        add(mainContents); // Add mainContents panel to the frame
        mainContents.setLayout(new BorderLayout()); // Set layout for mainContents
        mainContents.add(mainLabel, BorderLayout.NORTH); // Add label to the top of mainContents
        mainContents.add(buttonPanel, BorderLayout.CENTER); // Add buttonPanel to the center of mainContents

        mainContents.setVisible(true); // Make mainContents panel visible

        GridLayout glout = new GridLayout(rows, columns); // Create a grid layout for buttonPanel
        buttonPanel.setLayout(glout); // Set layout for buttonPanel

        setCrossPlatformLook(); // Set cross-platform look and feel

        // Create the menu bar
        JMenuBar menuBar = new JMenuBar();

        // Create the "Game" menu
        JMenu gameMenu = new JMenu("File");

        // Create the "Reset" menu item
        JMenuItem resetMenuItem = new JMenuItem("Reset");
        resetMenuItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resetGame(); // Call the method to reset the game
            }
        });

        // Create the "Exit" menu item
        JMenuItem exitMenuItem = new JMenuItem("Exit");
        exitMenuItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.exit(0); // Exit the application when "Exit" is clicked
            }
        });

        // Add the menu items to the "Game" menu
        gameMenu.add(resetMenuItem);
        gameMenu.add(exitMenuItem);

        // Add the "Game" menu to the menu bar
        menuBar.add(gameMenu);

        // Set the menu bar for the JFrame
        setJMenuBar(menuBar);

        // Add buttons and set action listener
        for (int i = 0; i < rows * columns; i++) {
            JButton btn = new JButton();
            btn.addActionListener(e -> ButtonClicked(e)); // Add action listener to buttons
            buttons.add(btn); // Add button to the list
            buttonPanel.add(btn); // Add button to the buttonPanel
        }

        InitColors(); // Initialize the colors
        setButtonNames(); // Set button names

        setSize(700, 700); // Set frame size
        setVisible(true); // Make the frame visible
        setResizable(false); // Disable frame resizing
        setDefaultCloseOperation(DISPOSE_ON_CLOSE); // Set default close operation
    }

    public void InitColors() {
        // Set the colors
        colors.add(Color.BLACK);
        colors.add(Color.BLACK);
        colors.add(Color.RED);
        colors.add(Color.RED);
        colors.add(Color.MAGENTA);
        colors.add(Color.MAGENTA);
        colors.add(Color.CYAN);
        colors.add(Color.CYAN);
        colors.add(Color.YELLOW);
        colors.add(Color.YELLOW);
        colors.add(Color.PINK);
        colors.add(Color.PINK);

        // Randomize the colors by shuffling the list
        Collections.shuffle(colors);
    }

    public void ButtonClicked(ActionEvent e) {
        Object btnObj = e.getSource(); // Get the source of the action event
        int index = buttons.indexOf(btnObj); // Get the index of the clicked button
        JButton currentBtn = buttons.get(index); // Get the clicked button
        currentBtn.setBackground(colors.get(index)); // Set the background color

        if (lastClickedButton == null) { // Check for first button click
            lastClickedButton = currentBtn;
        } else { // Check for second button click
            boolean isMatch = IsColorMatch(lastClickedButton, currentBtn);

            if (isMatch) {
                currentBtn.setEnabled(false);
                lastClickedButton.setEnabled(false);
                score += 10;
                totalMatched++;

                mainLabel.setText("Welcome new player. Your current score is: " + score);

                if (totalMatched == totalRounds) {
                    JOptionPane.showMessageDialog(this, "You've won! The total score is  " + score);
                }
            } else {
                if (score > 0) {
                    score -= 1;
                }
                JOptionPane.showMessageDialog(this, "The two colors did not match. Your score is " + score);
                mainLabel.setText("Welcome new player. Your current score is: " + score);

                currentBtn.setEnabled(true);
                lastClickedButton.setEnabled(true);
                currentBtn.setBackground(null);
                lastClickedButton.setBackground(null);
            }

            lastClickedButton = null;
        }
    }

    private boolean IsColorMatch(JButton lastClickedButton, JButton currentButton) {
        int index1 = buttons.indexOf(lastClickedButton); // Get index of last clicked button
        int index2 = buttons.indexOf(currentButton); // Get index of current clicked button
        return colors.get(index1).equals(colors.get(index2)); // Compare colors
    }

    public void setButtonNames() {
        String[] buttonNames = {"Button 1", "Button 2", "Button 3", "Button 4",
                                "Button 5", "Button 6", "Button 7", "Button 8",
                                "Button 9", "Button 10", "Button 11", "Button 12"};

        // Set button names
        for (int i = 0; i < rows * columns; i++) {
            buttons.get(i).setText(buttonNames[i]);
        }
    }

    // Method to reset the game
    private void resetGame() {
        // Clear the matchedIndices set
        matchedIndices.clear();

        // Reset backgrounds and enable all buttons
        for (JButton button : buttons) {
            button.setBackground(null);
            button.setEnabled(true);
        }

        // Reset score and total matched variables
        score = 0;
        totalMatched = 0;

        // Update the main label with the reset score
        mainLabel.setText("Welcome new player. Your current score is: " + score);
    }

    public void setCrossPlatformLook() {
        try {
            UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
