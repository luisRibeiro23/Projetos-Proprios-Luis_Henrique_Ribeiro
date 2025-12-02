package interfaceRIT;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JOptionPane;

/**
 * Classe DAO para realizar operações no banco de dados relacionadas às entidades Professor e Atividade.
 * Esta classe contém métodos para CRUD (Create, Read, Update, Delete) e listagem de dados.
 * @author luish
 * @version 8.4
 * @since 2024-11-27
 */
public class DAO {
	
    private static PreparedStatement preparedStatement = null;
    private static ResultSet resultSet = null;
    /**
     * Insere um novo professor no banco de dados.
     *
     * @param professor Objeto Professor contendo os dados a serem cadastrados.
     */
    private static String CADASTRAR_PROFESSOR = " INSERT INTO PROFESSORES  "
			+ " (ID, CODIGO, NOME, DEPARTAMENTO) " + " VALUES (NULL, ?, ?, ?) ";

    /**
     * Consulta um professor pelo ID no banco de dados.
     *
     * @param id ID do professor a ser consultado.
     * @return Objeto Professor correspondente ao ID informado.
     * @throws Exception Se o professor não for encontrado ou ocorrer algum erro durante a consulta.
     */
    private static String CONSULTAR_PROFESSOR = "SELECT * FROM PROFESSORES WHERE ID = ?";
    /**
     * Atualiza os dados de um professor no banco de dados.
     *
     * @param id ID do professor a ser atualizado.
     * @param codigoProfessor Código do professor a ser atualizado.
     * @param professor Objeto Professor com os novos dados.
     */
    private static String ALTERAR_PROFESSOR = "UPDATE PROFESSORES SET CODIGO = ?, NOME = ?, DEPARTAMENTO = ? WHERE ID = ?";
    /**
     * Exclui um professor do banco de dados pelo ID.
     *
     * @param id ID do professor a ser excluído.
     */
    private static String EXCLUIR_PROFESSOR = "DELETE FROM PROFESSORES WHERE ID = ?";
    /**
     * Lista todos os professores cadastrados no banco de dados.
     *
     * @return Lista de objetos Professor contendo os dados de todos os professores cadastrados.
     * @throws Exception Se não houver professores cadastrados ou ocorrer um erro na consulta.
     */
    private static String LISTAR_PROFESSORES = " SELECT * FROM PROFESSORES  " + " WHERE 1=1 ";

    public DAO() {}

    // Método para cadastrar um professor
    public void cadastrarProfessor(Professor professor) {
        Connection connection = Conexao.getInstancia().abrirConexao();
        String query = CADASTRAR_PROFESSOR;

        try {
            preparedStatement = connection.prepareStatement(query);

            int i = 1;
            // Configura os parâmetros da consulta (NOME, DEPARTAMENTO)
            preparedStatement.setString(i++, professor.getCodigoProfessor());
            preparedStatement.setString(i++, professor.getNome());
            preparedStatement.setString(i++, professor.getDepartamento());

            preparedStatement.execute();
            connection.commit();

            JOptionPane.showMessageDialog(null, "Professor incluído com sucesso");
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            fecharConexao();
        }
    }

