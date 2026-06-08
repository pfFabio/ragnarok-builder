Feature: Busca de Itens
  Como um jogador de Ragnarok
  Eu quero buscar um item por ID
  Para visualizar seus atributos antes de equipar na build

  Scenario: Busca de item existente
    Given que a API do Divine Pride esta operante e tem o item "1201" chamado "Faca"
    When eu buscar pelo item de ID "1201"
    Then o sistema deve retornar sucesso e o nome do item "Faca"

  Scenario: Busca de item inexistente
    Given que a API do Divine Pride esta operante e NAO tem o item "9999"
    When eu buscar pelo item de ID "9999"
    Then o sistema deve retornar erro com a mensagem "Nenhum item com o ID '9999' foi encontrado"
