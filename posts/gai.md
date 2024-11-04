[category]: <> (side projects)
[date]: <> (2024/11/03)
[title]: <> (Gai - AI for Git)
[color]: <> (green)

[Github](https://github.com/Danielratmiroff/gai) ![Github](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/linkicon.svg)
[PyPI](https://pypi.org/project/gai-tool/) ![PyPI](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/linkicon.svg)

# Gai is an AI-Powered Automation Tool for Git 🚀

command-line application that automates git commit messages and merge requests using AI. 

![Demo](/images/gai/video_demo.gif)

## ✨ Features

-  Generate commit messages based on code diffs.
-  Create merge requests with AI-generated titles and descriptions.
-  Works with both GitHub and GitLab.
-  Supports Groq and Hugging Face AI interfaces.

## 📦 Installation

Install gai-tool via pip:

```bash
pip install gai-tool
```

## 🚀 Getting Started

1. **Navigate to your git repository**:

   ```bash
   cd /path/to/your/git/repo
   ```

2. **Set API Tokens as Environment Variables**:

   ```bash
   # Ensure you have your AI interface and GitHub/GitLab API tokens set:
   export GROQ_API_KEY='your_groq_api_key'             # If you want to use Groq's API
   export HUGGINGFACE_API_TOKEN='your_hf_api_token'    # If you want to use Hugging Face's API
   export GITHUB_TOKEN='your_github_token'             # If using GitHub
   export GITLAB_TOKEN='your_gitlab_token'             # If using GitLab
   ```
3. **Start Using gai-tool**:

   ```bash
   # Generate an AI-powered commit message:
   gai commit -a
   ```

## ⚙️ Configuration

Configuration file is located at `~/.config/gai/config.yaml`. Customize settings like the AI interface, temperature, and target branch.

Example configuration:

```yaml
interface: huggingface
temperature: 0.7
target_branch: master
```

## 📖 Usage

gai-tool provides two main commands: `commit` and `merge`.

### 📝 Commit Messages

Generate an commit message:

```bash
gai commit
```

Options:

- `-a`, `--all`: Stage all changes before committing.
- `-t`, `--temperature`: Override the temperature specified in the config.
- `-i`, `--interface`: Specify and override the AI client API to use (`groq` or `huggingface`).

**Example**:
```bash
# Simply
gai commit -a
# Or
gai commit -a -t 0.5 -i huggingface
```

### 🔀 Merge Requests

Create a merge request:

```bash
gai merge
```

Options:

- `[remote]`: Specify the remote git repository (default is `origin`).
- `--push`, `-p`: Push changes to remote before creating a merge request.
- `--target-branch`, `-tb`: Specify the target branch for the merge request (default is `master`).
- `-t`, `--temperature`: Override the temperature specified in the config.
- `-i`, `--interface`: Specify and override the AI client API to use (`groq` or `huggingface`).

**Example**:
```bash
# Simply
gai merge -p
# Or
gai merge origin -p -tb develop -t 0.8 -i groq
```

## 🛠 Build Instructions

Build gai-tool from source:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Danielratmiroff/gai.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd gai
   ```

3. **Create a Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

4. **Install Build Tools and Dependencies**:

   ```bash
   pip install build
   pip install -r requirements.txt
   ```

5. **Build the Package**:

   ```bash
   python -m build
   ```

   This will generate distribution files in the `dist/` directory.

6. **Install the Built Package**:

   ```bash
   pip install dist/gai_tool-0.1.0-py3-none-any.whl
   ```


### Overview

The app should include:

- Task management system
- Creation/Edition of documents
- Meetings & Deadlines tracker
- Calendar view

It needed to have a nice UI, since I wanted to have a pleasent experience while using it 😀

### UI Design:

![Dashboard](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/projectmanager/dashboard.jpg)\

---

![Documents](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/projectmanager/documents.jpg)\

---

![Calendar](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/projectmanager/calendar.jpg)\

---

![New task](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/projectmanager/newtask.jpg)\

---

![New meeting](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/projectmanager/newmeeting.jpg)\
