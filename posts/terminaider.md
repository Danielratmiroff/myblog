[category]: <> (side projects)
[date]: <> (2024/07/20)
[title]: <> (Terminaider)
[color]: <> (green)

[Github](https://github.com/Danielratmiroff/terminaider) ![Github](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/linkicon.svg)

# Terminaider

AI within your terminal 🤖

## Description

Quickly prompt any supported AI from within your terminal, without being bound to any specific provider.

![terminaider demo](https://github.com/user-attachments/assets/14906c21-fb8c-41a5-8c7c-947f4dcceb55)

### Features

- Currently supports [GROQ APIs](https://groq.com/)
- Prompt caching
- Software engineering focus (for now)

## Installation

1. Ensure you have [Go installed](https://go.dev/doc/install) on your system.

2. Clone the repository and install:

```bash
git clone https://github.com/Danielratmiroff/terminaider.git
cd terminaider
go install
```

3. Set up your API key:

   Option 1: Set an environment variable:
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

   Option 2: Create a `config.yaml` file in the repo folder:
   ```yaml
   GroqAPIKey: "your_api_key_here"
   ```

## Usage

### Basic Usage

```bash
terminaider
```

### Prompt on Startup

```bash
terminaider How big is the Earth?
```

### Quick Command (copies executable command to clipboard)

```bash
terminaider -r How can I commit my changes to git?
```

---

### Recommendation: Create an Alias

Add this line to your shell configuration file (e.g., `~/.zshrc` or `~/.bashrc`):

```bash
alias ai='terminaider'
```

Then reload your shell or run `source ~/.zshrc` (or respective config file).

Now you can use `ai` as a shortcut:

```bash
ai is the earth flat?
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
