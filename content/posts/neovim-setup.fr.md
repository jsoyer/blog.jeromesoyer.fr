---
title: "Mon Setup Neovim en 2025 : LSP, Plugins, et un Workflow qui Fonctionne"
date: 2025-09-17T16:30:00+02:00
draft: false
author: "Jerome Soyer"
description: "Un guide pratique de ma configuration Neovim — lazy.nvim, setup LSP, Telescope, et les plugins que j'utilise vraiment tous les jours."
categories: ["Tooling", "Editor"]
tags: ["neovim", "nvim", "lua", "lsp", "productivity", "editor", "cli"]
cover:
  image: /images/covers/neovim-setup.webp
  alt: "Neovim Setup 2026"
---

Je ne vais pas vous convaincre d'utiliser Neovim. Si vous lisez ça, vous avez déjà décidé. Voici le guide pratique d'un setup qui fonctionne — rapide, maintenable, sans 400 plugins qui se battent.

> Config complète disponible dans mes [dotfiles](https://github.com/jsoyer) gérés via chezmoi.

---

### Structure

```
~/.config/nvim/
├── init.lua              # Point d'entrée — minimal
├── lua/
│   ├── config/
│   │   ├── options.lua   # Paramètres vim.opt
│   │   ├── keymaps.lua   # Raccourcis globaux
│   │   └── autocmds.lua  # Autocommandes
│   └── plugins/          # Un fichier par plugin (specs lazy.nvim)
│       ├── lsp.lua
│       ├── telescope.lua
│       ├── treesitter.lua
│       ├── oil.lua
│       └── ...
```

Un fichier par plugin. Quand quelque chose casse, vous savez exactement où chercher.

---

### Gestionnaire de plugins : lazy.nvim

```lua
-- init.lua
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({ "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git", lazypath })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup("plugins", {
  change_detection = { notify = false },
  performance = {
    rtp = { disabled_plugins = {
      "gzip", "tarPlugin", "tohtml", "tutor", "zipPlugin",
    }},
  },
})
```

lazy.nvim charge les plugins à la demande par défaut — le temps de démarrage reste rapide même avec 30+ plugins.

---

### Setup LSP

Le cœur de tout setup Neovim moderne. J'utilise `nvim-lspconfig` avec `mason.nvim` pour gérer les serveurs de langages :

```lua
-- plugins/lsp.lua
return {
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
      "hrsh7th/nvim-cmp",
      "hrsh7th/cmp-nvim-lsp",
    },
    config = function()
      require("mason").setup()
      require("mason-lspconfig").setup({
        ensure_installed = {
          "lua_ls", "ts_ls", "rust_analyzer",
          "pyright", "gopls", "bashls",
        },
      })

      local capabilities = require("cmp_nvim_lsp").default_capabilities()
      local lspconfig = require("lspconfig")

      -- Attacher à chaque LSP : raccourcis standards
      vim.api.nvim_create_autocmd("LspAttach", {
        callback = function(event)
          local map = function(keys, func)
            vim.keymap.set("n", keys, func, { buffer = event.buf })
          end
          map("gd", vim.lsp.buf.definition)
          map("gr", vim.lsp.buf.references)
          map("K",  vim.lsp.buf.hover)
          map("<leader>rn", vim.lsp.buf.rename)
          map("<leader>ca", vim.lsp.buf.code_action)
        end,
      })

      -- Setup par serveur
      lspconfig.lua_ls.setup({ capabilities = capabilities })
      lspconfig.ts_ls.setup({ capabilities = capabilities })
      lspconfig.rust_analyzer.setup({ capabilities = capabilities })
      lspconfig.pyright.setup({ capabilities = capabilities })
      lspconfig.gopls.setup({ capabilities = capabilities })
    end,
  },
}
```

---

### Fuzzy Finding : Telescope

Telescope est le centre de commande. Tout ce que j'ouvre passe par là :

```lua
-- plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
  },
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>",  desc = "Chercher des fichiers" },
    { "<leader>fg", "<cmd>Telescope live_grep<cr>",   desc = "Grep en direct" },
    { "<leader>fb", "<cmd>Telescope buffers<cr>",     desc = "Buffers" },
    { "<leader>fh", "<cmd>Telescope help_tags<cr>",   desc = "Tags d'aide" },
    { "<leader>fr", "<cmd>Telescope oldfiles<cr>",    desc = "Fichiers récents" },
    { "<leader>fc", "<cmd>Telescope git_commits<cr>", desc = "Commits Git" },
  },
}
```

---

### Navigation de fichiers : oil.nvim

oil.nvim est un explorateur de fichiers qui traite votre système de fichiers comme un buffer. Vous ouvrez un répertoire, l'éditez comme du texte, sauvegardez pour appliquer les changements (renommer, supprimer, déplacer des fichiers). C'est la bonne abstraction.

```lua
-- plugins/oil.lua
return {
  "stevearc/oil.nvim",
  keys = {
    { "-", "<cmd>Oil<cr>", desc = "Ouvrir le répertoire parent" },
  },
  opts = {
    default_file_explorer = true,
    view_options = { show_hidden = true },
    float = { padding = 2 },
  },
}
```

`-` depuis n'importe quel buffer pour ouvrir le répertoire parent. Éditez, sauvegardez, c'est fait.

---

### Les plugins qui comptent vraiment

**Core :**
- `nvim-treesitter` — syntaxe, indentation, text objects basés sur le vrai arbre syntaxique
- `gitsigns.nvim` — diff Git inline, blame, navigation de hunks
- `nvim-autopairs` — appariement parenthèses/guillemets
- `Comment.nvim` — `gcc` pour basculer les commentaires

**Apparence :**
- `catppuccin/nvim` — thème (variante Mocha, cohérent avec WezTerm/Kitty)
- `nvim-lualine/lualine.nvim` — barre de statut
- `lukas-reineke/indent-blankline.nvim` — guides d'indentation

**Workflow :**
- `ThePrimeagen/harpoon` — marque 4-5 fichiers par projet, navigation instantanée
- `folke/which-key.nvim` — popup montrant les raccourcis disponibles (essentiel pour apprendre)
- `folke/trouble.nvim` — diagnostics LSP sous forme de panneau

**Git :**
- `tpope/vim-fugitive` — Git depuis Neovim (`:Git blame`, `:Git diff`, etc.)

---

### Raccourcis clés

```lua
-- config/keymaps.lua
vim.g.mapleader = " "

local map = vim.keymap.set

-- Navigation
map("n", "<C-h>", "<C-w>h")  -- navigation entre fenêtres
map("n", "<C-l>", "<C-w>l")
map("n", "<C-j>", "<C-w>j")
map("n", "<C-k>", "<C-w>k")

-- Qualité de vie
map("n", "<leader>w", "<cmd>w<cr>")       -- sauvegarder
map("n", "<leader>q", "<cmd>q<cr>")       -- quitter
map("n", "<Esc>", "<cmd>nohlsearch<cr>") -- effacer la surbrillance de recherche

-- Déplacer des lignes en mode visuel
map("v", "J", ":m '>+1<CR>gv=gv")
map("v", "K", ":m '<-2<CR>gv=gv")
```

---

### Temps de démarrage

Avec le lazy loading, moins de 50ms. Je le mesure régulièrement :

```bash
hyperfine "nvim --headless +qa" --warmup 3
```

Si vous dépassez 100ms au démarrage, profilez avec `--startuptime /tmp/startup.log` et trouvez le coupable.

---

### Gestion de la config avec chezmoi

Toute ma config Neovim est gérée par chezmoi :

```bash
# Éditer depuis le répertoire personnel (fichier live)
nvim ~/.config/nvim/lua/plugins/telescope.lua

# Synchroniser avec la source chezmoi + auto-commit + auto-push
chezmoi re-add ~/.config/nvim/lua/plugins/telescope.lua
```

Chaque machine reçoit la même config via `chezmoi update`.

### Terminal & Environnement

Un bon terminal change tout pour Neovim. Voir :
- [Kitty Terminal : Plongée en profondeur](/fr/posts/kitty-deep-dive/) — GPU-accéléré, scriptable, le meilleur terminal pour Neovim.
- [Mes dotfiles avec chezmoi](/fr/posts/dotfiles/) — comment la config Neovim est gérée sur toutes les machines.

---

*Config complète dans mes [dotfiles](https://github.com/jsoyer)*
