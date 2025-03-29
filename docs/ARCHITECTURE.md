# アーキテクチャ概要

このドキュメントは FableMaze の全体的なアーキテクチャについて説明します。

## システム概要

FableMaze は、AIを活用したインタラクティブなストーリー生成システムです。フロントエンド（Gradio UI）、ストーリー生成エンジン、Wiki統合、HTML生成エンジンという4つの主要コンポーネントで構成されています。

```mermaid
graph TB
    subgraph "ユーザー"
        UI[Gradio Web UI]
    end
    
    subgraph "FableMaze コア"
        Controller[コアコントローラー]
        StoryEngine[ストーリー生成エンジン]
        WikiIntegration[Wiki統合モジュール]
        HTMLEngine[HTML生成エンジン]
        StoryGraph[ストーリーグラフ管理]
    end
    
    subgraph "外部システム"
        LLM[大規模言語モデル]
        DokuWiki[DokuWiki]
    end
    
    UI <--> Controller
    Controller <--> StoryEngine
    Controller <--> WikiIntegration
    Controller <--> HTMLEngine
    Controller <--> StoryGraph
    
    StoryEngine <--> LLM
    WikiIntegration <--> DokuWiki
    
    style Controller fill:#bbdefb,stroke:#1976d2
    style StoryEngine fill:#c8e6c9,stroke:#4caf50
    style WikiIntegration fill:#ffecb3,stroke:#ffa000
    style HTMLEngine fill:#e1bee7,stroke:#8e24aa
    style StoryGraph fill:#ffcdd2,stroke:#e53935
```

## 主要コンポーネント

### 1. コアコントローラー

システム全体の制御と調整を担当するコンポーネントです。

- **Session Manager**: ユーザーセッションの管理
- **Workflow Coordinator**: ストーリー生成ワークフローの調整
- **Component Integrator**: 各コンポーネント間の連携管理
- **Configuration Manager**: システム設定の管理

### 2. ストーリー生成エンジン

AIを活用したストーリー創作を担当するコンポーネントです。

- **AI Client**: 大規模言語モデルとの通信
- **Prompt Manager**: プロンプト設計と管理
- **Context Handler**: 物語コンテキストの管理
- **Choice Generator**: 分岐選択肢の生成

### 3. Wiki統合モジュール

世界観の一貫性を維持するためのWiki連携を担当するコンポーネントです。

- **Entity Extractor**: 物語からエンティティを抽出
- **Wiki Formatter**: DokuWiki形式へのフォーマット
- **Sync Manager**: Wiki内容と物語の同期
- **Consistency Checker**: 設定の一貫性チェック

### 4. HTML生成エンジン

物語をHTMLページとして出力するコンポーネントです。

- **Template Engine**: Jinja2テンプレート処理
- **CSS Manager**: スタイルシートの管理
- **Page Assembler**: ページの組み立て
- **Navigation Builder**: ナビゲーション構造の構築

### 5. ストーリーグラフ管理

物語の分岐構造を管理するコンポーネントです。

- **Graph Database**: 物語ノードとエッジの保存
- **Path Analyzer**: ストーリーパスの分析
- **Visualization Tool**: グラフの視覚化
- **Consistency Checker**: グラフの整合性検証

## データフロー

ユーザーがFableMazeを通じてストーリーを生成・閲覧する際のデータフローを示します。

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as Gradio UI
    participant Controller as コアコントローラー
    participant StoryEngine as ストーリー生成エンジン
    participant LLM as 大規模言語モデル
    participant WikiModule as Wiki統合モジュール
    participant HTMLEngine as HTML生成エンジン
    participant Graph as ストーリーグラフ管理
    
    User->>UI: ストーリー設定入力
    UI->>Controller: 設定情報送信
    Controller->>StoryEngine: ストーリー生成リクエスト
    
    StoryEngine->>LLM: プロンプト送信
    LLM-->>StoryEngine: 生成テキスト返却
    
    StoryEngine-->>Controller: ストーリー返却
    Controller->>WikiModule: エンティティ抽出リクエスト
    WikiModule-->>Controller: Wiki情報返却
    
    Controller->>HTMLEngine: HTML生成リクエスト
    HTMLEngine-->>Controller: HTML返却
    
    Controller->>Graph: ストーリーノード保存
    Graph-->>Controller: 保存確認
    
    Controller-->>UI: 生成ストーリー表示
    UI-->>User: ストーリー提示
    
    User->>UI: 選択肢選択
    UI->>Controller: 選択情報送信
    Controller->>StoryEngine: 続きのストーリー生成リクエスト
    
    StoryEngine->>LLM: 選択を含むプロンプト送信
    LLM-->>StoryEngine: 続きのテキスト返却
    
    StoryEngine-->>Controller: 続きのストーリー返却
    Controller->>Graph: 新ノード追加
    Graph-->>Controller: グラフ更新確認
    
    Controller-->>UI: 続きのストーリー表示
    UI-->>User: 続きのストーリー提示
