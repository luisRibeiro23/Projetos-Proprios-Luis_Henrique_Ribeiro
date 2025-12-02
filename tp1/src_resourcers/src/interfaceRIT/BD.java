package interfaceRIT;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
/**
 * A classe {@code BD} é responsável por gerenciar a conexão e interações básicas com o banco de dados SQLite.
 * Essa classe demonstra como criar uma tabela, inserir dados iniciais e realizar consultas.
 * <p>
 * Ela utiliza a classe {@link Conexao} para estabelecer e gerenciar conexões com o banco de dados.
 * </p>
 * 
 * <p><strong>Funções principais:</strong></p>
 * <ul>
 *   <li>Criar a tabela "professor" se ela não existir.</li>
 *   <li>Inserir registros iniciais na tabela "professor" caso ela esteja vazia.</li>
 *   <li>Consultar e exibir registros da tabela "professor".</li>
 * </ul>
 * 
 * <p><strong>Exemplo de uso:</strong></p>
 * <pre>{@code
 * public static void main(String[] args) {
 *     BD.main(args);
 * }
 * }</pre>
 * 
 * <p><strong>Nota:</strong> Certifique-se de que o banco de dados está configurado corretamente no caminho especificado
 * em {@link Conexao} antes de executar esta classe.</p>
 * 
 * @author Usuário
 * @version 1.0
 * @since 2024-11-27
 */

public class BD {
	/**
    * Método principal para executar operações no banco de dados.
    * <p>
    * Este método realiza as seguintes operações:
    * <ol>
    *   <li>Estabelece uma conexão com o banco de dados.</li>
    *   <li>Cria a tabela "professor" se ela não existir.</li>
    *   <li>Insere um registro inicial na tabela "professor" caso ela esteja vazia.</li>
    *   <li>Consulta todos os registros existentes na tabela "professor".</li>
    * </ol>
    * </p>
    * 
    * @param args argumentos passados pela linha de comando (não utilizados).
    */
    public static void main(String[] args) {
        Connection connection = null;
        Statement statement = null;
        ResultSet resultSet = null;

        try {
            // Abrir conexão com o banco
            connection = Conexao.getInstancia().abrirConexao();

            // Validar conexão
            if (connection == null) {
                System.out.println("Falha ao estabelecer conexão. Encerrando o programa.");
                return;
            }
            System.out.println("Conexão estabelecida com sucesso!");

            // Criar tabela "professor" caso não exista
            statement = connection.createStatement();
            String createTableQuery = """
                CREATE TABLE IF NOT EXISTS professor (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CodigoProfessor INTEGER NOT NULL UNIQUE,  -- Novo campo para Código do Professor
                    nome TEXT NOT NULL,
                    departamento TEXT NOT NULL
                );
            """;
            statement.execute(createTableQuery);
            System.out.println("Tabela 'professor' verificada/criada com sucesso.");

            // Inserir dados na tabela, caso ela esteja vazia
            String insertQuery = """
                INSERT INTO professor (CodigoProfessor, nome, departamento)
                SELECT 1, 'João Silva', 'Matemática'
                WHERE NOT EXISTS (SELECT 1 FROM professor);
            """;
            int rowsInserted = statement.executeUpdate(insertQuery);
            if (rowsInserted > 0) {
                System.out.println("Registros inseridos na tabela 'professor'.");
            }

            // Consultar dados da tabela "professor"
            String query = "SELECT * FROM professor";
            resultSet = statement.executeQuery(query);

            // Exibir os dados
            boolean hasResults = false;
            while (resultSet.next()) {
                hasResults = true;
                String id = resultSet.getString("ID");
                String codigoProfessor = resultSet.getString("CodigoProfessor");  // Exibindo o Código do Professor
                String nome = resultSet.getString("nome");
                String departamento = resultSet.getString("departamento");
                System.out.printf("ID: %s, Código: %s, Nome: %s, Departamento: %s%n", id, codigoProfessor, nome, departamento);
            }
            if (!hasResults) {
                System.out.println("Nenhum registro encontrado na tabela 'professor'.");
            }

        } catch (Exception e) {
            System.out.println("Erro ao acessar o banco de dados: " + e.getMessage());
            e.printStackTrace();
        } finally {
            try {
                // Fechar recursos
                if (resultSet != null) resultSet.close();
                if (statement != null) statement.close();
                if (connection != null) Conexao.getInstancia().fecharConexao(); // Fechar a conexão aqui
            } catch (Exception e) {
                System.out.println("Erro ao liberar recursos: " + e.getMessage());
            }
        }
    }
}
