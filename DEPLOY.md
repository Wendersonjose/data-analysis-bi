# Dashboard de Análise de Extratos Bancários

Dashboard interativo para análise de extratos bancários do Itaú PJ.

## 🚀 Deploy no Streamlit Cloud

### Passo 1: Preparar Repositório GitHub

1. Crie um repositório no GitHub
2. Faça upload dos seguintes arquivos:
   ```
   app.py
   requirements-streamlit.txt (renomear para requirements.txt)
   .streamlit/config.toml
   saida_analise/ (pasta completa com dados e gráficos)
   ```

### Passo 2: Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione:
   - Repository: seu-usuario/nome-do-repo
   - Branch: main
   - Main file path: app.py
5. Clique em "Deploy!"

### Passo 3: Configurar (Opcional)

Se precisar de configurações adicionais:
- Clique em "Advanced settings"
- Adicione secrets se necessário
- Configure Python version (3.12)

## 💻 Rodar Localmente

```bash
# Instalar dependências
pip install -r requirements-streamlit.txt

# Rodar aplicação
streamlit run app.py
```

A aplicação abrirá em: http://localhost:8501

## 📊 Funcionalidades

- ✅ Dashboard interativo com todos os gráficos
- ✅ Visualização de dados em tabelas
- ✅ Filtros por categoria e mês
- ✅ Download do Excel completo
- ✅ Métricas principais destacadas
- ✅ Design responsivo

## 🔐 Importante

**Não compartilhe dados financeiros sensíveis publicamente!**

Para uso público:
- Anonimize os dados antes do deploy
- Use dados de exemplo/mockados
- Configure o repositório como privado

Para uso privado:
- Configure o repositório como privado no GitHub
- Use Streamlit Cloud com compartilhamento restrito
- Adicione autenticação se necessário

## 📝 Notas

- Os dados devem estar na pasta `saida_analise/`
- Execute `python -m src.main` para gerar os dados
- O dashboard carrega dados dos CSVs gerados