```

## フォルダ構成

```mermaid
graph TD
    A[fablemaze] --> B[app.py]
    A --> C[requirements.txt]
    A --> D[docs/]
    A --> E[fablemaze/]
    
    E --> E1[__init__.py]
    E --> E2[controller.py]
    E --> E3[story_engine.py]
    E --> E4[wiki_integration.py]
    E --> E5[html_engine.py]
    E --> E6[story_graph.py]
    E --> E7[ui/]
    
    E7 --> E7A[__init__.py]
    E7 --> E7B[app.py]
    E7 --> E7C[components.py]
    E7 --> E7D[pages/]
    E7 --> E7E[templates/]
    
    A --> F[examples/]
    A --> G[tests/]
    
    style A fill:#f9f9f9,stroke:#999
    style E fill:#bbdefb,stroke:#1976d2
    style E7 fill:#c8e6c9,stroke:#4caf50
```

## 技術選定

| コンポーネント | 技術 | 選定理由 |
|----------------|------|----------|
| バックエンド言語 | Python 3.10+ | 機械学習ライブラリとの広範な互換性、asyncio での非同期処理サポート |
| AIエンジン | OpenAI API / Ollama | 高品質なテキスト生成、ローカル実行オプション |
| ウェブ UI | Gradio | 迅速な UI 開発、ML プロジェクトとの相性の良さ、コンポーネント豊富 |
| テンプレートエンジン | Jinja2 | 柔軟なHTMLテンプレート処理、Pythonとの統合の容易さ |
| Wiki システム | DokuWiki | シンプルなファイルベースの構造、APIの利用しやすさ |
| グラフデータベース | NetworkX | Pythonネイティブのグラフ処理、データ分析の容易さ |
| 依存関係管理 | Poetry | パッケージ管理の一貫性、仮想環境管理の容易さ |
| テスト | pytest | 豊富なテスト機能、asyncio 対応のテストサポート |

## アーキテクチャの原則

1. **モジュール性**: 機能を明確に分離し、独立して開発・テスト可能なコンポーネント設計
2. **拡張性**: 新しいストーリーテンプレートやモデルの追加が容易な柔軟な基盤
3. **一貫性**: 物語世界の設定と内容の一貫性を保証するメカニズム
4. **使いやすさ**: 作家と読者の両方にとって直感的なインターフェース
5. **堅牢性**: エラー処理と回復メカニズムの組み込み
6. **パフォーマンス**: 大規模な物語構造でも効率的に機能する設計
7. **創造性**: AIの創造性を最大限に引き出し、人間の創造性を拡張する

このアーキテクチャにより、FableMazeは複雑なインタラクティブストーリーの作成と体験を可能にし、作家と読者の双方に新たな物語体験の可能性を提供します。

## プロンプト設計システム

階層的なプロンプト設計構造により、一貫性のある魅力的なストーリーを生成します。

```mermaid
graph TD
    A[マスタープロンプト] --> B[設定プロンプト]
    A --> C[チャプタープロンプト]
    A --> D[分岐プロンプト]
    A --> E[エンディングプロンプト]
    
    B --> B1[世界観定義]
    B --> B2[キャラクター設定]
    B --> B3[ルール定義]
    
    C --> C1[導入部プロンプト]
    C --> C2[展開部プロンプト]
    C --> C3[クライマックスプロンプト]
    
    D --> D1[選択肢生成]
    D --> D2[結果予測]
    
    E --> E1[エピローグプロンプト]
    E --> E2[後日談プロンプト]
    
    style A fill:#bbdefb,stroke:#1976d2
    style B fill:#c8e6c9,stroke:#4caf50
    style C fill:#ffecb3,stroke:#ffa000
    style D fill:#e1bee7,stroke:#8e24aa
    style E fill:#ffcdd2,stroke:#e53935
