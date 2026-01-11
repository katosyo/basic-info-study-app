"""
基本情報技術者試験の問題生成支援ツール
AIに高精度な問題を作成させるためのプロンプト生成と品質チェック
"""

# 基本情報技術者試験の出題範囲
EXAM_TOPICS = {
    'テクノロジ系': {
        '基礎理論': [
            '基数変換', '論理演算', 'データ構造', 'アルゴリズム', 
            '計算量', 'ソートアルゴリズム', '探索アルゴリズム'
        ],
        'コンピュータシステム': [
            'CPU', 'メモリ', 'ストレージ', 'OS', 'ミドルウェア',
            'ファイルシステム', 'プロセス管理', 'メモリ管理'
        ],
        '技術要素': {
            'ネットワーク': [
                'TCP/IP', 'OSI参照モデル', 'HTTP/HTTPS', 'DNS',
                'ルーティング', 'サブネット', '無線LAN', 'VPN'
            ],
            'データベース': [
                'SQL', '正規化', 'トランザクション', 'ACID特性',
                'インデックス', 'JOIN', '外部キー', 'リレーショナルモデル'
            ],
            'セキュリティ': [
                '暗号化', '認証', 'アクセス制御', 'ファイアウォール',
                'SSL/TLS', '公開鍵暗号', 'ハッシュ関数', 'セキュリティポリシー'
            ]
        }
    },
    'マネジメント系': {
        'プロジェクトマネジメント': [
            'WBS', 'ガントチャート', 'クリティカルパス', 'リスク管理'
        ],
        'サービスマネジメント': [
            'ITIL', 'インシデント管理', '変更管理', '可用性管理'
        ]
    },
    'ストラテジ系': {
        'システム戦略': [
            'システム開発手法', '要件定義', 'システム設計', 'テスト'
        ],
        '経営戦略': [
            'ビジネスモデル', '競争戦略', 'IT投資評価'
        ]
    }
}

# 問題作成のプロンプトテンプレート
def generate_question_prompt(category, topic, difficulty='medium', question_type='適切なものはどれか'):
    """
    高精度な問題作成のためのプロンプトを生成
    
    Args:
        category: カテゴリ（例：'ネットワーク', 'データベース'）
        topic: トピック（例：'TCP/IP', 'SQL'）
        difficulty: 難易度（'easy', 'medium', 'hard'）
        question_type: 問題タイプ（'適切なものはどれか', '不適切なものはどれか'）
    """
    
    difficulty_map = {
        'easy': '基本レベル（用語の定義、基本的な概念）',
        'medium': '標準レベル（複数の概念の組み合わせ、実務でよく使われる知識）',
        'hard': '応用レベル（複数の知識の統合、計算が必要、実務経験が役立つ）'
    }
    
    prompt = f"""
基本情報技術者試験の予想問題を作成してください。

【出題分野】
{category}

【出題範囲】
{topic}

【難易度】
{difficulty_map.get(difficulty, 'medium')}

【問題形式】
- 4択問題
- 「{question_type}」形式

【要求事項】
1. 実際の基本情報技術者試験の過去問の形式に厳密に準拠すること
2. 選択肢は4つで、すべて同じ長さ程度（50-100文字程度）にすること
3. 正解は明確で、根拠があること
4. 不正解の選択肢は、よくある誤解や関連するが異なる概念を反映すること
5. 完全に的外れな選択肢は避けること（学習効果が低いため）
6. 詳細な解説を含めること：
   - 正解の理由（なぜその選択肢が正しいのか）
   - 不正解の理由（他の選択肢がなぜ間違っているのか）
   - 関連する重要な概念
   - 実務での活用例（可能な場合）
7. 実務で使われる知識を重視すること
8. 専門用語は正確に使用すること
9. 文法的に正しい文章であること

【出力形式】
以下のJSON形式で出力してください：
{{
    "question_text": "問題文",
    "question_type": "multiple_choice",
    "category": "{category}",
    "difficulty": "{difficulty}",
    "explanation": "詳細な解説（正解の理由、不正解の理由、関連知識を含む）",
    "options": [
        {{"option_text": "選択肢1", "is_correct": true}},
        {{"option_text": "選択肢2", "is_correct": false}},
        {{"option_text": "選択肢3", "is_correct": false}},
        {{"option_text": "選択肢4", "is_correct": false}}
    ]
}}

【参考情報】
- 基本情報技術者試験 シラバス（IPA公式）に準拠
- 実際の過去問の形式を参考にすること
- 実務でよく使われる技術を重視すること
"""
    
    return prompt

# 問題の品質チェック
def check_question_quality(question_data):
    """
    問題の品質をチェック
    
    Returns:
        dict: チェック結果と改善提案
    """
    issues = []
    suggestions = []
    
    # 問題文のチェック
    if not question_data.get('question_text'):
        issues.append('問題文が空です')
    elif len(question_data['question_text']) < 20:
        issues.append('問題文が短すぎます（20文字以上推奨）')
    elif len(question_data['question_text']) > 200:
        issues.append('問題文が長すぎます（200文字以下推奨）')
    
    # 選択肢のチェック
    options = question_data.get('options', [])
    if len(options) != 4:
        issues.append(f'選択肢が4つではありません（現在{len(options)}つ）')
    
    # 正解のチェック
    correct_count = sum(1 for opt in options if opt.get('is_correct', False))
    if correct_count == 0:
        issues.append('正解が設定されていません')
    elif correct_count > 1:
        issues.append(f'正解が複数設定されています（現在{correct_count}つ）')
    
    # 選択肢の長さのバランス
    if len(options) == 4:
        lengths = [len(opt.get('option_text', '')) for opt in options]
        max_len = max(lengths)
        min_len = min(lengths)
        if max_len > min_len * 2:
            suggestions.append('選択肢の長さのバランスを取ることを推奨します')
    
    # 解説のチェック
    explanation = question_data.get('explanation', '')
    if not explanation:
        issues.append('解説が空です')
    elif len(explanation) < 50:
        suggestions.append('解説をもう少し詳しく書くことを推奨します（50文字以上）')
    
    # 難易度のチェック
    difficulty = question_data.get('difficulty', 'medium')
    if difficulty not in ['easy', 'medium', 'hard']:
        issues.append(f'難易度が適切に設定されていません（現在: {difficulty}）')
    
    return {
        'is_valid': len(issues) == 0,
        'issues': issues,
        'suggestions': suggestions
    }

# 問題生成のヘルパー関数
def get_topics_by_category(category):
    """カテゴリからトピック一覧を取得"""
    topics = []
    for main_category, sub_categories in EXAM_TOPICS.items():
        if isinstance(sub_categories, dict):
            for sub_category, topic_list in sub_categories.items():
                if category.lower() in sub_category.lower() or category.lower() in main_category.lower():
                    if isinstance(topic_list, list):
                        topics.extend(topic_list)
                    elif isinstance(topic_list, dict):
                        for sub_topics in topic_list.values():
                            topics.extend(sub_topics)
    return topics if topics else ['一般的な知識']

if __name__ == '__main__':
    # 使用例
    prompt = generate_question_prompt(
        category='ネットワーク',
        topic='TCP/IP',
        difficulty='medium'
    )
    print(prompt)

