package interfaceRIT;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.SQLException;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextArea;
/**
 * Classe responsável por exibir a interface gráfica para gerenciar as atividades de um professor.
 * Esta classe permite que o usuário insira as atividades do professor e as salve no banco de dados.
 */
public class TelaAtividades extends JFrame {

    private JPanel contentPane;
    private JTextArea textAreaAtividades;
    private JButton btnSalvarAtividades;
    private Professor professor;
    private DAO dao;

    /**
     * Construtor da tela que recebe um objeto Professor.
     * 
     * @param professor O professor cujas atividades serão gerenciadas nesta tela.
     */
    public TelaAtividades(Professor professor) {
        this.professor = professor;
        dao = new DAO();

        setTitle("Gerenciar Atividades");
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setBounds(100, 100, 500, 400);
        contentPane = new JPanel();
        contentPane.setLayout(null);
        setContentPane(contentPane);

        JLabel lblAtividades = new JLabel("Atividades do Professor " + professor.getNome());
        lblAtividades.setBounds(10, 10, 300, 20);
        contentPane.add(lblAtividades);

        textAreaAtividades = new JTextArea();
        textAreaAtividades.setBounds(10, 40, 460, 200);
        contentPane.add(textAreaAtividades);

        btnSalvarAtividades = new JButton("Salvar Atividades");
        btnSalvarAtividades.setBounds(180, 300, 150, 30);
        btnSalvarAtividades.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                salvarAtividades();
            }
        });
        contentPane.add(btnSalvarAtividades);
    }

    /**
     * Método responsável por salvar as atividades inseridas pelo usuário no banco de dados.
     * Se as atividades não forem inseridas, exibe uma mensagem de erro.
     * Caso contrário, salva as atividades e exibe uma mensagem de sucesso.
     */
    private void salvarAtividades() {
        String atividades = textAreaAtividades.getText().trim();

        if (atividades.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Por favor, insira as atividades do professor.", "Erro", JOptionPane.ERROR_MESSAGE);
        } else {
            try {
                // Salva as atividades do professor no banco de dados
                dao.salvarAtividades(professor.getId(), atividades);
                JOptionPane.showMessageDialog(this, "Atividades salvas com sucesso.");
                dispose();  // Fecha a tela após salvar
            } catch (SQLException e) {
                JOptionPane.showMessageDialog(this, "Erro ao salvar as atividades: " + e.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
                e.printStackTrace();
            }
        }
    }
}