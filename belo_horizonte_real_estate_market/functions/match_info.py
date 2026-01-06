import pandas as pd

def match_logradouro(df, df_logradouros, verbose = 0): 

    df_log_nome = pd.DataFrame({
        "id_log": ["305202", "91130", "76640", "305000", "95589"],
        "logradouro": ["rua dois mil duzentos e vinte e sete", "rua professor mario werneck", 
                       "via ligacao br duzentos e sessenta e dois sabara",
                       "rua dois mil cento e trinta e sete", "viaduto henriqueta lisboa"]})

    df_log_nome_bairro = pd.DataFrame({
        "id_log": ["303289", "113548", "6542"],
        "bairro": ["parque sao pedro", "santa maria", "caicara adelaide"],
        "logradouro": ["rua dois", "rua d", "avenida atlantida"]})

    dict_filtro = {'nome': 'ind_nome_unico == 1',
                   'cep': 'ind_cep_unico == 1',
                   'cod3': 'ind_cod3_unico == 1',
                   'cod2': 'ind_cod2_unico == 1',
                   'cod1': 'ind_cod1_unico == 1',
                   'cod_zh': 'ind_zh == 1',
                   'prefixo_cep': 'ind_prefixo_cep == 1',
                   'sufixo_cep': 'ind_sufixo_cep == 1',
                   'regional': 'ind_regional == 1',
                   'bairro': 'ind_bairro == 1',
                   'cod3_regional': 'ind_cod3_regional == 1',
                   'cod2_regional': 'ind_cod2_regional == 1',
                   'cod1_regional': 'ind_cod1_regional == 1',
                   'cod3_bairro': 'ind_cod3_bairro == 1',
                   'cod2_bairro': 'ind_cod2_bairro == 1',
                   'cod1_bairro': 'ind_cod1_bairro == 1',
                   'cod3_cep': 'ind_cod3_cep == 1',
                   'cod2_cep': 'ind_cod2_cep == 1',
                   'cod1_cep': 'ind_cod1_cep == 1',
                   'cod3_zh': 'ind_cod3_zh == 1',
                   'cod2_zh': 'ind_cod2_zh == 1',
                   'cod1_zh': 'ind_cod1_zh == 1',
                   'cod3_prefixo_cep': 'ind_cod3_prefixo_cep == 1',
                   'cod2_prefixo_cep': 'ind_cod2_prefixo_cep == 1',
                   'cod1_prefixo_cep': 'ind_cod1_prefixo_cep == 1',
                   'cod3_sufixo_cep': 'ind_cod3_sufixo_cep == 1',
                   'cod2_sufixo_cep': 'ind_cod2_sufixo_cep == 1',
                   'cod1_sufixo_cep': 'ind_cod1_sufixo_cep == 1'}
    dict_variaveis = {'nome': ['logradouro'],
                      'cep': ['cep', 'logradouro'],
                      'cod3': ['cod3'],
                      'cod2': ['cod2'],
                      'cod1': ['cod1'],
                      'cod_zh': ["logradouro", "codigo_zh"],
                      'prefixo_cep': ['cep', 'logradouro'],
                      'sufixo_cep': ['cep', 'logradouro'],
                      'regional': ['nome_regional', 'logradouro'],
                      'bairro': ['bairro', 'logradouro'],
                      'cod3_regional': ['cod3', 'nome_regional', 'logradouro'],
                      'cod2_regional': ['cod2', 'nome_regional', 'logradouro'],
                      'cod1_regional': ['cod1', 'nome_regional', 'logradouro'],
                      'cod3_bairro': ['cod3', 'bairro'],
                      'cod2_bairro': ['cod2', 'bairro'],
                      'cod1_bairro': ['cod1', 'bairro'],
                      'cod3_cep': ['cod3', 'cep'],
                      'cod2_cep': ['cod2', 'cep'],
                      'cod1_cep': ['cod1', 'cep'],
                      'cod3_zh': ['cod3', 'codigo_zh'],
                      'cod2_zh': ['cod2', 'codigo_zh'],
                      'cod1_zh': ['cod1', 'codigo_zh'],
                      'cod3_prefixo_cep': ['cod3', 'prefixo_cep'],
                      'cod2_prefixo_cep': ['cod2', 'prefixo_cep'],
                      'cod1_prefixo_cep': ['cod1', 'prefixo_cep'],
                      'cod3_sufixo_cep': ['cod3', 'sufixo_cep'],
                      'cod2_sufixo_cep': ['cod2', 'sufixo_cep'],
                      'cod1_sufixo_cep': ['cod1', 'sufixo_cep']}    
    
    df_ = df.copy().assign(id_logr = pd.NA, fonte_logr = pd.NA)
    if 'cep' in df_.columns:
        df_ = df_\
        .assign(prefixo_cep = lambda df: df["cep"].fillna("").apply(lambda x: x[:5]))\
        .assign(sufixo_cep = lambda df: df["cep"].fillna("").apply(lambda x: x[-3:]))
    
    for key in dict_filtro.keys():
        variaveis = dict_variaveis[key]
        if sum([var in df.columns for var in variaveis]) == len(variaveis):
            if verbose: print(f"Tentando match de logradouro por {key}")
            filtro = dict_filtro[key]
            df_logradouros_ = df_logradouros.query(filtro)[variaveis + ["id_logradouro"]]\
            .drop_duplicates()
                
            df_ = df_\
            .merge(df_logradouros_, how = 'left')\
            .assign(fonte_logr = lambda df: [key if pd.isna(i) and pd.notna(j) else k for i, j, k in zip(df["id_logr"], df["id_logradouro"], df["fonte_logr"])])\
            .assign(id_logr = lambda df: df['id_logr'].fillna(df['id_logradouro']))\
            .drop(columns = "id_logradouro")
    
    df_ = df_\
    .merge(df_log_nome, how = 'left')\
    .assign(fonte_logr = lambda df: ['manual_nome_unico' if pd.isna(i) and pd.notna(j) else k for i, j, k in zip(df["id_logr"], df["id_log"], df["fonte_logr"])])\
    .assign(id_logr = lambda df: df['id_logr'].fillna(df['id_log']))\
    .drop(columns = 'id_log')\
    .merge(df_log_nome_bairro, how = 'left')\
    .assign(fonte_logr = lambda df: ['manual_nome_bairro_unico' if pd.isna(i) and pd.notna(j) else k for i, j, k in zip(df["id_logr"], df["id_log"], df["fonte_logr"])])\
    .assign(id_logr = lambda df: df['id_logr'].fillna(df['id_log']))\
    .drop(columns = 'id_log')\
    .rename(columns = {"id_logr": "id_logradouro"})
    return df_

def clean_column_text(df_, column):
    df_clean_column = df_[[column]].drop_duplicates()\
    .assign(aux = lambda df: df_[column])\
    .set_index(column)\
    .apply(lambda x: x.replace("[ãáà]", "a", regex = True))\
    .apply(lambda x: x.replace("[éê]", "e", regex = True))\
    .apply(lambda x: x.replace("[íìî]", "i", regex = True))\
    .apply(lambda x: x.replace("[óõô]", "o", regex = True))\
    .apply(lambda x: x.replace("[úùû]", "u", regex = True))\
    .apply(lambda x: x.replace("ç", "c", regex = True))\
    .apply(lambda x: x.str.lower())\
    .reset_index()

    return df_\
    .merge(df_clean_column, how = "left")\
    .drop(columns = [column])\
    .rename(columns = {"aux": column})