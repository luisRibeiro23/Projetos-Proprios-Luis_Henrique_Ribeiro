package interfaceRIT;

import java.awt.EventQueue;
import javax.swing.JPasswordField;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
/**
 * Classe responsável pela interface gráfica de login.
 * Esta classe cria uma janela onde o usuário pode inserir seu nome de usuário e senha.
 * A senha é criptografada e comparada com um valor pré-definido para autenticar o login.
 * @author luish
 * @version 8.4
 * @since 2024-11-27
 */
public class Login extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JTextField textField;
	private JTextField textField_1;

	/**
     * Método principal que executa a aplicação de login.
     * Cria e exibe a interface gráfica de login.
     * 
     * @param args Argumentos de linha de comando (não utilizados).
     */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Login frame = new Login();
					frame.setLocationRelativeTo(null);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
     * Constrói a interface gráfica de login.
     * Cria o painel de login com campos para inserir o usuário e a senha, e um botão de login.
     */
	public Login() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 450, 300);
		contentPane = new JPanel();
		contentPane.setBackground(new Color(49, 62, 64));
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JPanel panel = new JPanel();
		panel.setBackground(new Color(255, 255, 255));
		panel.setBounds(100, 10, 236, 210);
		contentPane.add(panel);
		panel.setLayout(null);
		
		JLabel lblNewLabel = new JLabel("Usuário");
		lblNewLabel.setBounds(98, 44, 45, 13);
		panel.add(lblNewLabel);
		
		textField = new JTextField();
		textField.setBounds(26, 57, 188, 19);
		panel.add(textField);
		textField.setColumns(10);
		
		JLabel lblNewLabel_1 = new JLabel("Senha");
		lblNewLabel_1.setBounds(98, 112, 45, 13);
		panel.add(lblNewLabel_1);
		
		JPasswordField passwordField;

		// No método `Login`:
		passwordField = new JPasswordField();
		passwordField.setBounds(26, 128, 188, 19);
		panel.add(passwordField);
		passwordField.setColumns(10);
		
		JButton btnNewButton = new JButton("Entrar");
		btnNewButton.addActionListener(new ActionListener() {
		    public void actionPerformed(ActionEvent e) {
		        // Obtendo a senha como um array de caracteres e convertendo para String
		        String senhaDigitada = new String(passwordField.getPassword());
		        
		        // Criptografando a senha digitada
		        Criptografia criptografia = new Criptografia(senhaDigitada, Criptografia.MD5);
		        String senhaCriptografada = criptografia.criptografar();

		        // Valor esperado (simulação de hash armazenado)
		        String senhaEsperadaCriptografada = "E10ADC3949BA59ABBE56E057F20F883E"; // hash de "password" em MD5

		        // Validação de usuário e senha
		        if (!textField.getText().isEmpty() && !senhaDigitada.isEmpty()) {
		            if (senhaCriptografada.equals(senhaEsperadaCriptografada)) {
		                JOptionPane.showMessageDialog(btnNewButton, "Informações válidas.");
		                dispose(); // Fecha a tela atual
		                TelaPrincipal telaPrincipal = new TelaPrincipal();
		                telaPrincipal.setVisible(true);
		                telaPrincipal.setLocationRelativeTo(null);
		            } else {
		                JOptionPane.showMessageDialog(btnNewButton, "Usuário ou senha incorretos.", "Erro", JOptionPane.ERROR_MESSAGE);
		            }
		        } else {
		            JOptionPane.showMessageDialog(btnNewButton, "Por favor, preencha todos os campos.", "Aviso", JOptionPane.WARNING_MESSAGE);
		        }
		    }
		});


        btnNewButton.setBackground(new Color(49, 62, 64));
        btnNewButton.setBounds(78, 157, 85, 21);
        btnNewButton.setForeground(new Color(0, 0, 0));
        panel.add(btnNewButton);

        JLabel lblNewLabel_2 = new JLabel("LOGIN");
        lblNewLabel_2.setFont(new Font("Tahoma", Font.BOLD, 18));
        lblNewLabel_2.setBounds(83, 10, 75, 13);
        panel.add(lblNewLabel_2);
    }
}