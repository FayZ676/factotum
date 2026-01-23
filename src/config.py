from pathlib import Path

from src.models import Action, Config, Param, Step


CONFIG_DIR = Path.home() / ".factotum"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG = Config(
    openai_api_key="",
    actions=[
        Action(
            name="commit-summary",
            description="Look at all commit messages in some block of time and use a LLM to summarize them.",
            steps=[
                Step(
                    name="git-log",
                    description="Log all commit message (one line) since some given commit.",
                    type="shell",
                    params=[
                        Param(
                            name="commit",
                            description="The commit hash to start looking at commit messages",
                            type="string",
                            default=None,
                        )
                    ],
                    value="git log {{commit}}..HEAD --pretty=oneline",
                ),
                Step(
                    name="summarize-logs",
                    description="Summarize git logs using an LLM.",
                    type="llm",
                    params=[
                        Param(
                            name="guidelines",
                            description="Summary guidelines describing the desired format of the summary.",
                            type="string",
                            default=None,
                        )
                    ],
                    value="## Git Log Results\n{{@git-log}}\n\n## Instructions\n\nSummarize the above commit messages according to the following guidelines.\n\n## Guidelines\n{{guidelines}}",
                ),
            ],
        ),
        Action(
            name="commit-changes",
            description="Generate a commit message for staged changes and commit.",
            steps=[
                Step(
                    name="diff",
                    description="Git diff all staged changes",
                    type="shell",
                    params=[],
                    value="git diff --staged",
                ),
                Step(
                    name="generate-message",
                    description="Generate a commit message based on unstaged code changes using an LLM.",
                    type="llm",
                    params=[],
                    value='## Git Diff Result\n{{@diff}}\n\n## Instructions\nAbove is the `git diff` of my staged code changes. Please generate a commit message that adheres to these guidelines.\n\n## Guidelines\nFollow conventional commit format:\n- Use imperative mood (e.g., "Add feature" not "Added feature")\n- Keep the message one line in length concise (10-20 words)\n- Start with a type prefix: feat:, fix:, docs:, style:, refactor:, test:, chore:\n\nExamples:\nfeat: Add user authentication with OAuth2\nfix: Resolve memory leak in data processing\ndocs: Update API documentation for v2\nrefactor: Simplify validation logic\n\n##Response Format\nRespond only with the final commit message.',
                ),
            ],
        ),
    ],
)


def load_config() -> Config:
    """Load configuration from ~/.factotum/config.json"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found at {CONFIG_FILE}. " f"Please run 'fac init'."
        )

    with open(CONFIG_FILE, "r") as f:
        return Config.model_validate_json(f.read())


def get_api_key() -> str:
    """Get OpenAI API key from config."""
    config = load_config()
    if not config.openai_api_key:
        raise ValueError("OpenAI API key not found in config. Please run 'fac init'.")
    return config.openai_api_key


def save_config(config: Config):
    """Save configuration to file."""
    _ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        f.write(config.model_dump_json(indent=2))


### private ###


def _ensure_config_dir():
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(exist_ok=True)
