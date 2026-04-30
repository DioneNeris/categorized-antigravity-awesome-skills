# 🛠️ Guia de Gestão e Distribuição de Skills

Este guia descreve como utilizar os scripts de automação para organizar, atualizar e distribuir sua biblioteca de skills para o Antigravity.

## 📂 Estrutura de Arquivos
Os scripts estão localizados em `.agents/scripts/`:
- `manage_skills.py`: Realiza a migração física das pastas para categorias e atualiza o manifesto `skills-lock.json`.
- `index_generator.py`: Extrai metadados de cada skill e gera o índice mestre `SKILL.md` e os índices por categoria `INDEX.md`.

---

## 🚀 Como Utilizar

### 1. Atualização e Organização
Sempre que adicionar novas skills (pastas individuais) na raiz da pasta `skills/`, execute o script de gestão:

```powershell
python .agents/scripts/manage_skills.py
```

O script irá:
1. Analisar as novas pastas.
2. Atribuir uma categoria baseada no nome (usando Regex).
3. Mover a pasta para a subpasta da categoria.
4. Atualizar o caminho (`skillPath`) no arquivo `skills-lock.json`.

### 2. Geração de Índices
Para atualizar o "Escopo Global" (o arquivo `SKILL.md` que o agente lê para saber o que está disponível), execute:

```powershell
python .agents/scripts/index_generator.py
```

---

## 📦 Parâmetros para Distribuição
Se você deseja distribuir este sistema de organização para outros usuários ou utilizá-lo em diferentes máquinas, os seguintes parâmetros nos scripts devem ser ajustados:

### No arquivo `manage_skills.py`:
Localize o bloco `if __name__ == "__main__":` ao final do arquivo e ajuste os caminhos absolutos:

```python
if __name__ == "__main__":
    # Caminho para o arquivo de manifesto (skills-lock.json)
    lock_file = r"C:\CAMINHO\PARA\SEU\PROJETO\skills-lock.json"
    
    # Biblioteca Global (Opcional - remova se não quiser mexer na pasta global do sistema)
    migrate(r"C:\Users\USUARIO\.gemini\antigravity\skills", lock_file)
    
    # Biblioteca Local do Projeto
    migrate(r"C:\CAMINHO\PARA\SEU\PROJETO\.agents\skills", lock_file)
```

### No arquivo `index_generator.py`:
Ajuste os caminhos no final do arquivo:

```python
if __name__ == "__main__":
    # Gera índices para a biblioteca Global
    generate_rich_indexes(r"C:\Users\USUARIO\.gemini\antigravity\skills")
    
    # Gera índices para a biblioteca Local
    generate_rich_indexes(r"C:\CAMINHO\PARA\SEU\PROJETO\.agents\skills")
```

---

## ⚙️ Personalização de Categorias
Você pode modificar a lógica de categorização editando o dicionário `CATEGORIES` no início dos scripts. Ele utiliza **Expressões Regulares (Regex)**:

```python
CATEGORIES = {
    "NOM_DA_CATEGORIA": r"palavra1|palavra2|prefixo-",
    ...
}
```

- **Dica:** Se uma skill não se encaixar em nenhuma regra, ela será movida automaticamente para `13_OTHER`.

---

## ⚠️ Notas Importantes
- **Backup:** O script cria automaticamente um `skills-lock.json.bak` antes de qualquer alteração.
- **GMT-3:** Os scripts preservam o contexto temporal do projeto.
- **Portabilidade:** Ao enviar o projeto para outro usuário, certifique-se de que ele possua o Python instalado e que os caminhos nos scripts apontem para a pasta correta no computador dele.
