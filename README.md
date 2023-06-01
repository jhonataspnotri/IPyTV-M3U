#IPTVPlayer
IPTVPlayer é um player de IPTV que permite carregar um arquivo M3U contendo uma lista de canais e reproduzir os canais selecionados. Ele é escrito em Python e usa a biblioteca PyQt5 para a interface gráfica e a biblioteca VLC para a reprodução de mídia.

Funcionalidades
- Carrega uma lista de canais a partir de um arquivo M3U
- Permite filtrar e pesquisar canais na lista
- Reproduz o canal selecionado
- Possui controles de reprodução (play, pause, stop, avançar, retroceder)
- Permite ajustar o volume de áudio
- Possui botões para selecionar o próximo ou o canal anterior na lista
- Permite avançar ou retroceder a reprodução em 10 segundos

Como usar?
instale usando os comandos no terminal

git clone https://github.com/jhonataspnotri/IPyTV-M3U.git

após isso acesse a pasta com:

cd IPyTV-M3U

Para usar o IPTVPlayer, siga os seguintes passos:

Execute o comando a seguir para iniciar o programa.:

python3 main.py 

Clique no botão "Selecionar arquivo" para carregar o arquivo M3U contendo a lista de canais.
Selecione um canal na lista e clique no botão "Play" para reproduzi-lo.
Use os botões de controle de reprodução para pausar, parar, avançar ou retroceder a reprodução.
Use o controle de volume para ajustar o nível de áudio.

Requisitos:
Testado e funcional no Ubuntu 22.04 Lts
Python 3
PyQt5
VLC

Contribuição:
Contribuições são bem-vindas! Se você quiser contribuir com o IPTVPlayer, siga os seguintes passos:

Faça um fork do repositório.
Crie um branch para a sua contribuição (git checkout -b minha-contribuicao).
Faça as alterações necessárias.
Faça o commit das alterações (git commit -am 'Adicionando minha contribuição').
Faça o push do branch para o seu fork (git push origin minha-contribuicao).
Abra um pull request no repositório original.
Licença
Este código é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
