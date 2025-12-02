package interfaceRIT;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
/**
 * A classe {@code Criptografia} fornece funcionalidades para realizar a criptografia de strings
 * utilizando algoritmos como SHA-256 e MD5.
 * <p>
 * O método principal, {@code criptografar()}, aplica o algoritmo especificado para gerar o hash
 * criptográfico de uma informação fornecida.
 * </p>
 * 
 * <p>
 * Exemplo de uso:
 * <pre>
 *     Criptografia criptografia = new Criptografia("minhaSenha", Criptografia.SHA256);
 *     String hash = criptografia.criptografar();
 *     System.out.println("Hash gerado: " + hash);
 * </pre>
 * </p>
 * 
 * @author luish
 * @version 1.0
 * @since 2024-11-27
 */
public class Criptografia {/**
     * Constante que representa o algoritmo de criptografia SHA-256.
     */
    public static final String SHA256 = "SHA-256";

    /**
     * Constante que representa o algoritmo de criptografia MD5.
     */
    public static final String MD5 = "MD5";

    private final String informacao;
    private final String padrao;
    /**
     * Construtor da classe {@code Criptografia}.
     * 
     * @param informacao A string que será criptografada.
     * @param padrao O algoritmo de criptografia a ser utilizado (e.g., {@link #SHA256}, {@link #MD5}).
     */
    public Criptografia(String informacao, String padrao) {
        this.informacao = informacao;
        this.padrao = padrao;
    }
    /**
     * Retorna a informação original que será criptografada.
     * 
     * @return A string a ser criptografada.
     */
    public String getInformacao() {
        return informacao;
    }
    /**
     * Retorna o padrão de criptografia utilizado.
     * 
     * @return O algoritmo de criptografia (e.g., {@link #SHA256}, {@link #MD5}).
     */
    public String getPadrao() {
        return padrao;
    }
    /**
     * Criptografa a informação utilizando o algoritmo especificado no campo {@code padrao}.
     * <p>
     * O hash gerado é retornado como uma string hexadecimal em letras maiúsculas.
     * </p>
     * 
     * @return O hash criptográfico da informação.
     * @throws IllegalArgumentException Se o algoritmo de criptografia especificado for inválido.
     */
    public String criptografar() {
        try {
            // Inicializa o MessageDigest com o padrão de criptografia
            MessageDigest messageDigest = MessageDigest.getInstance(padrao);

            // Gera o hash em bytes
            byte[] hash = messageDigest.digest(informacao.getBytes(StandardCharsets.UTF_8));

            // Converte o hash para formato hexadecimal
            StringBuilder hexString = new StringBuilder(2 * hash.length);
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString().toUpperCase();
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalArgumentException("Algoritmo de criptografia inválido: " + padrao, e);
        }
    }
}
