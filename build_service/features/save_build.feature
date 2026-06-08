Feature: Salvamento de Builds
  Como um jogador de Ragnarok
  Eu quero salvar as estatisticas e equipamentos do meu personagem
  Para poder carregar minha build posteriormente

  Scenario: Salvar uma build com sucesso
    Given que eu preenchi os dados do meu "cavaleiro" nivel 99 chamado "Build Teste"
    When eu envio a requisicao para salvar a build
    Then a build deve ser salva no banco de dados e retornar sucesso
