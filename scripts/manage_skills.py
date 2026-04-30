import os
import json
import shutil
import re

# Configuração de Categorias via Regex
CATEGORIES = {
    "01_AI_AGENTS": r"agent|ai-|hugging-face|gemini|langchain|crewai|llama|openai|anthropic|sutskever|karpathy|lecun|altman|hinton|prompt-|llm-|rag-|satori|mcp-",
    "02_WEB_DEV": r"react|nextjs|shadcn|tailwind|angular|vue|svelte|html|css|frontend|backend|javascript|typescript|hono|vite|webpack|radix|lucide|trpc|zustand|prisma|drizzle|clerk",
    "03_MOBILE_DEV": r"android|ios|flutter|react-native|expo|swiftui|jetpack|kotlin|swift-|mobile-|robius",
    "04_DEVOPS_INFRA": r"aws|azure|gcp|docker|kubernetes|terraform|cicd|github|gitlab|deployment|cloud|serverless|helm|ansible|jenkins|circleci|vercel|render|upstash",
    "05_SECURITY_AUDIT": r"security|pentest|hacking|burp|vulnerability|metasploit|exploit|audit-|sast|dast|scanning|threat|compliance|privilege-escalation|wireshark|idor|xss|sql-injection|authentication",
    "06_AUTOMATION_SCRAPING": r"n8n|zapier|apify|make-|automation|scraper|selenium|playwright|puppeteer|browser-automation|slack-|discord-|telegram-|whatsapp-|google-|airtable|trello|asana|hubspot|brevo|mailchimp|sendgrid|twilio",
    "07_DATA_SCIENCE_DB": r"postgres|sql|mysql|mongodb|redis|data-|pandas|numpy|scipy|scikit|ml-|pipeline|database|snowflake|bigquery|dbt|neon|convex|supabase|vector-|polars|matplotlib|seaborn|networkx",
    "08_BUSINESS_MARKETING": r"seo|shopify|marketing|business|crm|sales|leads|analytics|growth|entrepreneur|startup|pricing|monetization|conversion|lead-|market-|customer-|revenue",
    "09_LANGUAGES_CORE": r"python-|rust-|golang|c-pro|cpp-|java-pro|ruby-|rails|php-|haskell|julia|elixir|scala|posix-shell|busybox|jq",
    "10_SYSTEM_TOOLS": r"bash|git|powershell|linux|windows|cli|terminal|shell|productivity|obsidian|notion|jira|tmux|ssh-|devcontainer|environment-setup|documentation|readme|changelog|commit",
    "11_DESIGN_UX": r"design|ux-|ui-|figma|animation|animejs|threejs|spline|vizcom|canvas|layout|typography|color|magic-ui|iconsax|remotion|magic-animator|scroll-experience",
    "12_NICHE_SPECIALIZED": r"minecraft|legal|health|blockchain|nft|crypto|odoo|hospital|medical|fintech|insurance|scientific|agriculture|energy|food-|nutrition|fitness"
}

def get_category(skill_name):
    for cat, pattern in CATEGORIES.items():
        if re.search(pattern, skill_name, re.IGNORECASE):
            return cat
    return "13_OTHER"

def migrate(skills_dir, lock_file):
    print(f"--- Migrando: {skills_dir} ---")
    if not os.path.exists(lock_file):
        print(f"Erro: {lock_file} não encontrado.")
        return

    with open(lock_file, "r", encoding="utf-8") as f:
        lock_data = json.load(f)

    skills = lock_data.get("skills", {})
    
    # Backup do manifesto
    shutil.copy(lock_file, lock_file + ".bak")

    # Identifica pastas na raiz que precisam ser movidas
    try:
        existing_folders = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    except Exception as e:
        print(f"Erro ao ler diretório {skills_dir}: {e}")
        return
    
    for name in existing_folders:
        # Pula as pastas de categoria já existentes
        if name in CATEGORIES or name == "13_OTHER":
            continue
        
        cat = get_category(name)
        old_abs_dir = os.path.join(skills_dir, name)
        new_abs_parent = os.path.join(skills_dir, cat)
        new_abs_dir = os.path.join(new_abs_parent, name)

        if not os.path.exists(new_abs_parent):
            os.makedirs(new_abs_parent)
        
        print(f"Movendo: {name} -> {cat}")
        try:
            shutil.move(old_abs_dir, new_abs_dir)
            # Atualiza o caminho no skills-lock.json
            if name in skills:
                skills[name]["skillPath"] = f"skills/{cat}/{name}/SKILL.md"
        except Exception as e:
            print(f"Erro ao mover {name}: {e}")

    lock_data["skills"] = skills
    with open(lock_file, "w", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=2, ensure_ascii=False)
    
    print(f"Migração concluída para {skills_dir}.")

if __name__ == "__main__":
    # Tenta localizar o projeto dinamicamente
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    
    # 1. Caminho do Manifesto Local
    LOCK_FILE = os.path.join(PROJECT_ROOT, "skills-lock.json")
    
    # 2. Pasta de Skills Local do Projeto
    LOCAL_SKILLS = os.path.join(PROJECT_ROOT, ".agents", "skills")
    
    # 3. Pasta de Skills Global (Caminho padrão do Antigravity no Windows)
    USER_HOME = os.path.expanduser("~")
    GLOBAL_SKILLS = os.path.join(USER_HOME, ".gemini", "antigravity", "skills")

    # Executa Migração Local
    if os.path.exists(LOCAL_SKILLS):
        migrate(LOCAL_SKILLS, LOCK_FILE)
    
    # Executa Migração Global (Opcional)
    if os.path.exists(GLOBAL_SKILLS):
        migrate(GLOBAL_SKILLS, LOCK_FILE)