    // Método para consultar um professor
    public Professor consultarProfessor(String id) throws Exception {
        Connection connection = Conexao.getInstancia().abrirConexao();
        Professor professor = null;
        String query = CONSULTAR_PROFESSOR;

        try {
            preparedStatement = connection.prepareStatement(query);
            preparedStatement.setString(1, id);
            resultSet = preparedStatement.executeQuery();

            if (resultSet.next()) {
                professor = new Professor(
                        resultSet.getString("ID"),
                        resultSet.getString("CODIGO"),
                        resultSet.getString("NOME"),
                        resultSet.getString("DEPARTAMENTO"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            fecharConexao();
        }

        if (professor == null) {
            JOptionPane.showMessageDialog(null, "Não foi possível localizar o professor selecionado", "", JOptionPane.WARNING_MESSAGE);
            throw new Exception("Professor não encontrado.");
        }

        return professor;
    }

    // Método para alterar os dados de um professor
    public void alterarProfessor(String id,String codigoProfessor, Professor professor) {
        Connection connection = Conexao.getInstancia().abrirConexao();
        String query = ALTERAR_PROFESSOR;

        try {
            preparedStatement = connection.prepareStatement(query);

            int i = 1;
            preparedStatement.setString(i++, professor.getNome());
            preparedStatement.setString(i++, professor.getDepartamento());
            
            preparedStatement.setString(i++, professor.getCodigoProfessor());
            preparedStatement.setString(i++, id);

            preparedStatement.execute();
            connection.commit();

            JOptionPane.showMessageDialog(null, "Professor alterado com sucesso");
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            fecharConexao();
        }
    }

    // Método para excluir um professor
    public void excluirProfessor(String id) {
        Connection connection = Conexao.getInstancia().abrirConexao();
        String query = EXCLUIR_PROFESSOR;

        try {
            preparedStatement = connection.prepareStatement(query);
            preparedStatement.setString(1, id);
            preparedStatement.execute();
            connection.commit();

            JOptionPane.showMessageDialog(null, "Professor excluído com sucesso");
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            fecharConexao();
        }
    }
    /**
     * Salva atividades relacionadas a um professor no banco de dados.
     *
     * @param professorId ID do professor ao qual as atividades pertencem.
     * @param atividades Descrição das atividades a serem salvas.
     * @throws SQLException Se ocorrer um erro ao salvar as atividades.
     */
    public void salvarAtividades(String professorId, String atividades) throws SQLException {
        Connection connection = Conexao.getInstancia().abrirConexao();
        String query = "INSERT INTO ATIVIDADES (descricao, ID_professor) VALUES (?, ?)"; // Atualizado para ID_professor

        try {
            PreparedStatement preparedStatement = connection.prepareStatement(query);
            preparedStatement.setString(1, atividades);  // Descrição da atividade
            preparedStatement.setString(2, professorId); // ID do professor
            preparedStatement.executeUpdate();
        } finally {
            fecharConexao();
        }
    }



    // Método para listar todos os professores
    public ArrayList<Professor> listarProfessores() throws Exception {
        Connection connection = Conexao.getInstancia().abrirConexao();
        ArrayList<Professor> professores = new ArrayList<>();
        String query = "SELECT ID,NOME , DEPARTAMENTO, CODIGO FROM PROFESSORES";  // A consulta pode ser mais específica
        try {
            preparedStatement = connection.prepareStatement(query);
            resultSet = preparedStatement.executeQuery();

            while (resultSet.next()) {
                professores.add(new Professor(
                		resultSet.getString("ID"),
                		
                        resultSet.getString("nome"),
                        resultSet.getString("Departamento"),
                        resultSet.getString("codigo")));
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(null, "Erro ao listar professores: " + e.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
            e.printStackTrace();
        } finally {
            fecharConexao();
        }

        if (professores.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Não há professores cadastrados.", "", JOptionPane.WARNING_MESSAGE);
            throw new Exception("Não há professores cadastrados.");
        }
        return professores;
    }
    /**
     * Lista todas as atividades associadas a um professor pelo ID do professor.
     *
     * @param professorId ID do professor cujas atividades serão listadas.
     * @return Lista de objetos Atividade contendo os dados das atividades do professor.
     * @throws SQLException Se ocorrer um erro na consulta.
     */
    public ArrayList<Atividade> listarAtividades(String professorId) throws SQLException {
        ArrayList<Atividade> atividades = new ArrayList<>();
        Connection connection = Conexao.getInstancia().abrirConexao();
        String query = "SELECT * FROM ATIVIDADES WHERE ID_professor = ?"; // Usando ID_professor

        try {
            PreparedStatement preparedStatement = connection.prepareStatement(query);
            preparedStatement.setString(1, professorId);
            ResultSet resultSet = preparedStatement.executeQuery();

            while (resultSet.next()) {
                atividades.add(new Atividade(
                    resultSet.getInt("id"),
                    resultSet.getString("descricao"),
                    resultSet.getString("ID_professor") // Pode não ser necessário, pois você só está listando as atividades
                ));
            }
        } finally {
            fecharConexao();
        }

        return atividades;
    }


    // Método para fechar a conexão com o banco de dados
    private void fecharConexao() {
        try {
            if (resultSet != null) {
                resultSet.close();
            }
            if (preparedStatement != null) {
                preparedStatement.close();
            }
            Conexao.getInstancia().fecharConexao();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
