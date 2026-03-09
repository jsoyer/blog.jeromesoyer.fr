---
title: "My Neovim Setup in 2026: LSP, Plugins, and a Workflow That Actually Works"
date: 2026-03-09T14:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "A practical guide to my Neovim configuration — lazy.nvim, LSP setup, Telescope, and the plugins I actually use every day."
categories: ["Tooling", "Editor"]
tags: ["neovim", "nvim", "lua", "lsp", "productivity", "editor", "cli"]
cover:
  image: /images/covers/neovim-setup.png
  alt: "Neovim Setup 2026"
---

I'm not going to tell you why you should use Neovim. If you're reading this, you've already decided. This is the practical guide to a setup that works — fast, maintainable, and without 400 plugins that conflict with each other.

> Full config available in my [dotfiles](https://github.com/jsoyer) managed via chezmoi.

---

### Structure

```
~/.config/nvim/
├── init.lua              # Entry point — minimal
├── lua/
│   ├── config/
│   │   ├── options.lua   # vim.opt settings
│   │   ├── keymaps.lua   # Global keymaps
│   │   └── autocmds.lua  # Autocommands
│   └── plugins/          # One file per plugin (lazy.nvim specs)
│       ├── lsp.lua
│       ├── telescope.lua
│       ├── treesitter.lua
│       ├── oil.lua
│       └── ...
```

One file per plugin. When something breaks, you know exactly where to look.

---

### Plugin Manager: lazy.nvim

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

lazy.nvim loads plugins on-demand by default — startup time stays fast even with 30+ plugins.

---

### LSP Setup

The core of any modern Neovim setup. I use `nvim-lspconfig` with `mason.nvim` to manage language servers:

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

      -- Attach to every LSP: standard keymaps
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

      -- Per-server setup
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

### Fuzzy Finding: Telescope

Telescope is the command center. Everything I open comes through it:

```lua
-- plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
  },
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>",  desc = "Find files" },
    { "<leader>fg", "<cmd>Telescope live_grep<cr>",   desc = "Live grep" },
    { "<leader>fb", "<cmd>Telescope buffers<cr>",     desc = "Buffers" },
    { "<leader>fh", "<cmd>Telescope help_tags<cr>",   desc = "Help tags" },
    { "<leader>fr", "<cmd>Telescope oldfiles<cr>",    desc = "Recent files" },
    { "<leader>fc", "<cmd>Telescope git_commits<cr>", desc = "Git commits" },
  },
}
```

---

### File Navigation: oil.nvim

oil.nvim is a file explorer that treats your filesystem like a buffer. You open a directory, edit it like text, save to apply changes (rename, delete, move files). It's the right abstraction.

```lua
-- plugins/oil.lua
return {
  "stevearc/oil.nvim",
  keys = {
    { "-", "<cmd>Oil<cr>", desc = "Open parent directory" },
  },
  opts = {
    default_file_explorer = true,
    view_options = { show_hidden = true },
    float = { padding = 2 },
  },
}
```

`-` from any buffer to open the parent directory. Edit, save, done.

---

### The Plugins I Actually Use

**Core:**
- `nvim-treesitter` — syntax, indentation, text objects based on the actual parse tree
- `gitsigns.nvim` — inline Git diff, blame, hunk navigation
- `nvim-autopairs` — bracket/quote pairing
- `Comment.nvim` — `gcc` to toggle comments

**Appearance:**
- `catppuccin/nvim` — theme (Mocha variant, consistent with my WezTerm/Kitty)
- `nvim-lualine/lualine.nvim` — statusline
- `lukas-reineke/indent-blankline.nvim` — indentation guides

**Workflow:**
- `ThePrimeagen/harpoon` — bookmark 4-5 files per project, instant navigation
- `folke/which-key.nvim` — popup showing available keymaps (essential when learning)
- `folke/trouble.nvim` — LSP diagnostics as a panel

**Git:**
- `tpope/vim-fugitive` — Git from inside Neovim (`:Git blame`, `:Git diff`, etc.)

---

### Key Keymaps

```lua
-- config/keymaps.lua
vim.g.mapleader = " "

local map = vim.keymap.set

-- Navigation
map("n", "<C-h>", "<C-w>h")  -- window navigation
map("n", "<C-l>", "<C-w>l")
map("n", "<C-j>", "<C-w>j")
map("n", "<C-k>", "<C-w>k")

-- Quality of life
map("n", "<leader>w", "<cmd>w<cr>")       -- save
map("n", "<leader>q", "<cmd>q<cr>")       -- quit
map("n", "<Esc>", "<cmd>nohlsearch<cr>") -- clear search highlight

-- Move lines in visual mode
map("v", "J", ":m '>+1<CR>gv=gv")
map("v", "K", ":m '<-2<CR>gv=gv")
```

---

### Startup Time

With lazy loading, my startup time is under 50ms. I measure it regularly:

```bash
hyperfine "nvim --headless +qa" --warmup 3
```

If you're spending more than 100ms on startup, profile with `--startuptime /tmp/startup.log` and find the culprit.

---

### Managing Config With chezmoi

My entire Neovim config is managed by chezmoi. This means:

```bash
# Edit from home directory (live file)
nvim ~/.config/nvim/lua/plugins/telescope.lua

# Sync to chezmoi source + auto-commit + auto-push
chezmoi re-add ~/.config/nvim/lua/plugins/telescope.lua
```

Every machine gets the same config via `chezmoi update`.

---

*Full config available in my [dotfiles](https://github.com/jsoyer)*
