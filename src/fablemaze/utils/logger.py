"""
FableMazeロギング設定モジュール

このモジュールは、FableMazeのロギング設定を管理します。
loguru を使用して、構造化ログ出力を提供します。
"""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

def setup_logging(
    log_file: Optional[Path] = None,
    log_level: str = "INFO",
    rotation: str = "1 day",
    retention: str = "1 week"
) -> None:
    """
    ロギングの設定を行う
    
    Args:
        log_file: ログファイルのパス
        log_level: ログレベル
        rotation: ログローテーションの設定
        retention: ログ保持期間
    """
    # デフォルトのシンクを削除
    logger.remove()
    
    # 標準エラー出力へのログ設定
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    # ファイルへのログ設定
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_file),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
            rotation=rotation,
            retention=retention,
            encoding="utf-8"
        )

def get_logger(name: str = "fablemaze"):
    """
    名前付きロガーを取得する
    
    Args:
        name: ロガー名
    
    Returns:
        loguru.Logger: 設定済みのロガーインスタンス
    """
    return logger.bind(name=name) 