
Conheça a Zoe - A Inteligência Artificial da Vincers!

Ainda estou configurando para colocar ela totalmente online, mas já é um começo para começar a testar essa nova versão da Zoe!

Para rodar, basta seguir os seguintes passos:

	------

	1. Abra o terminal e troque para a pasta baixada
	(Para trocar entre pastas basta escrever

		cd NomeDaPasta/PróximaPasta/Zoe

	------
	
	2. Dentro da pasta Zoe, rode as seguintes linhas de comando

		python3 -m venv virt

		source virt/bin/activate 

		pip install flask==1.0.2   

		pip freeze > requirements.txt 

		python application.py  

	------

	3. Se tudo der certo, basta copiar a url abaixo e colar no seu navegador!

		http://127.0.0.1:5000/

	------

Para trabalhar com a Zoe:

	O arquivo para upload é o gerado na transcrição da AWS - basta clicar 'Download full transcript'.
	O formato desse arquivo é .json

	É possível ver se está dando certo pelas frases logo embaixo do logo.

	Ao subir o arquivo, clique em enviar transcrição. Se aparecer a mensagem que deu certo, clique em baixar legenda.

	Lembre-se de apagar o '.html' do final do nome do arquivo.

	Para enviar novamente, clique no botão de voltar do navegador e atualize a página. A mensagem de Vamos começar deve aparecer.
