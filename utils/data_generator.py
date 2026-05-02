import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

def gerar_dados_vendas_simulados(data_inicio=None, data_fim=None):
    """Gera dados simulados de vendas para demonstração."""
    if data_fim is None:
        data_fim = datetime.now()
    if data_inicio is None:
        data_inicio = data_fim - timedelta(days=90)
    
    datas = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    vendas = []
    
    produtos = ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E']
    categorias = ['Eletrônicos', 'Alimentos', 'Vestuário', 'Serviços', 'Outros']
    regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    vendedores = ['Carlos', 'Maria', 'João', 'Ana', 'Pedro']
    
    for data in datas:
        for _ in range(random.randint(3, 15)):
            vendas.append({
                'data_venda': data,
                'id_venda': f"VND{int(data.timestamp())}{random.randint(1000, 9999)}",
                'produto': random.choice(produtos),
                'categoria': random.choice(categorias),
                'regiao': random.choice(regioes),
                'vendedor': random.choice(vendedores),
                'quantidade': random.randint(1, 20),
                'valor_unitario': round(random.uniform(10, 500), 2),
                'desconto_percentual': random.choice([0, 0, 0, 5, 10, 15]),
                'cliente': f"Cliente_{random.randint(1, 100)}",
                'status': random.choice(['Concluída', 'Pendente', 'Cancelada'])
            })
    
    df = pd.DataFrame(vendas)
    df['valor_total'] = df['quantidade'] * df['valor_unitario']
    df['desconto'] = df['valor_total'] * (df['desconto_percentual'] / 100)
    df['valor_liquido'] = df['valor_total'] - df['desconto']
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    
    return df

def gerar_dados_clientes_simulados():
    """Gera dados simulados de clientes."""
    clientes = []
    for i in range(1, 101):
        clientes.append({
            'id_cliente': i,
            'nome': f'Cliente_{i}',
            'regiao': ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'][i % 5],
            'tipo': ['PJ', 'PF'][i % 2],
            'ativo': i % 10 != 0
        })
    return pd.DataFrame(clientes)
