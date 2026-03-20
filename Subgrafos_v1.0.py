"""
# SUBGRAFOS

Juliana Lombard Souza
"""

# ==============================================================================
# IDENTIFICAR E CLASSIFICAR SUBGRAFOS DE UMA REDE
# ==============================================================================
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DE CAMINHOS
# ==============================================================================
# Obtém o caminho absoluto da pasta onde o script está sendo executado
SCRIPT_DIR = Path(__file__).resolve().parent

# Define o caminho para a pasta raiz do projeto
PROJECT_ROOT = SCRIPT_DIR.parent

# Define os caminhos para as pastas de dados e de saída
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Cria a pasta de saída se ela não existir
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define os caminhos para os arquivos de entrada e saída
# IMPORTANTE: Certifique-se de que todos os arquivos do shapefile (.shp, .shx, .dbf, etc.)
# estão na pasta 'data'.
rede_shp = DATA_DIR / "rede_teste_lin.shp" # renomeie aqui
output_shp_path = OUTPUT_DIR / "rede_teste_subgrafos_lin.shp" # renomeie aqui
output_plot_path = OUTPUT_DIR / "mapa_subgrafos.png" # renomeie aqui
# ==============================================================================

def main():
    print("--- Iniciando a Análise de Subgrafos da Rede ---")

    # 1. Carrega e limpa o shapefile
    print(f"Carregando o arquivo de rede: {rede_shp}")
    try:
        gdf = gpd.read_file(rede_shp)
    except Exception as e:
        raise FileNotFoundError(f"ERRO: Não foi possível ler o shapefile '{rede_shp}'. Verifique se o arquivo .shp e seus arquivos associados (.dbf, .shx) existem na pasta 'data'. Erro original: {e}")

    # Limpeza de dados
    initial_count = len(gdf)
    gdf = gdf[gdf.geometry.notnull()]
    gdf = gdf[~gdf.is_empty]
    final_count = len(gdf)
    if initial_count != final_count:
        print(f"Limpeza de dados: {initial_count - final_count} feições com geometria nula ou vazia foram removidas.")
    print(f"Shapefile carregado com {final_count} feições válidas.")

    # 2. Correção de geometrias inválidas
    print("\nCorrigindo geometrias inválidas com make_valid()...")
    gdf.geometry = gdf.make_valid()
    print("Correção concluída.")

    # 3. Construir o grafo da rede
    print("\nConstruindo o grafo da rede...")
    G = nx.Graph()
    for idx, line in gdf.iterrows():
        geom = line.geometry
        if geom.geom_type == 'LineString':
            start_coord = (geom.coords[0][0], geom.coords[0][1])
            end_coord = (geom.coords[-1][0], geom.coords[-1][1])
            G.add_edge(start_coord, end_coord, original_fid=idx)
        elif geom.geom_type == 'MultiLineString':
            for part in geom.geoms:
                start_coord = (part.coords[0][0], part.coords[0][1])
                end_coord = (part.coords[-1][0], part.coords[-1][1])
                G.add_edge(start_coord, end_coord, original_fid=idx)
    
    # 4. Encontrar todos os componentes conectados
    components = list(nx.connected_components(G))
    print(f"\nA rede viária possui {len(components)} componente(s) conectado(s).")

    if not components:
        print("O grafo está vazio. Nenhuma aresta foi criada. Verifique as geometrias do seu shapefile.")
        return

    # 5. Identificar o componente principal
    largest_component_nodes = max(components, key=len)
    print(f"O componente principal (rede principal) tem {len(largest_component_nodes)} nós.")

    # 6. Classificar os subgrafos
    print("\nIniciando a classificação dos subgrafos...")
    gdf['subgrafo'] = 0  # 0 para a rede principal

    subgraph_components = [comp for comp in components if comp != largest_component_nodes]
    subgraph_sizes = []
    for comp_nodes in subgraph_components:
        edge_count = 0
        for u, v, data in G.edges(data=True):
            if u in comp_nodes and v in comp_nodes:
                edge_count += 1
        subgraph_sizes.append((comp_nodes, edge_count))
    
    subgraph_sizes.sort(key=lambda x: x[1], reverse=True)

    subgraph_id = 1
    for comp_nodes, size in subgraph_sizes:
        print(f"  -> Classificando Subgrafo {subgraph_id} com {size} trechos...")
        subgraph_fids = set()
        for u, v, data in G.edges(data=True):
            if u in comp_nodes and v in comp_nodes:
                subgraph_fids.add(data['original_fid'])
        gdf.loc[gdf.index.isin(subgraph_fids), 'subgrafo'] = subgraph_id
        subgraph_id += 1
    print("Classificação concluída.")

    # 7. Salvar o resultado em um novo shapefile
    print(f"\nSalvando o arquivo classificado em: {output_shp_path}")
    gdf.to_file(output_shp_path)

    # 8. Visualizar e salvar o mapa
    print(f"Gerando e salvando o mapa em: {output_plot_path}")
    fig, ax = plt.subplots(1, 1, figsize=(18, 18))
    gdf.plot(ax=ax, column='subgrafo', cmap='tab20', legend=True, categorical=True, linewidth=1.5,
             legend_kwds={'loc': 'upper left', 'bbox_to_anchor': (1, 1)})
    ax.set_title('Rede Viária Classificada por Subgrafos (0=Rede Principal)', fontsize=18)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(output_plot_path)
    plt.show() # Mostra o plot também no terminal se o ambiente permitir

    # 9. Exibe um resumo
    print("\n--- Análise Concluída com Sucesso! ---")
    print("\nResumo da Classificação (quantidade de trechos por subgrafo):")
    print(gdf['subgrafo'].value_counts().sort_index())


if __name__ == "__main__":
    main()