// --- Padrão de Projeto: Decorator ---
// Base do Personagem (Personagem "nu" e nível 1)
class PersonagemBase {
    get str() { return 0; }
    get agi() { return 0; }
    get vit() { return 0; }
    get int() { return 0; }
    get dex() { return 0; }
    get luk() { return 0; }
    get atk() { return 0; }
    get def() { return 0; }
}

// Decorator Base (Ele apenas repassa o status do objeto que ele está envolvendo)
class PersonagemDecorator {
    constructor(personagem) {
        this.personagem = personagem;
    }
    get str() { return this.personagem.str; }
    get agi() { return this.personagem.agi; }
    get vit() { return this.personagem.vit; }
    get int() { return this.personagem.int; }
    get dex() { return this.personagem.dex; }
    get luk() { return this.personagem.luk; }
    get atk() { return this.personagem.atk; }
    get def() { return this.personagem.def; }
}

// Decorator para somar atributos base da interface
class AtributosDecorator extends PersonagemDecorator {
    constructor(personagem, atributos) {
        super(personagem);
        this.atributos = atributos;
    }
    get str() { return super.str + (this.atributos.str || 0); }
    get agi() { return super.agi + (this.atributos.agi || 0); }
    get vit() { return super.vit + (this.atributos.vit || 0); }
    get int() { return super.int + (this.atributos.int || 0); }
    get dex() { return super.dex + (this.atributos.dex || 0); }
    get luk() { return super.luk + (this.atributos.luk || 0); }
}

// Decorator para somar status de um equipamento
class EquipamentoDecorator extends PersonagemDecorator {
    constructor(personagem, item) {
        super(personagem);
        this.item = item;
    }
    get str() { return super.str + (parseInt(this.item.str) || 0); }
    get agi() { return super.agi + (parseInt(this.item.agi) || 0); }
    get vit() { return super.vit + (parseInt(this.item.vit) || 0); }
    get int() { return super.int + (parseInt(this.item.int) || 0); }
    get dex() { return super.dex + (parseInt(this.item.dex) || 0); }
    get luk() { return super.luk + (parseInt(this.item.luk) || 0); }
    get atk() { return super.atk + (parseInt(this.item.attack) || 0); }
    get def() { return super.def + (parseInt(this.item.defense) || 0); }
}

let personagemAtual = new PersonagemBase(); // Estado global do personagem

// Função responsável por alternar entre as abas de Equipamentos e Visuais
function openTab(evt, tabName) {
    // Pega todos os elementos com class="tab-content" e esconde
    const tabContent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
        tabContent[i].classList.remove("active");
    }

    // Pega todos os elementos com class="tab-link" e remove a classe "active"
    const tabLinks = document.getElementsByClassName("tab-link");
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove("active");
    }

    // Mostra a aba atual e adiciona a classe "active" ao botão que abriu a aba
    const currentTab = document.getElementById(tabName);
    currentTab.style.display = "block";
    currentTab.classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Função para calcular o total de pontos de atributos disponíveis com base no Nível
function calcularMaxPontos(nivel) {
    const isTransclass = document.getElementById('is-transclass').checked;
    // Define a base de pontos (100 para transclasse, 48 para personagens normais)
    let pontos = isTransclass ? 100 : 48;

    // Aplica a fórmula matemática de evolução a cada level que o jogador ganhou
    for (let x = 1; x < nivel; x++) {
        if (x < 100) {
            pontos += Math.floor(x / 5) + 3;
        } else {
            pontos += Math.floor(x / 10) + 13;
        }
    }
    return pontos;
}

// Função para calcular o custo e atualizar a tela
function calcularCustoAtributos() {
    const levelInput = document.getElementById('level');
    let nivel = parseInt(levelInput.value);
    if (isNaN(nivel) || nivel < 1) nivel = 1;
    if (nivel > 250) nivel = 250;

    const maxPontos = calcularMaxPontos(nivel);
    const inputs = document.querySelectorAll('.attr-row input[type="number"]');
    let custoTotal = 0;

    inputs.forEach(input => {
        let valor = parseInt(input.value);
        
        // Garante que o valor para o cálculo estará entre 1 e 150
        if (isNaN(valor) || valor < 1) valor = 1;
        if (valor > 150) valor = 150;

        // Aplica a fórmula: Custo = Arredondar_Para_Baixo [ (Atributo Atual - 1) / 10 ] + 2
        // O laço soma o custo de cada nível evoluído
        for (let i = 1; i < valor; i++) {
            custoTotal += Math.floor((i - 1) / 10) + 2;
        }
        
        // Calcula e exibe o custo para subir o próximo nível
        const costSpan = input.parentElement.querySelector('.attr-cost');
        if (costSpan) {
            if (valor >= 150) {
                costSpan.textContent = 'Máx';
            } else {
                const nextCost = Math.floor((valor - 1) / 10) + 2;
                costSpan.textContent = `Custo: ${nextCost}`;
            }
        }
    });

    const pontosRestantes = maxPontos - custoTotal;
    const elementoPontos = document.getElementById('pontos-restantes');
    
    if (elementoPontos) {
        elementoPontos.textContent = pontosRestantes;
        // Fica vermelho se o jogador gastar mais pontos do que possui
        elementoPontos.style.color = pontosRestantes < 0 ? '#ff4d4d' : '#e0e0e0';
    }
    
    atualizarPersonagem(); // Sempre que calcular custo, reconstrói o personagem
}

