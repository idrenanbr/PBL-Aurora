# Fase 5 - Núcleo Cognitivo da Aurora Siger (NCAS)

Protótipo em Python para registrar, consultar e interpretar informações operacionais da colônia Aurora Siger. A solução integra arquivos texto, JSON, lógica booleana, engenharia de prompts, simulação de IA generativa, análise de otimização, arquitetura de computadores e uso responsável da inteligência artificial.

## Como executar

Pré-requisito: Python 3.9 ou superior. Não é necessário instalar bibliotecas externas nem configurar uma API.

```bash
cd Fase_5_NCAS
python codigo_fonte.py
```

Demonstração automática para ensaio do vídeo:

```bash
python codigo_fonte.py --demo
```

Validação automática dos arquivos e das regras:

```bash
python codigo_fonte.py --self-test
```

## Funcionalidades do menu

1. Cadastrar alertas da colônia e persistir os dados em JSON.
2. Consultar módulos, alertas, solicitações e interações salvas.
3. Acrescentar registros ao arquivo texto.
4. Ler os registros persistidos em TXT.
5. Analisar um alerta por uma regra booleana original e simplificada.
6. Exibir prompts zero-shot, few-shot e o contrato de saída estruturada.
7. Simular localmente a resposta de um assistente inteligente.
8. Comparar um prompt genérico e um otimizado por erro quadrático médio.
9. Explicar memória, armazenamento, fluxo de dados, ética e diversidade.

## Organização e justificativa dos dados

- `dados_colonia.json`: armazena informações estruturadas e relacionadas. Módulos, alertas, solicitações, interações e prompts precisam manter chaves, tipos booleanos, listas e relações por identificador. JSON permite validação e processamento direto pelo Python.
- `registros_colonia.txt`: mantém uma trilha cronológica simples, incremental e legível por pessoas. O modo `append` adiciona eventos sem apagar o histórico anterior.

O programa demonstra leitura (`r`), escrita (`w`), criação exclusiva (`x`) e adição com leitura (`a+`) por meio do gerenciador de contexto `with`. Também utiliza explicitamente `read()`, `readline()`, `readlines()`, `write()` e `writelines()`. O modo `x` cria o TXT somente quando ele ainda não existe; `a+` acrescenta eventos sem apagar o histórico e mantém disponível a capacidade de leitura.

## Regra lógica

Variáveis:

- `F`: há uma falha confirmada.
- `C`: a ocorrência foi classificada como crítica.
- `E`: existe consumo elevado.
- `M`: o módulo é essencial.

Expressão original:

```text
A = (F AND C) OR (F AND NOT C) OR (E AND M)
```

Simplificação:

```text
A = F OR (E AND M)
```

Pela distributividade, os dois primeiros termos se tornam `F AND (C OR NOT C)`. Como `C OR NOT C = 1`, temos `F AND 1 = F`.

Uma segunda regra aplica De Morgan para bloquear operações sem segurança ou sem dados consistentes:

```text
B = NOT (S AND D) = (NOT S) OR (NOT D)
```

Os detalhes, a tabela-verdade e exemplos estão em `regras_logicas.pdf`.

## Simulação de IA

A integração com uma API não é necessária. O código monta prompts completos e produz respostas determinísticas por regras auditáveis. Isso permite demonstrar:

- Zero-shot: uma instrução sem exemplos prévios.
- Few-shot: dois exemplos antes do caso atual.
- Structured output: resposta em JSON com campos obrigatórios.
- Supervisão humana: alertas críticos ou altos nunca são tratados como decisões autônomas finais.

## Otimização e aprendizado de máquina

O projeto compara uma instrução genérica com uma instrução estruturada. Quatro dimensões simuladas - clareza, completude, formato e segurança - são avaliadas contra o alvo `1,0`. O erro quadrático médio diminui depois da melhoria do prompt.

Essa comparação é educacional e não representa treinamento real. O gradiente descendente é relacionado ao processo iterativo de reduzir o erro; a regularização inspira a evitar instruções excessivamente específicas; e a generalização é avaliada usando alertas de módulos diferentes.

## Memória, armazenamento e fluxo

O JSON e o TXT permanecem no armazenamento secundário após o encerramento do programa. Durante a execução, os bytes são lidos para a memória principal, transportados pelos barramentos e processados pela CPU. Ao salvar, o fluxo retorna da memória para o dispositivo de armazenamento.

## Ética, diversidade e responsabilidade

O NCAS utiliza somente variáveis operacionais para priorizar ocorrências. Etnia, origem, gênero, deficiência e outras características pessoais não participam das regras. A solução recomenda revisão de dados, linguagem inclusiva, trilha de auditoria, possibilidade de contestação e supervisão humana para qualquer decisão crítica.

## Arquivos da entrega

- `codigo_fonte.py`
- `dados_colonia.json`
- `registros_colonia.txt`
- `regras_logicas.pdf`
- `prompts_utilizados.pdf`
- `link_video.txt`

Materiais auxiliares:

- `roteiro_video.md`: roteiro cronometrado para uma apresentação de até cinco minutos.
- `README.md`: instruções, justificativas e visão geral técnica.

## Equipe

| Nome | RM |
|---|---|
| Juan de Lucas Frois | RM563260 |
| Flávia Roberta Pennachin | RM561860 |
| Pedro Valente Toledo | RM570394 |
| Renan Mano Otero | RM573615 |

FIAP - Ciência da Computação - Turma 1CCOA - 2026.
