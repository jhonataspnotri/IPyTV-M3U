# M3U-PLAYER-IPTV-PYTHON
M3U Player IPTV Python
Este é um player de IPTV em Python que usa a biblioteca VLC para reproduzir streams de IPTV. Ele permite ao usuário selecionar canais de IPTV a partir de um arquivo M3U e reproduzi-los em uma janela de player de vídeo.

Requisitos
Python 3.6 ou superior
Biblioteca VLC
Biblioteca PyQt5
Testado no Linux dist Ubuntu 22.04 Lts
Instalação
Para instalar as dependências do programa, você pode usar o pip:

Copy

pip install python-vlc PyQt5

Como usar
Para executar o programa, execute o arquivo main.py:

Copy

python3 main.py

O programa irá abrir uma janela com a lista de canais disponíveis. Selecione um canal e clique no botão "Play" para reproduzir o stream.

Você também pode acessar as configurações do programa clicando no botão "Configurações". Lá, você pode configurar várias opções, como o diretório onde o arquivo M3U está localizado e a resolução do vídeo.

Estrutura do código
main.py: ponto de entrada do programa, contém a lógica principal do player.
ui: pasta contendo os arquivos de interface do usuário criados com a biblioteca PyQt5.
vlc: pasta contendo os arquivos para interagir com a biblioteca VLC.
O código usa o padrão de design Model-View-Controller (MVC) para separar as diferentes responsabilidades do código. A classe MainWindow é a "View", ou seja, a camada de apresentação do player. Ela é responsável por exibir a interface do usuário e responder às interações do usuário, como clicar em botões ou selecionar streams.

A classe Controller é o "Controller", ou seja, a camada de controle do player. Ela é responsável por gerenciar os modelos de dados e controlar o fluxo de informações entre a interface do usuário e o modelo. Ela também gerencia a criação de instâncias da classe VLCPlayer e configura a reprodução de streams.

A classe ChannelModel é o "Model", ou seja, a camada de modelo de dados. Ela é responsável por gerenciar a lista de canais disponíveis para reprodução e atualizar a interface do usuário quando a lista é alterada.

Limitações
O programa pode não funcionar corretamente em todos os sistemas, dependendo das versões das bibliotecas usadas e das configurações do ambiente em que é executado. Certifique-se de verificar se todas as dependências foram instaladas corretamente e se o código está atualizado antes de usá-lo em um ambiente de produção.

Contribuindo
Se você quiser contribuir para o projeto, fique à vontade para enviar pull requests ou abrir issues no GitHub. Qualquer ajuda é bem-vinda!

Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
