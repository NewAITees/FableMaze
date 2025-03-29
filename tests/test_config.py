"""
FableMaze設定管理のテスト
"""
import os
from pathlib import Path
import pytest
from fablemaze.utils.config import FableMazeConfig, load_config

def test_default_config():
    """デフォルト設定のテスト"""
    config = FableMazeConfig()
    assert config.model_name == "llama2"
    assert config.model_endpoint == "http://localhost:11434"
    assert config.max_tokens == 2048
    assert config.temperature == 0.7

def test_config_from_env():
    """環境変数からの設定読み込みテスト"""
    os.environ["FABLEMAZE_MODEL_NAME"] = "test_model"
    os.environ["FABLEMAZE_TEMPERATURE"] = "0.8"
    
    config = load_config()
    assert config.model_name == "test_model"
    assert config.temperature == 0.8
    
    # 環境変数をクリーンアップ
    del os.environ["FABLEMAZE_MODEL_NAME"]
    del os.environ["FABLEMAZE_TEMPERATURE"]

def test_config_save_load(tmp_path):
    """設定の保存と読み込みテスト"""
    config = FableMazeConfig(
        model_name="test_model",
        temperature=0.8,
        wiki_enabled=False
    )
    
    config_path = tmp_path / "test_config.json"
    config.save_to_file(config_path)
    
    loaded_config = FableMazeConfig.load_from_file(config_path)
    assert loaded_config.model_name == "test_model"
    assert loaded_config.temperature == 0.8
    assert loaded_config.wiki_enabled is False 