// Função que utiliza o Decorator para reconstruir e calcular o personagem do zero
function atualizarPersonagem() {
    let personagem = new PersonagemBase(); // Nasce zerado

    // 1. Aplica o Decorator de Atributos Base
    const atributosInputs = document.querySelectorAll('.attr-row input[type="number"]');
    if(atributosInputs.length >= 6) {
        const atributosAtuais = {
            str: parseInt(atributosInputs[0].value) || 1,
            agi: parseInt(atributosInputs[1].value) || 1,
            vit: parseInt(atributosInputs[2].value) || 1,
            int: parseInt(atributosInputs[3].value) || 1,
            dex: parseInt(atributosInputs[4].value) || 1,
            luk: parseInt(atributosInputs[5].value) || 1
        };
        personagem = new AtributosDecorator(personagem, atributosAtuais);
    }

    // 2. Aplica um Decorator de Equipamento para cada item que ele veste (Apenas equipamentos reais)
    const slots = document.querySelectorAll('#equipados .slot');
    slots.forEach(slot => {
        if (slot.dataset.itemId) {
            const item = {
                attack: slot.dataset.attack || 0,
                    defense: slot.dataset.defense || 0,
                    str: slot.dataset.str || 0,
                    agi: slot.dataset.agi || 0,
                    vit: slot.dataset.vit || 0,
                    int: slot.dataset.int || 0,
                    dex: slot.dataset.dex || 0,
                    luk: slot.dataset.luk || 0
            };
            personagem = new EquipamentoDecorator(personagem, item);
        }
    });

    personagemAtual = personagem; // Salva o personagem pronto e superpoderoso globalmente
    
    console.log("=== Personagem Atualizado via Decorator ===");
    console.log("Atributos:", { STR: personagemAtual.str, AGI: personagemAtual.agi, VIT: personagemAtual.vit, INT: personagemAtual.int, DEX: personagemAtual.dex, LUK: personagemAtual.luk });
    console.log("Status Extra:", { ATQ: personagemAtual.atk, DEF: personagemAtual.def });

    // --- Cálculos de Combate (Fórmula Renovação) ---
    const levelInput = document.getElementById('level');
    let nivel = parseInt(levelInput ? levelInput.value : 1) || 1;
    
    // Status ATQ (Corpo a Corpo) = STR + (DEX/5) + (LUK/3) + (Level/4)
    let statusAtk = Math.floor(personagemAtual.str + (personagemAtual.dex / 5) + (personagemAtual.luk / 3) + (nivel / 4));
    let totalAtk = statusAtk + personagemAtual.atk;
    
    // ASPD Base simplificada (156) + bônus de status (Limite 193)
    let aspd = Math.min(193, Math.floor(156 + (personagemAtual.agi * 10 + personagemAtual.dex) / 40));
    
    // Atualiza a Interface
    const aspdEl = document.getElementById('calc-aspd');
    const atkEl = document.getElementById('calc-atk');
    const defEl = document.getElementById('calc-def');
    
    if (aspdEl) aspdEl.textContent = aspd;
    if (atkEl) atkEl.textContent = `${totalAtk} (${statusAtk} + ${personagemAtual.atk})`;
    if (defEl) defEl.textContent = personagemAtual.def;
}

// Adiciona eventos para recalcular os pontos sempre que um atributo for alterado
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.attr-row input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', calcularCustoAtributos);
    });
    
    // Adiciona o evento para recalcular os pontos quando o nível for alterado
    const levelInput = document.getElementById('level');
    if (levelInput) {
        levelInput.addEventListener('input', calcularCustoAtributos);
    }

    // Adiciona o evento para recalcular os pontos ao marcar/desmarcar a opção Transclasse
    const transCheckbox = document.getElementById('is-transclass');
    if (transCheckbox) {
        transCheckbox.addEventListener('change', calcularCustoAtributos);
    }
    
    // Adiciona o evento para atualizar o sprite quando a classe for alterada
    const classSelect = document.getElementById('classe');
    if (classSelect) {
        classSelect.addEventListener('change', atualizarSprite);
    }
    
    // Roda uma vez ao carregar a página
    calcularCustoAtributos();
    atualizarSprite();
});

