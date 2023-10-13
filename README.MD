# Projeto para treinamento de ETL

Este projeto tem o objetivo de cumprir um desafio da DIO de desenvolvimento de um ETL.
O projeto consiste na decomposição de um campo de endereço completo em informações separadas pré-validadas por uma api.
Escolhi fazer dois scripts como opções para o tratamento de endereço:
- O script enderecos_via_cep.py extrai o cep do endereço e busca os dados na api do [ViaCEP](https://viacep.com.br/)
- O script enderecos_ideal_postcodes.py utiliza a api da [IdealPostcodes](https://ideal-postcodes.co.uk/)

> Ambos os scripts já contam com a criação de uma base de dados sqlite para teste do script.