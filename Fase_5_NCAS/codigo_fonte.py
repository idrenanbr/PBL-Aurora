"""Núcleo Cognitivo da Aurora Siger (NCAS) - Fase 5.

Protótipo educacional para registrar, consultar e interpretar informações
operacionais da colônia. O programa utiliza apenas a biblioteca padrão do
Python e funciona sem conexão com uma API de inteligência artificial.

Equipe:
    Juan de Lucas Frois - RM563260
    Flávia Roberta Pennachin - RM561860
    Pedro Valente Toledo - RM570394
    Renan Mano Otero - RM573615
"""

from __future__ import annotations

import argparse
import itertools
import json
from datetime import datetime
from pathlib import Path
from textwrap import fill
from typing import Any, Dict, List, Optional


PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_JSON = PASTA_PROJETO / "dados_colonia.json"
ARQUIVO_TEXTO = PASTA_PROJETO / "registros_colonia.txt"
LARGURA = 88


def titulo(texto: str) -> None:
    """Exibe um cabeçalho padronizado no terminal."""
    print("\n" + "=" * LARGURA)
    print(texto.center(LARGURA))
    print("=" * LARGURA)


def subtitulo(texto: str) -> None:
    """Exibe uma separação visual menor."""
    print("\n" + "-" * LARGURA)
    print(texto)
    print("-" * LARGURA)