```

各プロンプトレベルは特定の役割を持ち、全体として一貫性のある魅力的なストーリーを構築します。

## Wiki統合システムの詳細

DokuWikiをベースにした統合Wikiシステムにより、ストーリー間の一貫性を管理します。

```mermaid
graph TD
    A[Wiki統合モジュール] --> B[エンティティ抽出]
    A --> C[ページ生成]
    A --> D[クロスリンク管理]
    A --> E[メタデータ管理]
    
    B --> B1[キャラクター抽出]
    B --> B2[場所抽出]
    B --> B3[アイテム抽出]
    B --> B4[概念抽出]
    
    C --> C1[テンプレート選択]
    C --> C2[コンテンツ生成]
    C --> C3[タグ付け]
    
    D --> D1[ストーリーからWikiへのリンク]
    D --> D2[Wikiからストーリーへのリンク]
    D --> D3[Wiki内相互リンク]
    
    E --> E1[関係性メタデータ]
    E --> E2[登場頻度メタデータ]
    E --> E3[重要度メタデータ]
    
    style A fill:#bbdefb,stroke:#1976d2
    style B fill:#c8e6c9,stroke:#4caf50
    style C fill:#ffecb3,stroke:#ffa000
    style D fill:#e1bee7,stroke:#8e24aa
    style E fill:#ffcdd2,stroke:#e53935
```

## HTML生成システムの詳細

Jinja2テンプレートエンジンを用いたHTML生成システムの構造を示します。

```mermaid
graph TD
    A[HTML生成エンジン] --> B[テンプレート管理]
    A --> C[スタイル管理]
    A --> D[コンテンツ処理]
    A --> E[ナビゲーション生成]
    
    B --> B1[ジャンル別テンプレート]
    B --> B2[レイアウトテンプレート]
    B --> B3[コンポーネントテンプレート]
    
    C --> C1[テーマ管理]
    C --> C2[レスポンシブデザイン]
    C --> C3[アニメーション効果]
    
    D --> D1[テキスト整形]
    D --> D2[選択肢フォーマット]
    D --> D3[Wiki統合リンク]
    
    E --> E1[チャプター間ナビゲーション]
    E --> E2[選択肢リンク]
    E --> E3[Wiki参照リンク]
    
    style A fill:#bbdefb,stroke:#1976d2
    style B fill:#c8e6c9,stroke:#4caf50
    style C fill:#ffecb3,stroke:#ffa000
    style D fill:#e1bee7,stroke:#8e24aa
    style E fill:#ffcdd2,stroke:#e53935
```

## ストーリーグラフデータ構造

物語の分岐構造を有向グラフとして管理するシステムの詳細です。

```mermaid
graph TD
    A[ストーリーグラフ管理] --> B[ノード管理]
    A --> C[エッジ管理]
    A --> D[パス分析]
    A --> E[視覚化]
    
    B --> B1[チャプターノード]
    B --> B2[選択肢ノード]
    B --> B3[エンディングノード]
    
    C --> C1[選択肢エッジ]
    C --> C2[シーケンスエッジ]
    C --> C3[フラッシュバックエッジ]
    
    D --> D1[パス列挙]
    D --> D2[到達可能性分析]
    D --> D3[バランス分析]
    
    E --> E1[2Dグラフ表示]
    E --> E2[インタラクティブマップ]
    E --> E3[分析ダッシュボード]
    
    style A fill:#bbdefb,stroke:#1976d2
    style B fill:#c8e6c9,stroke:#4caf50
    style C fill:#ffecb3,stroke:#ffa000
    style D fill:#e1bee7,stroke:#8e24aa
    style E fill:#ffcdd2,stroke:#e53935
```

このアーキテクチャにより、FableMazeはAIの創造性を活用しながら一貫性のある豊かなストーリー体験を提供することが可能になります。