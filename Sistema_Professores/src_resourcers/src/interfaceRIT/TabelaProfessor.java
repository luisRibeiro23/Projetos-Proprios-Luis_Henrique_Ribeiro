package interfaceRIT;
import java.util.ArrayList;
import javax.swing.table.AbstractTableModel;

/**
 * Classe responsável por fornecer o modelo de dados para a tabela de professores.
 * Esta classe estende {@link AbstractTableModel} e define como os dados dos professores 
 * serão apresentados em uma tabela do tipo JTable.
 * @author luish
 * @version 8.4
 * @since 2024-11-27
 */
public class TabelaProfessor extends AbstractTableModel {
    
    private static final long serialVersionUID = 1L;
    
    // Nomes das colunas que serão exibidas na tabela
    private static final String[] colunas = { "ID", "Codigo", "Nome", "Departamento" };

    // Lista de objetos Professor que será exibida na tabela
    private ArrayList<Professor> professores;

    /**
     * Construtor da classe TabelaProfessor.
     * Inicializa a lista de professores que será exibida na tabela.
     * 
     * @param professores A lista de objetos Professor a ser exibida na tabela.
     */
    public TabelaProfessor(ArrayList<Professor> professores) {
    	super();
    	this.professores = professores;
    }
    /**
     * Retorna o número de linhas da tabela, que corresponde ao número de professores.
     * 
     * @return O número de professores (linhas) na tabela.
     */
    @Override
    public int getRowCount() {
        return professores.size();
    }

    /**
     * Retorna o número de colunas da tabela, que é fixo e determinado pelo número de colunas definidas no array {@code colunas}.
     * 
     * @return O número de colunas na tabela.
     */
    @Override
    public int getColumnCount() {
        return colunas.length;
    }

    /**
     * Retorna o valor contido em uma célula específica, dada a linha e a coluna.
     * 
     * @param rowIndex O índice da linha.
     * @param columnIndex O índice da coluna.
     * @return O valor da célula na posição especificada.
     */
    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Professor professor = professores.get(rowIndex);
        if(columnIndex == 0) {
        	return professor.getCodigo();
        }
        else if(columnIndex == 1) {
        	return professor.getCodigoProfessor();
        }
        else if(columnIndex == 2) {
        	
        	return professor.getNome();
        	
        }
        else if(columnIndex == 3) {
        	
        	return professor.getDepartamento();
        }
        return null;
    }
    /**
     * Retorna o nome da coluna na posição especificada.
     * 
     * @param column O índice da coluna.
     * @return O nome da coluna na posição especificada.
     */
    public String getColumnName(int column) {
    	// TODO Auto-generated method stub
    	return colunas[column];
    }
}
