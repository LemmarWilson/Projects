import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class FancyButton extends JButton {
    public FancyButton() {
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                setBorder(BorderFactory.createLineBorder(Color.MAGENTA));
            }

            @Override
            public void mouseExited(MouseEvent e) {
                setBorder(BorderFactory.createLineBorder(Color.GRAY));
            }
        });
    }

    // Copy constructor to create a copy of a FancyButton
    public FancyButton(FancyButton other) {
        // Copy the icon, border, and other properties of the original FancyButton
        this.setIcon(other.getIcon());
        this.setBorder(other.getBorder());
        this.setContentAreaFilled(other.isContentAreaFilled());
        // Add the same mouse listeners to the new copy
        for (MouseListener listener : other.getMouseListeners()) {
            this.addMouseListener(listener);
        }
    }
}
