import os
import re

def extract_summary(skill_path):
    """Extrai uma descrição curta do arquivo SKILL.md."""
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read(500)
            # Busca por metadados de descrição no frontmatter
            match = re.search(r"description:\s*(.*)", content)
            if match:
                return match.group(1).strip()
            
            # Caso não encontre, pega o primeiro parágrafo significativo
            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-") and ":" not in line:
                    return line[:120] + "..."
            return "Sem descrição disponível."
    except:
        return "Erro ao ler descrição."

def generate_rich_indexes(skills_dir):
    """Gera SKILL.md (Mestre) e INDEX.md (Categorias)."""
    print(f"--- Gerando Índices: {skills_dir} ---")
    if not os.path.exists(skills_dir):
        print(f"Aviso: Diretório {skills_dir} não encontrado.")
        return

    # Lista categorias (pastas que começam com números ou 13_OTHER)
    try:
        categories = sorted([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d)) and (re.match(r"^\d+_", d) or d == "13_OTHER")])
    except Exception as e:
        print(f"Erro ao ler {skills_dir}: {e}")
        return
        
    master_index = "# 🌐 Escopo Global de Skills\n\nEste arquivo é um guia rápido para seleção automática de ferramentas.\n\n"
    
    for cat in categories:
        cat_path = os.path.join(skills_dir, cat)
        skills = sorted([s for s in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, s))])
        if not skills: continue
        
        master_index += f"## 📁 {cat}\n\n"
        cat_index = f"# {cat}\n\nÍndice detalhado da categoria {cat}.\n\n"
        
        for skill in skills:
            skill_md_path = os.path.join(cat_path, skill, "SKILL.md")
            summary = extract_summary(skill_md_path)
            
            line = f"- **{skill}**: {summary}\n"
            master_index += line
            cat_index += line
        
        # Salva o INDEX.md da categoria
        with open(os.path.join(cat_path, "INDEX.md"), "w", encoding="utf-8") as f:
            f.write(cat_index)
            
    # Salva o SKILL.md mestre
    with open(os.path.join(skills_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(master_index)
    
    print(f"Índices gerados com sucesso em {skills_dir}.")

if __name__ == "__main__":
    # Tenta localizar o projeto dinamicamente
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    
    # 1. Pasta de Skills Local do Projeto
    LOCAL_SKILLS = os.path.join(PROJECT_ROOT, ".agents", "skills")
    
    # 2. Pasta de Skills Global
    USER_HOME = os.path.expanduser("~")
    GLOBAL_SKILLS = os.path.join(USER_HOME, ".gemini", "antigravity", "skills")

    # Gera Índices Local
    if os.path.exists(LOCAL_SKILLS):
        generate_rich_indexes(LOCAL_SKILLS)
    
    # Gera Índices Global
    if os.path.exists(GLOBAL_SKILLS):
        generate_rich_indexes(GLOBAL_SKILLS)