// Função para atualizar a imagem do boneco com base na classe selecionada
function atualizarSprite() {
    const classSelect = document.getElementById('classe');
    if (!classSelect) return;
    
    const className = classSelect.value;
    
    // Dicionário de Tradução de Nomes
    // Mude apenas os nomes que estão do LADO DIREITO, entre aspas, para bater 
    // exatamente com o nome do arquivo .png que você tem na sua pasta local.
    const spriteMap = {
        'cavaleiro': 'lorde',       // Ex: se o seu arquivo for 'knight_m.png', mude para 'knight_m'
        'bruxo': 'mago',
        'cacador': 'cacador',
        'sacerdote': 'sumo',
        'mercenario': 'algoz',
        'ferreiro': 'ferreiro',
        'templario': 'paladino',
        'sabio': 'professor',
        'bardo': 'bardo',
        'odalisca': 'odalisca',
        'arruaceiro': 'desordeiro',
        'mestre_taekwon': 'mestre_taekwon',
        'espiritualista': 'espiritualista',
        'ninja': 'ninja',
        'justiceiro': 'justiceiro'
    };

    const fileName = spriteMap[className] || className;
    const avatars = document.querySelectorAll('.character-avatar');
    
    const imageUrl = `${CLASS_IMG_PATH}${fileName}.png`;
    console.log(`[Debug] Classe selecionada: ${className}. Buscando imagem em: ${imageUrl}`);

    avatars.forEach(avatar => {
        // Tenta carregar a imagem em formato .png usando a rota e o nome traduzido.
        avatar.innerHTML = `<img src="${imageUrl}" 
                                 alt="${className}" 
                                 style="width: 150%; height: 150%; object-fit: contain; transform: scale(1.5); image-rendering: pixelated; pointer-events: none;"
                                 onerror="console.error('[Debug] Erro 404: Imagem não encontrada neste caminho:', this.src); this.onerror=null; this.parentElement.innerHTML='<span>Boneco</span>';">`;
    });
}

// --- Funções do Modal de Itens ---

let activeSlot = null; // Guarda o espaço de equipamento atual

function openModal(element, slotName) {
    activeSlot = element; // Registra qual div foi clicada na tela
    const modal = document.getElementById('item-modal');
    const title = document.getElementById('modal-title');
    const slotInput = document.getElementById('modal-slot-name');
    
    title.textContent = `Selecionar Item: ${slotName}`;
    if (slotInput) slotInput.value = slotName;
    
    // Limpa a busca anterior ao abrir
    const searchInput = modal.querySelector('input[name="q"]');
    const searchResults = document.getElementById('search-results');
    if (searchInput) searchInput.value = '';
    if (searchResults) searchResults.innerHTML = '<p style="color: #99aab5; text-align: center; margin-top: 20px;">Digite o ID do item para buscar.</p>';

    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('item-modal');
    modal.style.display = 'none';
}

// Fecha o modal automaticamente se o usuário clicar na área escura (fora da caixa)
window.onclick = function(event) {
    const modal = document.getElementById('item-modal');
    if (event.target == modal) {
        closeModal();
    }
}

// Equipa o item no espaço selecionado
function equipItem(id, name, iconUrl, attack, defense, str, agi, vit, int, dex, luk) {
    if (activeSlot) {
        if (!activeSlot.dataset.originalText) {
            activeSlot.dataset.originalText = activeSlot.innerText; // Guarda o texto original (ex: "Mão Direita")
        }
        // Substitui o conteúdo pela imagem do item
        activeSlot.innerHTML = `<a href="https://www.divine-pride.net/database/item/${id}?server=bRO" onclick="event.preventDefault();"><img src="${iconUrl}" alt="${name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 4px;"></a>`;
        activeSlot.dataset.itemId = id; // Guarda o ID para quando formos somar os status
        activeSlot.dataset.attack = attack;
        activeSlot.dataset.defense = defense;
        activeSlot.dataset.str = str;
        activeSlot.dataset.agi = agi;
        activeSlot.dataset.vit = vit;
        activeSlot.dataset.int = int;
        activeSlot.dataset.dex = dex;
        activeSlot.dataset.luk = luk;
        
        atualizarPersonagem(); // Recalcula tudo ao equipar
    }
    closeModal();
}

// Remove o item e restaura o texto vazio
function unequipItem() {
    if (activeSlot && activeSlot.dataset.originalText) {
        activeSlot.innerHTML = activeSlot.dataset.originalText;
        delete activeSlot.dataset.itemId;
        delete activeSlot.dataset.attack;
        delete activeSlot.dataset.defense;
        delete activeSlot.dataset.str;
        delete activeSlot.dataset.agi;
        delete activeSlot.dataset.vit;
        delete activeSlot.dataset.int;
        delete activeSlot.dataset.dex;
        delete activeSlot.dataset.luk;
        
        atualizarPersonagem(); // Recalcula tudo ao desequipar
    }
    closeModal();
}