package interfaceRIT;

import javax.swing.*;
import java.awt.*;
import java.util.List;
/**
 * Classe que representa a tela de visualização do relatório de atividades de um professor.
 * Exibe um relatório contendo a descrição e a data das atividades realizadas pelo professor.
 * @author luish
 * @version 8.4
 * @since 2024-11-27
 */
public class RelatorioAtividadesTela extends JFrame {
    private JTextArea textAreaRelatorio;
    /**
     * Constrói a tela de relatório de atividades para um determinado professor.
     * 
     * @param atividades A lista de atividades realizadas pelo professor.
     * @param professorNome O nome do professor para ser exibido no título da janela.
     */
    public RelatorioAtividadesTela(List<Atividade> atividades, String professorNome) {
        setTitle("Relatório de Atividades - " + professorNome);
        setSize(400, 300);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        textAreaRelatorio = new JTextArea();
        textAreaRelatorio.setEditable(false);
        textAreaRelatorio.setText(generateRelatorio(atividades));

        JScrollPane scrollPane = new JScrollPane(textAreaRelatorio);
        add(scrollPane, BorderLayout.CENTER);
    }
    /**
     * Gera o texto do relatório com base na lista de atividades.
     * 
     * @param atividades A lista de atividades realizadas pelo professor.
     * @return O texto formatado do relatório.
     */
    private String generateRelatorio(List<Atividade> atividades) {
        StringBuilder relatorio = new StringBuilder("Atividades realizadas:\n\n");

        if (atividades.isEmpty()) {
            relatorio.append("Nenhuma atividade registrada.");
        } else {
            for (Atividade atividade : atividades) {
                relatorio.append("Descrição: ").append(atividade.getDescricao()).append("\n");
                relatorio.append("Data: ").append(atividade.getData()).append("\n\n");
            }
        }

        return relatorio.toString();
    }
}