def carregar_dados() -> Dict[str, Any]:
    """Lê e valida a estrutura principal do arquivo JSON."""
    try:
        with ARQUIVO_JSON.open("r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            dados = json.loads(conteudo)
    except FileNotFoundError as erro:
        raise FileNotFoundError(
            f"Arquivo obrigatório não encontrado: {ARQUIVO_JSON.name}"
        ) from erro
    except json.JSONDecodeError as erro:
        raise ValueError(
            f"O arquivo {ARQUIVO_JSON.name} contém JSON inválido: {erro}"
        ) from erro

    chaves_obrigatorias = {
        "metadados",
        "modulos",
        "alertas",
        "solicitacoes",
        "interacoes",
        "prompts",
    }
    ausentes = chaves_obrigatorias.difference(dados)
    if ausentes:
        raise ValueError(
            "Estrutura JSON incompleta. Chaves ausentes: "
            + ", ".join(sorted(ausentes))
        )
    return dados


def salvar_dados(dados: Dict[str, Any]) -> None:
    """Grava os dados estruturados em JSON com caracteres UTF-8."""
    dados["metadados"]["ultima_atualizacao"] = datetime.now().isoformat(
        timespec="seconds"
    )
    with ARQUIVO_JSON.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")


def garantir_arquivo_texto() -> None:
    """Cria o arquivo TXT com modo exclusivo ``x`` apenas se ele não existir."""
    if not ARQUIVO_TEXTO.exists():
        with ARQUIVO_TEXTO.open("x", encoding="utf-8") as arquivo:
            arquivo.writelines(
                [
                    "REGISTROS OPERACIONAIS - AURORA SIGER\n",
                    "Arquivo criado automaticamente pelo NCAS.\n",
                ]
            )


def registrar_log(evento: str, detalhes: str) -> None:
    """Acrescenta um registro com ``a+`` e o método ``writelines``."""
    garantir_arquivo_texto()
    instante = datetime.now().isoformat(timespec="seconds")
    linha = f"[{instante}] {evento.upper()} | {detalhes}\n"
    with ARQUIVO_TEXTO.open("a+", encoding="utf-8") as arquivo:
        arquivo.writelines([linha])


def ler_booleano(mensagem: str) -> bool:
    """Lê uma resposta sim/não e devolve um valor booleano."""
    while True:
        resposta = input(f"{mensagem} [s/n]: ").strip().lower()
        if resposta in {"s", "sim"}:
            return True
        if resposta in {"n", "nao", "não"}:
            return False
        print("Entrada inválida. Digite 's' para sim ou 'n' para não.")


def ler_opcao(mensagem: str, opcoes_validas: List[str]) -> str:
    """Lê uma opção e repete a pergunta enquanto a entrada for inválida."""
    while True:
        escolha = input(mensagem).strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Escolha uma das opções exibidas.")


def buscar_modulo(dados: Dict[str, Any], modulo_id: str) -> Optional[Dict[str, Any]]:
    """Localiza um módulo pelo identificador."""
    return next(
        (modulo for modulo in dados["modulos"] if modulo["id"] == modulo_id),
        None,
    )


def buscar_alerta(dados: Dict[str, Any], alerta_id: str) -> Optional[Dict[str, Any]]:
    """Localiza um alerta pelo identificador."""
    return next(
        (alerta for alerta in dados["alertas"] if alerta["id"] == alerta_id),
        None,
    )


def proximo_id(registros: List[Dict[str, Any]], prefixo: str) -> str:
    """Gera um identificador sequencial sem depender da ordem da lista."""
    numeros = []
    for registro in registros:
        identificador = str(registro.get("id", ""))
        if identificador.startswith(prefixo):
            sufixo = identificador.removeprefix(prefixo)
            if sufixo.isdigit():
                numeros.append(int(sufixo))
    return f"{prefixo}{max(numeros, default=0) + 1:03d}"


def escolher_modulo(dados: Dict[str, Any]) -> Dict[str, Any]:
    """Exibe os módulos e permite selecionar um deles."""
    print("\nMódulos da colônia:")
    for indice, modulo in enumerate(dados["modulos"], start=1):
        indicador = "essencial" if modulo["essencial"] else "não essencial"
        print(
            f"  [{indice}] {modulo['nome']} ({modulo['id']}) - "
            f"{modulo['status']} | {indicador}"
        )
    opcoes = [str(i) for i in range(1, len(dados["modulos"]) + 1)]
    escolha = int(ler_opcao("Selecione o módulo: ", opcoes))
    return dados["modulos"][escolha - 1]


def cadastrar_alerta(dados: Dict[str, Any]) -> None:
    """Cadastra um alerta, salva no JSON e registra a ação no TXT."""
    titulo("CADASTRO DE ALERTA OPERACIONAL")
    modulo = escolher_modulo(dados)
    tipo = input("Tipo da ocorrência: ").strip() or "ocorrencia_operacional"
    mensagem = input("Descrição resumida: ").strip()
    while not mensagem:
        print("A descrição é obrigatória.")
        mensagem = input("Descrição resumida: ").strip()

    falha = ler_booleano("Há falha confirmada?")
    critico = ler_booleano("A ocorrência foi classificada como crítica?")
    consumo_elevado = ler_booleano("Há consumo elevado?")
    seguranca_ok = ler_booleano("As condições de segurança estão válidas?")
    dados_consistentes = ler_booleano("Os dados foram validados e são consistentes?")

    alerta = {
        "id": proximo_id(dados["alertas"], "ALT-"),
        "data_hora": datetime.now().isoformat(timespec="seconds"),
        "modulo_id": modulo["id"],
        "tipo": tipo.lower().replace(" ", "_"),
        "falha": falha,
        "critico": critico,
        "consumo_elevado": consumo_elevado,
        "seguranca_ok": seguranca_ok,
        "dados_consistentes": dados_consistentes,
        "mensagem": mensagem,
        "status": "aberto",
    }
    avaliacao = avaliar_regra(alerta, modulo)
    alerta["prioridade_calculada"] = avaliacao["prioridade"]
    dados["alertas"].append(alerta)
    salvar_dados(dados)
    registrar_log(
        "alerta_cadastrado",
        f"{alerta['id']} | {modulo['id']} | prioridade={avaliacao['prioridade']}",
    )
    print(
        f"\nAlerta {alerta['id']} salvo com prioridade "
        f"{avaliacao['prioridade'].upper()}.")


def imprimir_modulos(modulos: List[Dict[str, Any]]) -> None:
    """Mostra o inventário resumido dos módulos."""
    subtitulo("MÓDULOS DA COLÔNIA")
    for modulo in modulos:
        print(
            f"{modulo['id']:<12} | {modulo['nome']:<27} | "
            f"status={modulo['status']:<18} | essencial={modulo['essencial']}"
        )


def imprimir_alertas(alertas: List[Dict[str, Any]], dados: Dict[str, Any]) -> None:
    """Mostra os alertas sem perder a associação com o módulo."""
    subtitulo("ALERTAS OPERACIONAIS")
    if not alertas:
        print("Nenhum alerta cadastrado.")
        return
    for alerta in alertas:
        modulo = buscar_modulo(dados, alerta["modulo_id"])
        nome_modulo = modulo["nome"] if modulo else "Módulo desconhecido"
        prioridade = alerta.get("prioridade_calculada", "não analisada")
        print(
            f"{alerta['id']} | {nome_modulo} | {alerta['tipo']} | "
            f"prioridade={prioridade} | status={alerta['status']}"
        )
        print("  " + fill(alerta["mensagem"], width=LARGURA - 4))


def imprimir_solicitacoes(solicitacoes: List[Dict[str, Any]]) -> None:
    """Mostra as solicitações da tripulação."""
    subtitulo("SOLICITAÇÕES DA TRIPULAÇÃO")
    if not solicitacoes:
        print("Nenhuma solicitação cadastrada.")
        return
    for solicitacao in solicitacoes:
        print(
            f"{solicitacao['id']} | setor={solicitacao['setor']} | "
            f"urgente={solicitacao['urgente']} | status={solicitacao['status']}"
        )
        print("  " + fill(solicitacao["descricao"], width=LARGURA - 4))


def consultar_registros(dados: Dict[str, Any]) -> None:
    """Menu de consulta das estruturas persistidas em JSON."""
    titulo("CONSULTA DE DADOS ESTRUTURADOS - JSON")
    print("[1] Módulos\n[2] Alertas\n[3] Solicitações\n[4] Interações simuladas\n[5] Todos")
    escolha = ler_opcao("Selecione: ", ["1", "2", "3", "4", "5"])
    if escolha in {"1", "5"}:
        imprimir_modulos(dados["modulos"])
    if escolha in {"2", "5"}:
        imprimir_alertas(dados["alertas"], dados)
    if escolha in {"3", "5"}:
        imprimir_solicitacoes(dados["solicitacoes"])
    if escolha in {"4", "5"}:
        subtitulo("HISTÓRICO DE INTERAÇÕES")
        if not dados["interacoes"]:
            print("Nenhuma interação registrada.")
        for interacao in dados["interacoes"]:
            print(
                f"{interacao['id']} | {interacao['data_hora']} | "
                f"origem={interacao['origem_id']} | tipo={interacao['tipo_prompt']}"
            )


def gravar_registro_texto() -> None:
    """Permite acrescentar uma observação livre ao arquivo texto."""
    titulo("GRAVAÇÃO DE REGISTRO EM ARQUIVO TEXTO")
    setor = input("Setor responsável: ").strip() or "Centro de Controle"
    descricao = input("Registro operacional: ").strip()
    while not descricao:
        descricao = input("O registro não pode ficar vazio. Digite novamente: ").strip()
    registrar_log("registro_manual", f"setor={setor} | {descricao}")
    print(f"Registro adicionado a {ARQUIVO_TEXTO.name}.")


def ler_registros_texto() -> None:
    """Exibe o histórico usando ``readline`` e ``readlines``."""
    titulo("LEITURA DO ARQUIVO TEXTO")
    garantir_arquivo_texto()
    try:
        with ARQUIVO_TEXTO.open("r", encoding="utf-8") as arquivo:
            primeira_linha = arquivo.readline()
            linhas_restantes = arquivo.readlines()
            conteudo = (primeira_linha + "".join(linhas_restantes)).strip()
    except FileNotFoundError:
        print("O arquivo de registros ainda não existe.")
        return
    print(conteudo or "O arquivo está vazio.")


def regra_original(alerta: Dict[str, Any], modulo: Dict[str, Any]) -> bool:
    """Expressão original: (F e C) ou (F e não C) ou (E e M)."""
    f = bool(alerta["falha"])
    c = bool(alerta["critico"])
    e = bool(alerta["consumo_elevado"])
    m = bool(modulo["essencial"])
    return (f and c) or (f and not c) or (e and m)


def regra_simplificada(alerta: Dict[str, Any], modulo: Dict[str, Any]) -> bool:
    """Expressão equivalente simplificada: F ou (E e M)."""
    f = bool(alerta["falha"])
    e = bool(alerta["consumo_elevado"])
    m = bool(modulo["essencial"])
    return f or (e and m)


def regra_bloqueio_de_morgan(alerta: Dict[str, Any]) -> bool:
    """B = não (S e D), equivalente a (não S) ou (não D)."""
    s = bool(alerta["seguranca_ok"])
    d = bool(alerta["dados_consistentes"])
    return (not s) or (not d)


def avaliar_regra(alerta: Dict[str, Any], modulo: Dict[str, Any]) -> Dict[str, Any]:
    """Avalia equivalência, bloqueio e prioridade operacional."""
    original = regra_original(alerta, modulo)
    simplificada = regra_simplificada(alerta, modulo)
    bloqueio = regra_bloqueio_de_morgan(alerta)

    if bloqueio or (alerta["falha"] and alerta["critico"]):
        prioridade = "critica"
    elif simplificada:
        prioridade = "alta"
    else:
        prioridade = "normal"

    return {
        "regra_original": original,
        "regra_simplificada": simplificada,
        "expressoes_equivalentes": original == simplificada,
        "bloqueio_de_morgan": bloqueio,
        "prioridade": prioridade,
    }


def montar_prompt_zero_shot(alerta: Dict[str, Any], modulo: Dict[str, Any]) -> str:
    """Cria um prompt completo sem exemplos prévios."""
    entrada = {
        "alerta": alerta,
        "modulo": {
            "id": modulo["id"],
            "nome": modulo["nome"],
            "essencial": modulo["essencial"],
            "status": modulo["status"],
        },
    }
    return (
        "Você é o assistente operacional do Núcleo Cognitivo da Aurora Siger. "
        "Analise o alerta abaixo, aplique a regra F OR (E AND M), informe a "
        "prioridade e proponha uma ação segura. Não invente dados ausentes. "
        "Qualquer decisão crítica deve permanecer sob supervisão humana. "
        "Responda exclusivamente em JSON válido com as chaves alerta_id, "
        "prioridade, resumo, acao_recomendada, requer_supervisao_humana e "
        "justificativa_logica.\n\nENTRADA:\n"
        + json.dumps(entrada, ensure_ascii=False, indent=2)
    )


def montar_prompt_few_shot(
    alerta: Dict[str, Any], modulo: Dict[str, Any], dados: Dict[str, Any]
) -> str:
    """Cria um prompt com exemplos de classificação antes do caso atual."""
    exemplos = dados["prompts"]["few_shot"]["exemplos"]
    partes = [
        "Você classifica alertas da Aurora Siger. Use os exemplos como padrão. "
        "Aplique F OR (E AND M), preserve linguagem neutra e não deduza "
        "características pessoais dos tripulantes. Responda em JSON válido."
    ]
    for indice, exemplo in enumerate(exemplos, start=1):
        partes.append(
            f"\nEXEMPLO {indice} - ENTRADA:\n"
            + json.dumps(exemplo["entrada"], ensure_ascii=False, indent=2)
            + "\nEXEMPLO "
            + str(indice)
            + " - SAÍDA:\n"
            + json.dumps(exemplo["saida"], ensure_ascii=False, indent=2)
        )
    caso_atual = {
        "alerta_id": alerta["id"],
        "falha": alerta["falha"],
        "critico": alerta["critico"],
        "consumo_elevado": alerta["consumo_elevado"],
        "modulo_essencial": modulo["essencial"],
        "mensagem": alerta["mensagem"],
    }
    partes.append(
        "\nCASO ATUAL - ENTRADA:\n"
        + json.dumps(caso_atual, ensure_ascii=False, indent=2)
        + "\nCASO ATUAL - SAÍDA:"
    )
    return "\n".join(partes)


def simular_resposta(alerta: Dict[str, Any], modulo: Dict[str, Any]) -> Dict[str, Any]:
    """Simula localmente uma saída inteligente, determinística e auditável."""
    avaliacao = avaliar_regra(alerta, modulo)
    prioridade = avaliacao["prioridade"]

    if avaliacao["bloqueio_de_morgan"]:
        acao = "Bloquear a operação e solicitar validação humana dos dados e da segurança."
    elif prioridade == "critica":
        acao = "Isolar o subsistema afetado e acionar imediatamente o Centro de Controle."
    elif prioridade == "alta":
        acao = "Abrir atendimento prioritário e monitorar continuamente o módulo."
    else:
        acao = "Registrar a ocorrência e manter o monitoramento de rotina."

    return {
        "alerta_id": alerta["id"],
        "modulo": modulo["nome"],
        "prioridade": prioridade,
        "resumo": alerta["mensagem"],
        "acao_recomendada": acao,
        "requer_supervisao_humana": prioridade in {"critica", "alta"},
        "justificativa_logica": (
            "A regra F OR (E AND M) resultou em "
            f"{avaliacao['regra_simplificada']}; "
            "o bloqueio NOT(S AND D) resultou em "
            f"{avaliacao['bloqueio_de_morgan']}."
        ),
        "observacao_etica": (
            "A resposta utiliza somente dados operacionais e não substitui "
            "a decisão dos especialistas humanos."
        ),
    }


def imprimir_analise(
    alerta: Dict[str, Any], modulo: Dict[str, Any], avaliacao: Dict[str, Any]
) -> None:
    """Apresenta a avaliação lógica com suas variáveis."""
    subtitulo(f"ANÁLISE DE {alerta['id']} - {modulo['nome']}")
    print(
        f"F={alerta['falha']} | C={alerta['critico']} | "
        f"E={alerta['consumo_elevado']} | M={modulo['essencial']}"
    )
    print("Original     : (F AND C) OR (F AND NOT C) OR (E AND M)")
    print("Simplificada : F OR (E AND M)")
    print(f"Resultado original     : {avaliacao['regra_original']}")
    print(f"Resultado simplificado : {avaliacao['regra_simplificada']}")
    print(f"Equivalência confirmada: {avaliacao['expressoes_equivalentes']}")
    print(
        "De Morgan     : NOT(S AND D) = (NOT S) OR (NOT D) -> "
        f"bloqueio={avaliacao['bloqueio_de_morgan']}"
    )
    print(f"Prioridade final: {avaliacao['prioridade'].upper()}")


def selecionar_alerta(dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Lista alertas e devolve o selecionado."""
    if not dados["alertas"]:
        print("Nenhum alerta disponível.")
        return None
    print("\nAlertas disponíveis:")
    for indice, alerta in enumerate(dados["alertas"], start=1):
        print(f"  [{indice}] {alerta['id']} - {alerta['tipo']} - {alerta['status']}")
    opcoes = [str(i) for i in range(1, len(dados["alertas"]) + 1)]
    escolha = int(ler_opcao("Selecione o alerta: ", opcoes))
    return dados["alertas"][escolha - 1]


def registrar_interacao(
    dados: Dict[str, Any], alerta: Dict[str, Any], tipo_prompt: str, resposta: Dict[str, Any]
) -> None:
    """Persiste o histórico da simulação no JSON."""
    dados["interacoes"].append(
        {
            "id": proximo_id(dados["interacoes"], "INT-"),
            "data_hora": datetime.now().isoformat(timespec="seconds"),
            "origem_id": alerta["id"],
            "tipo_prompt": tipo_prompt,
            "resposta_simulada": resposta,
        }
    )
    salvar_dados(dados)


def analisar_alerta_interativo(dados: Dict[str, Any]) -> None:
    """Executa a validação lógica e a simulação inteligente de um alerta."""
    titulo("ANÁLISE DE ALERTA OPERACIONAL")
    alerta = selecionar_alerta(dados)
    if alerta is None:
        return
    modulo = buscar_modulo(dados, alerta["modulo_id"])
    if modulo is None:
        print("O módulo associado não foi encontrado.")
        return

    avaliacao = avaliar_regra(alerta, modulo)
    imprimir_analise(alerta, modulo, avaliacao)
    subtitulo("PROMPT ZERO-SHOT GERADO")
    print(montar_prompt_zero_shot(alerta, modulo))
    resposta = simular_resposta(alerta, modulo)
    subtitulo("RESPOSTA INTELIGENTE SIMULADA - STRUCTURED OUTPUT")
    print(json.dumps(resposta, ensure_ascii=False, indent=2))

    registrar_interacao(dados, alerta, "zero-shot", resposta)
    registrar_log(
        "alerta_analisado",
        f"{alerta['id']} | prioridade={avaliacao['prioridade']} | "
        f"bloqueio={avaliacao['bloqueio_de_morgan']}",
    )
    print("\nAnálise e interação salvas com sucesso.")


def exibir_prompts(dados: Dict[str, Any]) -> None:
    """Mostra zero-shot, few-shot e o contrato de saída estruturada."""
    titulo("PROMPT ENGINEERING")
    alerta = dados["alertas"][0]
    modulo = buscar_modulo(dados, alerta["modulo_id"])
    if modulo is None:
        print("Módulo de demonstração não encontrado.")
        return

    subtitulo("1. ZERO-SHOT PROMPTING")
    print(montar_prompt_zero_shot(alerta, modulo))
    subtitulo("2. FEW-SHOT PROMPTING")
    print(montar_prompt_few_shot(alerta, modulo, dados))
    subtitulo("3. STRUCTURED OUTPUT")
    print(json.dumps(dados["prompts"]["structured_output"], ensure_ascii=False, indent=2))


def simular_assistente_interativo(dados: Dict[str, Any]) -> None:
    """Simula uma interação few-shot e registra a resposta."""
    titulo("ASSISTENTE INTELIGENTE SIMULADO")
    alerta = selecionar_alerta(dados)
    if alerta is None:
        return
    modulo = buscar_modulo(dados, alerta["modulo_id"])
    if modulo is None:
        print("Módulo associado não encontrado.")
        return

    prompt = montar_prompt_few_shot(alerta, modulo, dados)
    resposta = simular_resposta(alerta, modulo)
    subtitulo("PROMPT FEW-SHOT")
    print(prompt)
    subtitulo("RESPOSTA SIMULADA")
    print(json.dumps(resposta, ensure_ascii=False, indent=2))
    registrar_interacao(dados, alerta, "few-shot", resposta)
    registrar_log(
        "interacao_simulada",
        f"{alerta['id']} | prompt=few-shot | prioridade={resposta['prioridade']}",
    )


def calcular_mse(valores_esperados: List[float], valores_obtidos: List[float]) -> float:
    """Calcula o erro quadrático médio entre dois conjuntos de avaliações."""
    if len(valores_esperados) != len(valores_obtidos) or not valores_esperados:
        raise ValueError("As listas devem possuir o mesmo tamanho e não podem ser vazias.")
    erros_quadrados = [
        (esperado - obtido) ** 2
        for esperado, obtido in zip(valores_esperados, valores_obtidos)
    ]
    return sum(erros_quadrados) / len(erros_quadrados)


def demonstrar_otimizacao(dados: Dict[str, Any]) -> None:
    """Compara um prompt genérico com um prompt estruturado por meio do MSE."""
    titulo("OTIMIZAÇÃO DA QUALIDADE DO PROMPT")
    avaliacao = dados["prompts"]["avaliacao_otimizacao"]
    criterios = avaliacao["criterios"]
    alvo = avaliacao["pontuacao_alvo"]
    antes = avaliacao["prompt_generico"]["pontuacoes"]
    depois = avaliacao["prompt_otimizado"]["pontuacoes"]
    mse_antes = calcular_mse(alvo, antes)
    mse_depois = calcular_mse(alvo, depois)
    reducao = ((mse_antes - mse_depois) / mse_antes) * 100

    print("Prompt inicial:")
    print("  " + avaliacao["prompt_generico"]["texto"])
    print("\nPrompt otimizado:")
    print("  " + avaliacao["prompt_otimizado"]["texto"])
    print("\nComparação simulada de qualidade (alvo = 1,00):")
    for criterio, valor_antes, valor_depois in zip(criterios, antes, depois):
        print(f"  {criterio:<18} antes={valor_antes:.2f} | depois={valor_depois:.2f}")
    print(f"\nMSE antes : {mse_antes:.4f}")
    print(f"MSE depois: {mse_depois:.4f}")
    print(f"Redução do erro: {reducao:.1f}%")
    print(
        "\nInterpretação: a melhoria das instruções funciona como uma etapa de "
        "otimização. O MSE mede a distância entre a qualidade observada e o "
        "alvo. Em modelos treinados, o gradiente descendente ajustaria parâmetros; "
        "neste protótipo, ajustamos o prompt. A regularização inspira a evitar "
        "regras excessivamente específicas, e os testes com diferentes módulos "
        "avaliam a capacidade de generalização."
    )


def exibir_memoria_etica() -> None:
    """Relaciona o protótipo à arquitetura computacional e ao uso responsável."""
    titulo("MEMÓRIA, FLUXO DE DADOS, ÉTICA E RESPONSABILIDADE")
    print(
        fill(
            "Fluxo computacional: ao abrir dados_colonia.json, os bytes são lidos "
            "do armazenamento persistente e transportados pelos barramentos até a "
            "memória principal. O Python converte o conteúdo em dicionários e listas, "
            "que o processador utiliza para aplicar as regras. Ao salvar, o caminho "
            "é inverso: memória, barramentos e dispositivo de armazenamento. O TXT "
            "mantém um histórico legível por pessoas; o JSON preserva relações e "
            "tipos de dados para processamento automático.",
            width=LARGURA,
        )
    )
    print()
    print(
        fill(
            "Responsabilidade: o NCAS não usa etnia, origem, gênero, deficiência ou "
            "qualquer característica pessoal para priorizar atendimento. As decisões "
            "se baseiam apenas em risco operacional. A linguagem deve ser inclusiva, "
            "os dados precisam ser revisados para detectar vieses e decisões críticas "
            "exigem supervisão humana. A simulação não substitui especialistas e deve "
            "manter trilhas de auditoria para permitir contestação e correção.",
            width=LARGURA,
        )
    )


def executar_demonstracao() -> None:
    """Demonstra os principais requisitos sem solicitar entradas do usuário."""
    dados = carregar_dados()
    titulo("DEMONSTRAÇÃO AUTOMÁTICA - NCAS")
    imprimir_modulos(dados["modulos"])
    imprimir_alertas(dados["alertas"], dados)

    alerta = dados["alertas"][0]
    modulo = buscar_modulo(dados, alerta["modulo_id"])
    if modulo is None:
        raise ValueError("Módulo da demonstração não encontrado.")
    avaliacao = avaliar_regra(alerta, modulo)
    imprimir_analise(alerta, modulo, avaliacao)
    subtitulo("SAÍDA ESTRUTURADA SIMULADA")
    print(json.dumps(simular_resposta(alerta, modulo), ensure_ascii=False, indent=2))
    demonstrar_otimizacao(dados)
    exibir_memoria_etica()
    titulo("DEMONSTRAÇÃO CONCLUÍDA")


def executar_autoteste() -> None:
    """Valida arquivos, JSON, equivalência booleana e otimização simulada."""
    dados = carregar_dados()
    assert ARQUIVO_TEXTO.exists(), "Arquivo texto obrigatório ausente."
    assert dados["modulos"], "É necessário ao menos um módulo."
    assert dados["alertas"], "É necessário ao menos um alerta."

    for f, c, e, m in itertools.product([False, True], repeat=4):
        alerta = {
            "falha": f,
            "critico": c,
            "consumo_elevado": e,
            "seguranca_ok": True,
            "dados_consistentes": True,
        }
        modulo = {"essencial": m}
        assert regra_original(alerta, modulo) == regra_simplificada(alerta, modulo)

    avaliacao = dados["prompts"]["avaliacao_otimizacao"]
    mse_antes = calcular_mse(
        avaliacao["pontuacao_alvo"], avaliacao["prompt_generico"]["pontuacoes"]
    )
    mse_depois = calcular_mse(
        avaliacao["pontuacao_alvo"], avaliacao["prompt_otimizado"]["pontuacoes"]
    )
    assert mse_depois < mse_antes, "O prompt otimizado deveria reduzir o MSE."

    for alerta in dados["alertas"]:
        modulo = buscar_modulo(dados, alerta["modulo_id"])
        assert modulo is not None, f"Módulo ausente no alerta {alerta['id']}"
        resposta = simular_resposta(alerta, modulo)
        json.dumps(resposta, ensure_ascii=False)

    print("AUTOTESTE NCAS: 100% dos testes concluídos com sucesso.")
    print("- JSON válido e estrutura obrigatória presente")
    print("- Arquivo texto encontrado")
    print("- 16 combinações booleanas equivalentes")
    print("- Structured outputs serializáveis")
    print("- MSE do prompt otimizado menor que o inicial")


def menu_principal() -> None:
    """Executa o menu interativo do Núcleo Cognitivo."""
    garantir_arquivo_texto()
    try:
        dados = carregar_dados()
    except (FileNotFoundError, ValueError) as erro:
        print(f"ERRO DE INICIALIZAÇÃO: {erro}")
        return

    while True:
        titulo("NCAS - NÚCLEO COGNITIVO DA AURORA SIGER")
        print("[1] Cadastrar alerta da colônia")
        print("[2] Consultar dados salvos em JSON")
        print("[3] Gravar registro no arquivo texto")
        print("[4] Ler registros do arquivo texto")
        print("[5] Analisar alerta com regra booleana")
        print("[6] Exibir prompts estruturados")
        print("[7] Simular resposta do assistente inteligente")
        print("[8] Demonstrar otimização e erro quadrático médio")
        print("[9] Explicar memória, fluxo de dados, ética e diversidade")
        print("[0] Encerrar")
        escolha = ler_opcao("\nDigite a opção desejada: ", list("0123456789"))

        if escolha == "1":
            cadastrar_alerta(dados)
        elif escolha == "2":
            consultar_registros(dados)
        elif escolha == "3":
            gravar_registro_texto()
        elif escolha == "4":
            ler_registros_texto()
        elif escolha == "5":
            analisar_alerta_interativo(dados)
        elif escolha == "6":
            exibir_prompts(dados)
        elif escolha == "7":
            simular_assistente_interativo(dados)
        elif escolha == "8":
            demonstrar_otimizacao(dados)
        elif escolha == "9":
            exibir_memoria_etica()
        else:
            registrar_log("sistema_encerrado", "Encerramento solicitado pelo usuário")
            print("\nNCAS encerrado. Os dados foram preservados.")
            break

        input("\nPressione ENTER para retornar ao menu...")


def main() -> None:
    """Processa argumentos de linha de comando ou abre o menu."""
    parser = argparse.ArgumentParser(description="Núcleo Cognitivo da Aurora Siger")
    parser.add_argument(
        "--demo", action="store_true", help="executa uma demonstração automática"
    )
    parser.add_argument(
        "--self-test", action="store_true", help="valida arquivos e regras do projeto"
    )
    argumentos = parser.parse_args()
    if argumentos.self_test:
        executar_autoteste()
    elif argumentos.demo:
        executar_demonstracao()
    else:
        menu_principal()


if __name__ == "__main__":
    main()
