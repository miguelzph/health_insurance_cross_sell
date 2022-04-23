# Health Insurance Cross Sell

![image](https://user-images.githubusercontent.com/64989931/164603908-81c192b7-0e45-4133-96fe-5f298aeb3371.png)

# 1. Business Problem.
A Insurance All é uma empresa que fornece seguro de saúde para seus clientes e o time de produtos está analisando a possibilidade de oferecer aos assegurados, um novo produto: Um seguro de automóveis.

Para isso, a empresa fez uma pesquisa com cerca de 380 mil clientes sobre o interesse em aderir a um novo produto de seguro de automóveis, no ano passado. Todos os clientes demonstraram interesse ou não em adquirir o seguro de automóvel e essas respostas ficaram salvas em um banco de dados junto com outros atributos dos clientes. Porém, o time de produtos selecionou novos clientes que não responderam a pesquisa para participar de uma campanha, no qual receberão a oferta do novo produto de seguro de automóveis.

Nesse contexto, o projeto tem como principal objetivo analisar os dados do banco de dados e responder as seguintes perguntas:
1. Principais Insights sobre os atributos mais relevantes de clientes interessados em adquirir um seguro de automóvel.
2. Qual a porcentagem de clientes interessados em adquirir um seguro de automóvel, o time de vendas conseguirá contatar fazendo 20.000 ligações?
3. E se a capacidade do time de vendas aumentar para 40.000 ligações, qual a porcentagem de clientes interessados em adquirir um seguro de automóvel o time de vendas conseguirá contatar?
4. Quantas ligações o time de vendas precisa fazer para contatar 80% dos clientes interessados em adquirir um seguro de automóvel?

Os dados para esse problema estão disponíveis no <a href="https://www.kaggle.com/datasets/anmolkumar/health-insurance-cross-sell-prediction" title="Clique e acesse agora!" target="_blank">Kaggle</a>.

# 2. Business Assumptions.
- Para avaliação e resposta das perguntas de negócio será utilizado 20% do dateset (76222 clientes)
- Para a simulação final do resultado de negócio:
  - Um cliente interessado têm 50% chance de realmente comprar o seguro.
  - Cada cliente vai pagar 2000 unidades monetárias no seguro de automóveis.
  - O custo para entrar em contato com o cliente será de 100.

# 3. Solution Strategy  
Nesse tópico serão listados os passos seguidos para encontrar a solução, sempre com foco em entregar valor o mais rápido possível e de forma cíclica. A abordagem do problema não seguirá o modelo de classificação tradicional tentando classificar em interessado, e sim gerando um score de propensão de compra para rankear os clientes, e permitir otimizar a ordenação da lista de contatos enviadas para o setor comercial.

Veja o notebook completo em: <a href="https://nbviewer.org/github/miguelzph/health_insurance_cross_sell/blob/main/notebooks/sprint03_health_insurance_cross_sell.ipynb" title="Clique e acesse agora!" target="_blank">Link no nbviewer</a>

### Step 01. Data Description
O dataset disponível possui 381109 linhas e 12 colunas que são:
| Feature | Descrição |
|--- |--- |
| Id | identificador único do cliente |
| Gender | gênero do cliente. |
| Age | idade do cliente. |
| Driving License | 0, o cliente não tem permissão para dirigir e 1, o cliente tem habilitação para dirigir |
| Region Code | código da região do cliente |
| Previously Insured | 0, o cliente não tem seguro de automóvel e 1, o cliente já tem seguro de automóvel. |
| Vehicle Age | idade do veículo |
| Anual Premium | quantidade que o cliente pagou à empresa pelo seguro de saúde anual. |
| Policy sales channel | código anônimo para o canal de contato com o cliente. |
| Vintage | número de dias que o cliente se associou à empresa através da compra do seguro de saúde. |
| Response | 0, o cliente não tem interesse e 1, o cliente tem interesse. |

Nesse passo foram avaliados valores vazios e tipo dos dados, porém nenhuma mudança foi necessária. Além disso, foram avaliadas também algumas métricas chaves dos valores númericos:

![image](https://user-images.githubusercontent.com/64989931/164591100-50a56653-fd27-4385-b0ef-1bcfd19d1aa9.png)

E a análise primária das variáveis categóricas textuais:

![image](https://user-images.githubusercontent.com/64989931/164591823-bad5e217-f3e8-45ff-a0a5-8035a643ef3f.png)

### Step 02. Feature Engineering 
Nesse passo as features disponíveis foram avaliadas:

![image](https://user-images.githubusercontent.com/64989931/164575385-2a287d5f-38e2-4a30-9f87-07b23d690b95.png)

Para a criação das seguintes hipóteses:
- Hipóteses Usuários:
  - H1. Usuários que são clientes a mais tempo respondem mais que querem o seguro.
  - H2. Usuários que já tem seguro de carro, são os que menos querem o novo produto.
  - H3. Usuários com idade mais avançada são os que mais querem o seguro.
  - H4. Usuários que pagam mais no seguro de saúde são os que mais querem o seguro.
  - H5. Usuários da nossa região mais populosa são os que mais querem o seguro.
- Hipóteses Veículos:
  - H6. Usuários com veículos mais antigo são os que menos querem o seguro.
  - H7. Usuários com com veículos que já foram danificados, são os que mais querem o seguro.
Até o ciclo atual, nenhuma nova feature foi criada.

### Step 03. Data Filtering
Nenhum restição de negócio foi encontrada até o momento, com isso nenhuma feature foi filtrada.

### Step 04. Exploratory Data Analysis
- Análise Univariada das Variáveis
- Análise Bivariada das Variáveis (Validação das Hipóteses)
- Análise Multivariada das Variáveis
  - Númericas: Correlação de Pearson
  - Categóricas: Cramer's V

### Step 05. Data Preparation
O Dataset foi separado em treino e teste (também utilizado para performance de negócio), e foi construida e aplicada uma classe que utilizava os seguintes métodos: 

- Para scaling:
  - RobustScaler (Quando havia muitos outliers)
  - MinMaxScaler 
- Encoding:
  - Label Encoding
  - TargetEncoder
  - OneHotEncoder

### Step 06. Feature Selection 
Os critérios para seleção de feature foram:
- EDA
- RandomForestClassifier para buscar a importância das features:

 ![image](https://user-images.githubusercontent.com/64989931/164580588-13dbf542-59d8-469f-8f5b-e249c189babe.png)

- Boruta que selecionou as features: **age** e **vintage**

Com isso, as features selecionadas foram:
- **vintage**
- **annual_premium**
- **age**
- **region_code**
- **policy_sales_channel**
- **vehicle_damage**
- **previously_insured**

### Step 07. Machine Learning Modelling 
Aplicados os seguindos modelos de ML:
- KNeighborsClassifier
- LogisticRegression
- RandomForestClassifier
- ExtraTreesClassifier
- XGBClassifier
- MLPClassifier

### Step 08. Hyperparameter Fine Tunning 
A biblioteca **hyperopt** foi utilizada para tunagem do modelo selecionado, porém sem grandes ganhos na performance.

### Step 09. Convert Model Performance to Business Values
Nesse passo o resultado do modelo de ML foi transformado em resultado de negócio e nas respostas que o problema de negócio visava responder.

### Step 10. Deploy Modelo to Production
O modelo foi retreinado com todos os dados, e seu deploy foi feito via API utilizando o Heroku. Além disso, foi desenvolvido script para que uma planilha do google sheets consiga acessar essa API e devolver o score de propensão de compra.

# 4. Top 3 Data Insights

**Hipótese 4: Usuários que pagam mais no seguro de saúde são os que mais querem o seguro para veículos**<br>
  **VERDADEIRO** - Há tendência de interesse maior para os usuários que gastam mais (dentro de intervalos com mais clientes)<br>
![image](https://user-images.githubusercontent.com/64989931/164580032-27138192-e2ec-4cba-8c24-3c4525fdf95d.png)<br>

**Hipótese 6: Usuários com veículos mais antigo são os que menos querem o seguro**<br>
  **FALSO** - Quanto mais antigo o carro maior o interesse do cliente no seguro<br>
![image](https://user-images.githubusercontent.com/64989931/164575575-938ec2ac-fa7b-45ee-844b-ffb8e496c491.png)<br>

**Hipótese 7: Clientes com veículos que já foram danificados, são os que mais querem o seguro**<br>
  **VERDADEIRO** - A esmagadora maioria dos clientes que estão interessados já tiveram seu veículos danificados<br>
![image](https://user-images.githubusercontent.com/64989931/164579220-6a463bf5-db52-470f-b732-0a8f3b9a2bb1.png)<br>


# 5. Machine Learning Model Applied
Apesar de ser um problema de classificação, utilizar métricas como a acuarácia, não é a melhor abordagem para o problema. Por isso, foram utilizadas duas métricas:
- SUM of Recall at K (Métrica Principal)
  - Recall at K é o % de interessados impactados quando selecionamos K clientes ordenados de acordo com o modelo.
  - Para tentar medir melhor será utilizado a soma do Recall at K em diferentes pontos.
  - Default:
    - 10%, 20%, 30% e 40% 
    - Consequentemente o valor de comparação de um modelo aleátorio será 1 (0.1+0.2+0.3+0.4).
- ROC_AUC
  - Resume a cuva ROC em um único valor --> A área baixo da curva ROC.
  - Vai de 0 a 1, onde 1 o modelo tem 100% das previsões corretas.

O resultado dessas métricas para os modelos avaliados, já utilizando a técnica de cross-validation com k=5, foi:

![image](https://user-images.githubusercontent.com/64989931/164581751-69d3bd85-1cda-4b21-8a8b-8567997cf6fd.png)

**O resultado do XGBoost Classifier foi o melhor e por isso ele será utilizado.**

- Obs1: Tentei tunar o Logistic Regression, mas ele continuou pior que o XGBoost Classifier.
- Obs2: O MLP Classifier possui boa performance, porém devido a complexidade não foi selecionado (A tentativa de tunar e reavaliar ficará para um próximo ciclo).

# 6. Machine Learning Model Performance
O resultado do XGBoost após o fine tuning com cross-validation é:

![image](https://user-images.githubusercontent.com/64989931/164582620-ed7bedbd-bed7-4c50-8446-7290feb59f0a.png)

Já avaliando os dados de teste o resultado foi:

![image](https://user-images.githubusercontent.com/64989931/164582672-1ace1068-6f25-443a-bcf0-99d57a120d7d.png)

O resultado do modelo final é muito interessante, chegando a ser mais de 3x melhor do que um modelo aleatório seria.

![image](https://user-images.githubusercontent.com/64989931/164583045-47c2b558-8aa5-4647-b8f4-824884dfb831.png)

Esse ganho também pode ser observado com a curva de ganho, já que ordenando os usuários de acordo com o modelo final, é possível selecionar quase 100% dos interessados, ao escolher 50% da base de teste.

![image](https://user-images.githubusercontent.com/64989931/164583233-4722331b-36c5-4236-8ab7-ef0d3304aa58.png)


# 7. Business Results 
### Respondendo a perguntas de negócio:
**1. Qual a porcentagem de clientes interessados em adquirir um seguro de automóvel, o time de vendas conseguirá contatar fazendo 20.000 ligações?**
  - Com 20.000 ligações (26.24% da base de testes) será possível impactar 70.57% dos clientes interessados.

**2. E se a capacidade do time de vendas aumentar para 40.000 ligações, qual a porcentagem de clientes interessados em adquirir um seguro de automóvel o time de vendas conseguirá contatar?**
 - Com 40.000 ligações (52.48%) será possível impactar 99.43% dos clientes interessados.

**3. Quantas ligações o time de vendas precisa fazer para contatar 80% dos clientes interessados em adquirir um seguro de automóvel?**
 - Para impactar 80% dos interessados é necessário contactar 23775 (31.19%)

# 8. Conclusions
### Simulação de ganho financeiro:
Assumindo:
  - Custo por contato = 100 unidades monetárias
  - Receita do cliente = 2000 unidades monetárias
  - Probabilidade do cliente que respondeu estar interessado realmente comprar = 50%

![image](https://user-images.githubusercontent.com/64989931/164584328-1d8cbfda-09cb-48d6-9f58-6cdc96196a8b.png)

Dentro desse cenário, ao contactar 42.17% (32142 clientes) da base de testes é possível obter um ganho financeiro de $5,565,500.00.

### Consumo da API via Google Sheets:
A solução para requisitar a previsão de propensão também foi estabelecida em uma planilha do google sheets:

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/64989931/164595494-498ec23f-e43a-4c0b-85e4-511e9d599d7f.gif)

A planilha está disponível em: <a href="https://docs.google.com/spreadsheets/d/1MhwpK0R-VQEoerJ_St5EQdZyMQAunC50X1cptpzFIoI/edit?usp=sharing" title="Clique e acesse agora!" target="_blank">Google Sheets</a>

# 9. Lessons Learned
- Resolver um problema de classificação de uma forma diferente, mas que trouxe um ótimo resultado.
- Consumo da API do modelo no Google Sheets.

# 10. Next Steps to Improve
- Melhorar os critérios assumidos na simulação de ganho financeiro, ex:
  - Utilizar valor fixo + % do annual_premium na receita por cliente
  - O valor de policy_sales_channel maior, provavelmente, deve ser de meios de contatos mais recente(email, whatsapp, telegram, etc) que tendem a ser mais baratos.
- Avaliar melhor o MLP Classifier (Hyperparameter Fine Tunning)
- Analisar melhor a variável vintage (buscar uma forma de analisar de forma temporal)


Veja o notebook completo em: <a href="https://nbviewer.org/github/miguelzph/health_insurance_cross_sell/blob/main/notebooks/sprint03_health_insurance_cross_sell.ipynb" title="Clique e acesse agora!" target="_blank">Link no nbviewer</a>
