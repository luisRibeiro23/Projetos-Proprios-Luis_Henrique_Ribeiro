package interfaceRIT;

public class Atividade {
	int id;
	String data;
	String Descricao;
	public Atividade(int id,String data,String Descricao) {
		this.id = id;
		this.data = data;
		this.Descricao = Descricao;
	}
	public int getIdProfessor() {
		return id;
	}
	public void setIdProfessor(int id) {
		this.id = id;
	}
	public String getData() {
		return data;
	}
	public void setData(String data) {
		this.data = data;
	}
	public String getDescricao() {
		return Descricao;
	}
	public void setDescricao(String descricao) {
		Descricao = descricao;
	}
}
