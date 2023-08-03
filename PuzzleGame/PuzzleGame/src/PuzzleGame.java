// Importing required libraries
import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.awt.image.CropImageFilter;
import java.awt.image.FilteredImageSource;
import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.List;

// The main class for the PuzzleGame, extending JFrame
public class PuzzleGame extends JFrame {
    private JPanel mainPanel; // Declaring the variable for the panel for the frame
    private int score = 0; // Variable to keep track of the player's score
    private JLabel mainLabel = new JLabel("Your current score is: " + score); // Label to display the player's score
    private ArrayList<FancyButton> buttons; // Declaring the buttons we will be using
    private int ROWS = 4, COLUMNS = 3; // Setting the values for the rows and columns of the puzzle grid
    private int WIDTH = 600; // Frame width
    private int HEIGHT = 600; // Frame height
    private BufferedImage imageSource; // Variable for the uploaded image
    private BufferedImage resizedImage; // Variable for the resized image
    private List<FancyButton> buttonSolution; // List to store the correct solution of the buttons


    // Constructor for the PuzzleGame class
    public PuzzleGame() {
        super("Puzzle Game"); // Setting the title

        // Creating a new instance of the panel
        mainPanel = new JPanel();
        // Creating the layout for the panel
        mainPanel.setLayout(new GridLayout(ROWS, COLUMNS));
        // Adding the main panel to JFrame
        add(mainPanel);
        // Adding the label to the frame
        add(mainLabel, BorderLayout.NORTH);

        try {
            // Loading the image from file
            imageSource = loadImage();

            // Resizing image to fit our given width
            int sourceWidth = imageSource.getWidth();
            int sourceHeight = imageSource.getHeight();

            // Calculating the height
            HEIGHT = (int) ((double) sourceHeight / sourceWidth * WIDTH);

            // Resizing the image using Graphics2D
            resizedImage = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_ARGB);
            var graphics = resizedImage.createGraphics();
            graphics.drawImage(imageSource, 0, 0, WIDTH, HEIGHT, null);
            graphics.dispose();
        } catch (IOException e) {
            // Display an error message if there's an issue loading the image
            JOptionPane.showMessageDialog(this, e.getMessage(), "Error loading this image", JOptionPane.ERROR_MESSAGE);
        }

        // Building the buttons
        buttons = new ArrayList<FancyButton>();
        for (int i = 0; i < COLUMNS * ROWS; i++) {
            // Variables to hold sections of images
            int row = i / COLUMNS, col = i % COLUMNS;

            // Creating slices of image
            Image imageSlice = createImage(new FilteredImageSource(resizedImage.getSource(),
                    new CropImageFilter(col * WIDTH / COLUMNS, row * HEIGHT / ROWS, WIDTH / COLUMNS, HEIGHT / ROWS)));

            // Instantiating a new button
            FancyButton btn = new FancyButton();

            // The last button
            if (i == COLUMNS * ROWS - 1) {
                btn.setBorderPainted(false);
                btn.setContentAreaFilled(false);
            } else {
                btn.setIcon(new ImageIcon(imageSlice));
            }

            // Adding the button to the ArrayList
            buttons.add(btn);
            btn.setBorder(BorderFactory.createLineBorder(Color.GRAY));
            btn.addActionListener(e -> ButtonClickEventHandler(e));
        }
        // Create the solution copy of all buttons
        buttonSolution = List.copyOf(buttons);

        // Shuffling the image slices
        Collections.shuffle(buttons);

        // Adding the buttons to the panel
        for (var btn : buttons) {
            mainPanel.add(btn);
        }

        // Setting up the window
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
        setSize(WIDTH, HEIGHT);

        // Create the menu bar and menu items
        JMenuBar menuBar = new JMenuBar();
        setJMenuBar(menuBar);

        // Create the "File" menu
        JMenu fileMenu = new JMenu("File");
        menuBar.add(fileMenu);

        // Add the "Open" menu item and register the ActionListener to handle the file selection
        JMenuItem openMenuItem = new JMenuItem("Open");
        fileMenu.add(openMenuItem);
        openMenuItem.addActionListener(e -> openImage());

        // Create the "View Solution" menu item and add ActionListener to show the solution
        JMenuItem viewSolutionMenuItem = new JMenuItem("View Solution");
        fileMenu.add(viewSolutionMenuItem);
        viewSolutionMenuItem.addActionListener(e -> showSolution());

        // Create the "Edit" menu
        JMenu editMenu = new JMenu("Edit");
        menuBar.add(editMenu);

