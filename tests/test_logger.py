"""
FableMazeロギング機能のテスト
"""
import sys
from pathlib import Path
import pytest
from fablemaze.utils.logger import setup_logging, get_logger

def test_logger_setup(tmp_path):
    """ロガーのセットアップテスト"""
    log_file = tmp_path / "test.log"
    setup_logging(log_file=log_file)
    
    logger = get_logger("test")
    test_message = "Test log message"
    logger.info(test_message)
    
    # ログファイルが作成されたことを確認
    assert log_file.exists()
    
    # ログメッセージが書き込まれたことを確認
    log_content = log_file.read_text()
    assert test_message in log_content

def test_logger_name():
    """ロガー名のテスト"""
    logger = get_logger("custom_name")
    assert "custom_name" in str(logger) 