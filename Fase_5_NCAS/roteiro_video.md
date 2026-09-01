# Roteiro do vídeo - Fase 5 NCAS

Duração planejada: **4 minutos e 50 segundos**. Limite do enunciado: 5 minutos.

Antes de gravar, abra o terminal na pasta `Fase_5_NCAS`, aumente a fonte e execute `python codigo_fonte.py`. Deixe também os PDFs disponíveis para compartilhamento de tela.

## 0:00-0:25 - Abertura e objetivo

**Tela:** pasta da Fase 5 ou título do sistema.

**Fala sugerida:**

> Olá, somos a equipe da Missão Aurora Siger. Nesta quinta fase desenvolvemos o NCAS, Núcleo Cognitivo da Aurora Siger. Ele é um protótipo em Python que organiza dados da colônia, mantém registros persistentes, aplica regras booleanas e simula respostas inteligentes por prompts estruturados. A API de IA é opcional no enunciado, por isso adotamos uma simulação local, determinística e auditável.

## 0:25-0:55 - Arquivos e persistência

**Tela:** mostrar `dados_colonia.json` e `registros_colonia.txt` rapidamente.

**Fala sugerida:**

> Escolhemos JSON para módulos, alertas, solicitações, interações e prompts porque esses dados possuem chaves, tipos e relações. O TXT funciona como log cronológico legível por pessoas. O Python utiliza `with open`, leitura no modo `r`, escrita no modo `w` e acréscimo no modo `a`. Assim, os dados permanecem disponíveis mesmo depois do encerramento do programa.

## 0:55-1:35 - Menu, leitura e gravação

**Tela:** executar opções 2 e 3 do menu. Na opção 2, selecionar alertas. Na opção 3, escrever um registro curto, como `Teste de redundância concluído`.

**Fala sugerida:**

> O menu permite cadastrar e consultar registros, ler e gravar arquivos, analisar alertas e demonstrar os prompts. Aqui consultamos os alertas estruturados do JSON. Agora adicionamos um registro ao TXT usando append, sem apagar o histórico. As mensagens indicam claramente a origem, o status e a prioridade de cada ocorrência.

## 1:35-2:20 - Regra booleana e simplificação

**Tela:** selecionar a opção 5 e o alerta `ALT-001`. Depois mostrar a primeira página técnica de `regras_logicas.pdf`.

**Fala sugerida:**

> A regra original é: falha e crítico, ou falha e não crítico, ou consumo elevado e módulo essencial. Fatorando a variável falha, obtemos falha vezes crítico ou não crítico. Como uma variável ou sua negação sempre resulta em verdadeiro, a expressão simplifica para: falha, ou consumo elevado e módulo essencial. A tabela-verdade confirma equivalência nas dezesseis combinações. Também usamos De Morgan: negar segurança e dados consistentes equivale a ausência de segurança ou inconsistência nos dados. Isso bloqueia a operação para revisão humana.

## 2:20-3:15 - Prompts e simulação inteligente

**Tela:** continuar a saída da opção 5 e depois abrir a opção 6.

**Fala sugerida:**

> O sistema cria um prompt zero-shot com papel, tarefa, dados, restrições e formato de saída. No few-shot, apresentamos dois exemplos para padronizar a classificação do caso atual. O structured output exige JSON válido com alerta, prioridade, resumo, ação, justificativa lógica e supervisão humana. A resposta exibida é simulada localmente a partir das regras; ela não inventa informações e não substitui a decisão dos especialistas.

## 3:15-3:50 - Otimização, MSE e generalização

**Tela:** executar opção 8.

**Fala sugerida:**

> Para relacionar o projeto à otimização, comparamos um prompt genérico com um estruturado nas dimensões clareza, completude, formato e segurança. Calculamos o erro quadrático médio contra a qualidade-alvo. A versão estruturada reduz fortemente o erro. A analogia com gradiente descendente está na melhoria iterativa; a regularização evita um prompt excessivamente específico; e diferentes tipos de alerta ajudam a observar generalização. As pontuações são uma simulação didática, não treinamento real de modelo.

## 3:50-4:20 - Memória e fluxo de dados

**Tela:** executar opção 9.

**Fala sugerida:**

> No nível computacional, JSON e TXT ficam no armazenamento persistente. Ao abrir um arquivo, seus bytes atravessam os barramentos e chegam à memória principal. O Python cria dicionários e listas, a CPU aplica as regras e, ao salvar, os dados retornam ao armazenamento. Portanto, o fluxo de software depende diretamente de memória, entrada e saída e movimentação interna de dados.

## 4:20-4:50 - Ética e encerramento

**Tela:** manter a opção 9 ou mostrar a conclusão de `prompts_utilizados.pdf`.

**Fala sugerida:**

> O NCAS prioriza ocorrências somente por risco operacional. Características como etnia, gênero, origem ou deficiência nunca entram na regra. Mantemos linguagem inclusiva, auditoria, revisão de possíveis vieses e supervisão humana em decisões críticas. Dessa forma, o protótipo integra programação, lógica, prompts, otimização, arquitetura de computadores e responsabilidade social. Obrigado.

## Checklist antes de publicar

- Confirmar que a gravação possui no máximo 5 minutos.
- Demonstrar leitura e gravação reais, sem apenas mostrar o código.
- Deixar visível a regra original e a simplificada.
- Mostrar ao menos um prompt e uma resposta estruturada.
- Mencionar que a otimização é uma simulação educacional.
- Publicar no YouTube como **Não listado**.
- Colar o endereço no arquivo `link_video.txt`.
- Gerar novamente o ZIP depois de atualizar o link.