        // Create the "Reshuffle" menu item and add ActionListener to reshuffle the puzzle
        JMenuItem reshuffleMenuItem = new JMenuItem("Reshuffle");
        editMenu.add(reshuffleMenuItem);
        reshuffleMenuItem.addActionListener(e -> reshuffle());
    }

    // Button Handler
    private void ButtonClickEventHandler(ActionEvent e) {
        // Instantiate which button was clicked
        FancyButton btnClicked = (FancyButton) e.getSource();

        // Getting the index of clicked button
        int i = buttons.indexOf(btnClicked);

        // Getting position of button in the grid - row and columns
        int row = i / COLUMNS;
        int col = i % COLUMNS;

        int isEmpty = -1;

        // Traverse the button list to find the empty button
        for (int j = 0; j < buttons.size(); j++) {
            if (buttons.get(j).getIcon() == null) { // We have found the empty button
                isEmpty = j;
                break;
            }
        }

        int rowEmpty = isEmpty / COLUMNS;
        int colEmpty = isEmpty % COLUMNS;

        // Check if clicked button is adjacent (same row + adjacent column, or same column and adjacent row)
        if ((row == rowEmpty && Math.abs(col - colEmpty) == 1) ||
                (col == colEmpty && Math.abs(row - rowEmpty) == 1)) {
            Collections.swap(buttons, i, isEmpty);
            updateButton();
            // Increase the player's score by 1 for each swap
            score += 1;
            mainLabel.setText("Your current score is: " + score);
        }
        // Check for the solution
        if (buttonSolution.equals(buttons)) {
            // Show a dialog to congratulate the player for completing the level
            showGameOverDialog();
        }
    }

    // Method to load image from file
    private BufferedImage loadImage() throws IOException {
        return ImageIO.read(new File("src/pancakes.jpg"));
    }

    // Method to load image from user selection
    private BufferedImage loadImage(File selectedFile) throws IOException {
        return ImageIO.read(selectedFile);
    }

    // Method to update the buttons on the panel after swapping
    public void updateButton() {
        mainPanel.removeAll();

        // Read all buttons to the panel
        for (var btn : buttons) {
            mainPanel.add(btn);
        }

        // Reload the panel
        mainPanel.validate();
    }

    // Method to load image from user selection
    private void openImage() {
        JFileChooser fileChooser = new JFileChooser();
        int result = fileChooser.showOpenDialog(this);

        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            try {
                imageSource = loadImage(selectedFile);
                int sourceWidth = imageSource.getWidth();
                int sourceHeight = imageSource.getHeight();
                HEIGHT = (int) ((double) sourceHeight / sourceWidth * WIDTH);
                resizedImage = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_ARGB);
                var graphics = resizedImage.createGraphics();
                graphics.drawImage(imageSource, 0, 0, WIDTH, HEIGHT, null);
                graphics.dispose();

                // Rebuild buttons with the new image
                rebuildButtons();
            } catch (IOException ex) {
                // Display an error message if there's an issue loading the selected image
                JOptionPane.showMessageDialog(this, "Error loading the selected image.", "Image Loading Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    // Method to create a copy of the current buttons as a solution
    private List<FancyButton> createButtonSolutionCopy() {
        List<FancyButton> copy = new ArrayList<>();
        for (FancyButton btn : buttons) {
            copy.add(new FancyButton(btn));
        }
        return copy;
    }

    // Method to rebuild the buttons based on the new image
    public void rebuildButtons() {
        mainPanel.removeAll();
        // Create a temporary copy
        List<FancyButton> tempButtons = new ArrayList<>(buttons);
        // Clear the original list
        buttons.clear();
        // Create a new button solution copy
        buttonSolution = createButtonSolutionCopy();
        for (int i = 0; i < COLUMNS * ROWS; i++) {
            int row = i / COLUMNS, col = i % COLUMNS;
            Image imageSlice = createImage(new FilteredImageSource(resizedImage.getSource(),
                    new CropImageFilter(col * WIDTH / COLUMNS, row * HEIGHT / ROWS, WIDTH / COLUMNS, HEIGHT / ROWS)));
            FancyButton btn = new FancyButton();
            if (i == COLUMNS * ROWS - 1) {
                btn.setBorderPainted(false);
                btn.setContentAreaFilled(false);
            } else {
                btn.setIcon(new ImageIcon(imageSlice));
            }
            buttons.add(btn);
            btn.setBorder(BorderFactory.createLineBorder(Color.GRAY));
            btn.addActionListener(e -> ButtonClickEventHandler(e));
        }
        Collections.shuffle(buttons);
        for (var btn : buttons) {
            mainPanel.add(btn);
        }
        mainPanel.validate();
    }

    // Method to show the solved image in a pop-up window
    private void showSolution() {
        BufferedImage solutionImage = resizedImage;
        ImageIcon solutionIcon = new ImageIcon(solutionImage);

        // Display the solved image in a pop-up window
        JOptionPane.showMessageDialog(this, solutionIcon, "Solution", JOptionPane.PLAIN_MESSAGE);
    }

    // Method to reshuffle the image slices randomly
    private void reshuffle() {
        // Shuffling the image slices randomly
        Collections.shuffle(buttons);

        // Remove and re-add the buttons to the panel
        mainPanel.removeAll();
        for (var btn : buttons) {
            mainPanel.add(btn);
        }
        mainPanel.validate();
        // Reset the user's score
        score = 0;
        mainLabel.setText("Your current score is: " + score);
    }

    // Method to show the game over dialog
    private void showGameOverDialog() {
        Object[] options = { "Replay", "Next Level", "Exit" };
        int choice = JOptionPane.showOptionDialog(
                this,
                "Congratulations! You completed the level. What do you want to do next?",
                "Game Over",
                JOptionPane.YES_NO_CANCEL_OPTION,
                JOptionPane.QUESTION_MESSAGE,
                null,
                options,
                options[0]);

        if (choice == JOptionPane.YES_OPTION) {
            // Replay the current level
            reshuffle();
        } else if (choice == JOptionPane.NO_OPTION) {
            // Proceed to the next level (if you have multiple levels)
            reshuffle(); // TODO implement new level
        } else if (choice == JOptionPane.CANCEL_OPTION || choice == JOptionPane.CLOSED_OPTION)

        {
            // Exit the game
            System.exit(0);
        }
    }
}

