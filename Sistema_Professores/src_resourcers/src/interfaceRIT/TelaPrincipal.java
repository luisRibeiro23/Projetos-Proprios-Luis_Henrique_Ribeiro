package interfaceRIT;

import java.awt.EventQueue;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import java.awt.Color;
import javax.swing.JButton;
import javax.swing.JTextField;
import javax.swing.RowFilter;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableRowSorter;
import javax.swing.JScrollPane;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.ActionEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
/**
 * A tela principal da aplicação, que exibe a lista de professores cadastrados e permite
 * realizar buscas, além de cadastrar novos professores.
 * 
 * @author luish
 */
public class TelaPrincipal extends JFrame {
	
    private static final long serialVersionUID = 1L;
    private JPanel contentPane;
    private JTextField textFieldBusca;
    private JTable table;
    private JScrollPane scrollPane;
    private ArrayList<Professor> professores;
    private DAO dao = new DAO();
    private TelaPrincipal principal;
    private TableRowSorter<TabelaProfessor> rowSorter;
    
    /**
     * Inicia a aplicação e exibe a tela principal.
     * 
     * @param args Os argumentos de linha de comando.
     */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					TelaPrincipal frame = new TelaPrincipal();
					frame.setLocationRelativeTo(frame);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	
	
	public TelaPrincipal() {
		DAO dao = new DAO();
		this.principal = this;

	    // Tenta carregar a lista de professores do banco de dados.
		try {
	        professores = dao.listarProfessores();
	        
	        // Se não houver professores cadastrados ou a lista estiver vazia, cria um professor fictício
	        if (professores == null || professores.isEmpty()) {
	            Professor professorPadrao = new Professor("1", "Professor Padrão", "Departamento Padrão", "12345");
	            professores = new ArrayList<>();
	            professores.add(professorPadrao);
	            // Caso deseje adicionar esse professor no banco de dados, você pode usar:
	            // dao.adicionarProfessor(professorPadrao);
	        }
	    } catch (Exception e) {
	        e.printStackTrace();
	    }

		
		try {
			professores = dao.listarProfessores();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		setBackground(new Color(255, 255, 255));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 720, 413);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
 
		setContentPane(contentPane);
		contentPane.setLayout(null);
		

		
		JButton btnNewButton = new JButton("Cadrastar");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Cadastro cadastro = new Cadastro(null,principal);
				cadastro.setLocationRelativeTo(cadastro);
				cadastro.setDefaultCloseOperation(DISPOSE_ON_CLOSE);
				cadastro.setVisible(true);
			}
		});
		btnNewButton.setBounds(25, 32, 102, 21);
		contentPane.add(btnNewButton);
		
		textFieldBusca = new JTextField();
		textFieldBusca.addKeyListener(new KeyAdapter() {
			@Override
			public void keyPressed(KeyEvent e) {
				filtrar();
			}
		});
		textFieldBusca.setBounds(137, 33, 513, 19);
		contentPane.add(textFieldBusca);
		textFieldBusca.setColumns(10);
		
		scrollPane = new JScrollPane();
		scrollPane.setBounds(22, 61, 674, 291);
		contentPane.add(scrollPane);
		TabelaProfessor tabelaProfessor = new TabelaProfessor(professores);
		
		table = new JTable();
		scrollPane.setViewportView(table);
		table.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				if(e.getButton()==1) {
					try {
						Professor professorSelecionado = dao.consultarProfessor(tabelaProfessor.getValueAt(table.getSelectedRow(), 0).toString());
						Cadastro cadastro = new Cadastro(professorSelecionado,principal);
						cadastro.setLocationRelativeTo(cadastro);
						cadastro.setDefaultCloseOperation(DISPOSE_ON_CLOSE);
						cadastro.setVisible(true);
					} catch (Exception e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
				}
			}
		
		});
		rowSorter = new TableRowSorter<>(tabelaProfessor);
		table.setRowSorter(rowSorter);
		table.setModel(tabelaProfessor);
		
	}

	protected void filtrar() {
		String busca = textFieldBusca.getText().trim();
		
		if(busca.length()==0) {
			rowSorter.setRowFilter(null);
			
		}
		else {
			rowSorter.setRowFilter(RowFilter.regexFilter("(?i)"+ busca));
		}
	}
} 
