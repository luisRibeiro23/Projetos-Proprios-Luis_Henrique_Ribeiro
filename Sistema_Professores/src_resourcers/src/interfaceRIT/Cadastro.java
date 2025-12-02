package interfaceRIT;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.sql.SQLException;
import java.util.List;
import java.awt.event.ActionEvent;
import java.awt.Color;
/**
 * A classe {@code Cadastro} representa a interface gráfica para o cadastro, alteração e exclusão
 * de professores no sistema. Também permite o gerenciamento de atividades associadas aos professores.
 * <p>
 * A interface oferece:
 * <ul>
 *   <li>Cadastro de novos professores.</li>
 *   <li>Edição de informações de professores existentes.</li>
 *   <li>Exclusão de professores do sistema.</li>
 *   <li>Gerenciamento de atividades relacionadas a um professor.</li>
 * </ul>
 * </p>
 * <p>
 * A classe utiliza a instância {@link DAO} para interagir com o banco de dados.
 * </p>
 * 
 * @author luish
 * @version 8.4
 * @since 2024-11-27
 */
public class Cadastro extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JTextField textFieldNome;
	private JTextField textFieldCodigo;
	DAO dao = new DAO();
	private JTextField textFieldDepartamento;
	private JButton btnNewButton_1;

	/**
     * Método principal para inicializar e exibir a interface de cadastro.
     * 
     * @param args argumentos da linha de comando (não utilizados).
     */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Cadastro frame = new Cadastro(null,null);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
     * Construtor da classe {@code Cadastro}. Inicializa a interface gráfica e define os comportamentos
     * para inclusão, alteração e exclusão de professores.
     * 
     * @param professorSelecionado o professor selecionado para edição. Caso seja {@code null}, 
     * será iniciado no modo de inclusão.
     * @param principal referência à tela principal, usada para navegar após as operações.
     */
	public Cadastro(Professor professorSelecionado,TelaPrincipal principal) {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 708, 258);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));

		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblNewLabel = new JLabel("Nome");
		lblNewLabel.setBounds(10, 10, 45, 13);
		contentPane.add(lblNewLabel);
		
		textFieldNome = new JTextField();
		textFieldNome.setBounds(10, 96, 179, 19);
		contentPane.add(textFieldNome);
		textFieldNome.setColumns(10);
		
		JLabel lblNewLabel_1 = new JLabel("Codigo de professor");
		lblNewLabel_1.setBounds(10, 57, 116, 13);
		contentPane.add(lblNewLabel_1);
		
		textFieldCodigo = new JTextField();
		textFieldCodigo.setBounds(238, 96, 184, 19);
		contentPane.add(textFieldCodigo);
		textFieldCodigo.setColumns(10);
		
		JLabel lblNewLabel_2 = new JLabel("Departamento");
		lblNewLabel_2.setBounds(238, 57, 116, 13);
		contentPane.add(lblNewLabel_2);
		
		textFieldDepartamento = new JTextField();
		textFieldDepartamento.setBounds(10, 33, 369, 19);
		contentPane.add(textFieldDepartamento);
		textFieldDepartamento.setColumns(10);
		
		JButton btnNewButton = new JButton(professorSelecionado==null?"Incluir":"Alterar");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int i = 0;
				
				Professor professor = new Professor(null,textFieldCodigo.getText(),
						textFieldNome.getText(),textFieldDepartamento.getText());
				TelaPrincipal principal = new TelaPrincipal();
				
				if(professorSelecionado==null) {
					if(!"".equalsIgnoreCase(textFieldCodigo.getText())&&!"".equalsIgnoreCase(textFieldNome.getText())&&!"".equalsIgnoreCase(textFieldDepartamento.getText())) {
						principal.setLocationRelativeTo(principal);
						abrirTelaPrincipal(principal);
						i++;
						dao.cadastrarProfessor(professor);
					}
					else {
						JOptionPane.showMessageDialog(null, "Há campos vazios.");
					}
					
				}
				else {
					if(!"".equalsIgnoreCase(textFieldCodigo.getText())&&!"".equalsIgnoreCase(textFieldNome.getText())&&!"".equalsIgnoreCase(textFieldDepartamento.getText())) {
						dao.alterarProfessor(professorSelecionado.getId(), getName(), professor);
						dispose();
						principal.setLocationRelativeTo(principal);
						abrirTelaPrincipal(principal);
						i++;
					}
					else {
						JOptionPane.showMessageDialog(null, "Há campos vazios.");
					}
					
				}
				if(i!=0) {
					principal.setVisible(true);
				}
			}
		});
		btnNewButton.setBounds(478, 125, 100, 30);
		contentPane.add(btnNewButton);
		
		btnNewButton_1 = new JButton("Excluir");
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				dao.excluirProfessor(professorSelecionado.getId());
				
				abrirTelaPrincipal(principal);
				
				
			}
		});
		btnNewButton_1.setForeground(new Color(0, 0, 0));
		btnNewButton_1.setBackground(new Color(128, 0, 0));
		btnNewButton_1.setBounds(93, 125, 90, 30);
		btnNewButton_1.setVisible(false);
		
		contentPane.add(btnNewButton_1);
		if(professorSelecionado!=null) {
			preencherCampos(professorSelecionado);
			btnNewButton_1.setVisible(true);
			

			
		}
	}
	/**
     * Preenche os campos da interface com os dados de um professor selecionado.
     * 
     * @param professorSelecionado o professor cujos dados serão exibidos.
     */
	private void preencherCampos(Professor professorSelecionado) {
		textFieldCodigo.setText(professorSelecionado.getCodigoProfessor());
		textFieldNome.setText(professorSelecionado.getNome());
		textFieldDepartamento.setText(professorSelecionado.getDepartamento());
		
	}
	/**
     * Retorna à tela principal após fechar a tela de cadastro.
     * 
     * @param principal a tela principal que será reaberta.
     */
	private void abrirTelaPrincipal(TelaPrincipal principal) {
		principal.dispose();
		dispose();
		principal = new TelaPrincipal();
		principal.setLocationRelativeTo(principal);
		principal.setVisible(true);
	}
	/**
     * Exibe o relatório de atividades associadas a um professor.
     * 
     * @param professor o professor cujas atividades serão exibidas.
     */
	private void exibirRelatorioDeAtividades(Professor professor) {
	    try {
	        // Recupera as atividades do professor. Aqui estou assumindo que o ID do professor é um inteiro.
	        List<Atividade> atividades = dao.listarAtividades(professor.getId()); // Se o ID for String, remova o parseInt

	        // Cria e exibe a nova tela para o relatório
	        RelatorioAtividadesTela relatorioTela = new RelatorioAtividadesTela(atividades, professor.getNome());
	        relatorioTela.setVisible(true);

	    } catch (SQLException e) {
	        // Exibe mensagem de erro caso algo aconteça durante a consulta ao banco
	        JOptionPane.showMessageDialog(null, "Erro ao carregar atividades: " + e.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
	    } catch (Exception e) {
	        // Captura erros gerais
	        JOptionPane.showMessageDialog(null, "Erro inesperado: " + e.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
	    }
	}


}
