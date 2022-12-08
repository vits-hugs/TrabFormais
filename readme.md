# Autores
Enzo Bassani, Pedro Henrique D. Queiroz, Vitor Hugo Homem.

# Gerador de analisador léxico
Um exemplo do funcionamento do gerador de analisador léxico pode ser encontrado no arquivo AnalisadorLexico_exemplo.py. No exemplo, a variável *file_id* pode ser alterada, de 0 a 2, para facilmente trocar as ERs e strings utilizadas no teste. Durante a execução, são realizados prints que mostram os procedimentos da geração do analisador, exibindo todos os autômatos intermediários. Ao final do exemplo, são exibidos os tokens e a tabela de símbolos.

## Interface

Dois métodos são suficientes para utilizar o framework.

```py
LexicalAnalyserGenerator.getLexicalAnalyser(REs: str) -> LexicalAnalyser
```
Esse método estático retorna um analisador sintático construído a partir das expressões regulares, como string, passadas como argumento.

```py
tokens, symbolList = LexicalAnalyser.exec(string: str)
```
Por fim, o método exec() do analisador léxico lê a string passada como argumento e retorna uma lista de tokens e a tabela de símbolos.
