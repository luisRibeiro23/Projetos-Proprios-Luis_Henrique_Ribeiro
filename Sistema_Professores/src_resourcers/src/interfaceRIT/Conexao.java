package interfaceRIT;

import java.io.File;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
/**
 * A classe {@code Conexao} gerencia a conexão com o banco de dados SQLite utilizado pelo sistema.
 * <p>
 * Implementa o padrão Singleton para garantir que apenas uma instância da conexão seja criada
 * e compartilhada em toda a aplicação.
 * </p>
 * <p>
 * O banco de dados está localizado em: {@code C:/Users/luish/resources/bdprofessores.db}.
 * Se o diretório ou o arquivo não existir, serão criados automaticamente.
 * </p>
 * 
 * <p>
 * Funcionalidades principais:
 * <ul>
 *   <li>Abertura de conexão com o banco de dados.</li>
 *   <li>Verificação e criação do diretório/arquivo do banco de dados, caso necessário.</li>
 *   <li>Encerramento seguro da conexão.</li>
 * </ul>
 * </p>
 * 
 * @author luish
 * @version 1.0
 * @since 2024-11-27
 */
public class Conexao {
    private static Conexao instancia;
    private static final String DRIVER = "org.sqlite.JDBC";
    private static final String BD = "jdbc:sqlite:C:/Users/luish/eclipse-workspace/TP-01/resources/bdprofessores.db";
    private Connection conexao;
    /**
     * Construtor privado para implementar o padrão Singleton.
     */
    private Conexao() {}

    /**
     * Obtém a instância única da classe {@code Conexao}.
     * 
     * @return A instância única de {@code Conexao}.
     */

    public static synchronized Conexao getInstancia() {
        if (instancia == null) {
            instancia = new Conexao();
        }
        return instancia;
    }
    /**
     * Abre uma conexão com o banco de dados SQLite.
     * <p>
     * Antes de abrir a conexão, o método verifica a existência do diretório e do arquivo
     * do banco de dados. Se necessário, cria o diretório e/ou o arquivo.
     * </p>
     * 
     * @return A conexão aberta com o banco de dados, ou {@code null} em caso de erro.
     */

    public Connection abrirConexao() {
        try {
            // Definir o caminho do banco de dados
            File bdFile = new File("C:/Users/luish/resources/bdprofessores.db");

            // Verificar se o diretório existe
            if (!bdFile.getParentFile().exists()) {
                System.out.println("Diretório não encontrado. Criando diretório: " + bdFile.getParent());
                bdFile.getParentFile().mkdirs(); // Criar o diretório
            }

            // Verificar se o arquivo do banco de dados existe
            if (!bdFile.exists()) {
                System.out.println("Arquivo do banco de dados não encontrado: " + bdFile.getAbsolutePath());
                System.out.println("Criando um novo banco de dados...");
                // Isso cria o banco se ele não existir
                bdFile.createNewFile();
            }

            // Abrir conexão com o banco de dados SQLite
            Class.forName(DRIVER);
            conexao = DriverManager.getConnection(BD);

            // Caso a conexão tenha sido estabelecida
            if (conexao != null) {
                System.out.println("Conexão com o banco de dados estabelecida com sucesso!");
                conexao.setAutoCommit(false);
            }
        } catch (SQLException | ClassNotFoundException | IOException e) {
            System.out.println("Erro ao conectar com o banco de dados: " + e.getMessage());
            e.printStackTrace();
        }
        return conexao;
    }

    /**
     * Fecha a conexão com o banco de dados.
     * <p>
     * Verifica se a conexão está ativa antes de fechá-la. Em caso de falha, exibe uma mensagem de erro.
     * </p>
     */

    public void fecharConexao() {
        try {
            if (conexao != null && !conexao.isClosed()) {
                conexao.close();
                System.out.println("Conexão fechada com sucesso.");
            }
        } catch (SQLException e) {
            System.out.println("Erro ao fechar a conexão: " + e.getMessage());
        } finally {
            conexao = null;
        }
    }
}
