"""
FableMaze - インタラクティブストーリー生成システム

FableMazeは、AIパワードのストーリー生成エンジン、Wiki統合、
HTML生成エンジンを組み合わせて、分岐型の物語創作をサポートする
フレームワークです。

主な機能:
- インタラクティブなストーリー生成
- Wiki統合による世界観管理
- 分岐ストーリーの視覚化と管理
- HTML形式のエクスポート
"""

__version__ = "0.1.0"

from . import (
    story_engine,
    wiki_integration,
    html_engine,
    story_graph,
    ui,
    utils,
) 