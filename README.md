[Fabrício Jailson Barth, Dr.](http://lattes.cnpq.br/3446364988774155).
Rinforcement Learning. [Insper](https://github.com/Insper), 2023.

# Taxi Driver

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/2z7X09GL)

[![Pytest](../../actions/workflows/pytest.yml/badge.svg)](.github/workflows/pytest.yml)

Implementação de um agente taxista que pode pegar um passageiro em um ponto e
deixar este passageiro em outro ponto considerando um mapa específico. Um
exemplo de mapa é apresentado abaixo:

![Exemplo](assets/image/grid_example.png)

O agente taxista pode executar as seguintes ações:

- `GO_DOWN`: o resultado da execução desta ação é mover o táxi para uma linha
  abaixo;
- `GO_UP`: o resultado da execução desta ação é mover o táxi para uma linha
  acima;
- `GO_RIGHT`: o resultado da execução desta ação é mover o táxi para uma coluna
  à direita;
- `GO_LEFT`: o resultado da execução desta ação é mover o táxi para uma coluna à
  esquerda;
- `PICK_PASSENGER`: o táxi só pode executar esta ação se estiver na mesma
  posição que o passageiro e o passageiro não estiver dentro do táxi. Após a
  execução desta ação, o passageiro estará dentro do táxi;
- `DROP_PASSENGER`: o táxi só pode executar esta ação se o passageiro estiver
  dentro do táxi. O resultado da execução desta ação é deixar o passageiro na
  mesma posição que o táxi.

O resultado deste programa é imprimir uma lista de passos que o taxista deve
seguir para concluir seu objetivo.

## Instalando dependências

```sh
pip install -r requiremens.txt
```

## Executando o programa

```sh
python src/main.py data/testcase_0.txt
```

## Rotina de testes

```sh
pytes -s
```
