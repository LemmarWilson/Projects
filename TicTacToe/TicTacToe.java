/**
 ========================================================================================
 Lemmar Wilson & Karman Howard
 CSC205 TicTacToe
 ========================================================================================
 */
import javax.swing.*;
import java.awt.event.*;
import java.awt.*;

public class TicTacToe  extends JFrame{
    //fields
    private JPanel mainPanel = new JPanel(); //this will hold the buttons
    private String currentPlayer; //this will hold the current player
    private Font font4buttons = new Font(Font.SERIF, Font.BOLD, 100);//creating font for buttons
    private JButton [] buttons; //this will hold the buttons
    private JMenuBar mainMenu = new JMenuBar(); //this will hold the menu bar
    private JMenu file = new JMenu("File"); //this will hold the file menu
    private JMenu edit = new JMenu("Edit"); //this will hold the edit menu
    private JMenu help = new JMenu("Help"); //this will hold the help menu

    private JMenuItem reset = new JMenuItem("Reset"); //this will hold the reset menu item
    private JMenuItem exit = new JMenuItem("Exit"); //this will hold the exit menu item
    private JMenuItem about = new JMenuItem("About"); //this will hold the about menu item

    //***************** CSC205 HOMEWORK **************************
    private int playerXWins = 0; // Counter for Player X wins
    private int playerOWins = 0; // Counter for Player O wins
    private int totalGames = 0; // Counter for total games played
    //***************** END HOMEWORK *****************************


    //Methods

    //******************* CSC205 HOMEWORK ***************************
    // New method to check for a tie
    public boolean CheckForTie() {
        for (int i = 0; i < 9; i++) {
            if (buttons[i].isEnabled()) {
                return false; // There are still available moves, not a tie
            }
        }
        return true; // All buttons are disabled, it's a tie
    }
    //********************END HOMEWORK *************************




    public void SwitchPlayer() {
        currentPlayer = currentPlayer.equals("X")? "O" : "X"; //switching the
                    
    }

    //click event handler
    public void ButtonClickHandler(ActionEvent e) {
        JButton clickedButton = (JButton) e.getSource(); // Getting the button that was clicked
        clickedButton.setEnabled(false); // Disabling the button
        clickedButton.setText(currentPlayer); // Changing the text of the button to the current player
        currentPlayer = clickedButton.getText(); // Getting the text of the button that was clicked

        // Set background color
        clickedButton.setOpaque(true); // Making the button opaque
        clickedButton.setBackground(currentPlayer.equals("X") ? Color.MAGENTA : Color.CYAN); // Changing the background color of button

        if (CheckForWinner()) { // Checking for a winner
            JOptionPane.showMessageDialog(this, "Player " + currentPlayer + " has won!");
            if (currentPlayer.equals("X")) {
                playerXWins++;
            } else {
                playerOWins++;
            }

            resetGame(); // Resetting the game
            return; // Return after resetting the game to avoid switching player again
        }

        // Switching the player
        SwitchPlayer();
    }


    public boolean CheckForWinner() {
        // Check for win in rows
        for (int i = 0; i <= 6; i += 3) {
            if (buttons[i].getText().equals(currentPlayer)
                && buttons[i].getText().equals(buttons[i + 1].getText())
                && buttons[i].getText().equals(buttons[i + 2].getText())) {
                return true;
            }
        }
    
        // Check for win in columns
        for (int i = 0; i < 3; i++) {
            if (buttons[i].getText().equals(currentPlayer)
                && buttons[i].getText().equals(buttons[i + 3].getText())
                && buttons[i].getText().equals(buttons[i + 6].getText())) {
                return true;
            }
        }
    
        // Check for win in the diagonals
        if (buttons[0].getText().equals(currentPlayer)
            && buttons[0].getText().equals(buttons[4].getText())
            && buttons[0].getText().equals(buttons[8].getText())) {
            return true;
        }
    
        if (buttons[2].getText().equals(currentPlayer)
            && buttons[2].getText().equals(buttons[4].getText())
            && buttons[2].getText().equals(buttons[6].getText())) {
            return true;
        }
        //*************** CSC205 HOMEWORK *********************************************
        //check for tie
        if (CheckForTie()) {
            JOptionPane.showMessageDialog(this, "It's a tie!");
            resetGame();
            return false;
        }
        //*************** END HOMEWORK *********************************************
        return false;
    }

    public void resetGame() {
        // Show a confirmation dialog to the user asking if they want to reset the game
        int option = JOptionPane.showConfirmDialog(this, "Are you sure you want to reset the game?", "Reset Game", JOptionPane.YES_NO_OPTION);

        // Check if the user selected "Yes" in the confirmation dialog
        if (option == JOptionPane.YES_OPTION) {
            // Iterate through all components on the form's content pane
            for (Component component : getContentPane().getComponents()) {
                // Check if the component is an instance of JButton
                if (component instanceof JButton) {
                    // Cast the component to JButton since we know it's a button
                    JButton button = (JButton) component;

                    // Enable the button to allow clicks on it
                    button.setEnabled(true);

                    // Reset the text of the button to an empty string, effectively clearing it
                    button.setText("");

                    // Set the button's background color to null to remove any custom background color
                    button.setBackground(null); // Reset the background color
                }
            }

            // Reset the currentPlayer to "X" to start the game with the "X" player
            currentPlayer = "X";

            // Check for winner and update win counts
            if (CheckForWinner()) {
                if (currentPlayer.equals("X")) {
                    playerXWins++;
                } else {
                    playerOWins++;
                }
            }

            totalGames++; // Increment total games played

            // Display player wins and total games played
            JOptionPane.showMessageDialog(this, "Player X wins: " + playerXWins +
                    "\nPlayer O wins: " + playerOWins +
                    "\nTotal games played: " + totalGames);
        }
        // If the user selected "No" in the confirmation dialog, the game will not be reset
    }


    public void exitgame() {
        // Show a confirmation dialog to the user asking if they want to exit the game
        int option = JOptionPane.showConfirmDialog(this, "Are you sure you want to exit the game?", "Exit Game", JOptionPane.YES_NO_OPTION);

        // Check if the user selected "Yes" in the confirmation dialog
        if (option == JOptionPane.YES_OPTION) {
            // Exit the application with status code 0 (success)
            System.exit(0);
        }
        
    }

    

    //Contructor to set defult settings after creating the window
    public TicTacToe() {
        super();
        setContentPane(mainPanel);

        //building buttons
        buttons = new JButton[9]; //creating arrays of buttons

        for (int i = 0; i < 9; i++) { //traversing through the buttons array
            buttons[i] = new JButton(); //creating a new button
            mainPanel.add(buttons[i]); //adding the button to the main panel
        }
         
        for (int i = 0; i < 9; i++) { 
            buttons[i].addActionListener(e -> ButtonClickHandler(e)); //adding an action listener to the button
            buttons[i].setFont(font4buttons); //changing the font of the button
        }

        currentPlayer = "X"; //setting the current player to X

        //setting the menu bar
        setJMenuBar(mainMenu);
        mainMenu.add(file); //setting the main menu bar
        mainMenu.add(help);

        //setting the file menu
        file.add(reset);
        reset.addActionListener(e -> resetGame());

        file.add(edit);
        file.add(exit);

        //setting the help menu
        help.add(about);

        //add a layout manager to the main panel
        mainPanel.setLayout(new GridLayout(3,3));


        //this sets the title and size of the main window
        setTitle("CSC205 Tic Tac Toe");
        setSize(500, 500);
        setLocation(100,100);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
    }

}
