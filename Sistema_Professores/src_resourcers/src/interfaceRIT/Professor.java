package interfaceRIT;

import java.util.ArrayList;
import java.util.List;
/**
 * Classe que representa um professor.
 * Cada professor possui um ID, nome, departamento, código do professor e uma lista de atividades associadas.
 * A classe fornece métodos para acessar e modificar esses atributos.
 * @author luish
 * @version 8.4
 * @since 2024-11-27
 */
public class Professor {
    private String id;
    private String nome;
    private String departamento;
    private String codigoProfessor;
    private List<Atividade> atividades;  // Lista de atividades associadas ao professor
    /**
     * Constrói um novo objeto Professor com os valores fornecidos.
     * 
     * @param id O identificador único do professor.
     * @param nome O nome do professor.
     * @param departamento O departamento ao qual o professor pertence.
     * @param codigoProfessor O código único atribuído ao professor.
     */
    public Professor(String id, String nome, String departamento, String codigoProfessor) {
        this.id = id;
        this.nome = nome;
        this.departamento = departamento;
        this.codigoProfessor = codigoProfessor;
        this.atividades = new ArrayList<>();
    }
    /**
     * Retorna a lista de atividades associadas ao professor.
     * 
     * @return A lista de atividades.
     */
    public List<Atividade> getAtividades() {
        return atividades;
    }
    /**
     * Define a lista de atividades associadas ao professor.
     * 
     * @param atividades A lista de atividades a ser associada ao professor.
     */
    public void setAtividades(List<Atividade> atividades) {
        this.atividades = atividades;
    }
    /**
     * Retorna o código do professor.
     * 
     * @return O código do professor.
     */
	public String getCodigoProfessor() {
		return codigoProfessor;
	}

    /**
     * Define o código do professor.
     * 
     * @param codigoProfessor O código a ser atribuído ao professor.
     */
	public void setCodigoProfessor(String codigoProfessor) {
		this.codigoProfessor = codigoProfessor;
	}

    /**
     * Retorna o nome do professor.
     * 
     * @return O nome do professor.
     */
	public String getNome() {
		return nome;
	}
	/**
     * Retorna o identificador único (ID) do professor.
     * 
     * @return O ID do professor.
     */
	public String getCodigo() {
		return id;
	}
	/**
     * Retorna o identificador único (ID) do professor.
     * 
     * @return O ID do professor.
     */
	public String getId() {
		return id;
	}
	/**
     * Define o identificador único (ID) do professor.
     * 
     * @param id O ID a ser atribuído ao professor.
     */
	public void setId(String id) {
		this.id = id;
	}

    /**
     * Define o nome do professor.
     * 
     * @param nome O nome a ser atribuído ao professor.
     */
    public void setNome(String nome) {
        this.nome = nome;
    }

    /**
     * Define o departamento ao qual o professor pertence.
     * 
     * @param departamento O departamento a ser atribuído ao professor.
     */
    public void setDepartamento(String departamento) {
        this.departamento = departamento;
    }

    /**
     * Retorna o nome do departamento ao qual o professor pertence.
     * 
     * @return O nome do departamento.
     */
    public String getDepartamento() {
        return departamento;
    }

    /**
     * Retorna uma descrição detalhada do professor, incluindo nome, matrícula e departamento.
     * 
     * @return A descrição do professor em formato de String.
     */
    public String getDescricao() {
        return String.format("Professor(a): %s\nMatricula: %s\nDepartamento: %s", nome, id, departamento);
    }
}