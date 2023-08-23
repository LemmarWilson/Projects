/**
 ========================================================================================
 Lemmar Wilson
 CSC205 TicTacToe
 ========================================================================================
 */
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

public class Main {

    public static void main(String[] args) {
        TicTacToe game = new TicTacToe();

    }
}




// // JOptionPane.showMessageDialog(null, "Hello World!");
// JFrame myFrame = new JFrame(null, null);
// myFrame.setSize(500, 500);
// myFrame.setLocation(100,100);
// myFrame.setVisible(true);
// myFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

//    public void ButtonClickHandler(ActionEvent e) {
//        JButton clickedButton = (JButton) e.getSource(); //getting the button that was clicked
//        clickedButton.setEnabled(false); //disabling the button
//        clickedButton.setText(currentPlayer); //changing the text of the button to the current player
//        currentPlayer = clickedButton.getText(); //getting the text of the button that was clicked
//
//        //set background color
//        clickedButton.setOpaque(true); //making the button opaque
//        clickedButton.setBackground(currentPlayer.equals("X")? Color.MAGENTA : Color.CYAN); //changing the background color of button
//
//        if(CheckForWinner()){//checking for a winner
//            JOptionPane.showMessageDialog(this, "Player " + currentPlayer + " has won!");
//            resetGame(); //resetting the game
//            exitgame(); //exiting the game
//        }
//
//        SwitchPlayer(); //switching the player
//    }