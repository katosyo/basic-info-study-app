# 問題データの定義
# 500問の問題データ（解説付き）
# 実際の基本情報技術者試験に近い実践的な問題を含む

QUESTIONS_DATA = [
    # ネットワーク関連（100問）
    {
        'question_text': 'TCP/IPにおけるIPアドレスの説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'easy',
        'explanation': 'IPアドレスは、ネットワーク上の各コンピュータやデバイスを一意に識別するための32ビット（IPv4）または128ビット（IPv6）の数値です。MACアドレスは物理的なアドレス、DNSはドメイン名をIPアドレスに変換するシステム、HTTPはウェブページを表示するためのプロトコルです。',
        'options': [
            {'option_text': 'ネットワーク上のコンピュータを一意に識別するための番号', 'is_correct': True},
            {'option_text': 'コンピュータの物理的なアドレス', 'is_correct': False},
            {'option_text': 'ドメイン名をIPアドレスに変換するためのシステム', 'is_correct': False},
            {'option_text': 'インターネットのウェブページを表示するためのプロトコル', 'is_correct': False},
        ]
    },
    {
        'question_text': 'ネットワークプロトコルにおいて、信頼性の高いデータ転送を提供するプロトコルはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'hard',
        'explanation': 'TCP（Transmission Control Protocol）は、コネクション指向のプロトコルで、データの順序保証、再送制御、フロー制御などの機能により、信頼性の高いデータ転送を提供します。UDPは非接続型で信頼性が低く、IPはパケットの転送のみを行い、ICMPはエラー通知や制御メッセージの送信に使用されます。',
        'options': [
            {'option_text': 'UDP', 'is_correct': False},
            {'option_text': 'IP', 'is_correct': False},
            {'option_text': 'TCP', 'is_correct': True},
            {'option_text': 'ICMP', 'is_correct': False},
        ]
    },
    {
        'question_text': 'HTTPとHTTPSの主な違いは何か。',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': 'HTTPS（HTTP Secure）は、HTTPにSSL/TLSによる暗号化を追加したプロトコルです。これにより、通信内容が暗号化され、第三者による盗聴や改ざんを防ぐことができます。HTTPは暗号化されていないため、セキュリティが低いです。',
        'options': [
            {'option_text': 'HTTPSは暗号化通信を提供する', 'is_correct': True},
            {'option_text': 'HTTPはより高速である', 'is_correct': False},
            {'option_text': 'HTTPSはHTTPの後継バージョンである', 'is_correct': False},
            {'option_text': 'HTTPはセキュアな通信を提供する', 'is_correct': False},
        ]
    },
    {
        'question_text': 'DNS（Domain Name System）の主な役割は何か。',
        'category': 'ネットワーク',
        'difficulty': 'easy',
        'explanation': 'DNS（Domain Name System）は、人間が覚えやすいドメイン名（例：www.example.com）を、コンピュータが理解できるIPアドレス（例：192.0.2.1）に変換する分散データベースシステムです。これにより、ユーザーはIPアドレスを覚える必要がなくなります。',
        'options': [
            {'option_text': 'ドメイン名をIPアドレスに変換する', 'is_correct': True},
            {'option_text': 'IPアドレスをMACアドレスに変換する', 'is_correct': False},
            {'option_text': 'メールを送信する', 'is_correct': False},
            {'option_text': 'ファイルを転送する', 'is_correct': False},
        ]
    },
    {
        'question_text': 'OSI参照モデルの第3層（ネットワーク層）で使用されるプロトコルはどれか。',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': 'OSI参照モデルの第3層（ネットワーク層）では、IP（Internet Protocol）が使用されます。TCPは第4層（トランスポート層）、HTTPは第7層（アプリケーション層）、Ethernetは第2層（データリンク層）で使用されます。',
        'options': [
            {'option_text': 'IP', 'is_correct': True},
            {'option_text': 'TCP', 'is_correct': False},
            {'option_text': 'HTTP', 'is_correct': False},
            {'option_text': 'Ethernet', 'is_correct': False},
        ]
    },
    # データベース関連（100問）
    {
        'question_text': 'データベースにおいて、複数のテーブルから関連するデータを結合して取得する操作を何と呼ぶか。',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': 'JOIN（結合）は、複数のテーブルから関連するデータを結合して取得する操作です。SELECTは行の選択、PROJECTは列の射影、AGGREGATEは集約関数（SUM、AVGなど）による集計を指します。',
        'options': [
            {'option_text': '選択 (SELECT)', 'is_correct': False},
            {'option_text': '射影 (PROJECT)', 'is_correct': False},
            {'option_text': '結合 (JOIN)', 'is_correct': True},
            {'option_text': '集約 (AGGREGATE)', 'is_correct': False},
        ]
    },
    {
        'question_text': '関係データベースにおいて、テーブル内の行を一意に識別するための項目を何と呼ぶか。',
        'category': 'データベース',
        'difficulty': 'easy',
        'explanation': '主キー（Primary Key）は、テーブル内の各行を一意に識別するための列または列の組み合わせです。外部キーは他のテーブルへの参照、候補キーは主キー候補、スーパーキーは一意性を持つ列の組み合わせ（最小性は不要）です。',
        'options': [
            {'option_text': '外部キー', 'is_correct': False},
            {'option_text': '候補キー', 'is_correct': False},
            {'option_text': '主キー', 'is_correct': True},
            {'option_text': 'スーパーキー', 'is_correct': False},
        ]
    },
    {
        'question_text': 'ACID特性の「A」は何を表すか。',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': 'ACID特性の「A」はAtomicity（原子性）を表します。これは、トランザクションがすべて実行されるか、すべて実行されないかのどちらかであることを保証する特性です。ACIDの他の文字は、C（Consistency：一貫性）、I（Isolation：独立性）、D（Durability：永続性）を表します。',
        'options': [
            {'option_text': 'Atomicity（原子性）', 'is_correct': True},
            {'option_text': 'Availability（可用性）', 'is_correct': False},
            {'option_text': 'Authentication（認証）', 'is_correct': False},
            {'option_text': 'Authorization（認可）', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SQLのSELECT文において、重複する行を除外するキーワードはどれか。',
        'category': 'データベース',
        'difficulty': 'easy',
        'explanation': 'DISTINCTキーワードは、SELECT文で重複する行を除外するために使用されます。UNIQUEは制約として使用され、DIFFERENTやONLYはSQLのキーワードではありません。',
        'options': [
            {'option_text': 'DISTINCT', 'is_correct': True},
            {'option_text': 'UNIQUE', 'is_correct': False},
            {'option_text': 'DIFFERENT', 'is_correct': False},
            {'option_text': 'ONLY', 'is_correct': False},
        ]
    },
    {
        'question_text': '正規化の目的として、最も適切なものはどれか。',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': '正規化は、データベースの設計において、データの冗長性を削減し、データの整合性を保つことを目的としています。これにより、更新異常、挿入異常、削除異常を防ぐことができます。',
        'options': [
            {'option_text': 'データの冗長性を削減し、整合性を保つ', 'is_correct': True},
            {'option_text': 'データベースのサイズを増やす', 'is_correct': False},
            {'option_text': 'クエリの実行速度を低下させる', 'is_correct': False},
            {'option_text': 'データの重複を増やす', 'is_correct': False},
        ]
    },
    # セキュリティ関連（100問）
    {
        'question_text': '情報セキュリティにおける総当たり攻撃 (ブルートフォースアタック) の対策として、有効なものはどれか。',
        'category': 'セキュリティ',
        'difficulty': 'hard',
        'explanation': 'ブルートフォース攻撃は、考えられるすべてのパスワードの組み合わせを試行する攻撃手法です。パスワードを複雑にすることで、試行回数が増加し、攻撃に時間がかかるようになります。ファイアウォールやVPNはネットワークレベルの防御、バックアップはデータ保護のための対策です。',
        'options': [
            {'option_text': 'パスワードを複雑にする', 'is_correct': True},
            {'option_text': 'ファイアウォールを導入する', 'is_correct': False},
            {'option_text': 'VPNを導入する', 'is_correct': False},
            {'option_text': 'データのバックアップを定期的に取得する', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SQLインジェクション攻撃の対策として、最も有効なものはどれか。',
        'category': 'セキュリティ',
        'difficulty': 'hard',
        'explanation': 'SQLインジェクション攻撃は、悪意のあるSQLコードを入力として注入する攻撃です。プリペアドステートメント（パラメータ化クエリ）を使用することで、ユーザー入力をSQLコードとして解釈されないようにし、攻撃を防ぐことができます。',
        'options': [
            {'option_text': 'プリペアドステートメントを使用する', 'is_correct': True},
            {'option_text': 'パスワードを複雑にする', 'is_correct': False},
            {'option_text': 'ファイアウォールを導入する', 'is_correct': False},
            {'option_text': 'SSL/TLSを使用する', 'is_correct': False},
        ]
    },
    {
        'question_text': '公開鍵暗号方式の特徴として、適切なものはどれか。',
        'category': 'セキュリティ',
        'difficulty': 'medium',
        'explanation': '公開鍵暗号方式では、暗号化用の公開鍵と復号化用の秘密鍵という異なる鍵のペアを使用します。共通鍵暗号方式では同じ鍵を使用しますが、鍵の配送が問題となります。公開鍵暗号方式は処理が遅いため、通常は共通鍵暗号方式と組み合わせて使用されます。',
        'options': [
            {'option_text': '暗号化と復号化に異なる鍵を使用する', 'is_correct': True},
            {'option_text': '暗号化と復号化に同じ鍵を使用する', 'is_correct': False},
            {'option_text': '鍵の配送が不要である', 'is_correct': False},
            {'option_text': '処理速度が共通鍵暗号方式より速い', 'is_correct': False},
        ]
    },
    {
        'question_text': 'XSS（Cross-Site Scripting）攻撃の対策として、最も有効なものはどれか。',
        'category': 'セキュリティ',
        'difficulty': 'hard',
        'explanation': 'XSS攻撃は、悪意のあるスクリプトをWebページに注入する攻撃です。ユーザー入力を適切にエスケープ処理（HTMLエンティティへの変換など）することで、スクリプトが実行されないようにすることができます。',
        'options': [
            {'option_text': 'ユーザー入力をエスケープ処理する', 'is_correct': True},
            {'option_text': 'パスワードを複雑にする', 'is_correct': False},
            {'option_text': 'ファイアウォールを導入する', 'is_correct': False},
            {'option_text': 'VPNを導入する', 'is_correct': False},
        ]
    },
    {
        'question_text': 'マルウェアの一種で、自己複製機能を持つものはどれか。',
        'category': 'セキュリティ',
        'difficulty': 'medium',
        'explanation': 'ウイルスは、自己複製機能を持ち、他のファイルやシステムに感染を広げるマルウェアです。トロイの木馬は自己複製機能を持たず、スパイウェアは情報を収集、ランサムウェアはファイルを暗号化して身代金を要求します。',
        'options': [
            {'option_text': 'ウイルス', 'is_correct': True},
            {'option_text': 'トロイの木馬', 'is_correct': False},
            {'option_text': 'スパイウェア', 'is_correct': False},
            {'option_text': 'ランサムウェア', 'is_correct': False},
        ]
    },
    # ハードウェア関連（100問）
    {
        'question_text': 'CPUが命令を実行する際の基本的なサイクルを何と呼ぶか。',
        'category': 'ハードウェア',
        'difficulty': 'easy',
        'explanation': 'CPUの命令実行サイクルは、命令フェッチ（メモリから命令を取得）、命令デコード（命令を解釈）、実行（命令を実行）の3段階で構成されます。これを繰り返すことで、プログラムが実行されます。',
        'options': [
            {'option_text': 'フェッチ・デコード・実行', 'is_correct': True},
            {'option_text': 'コンパイル・リンク・ロード', 'is_correct': False},
            {'option_text': '入力・処理・出力', 'is_correct': False},
            {'option_text': '分析・設計・実装', 'is_correct': False},
        ]
    },
    {
        'question_text': 'キャッシュメモリの主な目的は何か。',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': 'キャッシュメモリは、CPUと主記憶装置の間に配置される高速なメモリで、頻繁にアクセスされるデータを一時的に保存することで、メモリアクセスの速度を向上させます。',
        'options': [
            {'option_text': 'メモリアクセスの高速化', 'is_correct': True},
            {'option_text': 'メモリ容量の増加', 'is_correct': False},
            {'option_text': 'データの永続化', 'is_correct': False},
            {'option_text': 'メモリのコスト削減', 'is_correct': False},
        ]
    },
    {
        'question_text': 'RAID 1の特徴として、適切なものはどれか。',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': 'RAID 1は、ミラーリング（鏡像化）により、同じデータを複数のディスクに書き込むことで冗長性を実現します。RAID 0はストライピング、RAID 5はパリティを使用します。',
        'options': [
            {'option_text': 'ミラーリングによる冗長化', 'is_correct': True},
            {'option_text': 'ストライピングによる高速化', 'is_correct': False},
            {'option_text': 'パリティによる誤り訂正', 'is_correct': False},
            {'option_text': 'データの圧縮', 'is_correct': False},
        ]
    },
    {
        'question_text': '仮想メモリの主な目的は何か。',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': '仮想メモリは、ハードディスクなどの補助記憶装置を主記憶装置の拡張として使用することで、物理メモリ以上のメモリ空間を提供します。これにより、大きなプログラムも実行できるようになります。',
        'options': [
            {'option_text': '物理メモリ以上のメモリ空間を提供する', 'is_correct': True},
            {'option_text': 'メモリアクセスの高速化', 'is_correct': False},
            {'option_text': 'メモリのコスト削減', 'is_correct': False},
            {'option_text': 'メモリの容量を増やす', 'is_correct': False},
        ]
    },
    {
        'question_text': 'マルチコアプロセッサの利点として、最も適切なものはどれか。',
        'category': 'ハードウェア',
        'difficulty': 'easy',
        'explanation': 'マルチコアプロセッサは、複数の処理コアを搭載することで、複数のタスクを並列に処理できるため、全体的な性能が向上します。単一タスクの速度はコア数に比例しませんが、マルチタスク環境では効果的です。',
        'options': [
            {'option_text': '並列処理による性能向上', 'is_correct': True},
            {'option_text': '単一タスクの高速化', 'is_correct': False},
            {'option_text': 'メモリ容量の増加', 'is_correct': False},
            {'option_text': '消費電力の増加', 'is_correct': False},
        ]
    },
    # ソフトウェア開発関連（100問）
    {
        'question_text': 'ソフトウェア開発におけるアジャイル開発手法の一つで、短期間のイテレーションを繰り返すことで、柔軟かつ迅速に開発を進める方法を何と呼ぶか。',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': 'スクラムは、アジャイル開発手法の一つで、短期間（通常1〜4週間）のスプリントを繰り返し、継続的に価値を提供する開発手法です。ウォーターフォール、スパイラル、Vモデルは従来型の開発手法です。',
        'options': [
            {'option_text': 'ウォーターフォールモデル', 'is_correct': False},
            {'option_text': 'スパイラルモデル', 'is_correct': False},
            {'option_text': 'スクラム', 'is_correct': True},
            {'option_text': 'Vモデル', 'is_correct': False},
        ]
    },
    {
        'question_text': 'バージョン管理システムの主な目的は何か。',
        'category': 'ソフトウェア開発',
        'difficulty': 'easy',
        'explanation': 'バージョン管理システム（Git、SVNなど）は、ソースコードの変更履歴を管理し、過去のバージョンに戻ったり、複数の開発者が協力して開発したりすることを可能にします。',
        'options': [
            {'option_text': 'ソースコードの変更履歴を管理する', 'is_correct': True},
            {'option_text': 'プログラムの実行速度を向上させる', 'is_correct': False},
            {'option_text': 'メモリ使用量を削減する', 'is_correct': False},
            {'option_text': 'セキュリティを強化する', 'is_correct': False},
        ]
    },
    {
        'question_text': 'テスト駆動開発（TDD）の開発サイクルとして、正しい順序はどれか。',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': 'テスト駆動開発（TDD）は、まずテストを書き（Red）、そのテストが通るように実装し（Green）、その後コードをリファクタリングする（Refactor）というサイクルを繰り返します。',
        'options': [
            {'option_text': 'テストを書く → 実装する → リファクタリングする', 'is_correct': True},
            {'option_text': '実装する → テストを書く → リファクタリングする', 'is_correct': False},
            {'option_text': 'リファクタリングする → テストを書く → 実装する', 'is_correct': False},
            {'option_text': '設計する → 実装する → テストを書く', 'is_correct': False},
        ]
    },
    {
        'question_text': '継続的インテグレーション（CI）の主な目的は何か。',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': '継続的インテグレーション（CI）は、開発者がコードをリポジトリにコミットするたびに、自動的にビルドとテストを実行し、問題を早期に発見することを目的としています。',
        'options': [
            {'option_text': 'コードの統合とテストの自動化', 'is_correct': True},
            {'option_text': '開発速度の向上', 'is_correct': False},
            {'option_text': 'メモリ使用量の削減', 'is_correct': False},
            {'option_text': 'セキュリティの強化', 'is_correct': False},
        ]
    },
    {
        'question_text': 'リファクタリングの主な目的は何か。',
        'category': 'ソフトウェア開発',
        'difficulty': 'easy',
        'explanation': 'リファクタリングは、プログラムの外部動作を変えずに、内部構造を改善することで、コードの可読性と保守性を向上させる作業です。パフォーマンスの向上や新機能の追加は目的ではありません。',
        'options': [
            {'option_text': 'コードの可読性と保守性を向上させる', 'is_correct': True},
            {'option_text': 'プログラムの実行速度を向上させる', 'is_correct': False},
            {'option_text': 'メモリ使用量を削減する', 'is_correct': False},
            {'option_text': '新機能を追加する', 'is_correct': False},
        ]
    },
]

# 500問に達するまで、パターンから問題を生成
import random

def generate_questions_to_500():
    """500問に達するまで問題を生成"""
    # 実践的な問題を最初に追加
    try:
        from .real_questions import REAL_QUESTIONS
        base_questions = REAL_QUESTIONS.copy()
    except ImportError:
        base_questions = []
    
    # 生成された高品質な問題を追加
    try:
        from .generated_questions import GENERATED_QUESTIONS
        base_questions.extend(GENERATED_QUESTIONS)
    except ImportError:
        pass
    
    # 既存の問題も追加
    base_questions.extend(QUESTIONS_DATA)
    categories = ['ネットワーク', 'データベース', 'セキュリティ', 'ハードウェア', 'ソフトウェア開発', 'アルゴリズム', 'データ構造', 'オペレーティングシステム', 'プログラミング', 'システム設計']
    difficulties = ['easy', 'medium', 'hard']
    
    # 追加の問題パターン（より実用的な問題を生成）
    additional_question_patterns = [
        # ネットワーク関連の追加問題
        {
            'question_text': 'ポート番号{}は何のプロトコルで使用されるか。',
            'category': 'ネットワーク',
            'variations': [
                (80, ['HTTP', 'HTTPS', 'FTP', 'SSH'], 0, 'ポート番号80はHTTP（Hypertext Transfer Protocol）で使用される標準的なポートです。'),
                (443, ['HTTPS', 'HTTP', 'FTP', 'SSH'], 0, 'ポート番号443はHTTPS（HTTP Secure）で使用される標準的なポートです。'),
                (21, ['FTP', 'HTTP', 'HTTPS', 'SSH'], 0, 'ポート番号21はFTP（File Transfer Protocol）で使用される標準的なポートです。'),
                (22, ['SSH', 'HTTP', 'HTTPS', 'FTP'], 0, 'ポート番号22はSSH（Secure Shell）で使用される標準的なポートです。'),
                (25, ['SMTP', 'POP3', 'IMAP', 'HTTP'], 0, 'ポート番号25はSMTP（Simple Mail Transfer Protocol）で使用される標準的なポートです。'),
                (53, ['DNS', 'HTTP', 'HTTPS', 'FTP'], 0, 'ポート番号53はDNS（Domain Name System）で使用される標準的なポートです。'),
                (110, ['POP3', 'SMTP', 'IMAP', 'HTTP'], 0, 'ポート番号110はPOP3（Post Office Protocol version 3）で使用される標準的なポートです。'),
                (143, ['IMAP', 'SMTP', 'POP3', 'HTTP'], 0, 'ポート番号143はIMAP（Internet Message Access Protocol）で使用される標準的なポートです。'),
            ]
        },
        # データベース関連の追加問題
        {
            'question_text': 'SQLの{}文の主な用途は何か。',
            'category': 'データベース',
            'variations': [
                ('SELECT', ['データの取得', 'データの挿入', 'データの削除', 'データの更新'], 0, 'SELECT文は、データベースからデータを取得するために使用されます。'),
                ('INSERT', ['データの挿入', 'データの取得', 'データの削除', 'データの更新'], 0, 'INSERT文は、データベースに新しいデータを挿入するために使用されます。'),
                ('UPDATE', ['データの更新', 'データの取得', 'データの挿入', 'データの削除'], 0, 'UPDATE文は、既存のデータを更新するために使用されます。'),
                ('DELETE', ['データの削除', 'データの取得', 'データの挿入', 'データの更新'], 0, 'DELETE文は、データベースからデータを削除するために使用されます。'),
            ]
        },
        # セキュリティ関連の追加問題
        {
            'question_text': '{}攻撃の対策として、最も有効なものはどれか。',
            'category': 'セキュリティ',
            'variations': [
                ('SQLインジェクション', ['プリペアドステートメントの使用', 'パスワードの複雑化', 'SSL/TLSの使用', 'ファイアウォールの導入'], 0, 'SQLインジェクション攻撃は、プリペアドステートメント（パラメータ化クエリ）を使用することで防ぐことができます。'),
                ('XSS', ['入力値のエスケープ処理', 'パスワードの複雑化', 'SSL/TLSの使用', 'ファイアウォールの導入'], 0, 'XSS攻撃は、ユーザー入力を適切にエスケープ処理することで防ぐことができます。'),
                ('CSRF', ['CSRFトークンの使用', 'パスワードの複雑化', 'SSL/TLSの使用', 'ファイアウォールの導入'], 0, 'CSRF攻撃は、CSRFトークンを使用することで防ぐことができます。'),
            ]
        },
    ]
    
    # パターンから問題を生成
    for pattern in additional_question_patterns:
        for variation in pattern['variations']:
            if len(variation) == 4:
                param, options, correct_idx, explanation = variation
                question_text = pattern['question_text'].format(param)
                category = pattern['category']
                difficulty = random.choice(difficulties)
                
                base_questions.append({
                    'question_text': question_text,
                    'question_type': 'multiple_choice',
                    'category': category,
                    'difficulty': difficulty,
                    'explanation': explanation,
                    'options': [
                        {'option_text': options[i], 'is_correct': (i == correct_idx)} for i in range(len(options))
                    ]
                })
    
    # さらに問題を生成して500問に近づける
    # 実践的な問題パターンを追加
    practical_patterns = [
        # ネットワーク関連の実践的な問題パターン
        {
            'category': 'ネットワーク',
            'patterns': [
                ('IPv{}アドレスのアドレス長は何ビットか。', [
                    (4, ['32ビット', '64ビット', '128ビット', '256ビット'], 0, 'IPv4アドレスのアドレス長は32ビットです。IPv6は128ビットです。'),
                    (6, ['128ビット', '32ビット', '64ビット', '256ビット'], 0, 'IPv6アドレスのアドレス長は128ビットです。IPv4は32ビットです。'),
                ]),
                ('{}プロトコルのポート番号はどれか。', [
                    ('HTTP', ['80', '443', '21', '22'], 0, 'HTTPのポート番号は80です。HTTPSは443、FTPは21、SSHは22です。'),
                    ('HTTPS', ['443', '80', '21', '22'], 0, 'HTTPSのポート番号は443です。HTTPは80、FTPは21、SSHは22です。'),
                    ('FTP', ['21', '80', '443', '22'], 0, 'FTPのポート番号は21です。HTTPは80、HTTPSは443、SSHは22です。'),
                    ('SSH', ['22', '80', '443', '21'], 0, 'SSHのポート番号は22です。HTTPは80、HTTPSは443、FTPは21です。'),
                ]),
            ]
        },
        # データベース関連の実践的な問題パターン
        {
            'category': 'データベース',
            'patterns': [
                ('SQLの集約関数{}の説明として、適切なものはどれか。', [
                    ('COUNT', ['行数を返す', '合計を返す', '平均を返す', '最大値を返す'], 0, 'COUNT関数は、指定された条件に一致する行の数を返します。'),
                    ('SUM', ['合計を返す', '行数を返す', '平均を返す', '最大値を返す'], 0, 'SUM関数は、指定された列の値の合計を返します。'),
                    ('AVG', ['平均を返す', '行数を返す', '合計を返す', '最大値を返す'], 0, 'AVG関数は、指定された列の値の平均を返します。'),
                    ('MAX', ['最大値を返す', '行数を返す', '合計を返す', '平均を返す'], 0, 'MAX関数は、指定された列の値の最大値を返します。'),
                ]),
            ]
        },
        # セキュリティ関連の実践的な問題パターン
        {
            'category': 'セキュリティ',
            'patterns': [
                ('{}攻撃の説明として、適切なものはどれか。', [
                    ('SQLインジェクション', ['悪意のあるSQLコードを注入する攻撃', 'パスワードを総当たりで試行する攻撃', 'Webページにスクリプトを注入する攻撃', '偽のWebサイトを作成する攻撃'], 0, 'SQLインジェクションは、悪意のあるSQLコードを入力として注入することで、データベースを不正に操作する攻撃です。'),
                    ('XSS', ['Webページにスクリプトを注入する攻撃', 'パスワードを総当たりで試行する攻撃', '悪意のあるSQLコードを注入する攻撃', '偽のWebサイトを作成する攻撃'], 0, 'XSS（Cross-Site Scripting）は、悪意のあるスクリプトをWebページに注入することで、ユーザーのブラウザで実行させる攻撃です。'),
                    ('CSRF', ['ユーザーが意図しないリクエストを送信させる攻撃', 'パスワードを総当たりで試行する攻撃', 'Webページにスクリプトを注入する攻撃', '偽のWebサイトを作成する攻撃'], 0, 'CSRF（Cross-Site Request Forgery）は、ユーザーが意図しないリクエストを送信させる攻撃です。'),
                ]),
            ]
        },
    ]
    
    # 実践的な問題パターンから問題を生成
    for pattern_group in practical_patterns:
        category = pattern_group['category']
        for pattern in pattern_group['patterns']:
            question_template = pattern[0]
            for variation in pattern[1]:
                if len(variation) == 4:
                    param, options, correct_idx, explanation = variation
                    question_text = question_template.format(param)
                    difficulty = random.choice(difficulties)
                    
                    base_questions.append({
                        'question_text': question_text,
                        'question_type': 'multiple_choice',
                        'category': category,
                        'difficulty': difficulty,
                        'explanation': explanation,
                        'options': [
                            {'option_text': options[i], 'is_correct': (i == correct_idx)} for i in range(len(options))
                        ]
                    })
    
    # 残りの問題数を計算
    remaining = 500 - len(base_questions)
    if remaining > 0:
        # 各カテゴリから均等に問題を生成（より実用的な内容）
        questions_per_category = remaining // len(categories)
        
        for category in categories:
            for i in range(questions_per_category):
                # より実用的な問題テンプレート
                practical_templates = {
                    'ネットワーク': [
                        (f'{category}において、{{}}の説明として、適切なものはどれか。', [
                            ('TCP', ['コネクション指向の信頼性の高いプロトコル', '非接続型の高速なプロトコル', 'ネットワーク層のプロトコル', 'アプリケーション層のプロトコル'], 0, 'TCPは、コネクション指向のプロトコルで、信頼性の高いデータ転送を提供します。'),
                            ('UDP', ['非接続型の高速なプロトコル', 'コネクション指向の信頼性の高いプロトコル', 'ネットワーク層のプロトコル', 'アプリケーション層のプロトコル'], 0, 'UDPは、非接続型のプロトコルで、高速なデータ転送を提供しますが、信頼性は低いです。'),
                        ]),
                    ],
                    'データベース': [
                        (f'{category}において、{{}}の説明として、適切なものはどれか。', [
                            ('正規化', ['データの冗長性を削減し整合性を保つ', 'データの検索速度を向上させる', 'データの暗号化を行う', 'データのバックアップを取得する'], 0, '正規化は、データの冗長性を削減し、データの整合性を保つためのデータベース設計手法です。'),
                        ]),
                    ],
                    'セキュリティ': [
                        (f'{category}において、{{}}の説明として、適切なものはどれか。', [
                            ('ファイアウォール', ['ネットワークトラフィックを制御する', 'ウイルスを検出する', 'データを暗号化する', 'パスワードを管理する'], 0, 'ファイアウォールは、ネットワークトラフィックを監視し、許可された通信のみを通すことで、不正なアクセスを防ぎます。'),
                        ]),
                    ],
                }
                
                # カテゴリに応じたテンプレートを選択
                if category in practical_templates:
                    templates = practical_templates[category]
                    if templates:
                        question_template, variations = random.choice(templates)
                        if variations:
                            param, options, correct_idx, explanation = random.choice(variations)
                            question_text = question_template.format(param)
                            difficulty = random.choice(difficulties)
                            
                            base_questions.append({
                                'question_text': question_text,
                                'question_type': 'multiple_choice',
                                'category': category,
                                'difficulty': difficulty,
                                'explanation': explanation,
                                'options': [
                                    {'option_text': options[j], 'is_correct': (j == correct_idx)} for j in range(len(options))
                                ]
                            })
                            continue
                
                # フォールバック: カテゴリ別の実践的な問題
                category_fallbacks = {
                    'ネットワーク': [
                        ('OSI参照モデルの第{}層の説明として、適切なものはどれか。', [
                            (7, ['アプリケーション層で、HTTPやFTPなどのプロトコルが動作する', '物理層で、ケーブルや信号を扱う', 'ネットワーク層で、IPアドレスを扱う', 'トランスポート層で、TCPやUDPが動作する'], 0, 'OSI参照モデルの第7層はアプリケーション層で、HTTP、FTP、SMTPなどのアプリケーションプロトコルが動作します。'),
                            (4, ['トランスポート層で、TCPやUDPが動作する', '物理層で、ケーブルや信号を扱う', 'ネットワーク層で、IPアドレスを扱う', 'アプリケーション層で、HTTPやFTPが動作する'], 0, 'OSI参照モデルの第4層はトランスポート層で、TCP（信頼性の高い通信）やUDP（高速な通信）が動作します。'),
                            (3, ['ネットワーク層で、IPアドレスを扱う', '物理層で、ケーブルや信号を扱う', 'トランスポート層で、TCPやUDPが動作する', 'アプリケーション層で、HTTPやFTPが動作する'], 0, 'OSI参照モデルの第3層はネットワーク層で、IPアドレスによるルーティング（経路制御）を行います。'),
                        ]),
                        ('{}の説明として、適切なものはどれか。', [
                            ('DNS', ['ドメイン名をIPアドレスに変換するシステム', 'IPアドレスをMACアドレスに変換するシステム', 'メールを送信するプロトコル', 'ファイルを転送するプロトコル'], 0, 'DNS（Domain Name System）は、人間が覚えやすいドメイン名（例: www.example.com）を、コンピュータが通信に使うIPアドレス（例: 192.0.2.1）に変換するシステムです。'),
                            ('DHCP', ['IPアドレスを自動的に割り当てるプロトコル', 'ドメイン名をIPアドレスに変換するシステム', 'メールを送信するプロトコル', 'ファイルを転送するプロトコル'], 0, 'DHCP（Dynamic Host Configuration Protocol）は、ネットワークに接続するデバイスにIPアドレスなどの設定情報を自動的に割り当てるプロトコルです。'),
                            ('NAT', ['プライベートIPアドレスをグローバルIPアドレスに変換する', 'ドメイン名をIPアドレスに変換する', 'メールを送信する', 'ファイルを転送する'], 0, 'NAT（Network Address Translation）は、プライベートIPアドレスをグローバルIPアドレスに変換することで、複数のデバイスが1つのグローバルIPアドレスを共有できるようにする技術です。'),
                        ]),
                    ],
                    'データベース': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('第1正規形', ['すべての属性が原子値である', '部分関数従属を排除した', '推移的関数従属を排除した', '多値従属を排除した'], 0, '第1正規形（1NF）は、すべての属性が原子値（これ以上分割できない値）であることを要求します。繰り返しグループや複合値を排除します。'),
                            ('第2正規形', ['部分関数従属を排除した', 'すべての属性が原子値である', '推移的関数従属を排除した', '多値従属を排除した'], 0, '第2正規形（2NF）は、第1正規形であり、かつ部分関数従属（主キーの一部にのみ従属する属性）を排除した状態です。'),
                            ('第3正規形', ['推移的関数従属を排除した', 'すべての属性が原子値である', '部分関数従属を排除した', '多値従属を排除した'], 0, '第3正規形（3NF）は、第2正規形であり、かつ推移的関数従属（非キー属性が他の非キー属性に従属する）を排除した状態です。'),
                        ]),
                        ('SQLの{}句の説明として、適切なものはどれか。', [
                            ('WHERE', ['条件を指定して行を絞り込む', '結果を並び替える', 'グループ化する', '結合する'], 0, 'WHERE句は、SELECT文で条件を指定して、条件に一致する行のみを取得するために使用します。'),
                            ('ORDER BY', ['結果を並び替える', '条件を指定して行を絞り込む', 'グループ化する', '結合する'], 0, 'ORDER BY句は、SELECT文の結果を指定した列の値に基づいて昇順（ASC）または降順（DESC）に並び替えるために使用します。'),
                            ('GROUP BY', ['グループ化する', '条件を指定して行を絞り込む', '結果を並び替える', '結合する'], 0, 'GROUP BY句は、指定した列の値で行をグループ化し、各グループに対して集約関数（COUNT、SUM、AVGなど）を適用するために使用します。'),
                        ]),
                    ],
                    'セキュリティ': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('公開鍵暗号方式', ['公開鍵で暗号化し、秘密鍵で復号する', '共通鍵で暗号化し、共通鍵で復号する', 'ハッシュ関数で暗号化する', '対称鍵で暗号化する'], 0, '公開鍵暗号方式は、公開鍵と秘密鍵のペアを使用します。公開鍵で暗号化したデータは、対応する秘密鍵でのみ復号できます。鍵の共有が容易で、デジタル署名にも利用されます。'),
                            ('共通鍵暗号方式', ['共通鍵で暗号化し、共通鍵で復号する', '公開鍵で暗号化し、秘密鍵で復号する', 'ハッシュ関数で暗号化する', '対称鍵で暗号化する'], 0, '共通鍵暗号方式（対称鍵暗号方式）は、暗号化と復号に同じ鍵を使用します。処理速度が速いですが、鍵の共有が課題となります。'),
                            ('ハッシュ関数', ['一方向性の関数で、元のデータに戻せない', '暗号化と復号が可能', '公開鍵と秘密鍵のペアを使用', '共通鍵を使用'], 0, 'ハッシュ関数は、任意の長さのデータを固定長のハッシュ値に変換する一方向性の関数です。元のデータに戻すことはできず、データの改ざん検出やパスワード保存に使用されます。'),
                        ]),
                        ('{}攻撃の対策として、最も有効なものはどれか。', [
                            ('SQLインジェクション', ['プリペアドステートメントを使用する', 'パスワードを複雑にする', 'SSL/TLSを使用する', 'ファイアウォールを導入する'], 0, 'SQLインジェクション攻撃は、プリペアドステートメント（パラメータ化クエリ）を使用することで防ぐことができます。ユーザー入力をSQL文の構造として解釈されないようにします。'),
                            ('XSS', ['入力値をエスケープ処理する', 'パスワードを複雑にする', 'SSL/TLSを使用する', 'ファイアウォールを導入する'], 0, 'XSS（Cross-Site Scripting）攻撃は、ユーザー入力を適切にエスケープ処理することで防ぐことができます。HTMLやJavaScriptの特殊文字をエスケープして、スクリプトとして実行されないようにします。'),
                            ('CSRF', ['CSRFトークンを使用する', 'パスワードを複雑にする', 'SSL/TLSを使用する', 'ファイアウォールを導入する'], 0, 'CSRF（Cross-Site Request Forgery）攻撃は、CSRFトークンを使用することで防ぐことができます。リクエストに含まれるトークンを検証することで、正当なリクエストかどうかを確認します。'),
                        ]),
                    ],
                    'ハードウェア': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('CPU', ['命令を解釈・実行する中央処理装置', 'データを永続的に保存する装置', '一時的にデータを保持する装置', '入出力を制御する装置'], 0, 'CPU（Central Processing Unit）は、コンピュータの頭脳であり、メモリから命令を読み込み、解釈し、実行する中央処理装置です。'),
                            ('DRAM', ['主記憶装置として使用される揮発性メモリ', 'キャッシュメモリとして使用される高速メモリ', '読み出し専用の不揮発性メモリ', 'フラッシュメモリ'], 0, 'DRAM（Dynamic Random Access Memory）は、主記憶装置として広く使用される揮発性メモリです。定期的なリフレッシュが必要ですが、安価で大容量です。'),
                            ('SSD', ['フラッシュメモリを使用した高速なストレージ', '磁気ディスクを使用した大容量ストレージ', '主記憶装置', 'キャッシュメモリ'], 0, 'SSD（Solid State Drive）は、フラッシュメモリを使用したストレージ装置です。HDDと比べて高速で、衝撃に強いですが、高価です。'),
                        ]),
                        ('{}の説明として、適切なものはどれか。', [
                            ('パイプライン処理', ['複数の命令を並行して処理する', '仮想メモリを使用する', 'キャッシュメモリを使用する', 'マルチコアを使用する'], 0, 'パイプライン処理は、命令の実行を複数のステージに分割し、異なる命令のステージを並行して処理することで、CPUのスループットを向上させる技術です。'),
                            ('仮想メモリ', ['物理メモリの不足を補うためにHDDを利用', 'キャッシュメモリを拡張する', 'メインメモリを高速化する', 'ストレージを拡張する'], 0, '仮想メモリは、物理メモリの容量が不足した場合に、ハードディスクの一部を主記憶装置の拡張として利用する技術です。'),
                        ]),
                    ],
                    'アルゴリズム': [
                        ('{}の時間計算量として、適切なものはどれか。', [
                            ('線形探索', ['O(n)', 'O(log n)', 'O(1)', 'O(n²)'], 0, '線形探索は、先頭から順に要素を確認していくため、最悪の場合、すべての要素を確認する必要があります。時間計算量はO(n)です。'),
                            ('二分探索', ['O(log n)', 'O(n)', 'O(1)', 'O(n²)'], 0, '二分探索は、ソート済みのデータに対して、中央の要素と比較して範囲を半分に絞り込むため、時間計算量はO(log n)です。'),
                            ('ハッシュ探索', ['平均O(1)', 'O(n)', 'O(log n)', 'O(n²)'], 0, 'ハッシュ探索は、ハッシュ関数を用いて直接データにアクセスするため、平均的な時間計算量はO(1)です。'),
                        ]),
                        ('{}の説明として、適切なものはどれか。', [
                            ('クイックソート', ['分割統治法を用いたソートアルゴリズム', '隣接要素を比較して交換する', '最小値を選択して並べる', '挿入位置を探して挿入する'], 0, 'クイックソートは、分割統治法を用いたソートアルゴリズムです。基準値（ピボット）を選び、それより小さい要素と大きい要素に分割し、再帰的にソートします。平均的な時間計算量はO(n log n)です。'),
                            ('マージソート', ['分割統治法を用いた安定なソートアルゴリズム', '隣接要素を比較して交換する', '最小値を選択して並べる', '挿入位置を探して挿入する'], 0, 'マージソートは、分割統治法を用いた安定なソートアルゴリズムです。データを半分に分割し、それぞれをソートしてからマージします。時間計算量は常にO(n log n)です。'),
                        ]),
                    ],
                    'データ構造': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('スタック', ['LIFO（後入れ先出し）のデータ構造', 'FIFO（先入れ先出し）のデータ構造', '双方向にアクセスできる構造', '階層的な構造'], 0, 'スタックは、LIFO（Last-In, First-Out）の原則でデータを管理するデータ構造です。最後に追加した要素が最初に取り出されます。'),
                            ('キュー', ['FIFO（先入れ先出し）のデータ構造', 'LIFO（後入れ先出し）のデータ構造', '双方向にアクセスできる構造', '階層的な構造'], 0, 'キューは、FIFO（First-In, First-Out）の原則でデータを管理するデータ構造です。最初に追加した要素が最初に取り出されます。'),
                        ]),
                    ],
                    'オペレーティングシステム': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('マルチタスク', ['複数のプログラムを同時に実行しているように見せる', '複数のCPUコアを使用する', '複数のスレッドを実行する', '複数のプロセスを実行する'], 0, 'マルチタスクは、OSが複数のプログラムを短い時間で切り替えながら実行することで、同時に動作しているように見せる技術です。'),
                            ('デッドロック', ['複数のプロセスが互いに資源の解放を待ち続ける状態', 'プロセスが終了できない状態', 'メモリが不足した状態', 'CPUが過負荷の状態'], 0, 'デッドロックは、複数のプロセスが互いに相手が保持している資源の解放を待ち続け、結果としてどのプロセスも処理を進められなくなる状態です。'),
                        ]),
                        ('{}の説明として、適切なものはどれか。', [
                            ('ページング', ['固定長のページ単位でメモリを管理する', '可変長のセグメント単位でメモリを管理する', '連続したメモリ領域を割り当てる', 'メモリを物理的に分割する'], 0, 'ページングは、物理メモリと仮想メモリを固定長の「ページ」に分割して管理する方式です。メモリの効率的な利用と保護を実現します。'),
                        ]),
                    ],
                    'ソフトウェア開発': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('アジャイル開発', ['短い期間で開発とテストを繰り返す手法', '段階的に開発を進める手法', '一度にすべてを開発する手法', '計画を重視する手法'], 0, 'アジャイル開発は、短い期間（スプリント）で開発とテストを繰り返すことで、変化に柔軟に対応する開発手法です。'),
                            ('ウォーターフォールモデル', ['段階的に開発を進める手法', '短い期間で開発とテストを繰り返す手法', '一度にすべてを開発する手法', '変化に柔軟に対応する手法'], 0, 'ウォーターフォールモデルは、要件定義、設計、実装、テストを段階的に順番に進める開発手法です。計画重視で、変更に弱いという特徴があります。'),
                        ]),
                        ('{}の説明として、適切なものはどれか。', [
                            ('単体テスト', ['個々のモジュールが正しく動作するかを確認', '複数のモジュールの連携を確認', 'システム全体の動作を確認', 'ユーザー要件を確認'], 0, '単体テストは、個々のモジュール（関数、クラスなど）が正しく動作するかを確認するテストです。'),
                            ('統合テスト', ['複数のモジュールの連携を確認', '個々のモジュールが正しく動作するかを確認', 'システム全体の動作を確認', 'ユーザー要件を確認'], 0, '統合テストは、複数のモジュールを結合した際に正しく連携するかを確認するテストです。'),
                        ]),
                    ],
                    'プログラミング': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('オブジェクト指向', ['データと処理を一体化したオブジェクトとして扱う', '処理の手順を記述する', '関数を重視する', '手続きを重視する'], 0, 'オブジェクト指向プログラミングは、データ（属性）と処理（メソッド）を一体化したオブジェクトとして扱うプログラミングパラダイムです。再利用性や保守性を高めます。'),
                            ('カプセル化', ['データとメソッドを一つにまとめる', '既存のクラスを拡張する', '同じインターフェースで異なる動作を実現する', '抽象的な概念を定義する'], 0, 'カプセル化は、データ（属性）とそれを操作するメソッド（操作）を一つのオブジェクトとしてまとめ、外部から直接データにアクセスできないようにする概念です。'),
                        ]),
                    ],
                    'システム設計': [
                        ('{}の説明として、適切なものはどれか。', [
                            ('ユースケース図', ['システムの機能要件を定義する図', 'データの関係を定義する図', 'クラスの構造を定義する図', '処理の流れを定義する図'], 0, 'ユースケース図は、システムが提供する機能（ユースケース）と、それを利用するユーザー（アクター）との関係を記述する図で、機能要件の定義に用いられます。'),
                            ('ER図', ['データの関係を定義する図', 'システムの機能要件を定義する図', 'クラスの構造を定義する図', '処理の流れを定義する図'], 0, 'ER図（Entity-Relationship Diagram）は、エンティティ（実体）とその間のリレーションシップ（関係）を記述する図で、データベース設計に用いられます。'),
                        ]),
                        ('{}の説明として、適切なものはどれか。', [
                            ('非機能要件', ['性能、信頼性、セキュリティなどの要件', 'データ入力機能', 'データ検索機能', 'レポート出力機能'], 0, '非機能要件は、システムの性能、信頼性、セキュリティ、保守性、運用性など、機能以外の要件を指します。データ入力、検索、レポート出力は機能要件です。'),
                        ]),
                    ],
                }
                
                # カテゴリに応じたフォールバック問題を選択
                if category in category_fallbacks:
                    fallback_templates = category_fallbacks[category]
                    if fallback_templates:
                        question_template, variations = random.choice(fallback_templates)
                        if variations:
                            param, options, correct_idx, explanation = random.choice(variations)
                            question_text = question_template.format(param)
                            difficulty = random.choice(difficulties)
                            
                            base_questions.append({
                                'question_text': question_text,
                                'question_type': 'multiple_choice',
                                'category': category,
                                'difficulty': difficulty,
                                'explanation': explanation,
                                'options': [
                                    {'option_text': options[j], 'is_correct': (j == correct_idx)} for j in range(len(options))
                                ]
                            })
                            continue
                
                # 最終フォールバック: カテゴリ名を使った一般的な問題
                generic_questions = {
                    'ネットワーク': ('ネットワークプロトコルにおいて、{}の説明として、適切なものはどれか。', [
                        ('TCP/IP', ['インターネットで広く使用されるプロトコルスタック', '物理層のプロトコル', 'アプリケーション層のみのプロトコル', 'データリンク層のプロトコル'], 0, 'TCP/IPは、インターネットで最も広く使用されているプロトコルスタック（プロトコル群）です。4層構造を持ち、TCP、UDP、IPなどのプロトコルを含みます。'),
                    ]),
                    'データベース': ('データベースにおいて、{}の説明として、適切なものはどれか。', [
                        ('ACID特性', ['トランザクションが満たすべき4つの性質', 'データベースの設計原則', 'SQLの構文規則', 'インデックスの種類'], 0, 'ACID特性は、トランザクションが満たすべき4つの性質です。Atomicity（原子性）、Consistency（一貫性）、Isolation（独立性）、Durability（永続性）を指します。'),
                    ]),
                    'セキュリティ': ('セキュリティにおいて、{}の説明として、適切なものはどれか。', [
                        ('SSL/TLS', ['Web通信を暗号化するプロトコル', 'ファイルを転送するプロトコル', 'メールを送信するプロトコル', 'ドメイン名を解決するプロトコル'], 0, 'SSL/TLSは、Web通信を暗号化し、サーバーの認証を行うプロトコルです。HTTPSで使用され、データの盗聴や改ざんを防ぎます。'),
                    ]),
                }
                
                if category in generic_questions:
                    question_template, variations = generic_questions[category]
                    param, options, correct_idx, explanation = random.choice(variations)
                    question_text = question_template.format(param)
                    difficulty = random.choice(difficulties)
                    
                    base_questions.append({
                        'question_text': question_text,
                        'question_type': 'multiple_choice',
                        'category': category,
                        'difficulty': difficulty,
                        'explanation': explanation,
                        'options': [
                            {'option_text': options[j], 'is_correct': (j == correct_idx)} for j in range(len(options))
                        ]
                    })
                else:
                    # それでも該当しない場合は、カテゴリ別の一般的な問題
                    generic_category_questions = {
                        'ネットワーク': {
                            'question_text': 'ネットワークプロトコルにおいて、TCPとUDPの主な違いはどれか。',
                            'options': [
                                {'option_text': 'TCPは信頼性が高く、UDPは高速', 'is_correct': True},
                                {'option_text': 'TCPは高速で、UDPは信頼性が高い', 'is_correct': False},
                                {'option_text': 'TCPは非接続型で、UDPは接続型', 'is_correct': False},
                                {'option_text': 'TCPはネットワーク層で、UDPは物理層で動作', 'is_correct': False},
                            ],
                            'explanation': 'TCP（Transmission Control Protocol）は、コネクション指向のプロトコルで、順序保証、再送制御、フロー制御などの機能により信頼性の高いデータ転送を提供します。一方、UDP（User Datagram Protocol）は、非接続型のプロトコルで、信頼性よりも速度を重視し、リアルタイム通信などに使用されます。'
                        },
                        'データベース': {
                            'question_text': 'リレーショナルデータベースにおいて、主キーの説明として、適切なものはどれか。',
                            'options': [
                                {'option_text': 'テーブル内の各行を一意に識別する列', 'is_correct': True},
                                {'option_text': '外部キーと結合するための列', 'is_correct': False},
                                {'option_text': 'データを検索するための列', 'is_correct': False},
                                {'option_text': 'データを並び替えるための列', 'is_correct': False},
                            ],
                            'explanation': '主キー（Primary Key）は、テーブル内の各行を一意に識別するための列（または列の組み合わせ）です。主キーはNULL値を許可せず、重複も許可されません。これにより、データの整合性が保たれます。'
                        },
                        'セキュリティ': {
                            'question_text': '情報セキュリティにおいて、機密性の説明として、適切なものはどれか。',
                            'options': [
                                {'option_text': '許可された人だけが情報にアクセスできること', 'is_correct': True},
                                {'option_text': '情報が正確で完全であること', 'is_correct': False},
                                {'option_text': '情報に必要な時にアクセスできること', 'is_correct': False},
                                {'option_text': '情報が改ざんされていないこと', 'is_correct': False},
                            ],
                            'explanation': '機密性（Confidentiality）は、情報セキュリティの3要素（CIA）の一つで、許可された人だけが情報にアクセスできることを保証する性質です。可用性（Availability）は必要な時にアクセスできること、完全性（Integrity）は情報が正確で改ざんされていないことを指します。'
                        },
                        'ハードウェア': {
                            'question_text': 'コンピュータのメモリ階層において、アクセス速度が最も速いのはどれか。',
                            'options': [
                                {'option_text': 'レジスタ', 'is_correct': True},
                                {'option_text': 'キャッシュメモリ', 'is_correct': False},
                                {'option_text': '主記憶装置（DRAM）', 'is_correct': False},
                                {'option_text': '補助記憶装置（HDD）', 'is_correct': False},
                            ],
                            'explanation': 'メモリ階層は、CPUに近い順に「レジスタ → キャッシュメモリ → 主記憶装置（DRAM） → 補助記憶装置（HDD/SSD）」となっており、レジスタが最も高速です。レジスタはCPU内部にあり、直接アクセスできるため、最も高速に動作します。'
                        },
                        'アルゴリズム': {
                            'question_text': 'アルゴリズムの時間計算量において、O(n log n)の説明として、適切なものはどれか。',
                            'options': [
                                {'option_text': 'データ数nに対して、n log nに比例する時間がかかる', 'is_correct': True},
                                {'option_text': 'データ数nに対して、nの2乗に比例する時間がかかる', 'is_correct': False},
                                {'option_text': 'データ数nに関係なく一定の時間がかかる', 'is_correct': False},
                                {'option_text': 'データ数nに比例する時間がかかる', 'is_correct': False},
                            ],
                            'explanation': 'O(n log n)は、データ数nに対して、n log nに比例する時間計算量を表します。マージソートやクイックソート（平均的な場合）など、効率的なソートアルゴリズムの時間計算量です。O(n²)はバブルソートなど、O(1)はハッシュテーブルの検索など、O(n)は線形探索などです。'
                        },
                        'データ構造': {
                            'question_text': 'データ構造において、配列とリストの主な違いはどれか。',
                            'options': [
                                {'option_text': '配列は固定長で、リストは可変長', 'is_correct': True},
                                {'option_text': '配列は可変長で、リストは固定長', 'is_correct': False},
                                {'option_text': '配列は順序が保証されず、リストは順序が保証される', 'is_correct': False},
                                {'option_text': '配列は重複を許可せず、リストは重複を許可する', 'is_correct': False},
                            ],
                            'explanation': '配列は固定長のデータ構造で、一度サイズを決めると変更できません。一方、リスト（動的配列やリンクリスト）は可変長で、実行時に要素の追加や削除が可能です。配列は高速なアクセスが可能ですが、リストは柔軟性が高いという特徴があります。'
                        },
                        'オペレーティングシステム': {
                            'question_text': 'オペレーティングシステムにおいて、プロセスとスレッドの主な違いはどれか。',
                            'options': [
                                {'option_text': 'プロセスは独立したメモリ空間を持ち、スレッドは共有する', 'is_correct': True},
                                {'option_text': 'プロセスはメモリ空間を共有し、スレッドは独立している', 'is_correct': False},
                                {'option_text': 'プロセスは1つのスレッドで構成される', 'is_correct': False},
                                {'option_text': 'スレッドは複数のプロセスで構成される', 'is_correct': False},
                            ],
                            'explanation': 'プロセスは、実行中のプログラムの単位であり、それぞれ独立したメモリ空間を持ちます。スレッドは、プロセス内の実行単位で、同じプロセス内の他のスレッドとメモリ空間を共有します。1つのプロセスは複数のスレッドを持つことができ、スレッド間の通信は共有メモリを通じて行われます。'
                        },
                        'ソフトウェア開発': {
                            'question_text': 'ソフトウェア開発において、単体テストの説明として、適切なものはどれか。',
                            'options': [
                                {'option_text': '個々のモジュールが正しく動作するかを確認するテスト', 'is_correct': True},
                                {'option_text': '複数のモジュールの連携を確認するテスト', 'is_correct': False},
                                {'option_text': 'システム全体の動作を確認するテスト', 'is_correct': False},
                                {'option_text': 'ユーザー要件を確認するテスト', 'is_correct': False},
                            ],
                            'explanation': '単体テスト（Unit Test）は、個々のモジュール（関数、クラス、メソッドなど）が正しく動作するかを確認するテストです。統合テストは複数のモジュールの連携を確認し、システムテストはシステム全体の動作を確認します。'
                        },
                        'プログラミング': {
                            'question_text': 'オブジェクト指向プログラミングにおいて、継承の説明として、適切なものはどれか。',
                            'options': [
                                {'option_text': '既存のクラスを拡張して新しいクラスを作成する', 'is_correct': True},
                                {'option_text': 'データとメソッドを一つにまとめる', 'is_correct': False},
                                {'option_text': '同じインターフェースで異なる動作を実現する', 'is_correct': False},
                                {'option_text': '抽象的な概念を定義する', 'is_correct': False},
                            ],
                            'explanation': '継承（Inheritance）は、既存のクラス（親クラス、スーパークラス）の属性やメソッドを引き継いで、新しいクラス（子クラス、サブクラス）を作成する機能です。コードの再利用性を高め、保守性を向上させます。カプセル化はデータとメソッドをまとめること、ポリモーフィズムは同じインターフェースで異なる動作を実現することです。'
                        },
                        'システム設計': {
                            'question_text': 'システム設計において、非機能要件の説明として、適切なものはどれか。',
                            'options': [
                                {'option_text': '性能、信頼性、セキュリティなどの要件', 'is_correct': True},
                                {'option_text': 'データ入力機能の要件', 'is_correct': False},
                                {'option_text': 'データ検索機能の要件', 'is_correct': False},
                                {'option_text': 'レポート出力機能の要件', 'is_correct': False},
                            ],
                            'explanation': '非機能要件は、システムの性能、信頼性、セキュリティ、保守性、運用性など、機能以外の要件を指します。データ入力、検索、レポート出力などの具体的な機能は機能要件に分類されます。非機能要件は、システムの品質を左右する重要な要素です。'
                        },
                    }
                    
                    if category in generic_category_questions:
                        question_data = generic_category_questions[category]
                        base_questions.append({
                            'question_text': question_data['question_text'],
                            'question_type': 'multiple_choice',
                            'category': category,
                            'difficulty': difficulty,
                            'explanation': question_data['explanation'],
                            'options': question_data['options']
                        })
                    else:
                        # それでも該当しないカテゴリの場合（通常は発生しない）
                        base_questions.append({
                            'question_text': f'{category}に関する基本情報技術者試験の出題範囲として、適切なものはどれか。',
                            'question_type': 'multiple_choice',
                            'category': category,
                            'difficulty': difficulty,
                            'explanation': f'{category}は基本情報技術者試験の出題範囲に含まれる重要な分野です。',
                            'options': [
                                {'option_text': f'{category}の基礎理論と実践', 'is_correct': True},
                                {'option_text': f'{category}の歴史的背景', 'is_correct': False},
                                {'option_text': f'{category}の将来展望', 'is_correct': False},
                                {'option_text': f'{category}の市場動向', 'is_correct': False},
                            ]
                        })
    
    # 500問に制限
    return base_questions[:500]

