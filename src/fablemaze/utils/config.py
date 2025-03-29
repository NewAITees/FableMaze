"""
FableMaze設定管理モジュール

このモジュールは、FableMazeの設定を管理します。
環境変数、設定ファイル、デフォルト値の優先順位付けを行います。
"""

from pathlib import Path
from typing import Any, Dict, Optional
import os
import json

from pydantic import BaseModel, Field

class FableMazeConfig(BaseModel):
    """FableMazeの設定を管理するPydanticモデル"""
    
    # AIモデル設定
    model_name: str = Field(default="llama2", description="使用するAIモデルの名前")
    model_endpoint: str = Field(default="http://localhost:11434", description="AIモデルのエンドポイント")
    
    # ストーリー生成設定
    max_tokens: int = Field(default=2048, description="生成するテキストの最大トークン数")
    temperature: float = Field(default=0.7, description="生成の多様性を制御するパラメータ")
    
    # Wiki統合設定
    wiki_enabled: bool = Field(default=True, description="Wiki統合機能の有効/無効")
    wiki_base_path: Path = Field(default=Path("./wiki"), description="Wikiファイルの保存場所")
    
    # HTML生成設定
    template_dir: Path = Field(default=Path("./templates"), description="HTMLテンプレートのディレクトリ")
    output_dir: Path = Field(default=Path("./output"), description="生成されたHTMLの出力先")

    @classmethod
    def load_from_file(cls, config_path: Path) -> "FableMazeConfig":
        """設定ファイルから設定を読み込む"""
        if not config_path.exists():
            return cls()
        
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        return cls(**config_data)

    def save_to_file(self, config_path: Path) -> None:
        """設定をファイルに保存する"""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, indent=2, ensure_ascii=False)

def load_config(config_path: Optional[Path] = None) -> FableMazeConfig:
    """
    設定を読み込む
    
    1. 環境変数
    2. 設定ファイル
    3. デフォルト値
    の順で優先される
    """
    if config_path is None:
        config_path = Path("config/fablemaze.json")
    
    # 設定ファイルから読み込み
    config = FableMazeConfig.load_from_file(config_path)
    
    # 環境変数で上書き
    env_prefix = "FABLEMAZE_"
    for field_name in config.model_fields:
        env_name = f"{env_prefix}{field_name.upper()}"
        if env_name in os.environ:
            setattr(config, field_name, os.environ[env_name])
    
    return config 