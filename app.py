import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Posts WB", layout="centered")

# Cores da WB (Aproximadas)
AZUL_WB = (10, 25, 60)  # Azul escuro
BRANCO = (255, 255, 255)
VERDE_SUCESSO = (0, 100, 0)

st.title("🇧🇷 Gerador de Posts - WB Assessoria")
st.markdown("### Transforme fotos de clientes em posts prontos!")

# --- BARRA LATERAL (ENTRADA DE DADOS) ---
st.sidebar.header("📝 Preencha os Dados")
uploaded_file = st.sidebar.file_uploader("1. Foto do Cliente", type=['jpg', 'png', 'jpeg'])
uploaded_logo = st.sidebar.file_uploader("2. Seu Logo (Opcional)", type=['png'])
nome_cliente = st.sidebar.text_input("3. Nome do Cliente", placeholder="Ex: Kedson")
nacionalidade = st.sidebar.text_input("4. Nacionalidade", placeholder="Ex: Haiti")
tipo_conquista = st.sidebar.selectbox("5. Conquista", 
                                      ["Naturalização Deferida", "Passaporte em Mãos", "Residência Aprovada"])

# --- FUNÇÃO DE CRIAÇÃO DO POST ---
def criar_post(foto_cliente, logo_wb, nome, pais, conquista):
    # 1. Cria a base quadrada (Post Instagram 1080x1080)
    base = Image.new('RGB', (1080, 1080), AZUL_WB)
    draw = ImageDraw.Draw(base)
    
    # 2. Processa a foto do cliente
    img = Image.open(foto_cliente).convert("RGBA")
    
    # Ajusta tamanho da foto para caber no centro (mantendo proporção)
    # Vamos fazer a foto ocupar 80% da altura disponível
    altura_foto = 800
    ratio = img.width / img.height
    largura_foto = int(altura_foto * ratio)
    img = img.resize((largura_foto, altura_foto))
    
    # Centraliza horizontalmente
    pos_x = (1080 - largura_foto) // 2
    pos_y = 100 # Margem do topo
    
    base.paste(img, (pos_x, pos_y), img if img.mode == 'RGBA' else None)
    
    # 3. Adiciona Faixa Branca no Rodapé
    draw.rectangle([(0, 920), (1080, 1080)], fill=BRANCO)
    
    # 4. Adiciona Textos (Usando fonte padrão do sistema para simplificar)
    # Título no Topo
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 60)
        font_nome = ImageFont.truetype("arial.ttf", 55)
        font_sub = ImageFont.truetype("arial.ttf", 40)
    except:
        font_titulo = ImageFont.load_default()
        font_nome = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((50, 20), "WB ASSESSORIA MIGRATÓRIA", fill=BRANCO, font=font_titulo)
    
    # Textos do Rodapé (Preto no Branco)
    draw.text((40, 940), f"{nome.upper()} - {pais.upper()}", fill="black", font=font_nome)
    draw.text((40, 1010), f"✅ {conquista.upper()}", fill=VERDE_SUCESSO, font=font_sub)
    
    # 5. Adiciona Logo (Se tiver)
    if logo_wb:
        logo = Image.open(logo_wb).convert("RGBA")
        # Redimensiona logo pequeno
        logo.thumbnail((150, 150))
        # Cola no canto inferior direito
        base.paste(logo, (900, 930), logo)
    
    return base

# --- LÓGICA DO APP ---
if uploaded_file and nome_cliente and nacionalidade:
    if st.button("GERAR POST AGORA 🚀"):
        
        # Gera a imagem
        imagem_final = criar_post(uploaded_file, uploaded_logo, nome_cliente, nacionalidade, tipo_conquista)
        
        # Mostra na tela
        st.image(imagem_final, caption="Post Gerado - Pronto para Salvar", use_column_width=True)
        
        # Botão de Download
        buf = io.BytesIO()
        imagem_final.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="⬇️ BAIXAR IMAGEM PARA POSTAR",
            data=byte_im,
            file_name=f"post_{nome_cliente}.png",
            mime="image/png"
        )
        
        # Gera Legenda
        st.success("Legenda Sugerida (Copie abaixo):")
        texto_legenda = f"""
🔥 MAIS UM {tipo_conquista.upper()}!

Parabéns, {nome_cliente}! Vindo do {nacionalidade} para conquistar sua liberdade definitiva no Brasil. 🇧🇷

A WB Assessoria teve a honra de cuidar de cada detalhe.
✅ Sem burocracia.
✅ Com segurança jurídica.

Você também quer resolver sua situação? Comente "EU QUERO" abaixo! 👇

#WBAssessoria #NaturalizaçãoBrasileira #Imigração #{nacionalidade}NoBrasil
        """
        st.code(texto_legenda)

else:
    st.info("👈 Use a barra lateral para enviar a foto e os dados do cliente.")