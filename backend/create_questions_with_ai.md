# AIを使って高精度な問題を作成する方法

## 概要
このドキュメントでは、AI（ChatGPT、Claude、Geminiなど）を使って基本情報技術者試験の高精度な問題を作成する方法を説明します。

## 手順

### 1. プロンプト生成ツールの使用

`backend/question_generator.py`の`generate_question_prompt()`関数を使用して、高精度なプロンプトを生成します。

```python
from backend.question_generator import generate_question_prompt

prompt = generate_question_prompt(
    category='ネットワーク',
    topic='TCP/IP',
    difficulty='medium'
)
print(prompt)
```

### 2. AIにプロンプトを送信

生成されたプロンプトをAIに送信し、問題を作成してもらいます。

### 3. 品質チェック

作成された問題を`check_question_quality()`関数でチェックします。

```python
from backend.question_generator import check_question_quality

result = check_question_quality(question_data)
if result['is_valid']:
    print("問題は有効です")
else:
    print("問題に問題があります:", result['issues'])
    print("改善提案:", result['suggestions'])
```

### 4. 問題データの追加

品質チェックを通過した問題を`backend/real_questions.py`または`backend/question_data.py`に追加します。

## 推奨されるワークフロー

1. **トピックの選定**: 出題範囲から重要なトピックを選ぶ
2. **プロンプト生成**: `generate_question_prompt()`でプロンプトを生成
3. **AIに送信**: 生成されたプロンプトをAIに送信
4. **品質チェック**: `check_question_quality()`でチェック
5. **修正**: 必要に応じて問題を修正
6. **追加**: 問題データファイルに追加
7. **テスト**: データベースに投入して動作確認

## 注意事項

- AIが生成した問題は必ず品質チェックを行う
- 実際の過去問と照らし合わせて確認する
- 専門家のレビューを受けることが望ましい（可能な場合）
- 継続的に改善する

## バッチ処理

複数の問題を一度に作成する場合：

```python
from backend.question_generator import generate_question_prompt, check_question_quality

topics = [
    ('ネットワーク', 'TCP/IP', 'medium'),
    ('データベース', 'SQL', 'medium'),
    ('セキュリティ', '暗号化', 'hard'),
]

for category, topic, difficulty in topics:
    prompt = generate_question_prompt(category, topic, difficulty)
    # AIに送信して問題を取得
    # 品質チェック
    # 問題データに追加
```

