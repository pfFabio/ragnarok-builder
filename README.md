# API de Ragnarok - Construtor de Builds

## Descrição do Problema Escolhido
Jogadores de **Ragnarok Online** frequentemente encontram dificuldades para planejar, calcular e simular a distribuição de atributos e os efeitos dos equipamentos em seus personagens antes de aplicá-los no jogo real. Devido à grande variedade de itens e combinações de atributos (Força, Agilidade, Vitalidade, Inteligência, Destreza e Sorte), uma ferramenta que centralize essas informações e permita simular uma *Build* é extremamente valiosa. 

A **API de Ragnarok** resolve este problema fornecendo uma plataforma web e microsserviços capazes de se integrar a bancos de dados oficiais (como o Divine Pride), buscar informações precisas sobre equipamentos e calcular/salvar as builds dos jogadores para uso futuro.

---

## Justificativa Técnica das Escolhas Realizadas
Para resolver o problema proposto, optou-se pela utilização do framework **Django** devido à sua robustez, segurança embutida e capacidade de escalar projetos rapidamente através da separação em apps (que neste projeto foram estruturados como microsserviços). O banco de dados escolhido foi o **PostgreSQL**, ideal para ambientes corporativos e com excelente compatibilidade com o ORM do Django e o Docker. A comunicação com dados externos foi abstraída utilizando o padrão Gateway, evitando o acoplamento do nosso sistema com a instabilidade de APIs externas.

---

## Arquitetura e Padrões Utilizados

### Divisão da Solução em Microsserviços
O projeto foi estruturado em um ecossistema de microsserviços para separar as responsabilidades, facilitando manutenções e futuros dimensionamentos (escalonamento). A aplicação conta com:
- **Build Service:** Responsável por criar, armazenar e gerenciar as builds e atributos dos personagens.
- **Item Service:** Responsável por se comunicar com a API do Divine Pride, buscar e manter em cache os itens e equipamentos.
- **API Gateway (Nginx):** Um proxy reverso orquestrado via Docker Compose que centraliza as rotas para o frontend e os respectivos serviços.
- **Frontend / Calculator:** Camada de interface e lógica de apresentação para o usuário final.

### Organização utilizando Arquitetura Limpa (Clean Architecture)
O serviço `item_service` foi desenhado seguindo premissas de Arquitetura Limpa. Suas responsabilidades estão divididas da seguinte maneira:
- `domain/entities.py`: Regras vitais do negócio que não dependem de frameworks (ex: Entidade `Item`).
- `services/`: Contém as regras de aplicação (Casos de Uso), como a checagem no cache do banco antes de bater na API externa.
- `gateways/`: Camada de adaptadores/interfaces para comunicação com o mundo exterior (API HTTP e Banco de Dados).

### Aplicação dos Princípios SOLID
- **Single Responsibility Principle (SRP):** As *Views* do Django (`views.py`) apenas recebem a requisição HTTP e retornam a resposta. Toda a regra de validação e salvamento ocorre dentro das classes de `Service` e `Gateway`.
- **Open/Closed Principle (OCP) & Dependency Inversion Principle (DIP):** O sistema depende de abstrações (Interfaces). No `ItemService`, o serviço recebe a interface abstrata `ItemGateway`. Se for necessário alterar o provedor de itens (ex: mudar do Divine Pride para o RateMyServer), basta criar uma nova classe que implemente a interface, sem necessidade de alterar o código do serviço.
- **Interface Segregation Principle (ISP):** A interface `ItemGateway` possui apenas o método `get_item_by_id`, sendo coesa e específica.

### Aplicação de Design Patterns
Foram aplicados no mínimo quatro padrões de projeto (Design Patterns) clássicos no desenvolvimento da API:
1. **Factory Method:** Utilizado na entidade `Item` (`Item.from_divine_pride_dict()`) para encapsular a lógica complexa de criação e mapeamento do objeto a partir do JSON poluído retornado pela API externa.
2. **Gateway / Adapter:** A classe `DivinePrideGateway` atua como um adaptador que converte a complexidade e a tecnologia HTTP da API externa para o formato que o nosso domínio (`Item`) compreende.
3. **Dependency Injection:** O `ItemService` não instancia seu próprio Gateway. A dependência é injetada via construtor (`def __init__(self, gateway: ItemGateway)`), facilitando a criação de testes e o desacoplamento.
4. **Facade (Fachada):** As classes em `services/` (`ItemService` e `BuildService`) operam como fachadas para as *Views*. As views não precisam saber se o item veio do Cache (Banco de Dados) ou da Internet (API), o Service encapsula toda essa complexidade.

### Evidências de Clean Code
O projeto foca em legibilidade e manutenção. As funções são pequenas e executam ações específicas (ex: métodos privados como `_get_from_db` e `_save_to_db` no serviço de itens). Variáveis e métodos possuem nomes descritivos em inglês e português claro, não dependendo de comentários redundantes para explicar o código.

---

## Testes e Qualidade

### Testes criados com TDD
Foram implementados testes unitários utilizando o framework `pytest` (e a fixture `pytest.mark.django_db`) visando cobrir os endpoints e a criação de builds no banco de dados. Os cenários de TDD focaram em testar os retornos da API REST e o comportamento esperado antes da conclusão total das rotas no `build_service/tests/test_views.py`.

### Cenários de Comportamento usando BDD
Para validar as regras do ponto de vista do usuário final, foi utilizado o framework `pytest-bdd`. 
No diretório `build_service/features/` encontra-se o arquivo `.feature` que descreve cenários em linguagem Gherkin (Given-When-Then):
```gherkin
  Scenario: Salvar uma build com sucesso
    Given que eu preenchi os dados do meu "cavaleiro" nivel 99 chamado "Build Teste"
    When eu envio a requisicao para salvar a build
    Then a build deve ser salva no banco de dados e retornar sucesso
```
A sua implementação técnica reside no step definition em `build_service/tests/test_save_build_bdd.py`.

---

## Infraestrutura e Execução

### Configuração com Docker Compose
Toda a aplicação foi conteinerizada visando portabilidade e consistência entre ambientes de desenvolvimento e produção.
Na raiz do projeto, o arquivo `docker-compose.yml` declara:
- Um serviço de Banco de Dados (`postgres`).
- Os microsserviços da aplicação (`build_service` e `item_service`) provisionados via Dockerfiles individuais.
- Um API Gateway em Nginx expondo o frontend e fazendo proxy reverso na porta `80`.

**Para executar localmente:**
```bash
docker-compose up --build
```

---

## Deploy (Acesso ao Sistema Publicado)
**Plataforma de Deploy:** Render
**Link de acesso:** 
