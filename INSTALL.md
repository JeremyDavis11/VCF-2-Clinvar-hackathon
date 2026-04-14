# Installing pixi and just

Two tools to install before the hackathon starts. Both are single-binary installs — no admin rights needed.

---

## 1. pixi

pixi manages the Python environment for this project. It reads `pixi.toml` and installs the exact right packages for everyone.

### macOS / Linux

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

Then restart your terminal, or run:

```bash
source ~/.bashrc   # or ~/.zshrc if you use zsh
```

### Windows (PowerShell)

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

### Verify

```bash
pixi --version
```

---

## 2. just

`just` is a command runner — like `make` but readable. It lets you run project tasks with short commands like `just download`.

### macOS (Homebrew)

```bash
brew install just
```

### Linux

```bash
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
```

Make sure `~/.local/bin` is on your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

### Windows (PowerShell — via winget)

```powershell
winget install --id Casey.Just
```

Or via Chocolatey:

```powershell
choco install just
```

### Verify

```bash
just --version
```

---

## 3. Get the project running

Once both tools are installed, clone the repo and run:

```bash
# Install Python dependencies
pixi install

# See all available commands
just

# Download demo data (ClinVar + 1000 Genomes chr21 VCF)
just download
```

That's it. You should see the first 10 lines of each file printed to the console confirming the downloads worked.
