# AI Career Discovery Assistant

日本の求職者向けのAIキャリア分析システム。履歴書や職務経歴書をアップロードすることで、AIが分析し、最適なキャリアパスを提案します。

## 🚀 主な機能

- **書類分析**: PDF/Word形式の履歴書・職務経歴書を自動分析
- **OCR対応**: スキャンされたPDFも自動でテキスト抽出
- **AIキャリア提案**: 3つのキャリアパス（企業転職、フリーランス、起業）を提案
- **スキルマッチング**: 経験・スキルと求人市場のマッチング度を計算
- **年収予測**: 各キャリアパスでの想定年収レンジを提示

## 🛠️ 技術スタック

### Backend
- FastAPI (Python 3.11)
- PostgreSQL
- Redis (キャッシュ・キュー)
- Celery (非同期タスク処理)
- Google Gemini API (AI分析)

### Frontend
- React 18 + TypeScript
- Vite
- Ant Design
- Tailwind CSS

### Infrastructure
- Docker & Docker Compose
- MinIO (S3互換ストレージ)

## 📋 必要な環境

- Docker Desktop
- Git
- Google Cloud Platform アカウント（Gemini API用）

## 🚦 セットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/ai-career-discovery-assistant.git
cd ai-career-discovery-assistant
```

2. 環境変数の設定
```bash
# backend/.env ファイルを作成
cp backend/.env.example backend/.env
```

3. Gemini API キーの設定
```env
GEMINI_API_KEY=your-api-key-here
```

4. Dockerコンテナの起動
```bash
docker-compose up -d
```

5. アプリケーションへアクセス
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📝 使い方

1. ユーザー登録
2. ログイン
3. 履歴書または職務経歴書をアップロード
4. AI分析の完了を待つ（通常1-2分）
5. 分析結果とキャリア提案を確認

## 🐳 Docker コマンド

```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# ログ確認
docker-compose logs -f

# 再ビルド
docker-compose up -d --build
```

## 📊 システム構成

```
ai-career-discovery-assistant/
├── backend/           # FastAPI バックエンド
│   ├── app/          # アプリケーションコード
│   ├── alembic/      # データベースマイグレーション
│   └── tests/        # テストコード
├── frontend/         # React フロントエンド
│   ├── src/          # ソースコード
│   └── public/       # 静的ファイル
├── docker-compose.yml # Docker構成
└── README.md         # このファイル
```

## 🔒 セキュリティ

- JWT認証によるセキュアなAPI
- ファイルアップロードのバリデーション
- SQL インジェクション対策
- CORS設定による適切なアクセス制御

## 🤝 貢献

プルリクエストを歓迎します！大きな変更の場合は、まずissueを作成して変更内容について議論してください。

## 📄 ライセンス

[MIT License](LICENSE)

## 👥 作者

AI Career Discovery Team

## 🙏 謝辞

- Google Gemini API
- FastAPI コミュニティ
- React コミュニティ