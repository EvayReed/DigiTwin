import threading
import tomllib
from typing import Dict, Optional
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).resolve().parent.parent

PROJECT_ROOT = get_project_root()
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"

def load_env_config():
    # 加载优先级：项目根目录.env > 系统环境变量
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path)  # [[2]](#__2) [[6]](#__6)
    else:
        load_dotenv()  # 回退到系统环境变量

load_env_config()


class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix = "OPENAI_",extra = "ignore")
    
    model: str = Field(..., description="model")
    base_url: str = Field(..., description="API base URL")
    api_key: str = Field(..., description="API key")
    max_tokens: int = Field(4096)
    max_input_tokens: Optional[int] = Field(None)
    temperature: float = Field(1.0)
    api_type: Optional[str] = Field(None)
    api_version: Optional[str] = Field(None)

# test
# llm = LLMSettings()
# print(llm)

class ProxySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROXY_")
    
    server: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

# test
# proxy = ProxySettings()
# print(proxy)

class BrowserSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BROWSER_")
    
    headless: bool = False
    disable_security: bool = True
    # ... 其他字段保持原样
    proxy: Optional[ProxySettings] = None
    @model_validator(mode="after")
    def validate_proxy(self):
        if self.proxy and not self.proxy.server:
            self.proxy = None
        return self

# test
# browser = BrowserSettings()
# print(browser)


class SearchSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SEARCH_")
    engine: str = Field(default="Google", description="Search engine the llm to use")

# test
# search = SearchSettings()
# print(search)

class SandboxSettings(BaseSettings):
    """Configuration for the execution sandbox"""
    model_config = SettingsConfigDict(env_prefix="SANDBOX_")
    use_sandbox: bool = Field(False, description="Whether to use the sandbox")
    image: str = Field("python:3.12-slim", description="Base image")
    work_dir: str = Field("/workspace", description="Container working directory")
    memory_limit: str = Field("512m", description="Memory limit")
    cpu_limit: float = Field(1.0, description="CPU limit")
    timeout: int = Field(300, description="Default command timeout (seconds)")
    network_enabled: bool = Field(
        False, description="Whether network access is allowed"
    )

# test
# Sandbox = SandboxSettings()
# print(Sandbox)

class AppConfig():
    llm: Dict[str, LLMSettings]
    sandbox: Optional[SandboxSettings] = Field(
        None, description="Sandbox configuration"
    )
    browser_config: Optional[BrowserSettings] = Field(
        None, description="Browser configuration"
    )
    search_config: Optional[SearchSettings] = Field(
        None, description="Search configuration"
    )

    class Config:
        arbitrary_types_allowed = True

# test
# app = AppConfig()
# print(app)


class Config:

    _sandbox = SandboxSettings()
    _search = SearchSettings()
    _proxy = ProxySettings()
    _llm = LLMSettings()
    _browser = BrowserSettings()


    @property
    def llm(self) -> Dict[str, LLMSettings]:
        return {"default": self._llm}
    @property
    def sandbox(self) -> SandboxSettings:
        return self._sandbox

    @property
    def browser_config(self) -> Optional[BrowserSettings]:
        return self._browser

    @property
    def search_config(self) -> Optional[SearchSettings]:
        return self._search

    @property
    def workspace_root(self) -> Path:
        """Get the workspace root directory"""
        return WORKSPACE_ROOT

config = Config()
# print(config.llm.get("default"))

