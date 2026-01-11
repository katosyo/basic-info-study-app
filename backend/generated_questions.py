# 生成された基本情報技術者試験の予想問題
# 実際の試験形式に準拠した高品質な問題

GENERATED_QUESTIONS = [
    # ネットワーク関連
    {
        'question_text': 'IPv4アドレス 192.168.1.100/24 が属するネットワークアドレスはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': '/24は、ネットワーク部が24ビット、ホスト部が8ビットであることを意味します。CIDR表記（Classless Inter-Domain Routing）では、スラッシュの後の数字がネットワーク部のビット数を示します。192.168.1.100を2進数で表すと11000000.10101000.00000001.01100100となり、最初の24ビット（11000000.10101000.00000001）がネットワーク部、最後の8ビット（01100100 = 100）がホスト部です。ネットワークアドレスは、ホスト部をすべて0にしたアドレス（192.168.1.0）となります。ブロードキャストアドレスは192.168.1.255（ホスト部をすべて1にしたアドレス）です。このネットワークでは、192.168.1.1から192.168.1.254までがホストとして使用可能です（合計254台）。',
        'options': [
            {'option_text': '192.168.1.0', 'is_correct': True},
            {'option_text': '192.168.0.0', 'is_correct': False},
            {'option_text': '192.168.1.100', 'is_correct': False},
            {'option_text': '192.168.1.255', 'is_correct': False},
        ]
    },
    {
        'question_text': 'TCP/IPネットワークにおいて、ポート番号80が使用されるプロトコルはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'easy',
        'explanation': 'ポート番号80はHTTP（HyperText Transfer Protocol）で使用される標準的なポート番号です。HTTPは、WebブラウザとWebサーバー間でHTMLなどのリソースを転送するために使用されるアプリケーション層のプロトコルです。よく使用されるポート番号の覚え方：HTTPは80、HTTPSは443（暗号化されたHTTP）、FTPは21（ファイル転送）、SSHは22（セキュアなリモートログイン）、SMTPは25（メール送信）、DNSは53（ドメイン名解決）、POP3は110（メール受信）、IMAPは143（メール受信）です。ポート番号は0〜65535の範囲で、0〜1023はWell-Known Ports（よく知られたポート）としてIANA（Internet Assigned Numbers Authority）によって管理されています。',
        'options': [
            {'option_text': 'HTTP', 'is_correct': True},
            {'option_text': 'HTTPS', 'is_correct': False},
            {'option_text': 'FTP', 'is_correct': False},
            {'option_text': 'SSH', 'is_correct': False},
        ]
    },
    {
        'question_text': 'OSI参照モデルの第4層（トランスポート層）の主な機能はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': 'トランスポート層（第4層）は、エンドツーエンドの通信制御を行い、信頼性のあるデータ転送を提供します。OSI参照モデルは7層構造で、第1層（物理層）から第7層（アプリケーション層）まであります。トランスポート層の主な役割は、送信元と宛先のアプリケーション間でのデータ転送を保証することです。TCP（Transmission Control Protocol）は、コネクション指向のプロトコルで、順序保証、再送制御、フロー制御、輻輳制御などの機能により、信頼性の高いデータ転送を実現します。一方、UDP（User Datagram Protocol）は非接続型で、高速転送を優先しますが、信頼性は低いです。ルーティング（経路制御）は第3層（ネットワーク層）の機能、データの暗号化は第6層（プレゼンテーション層）の機能、アプリケーション間の通信プロトコルは第7層（アプリケーション層）の機能です。',
        'options': [
            {'option_text': 'エンドツーエンドの通信制御と信頼性のあるデータ転送', 'is_correct': True},
            {'option_text': 'ネットワーク間のルーティング', 'is_correct': False},
            {'option_text': 'データの暗号化と復号化', 'is_correct': False},
            {'option_text': 'アプリケーション間の通信プロトコル', 'is_correct': False},
        ]
    },
    {
        'question_text': 'DNS（Domain Name System）のクエリタイプにおいて、ドメイン名からIPアドレスを取得するクエリはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': 'Aレコード（Address Record）は、ドメイン名をIPv4アドレスに変換するDNSレコードです。DNS（Domain Name System）は、人間が覚えやすいドメイン名（例：www.example.com）を、コンピュータが理解できるIPアドレス（例：192.0.2.1）に変換する分散データベースシステムです。Aレコードは最も基本的なDNSレコードで、IPv4アドレス（32ビット）を返します。AAAAレコードはIPv6アドレス（128ビット）を返すレコードです。MXレコード（Mail Exchange Record）は、そのドメインのメールサーバーのホスト名と優先度を指定します。CNAMEレコード（Canonical Name Record）は、別名（エイリアス）を正規のドメイン名に変換します。例えば、www.example.comをexample.comの別名として設定できます。その他、NSレコード（ネームサーバー）、PTRレコード（逆引き）、TXTレコード（テキスト情報）などがあります。',
        'options': [
            {'option_text': 'Aレコード', 'is_correct': True},
            {'option_text': 'AAAAレコード', 'is_correct': False},
            {'option_text': 'MXレコード', 'is_correct': False},
            {'option_text': 'CNAMEレコード', 'is_correct': False},
        ]
    },
    {
        'question_text': '無線LAN規格IEEE 802.11nの最大伝送速度はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'hard',
        'explanation': 'IEEE 802.11n（Wi-Fi 4）の最大伝送速度は約600Mbpsです。これは、MIMO（Multiple Input Multiple Output）技術とチャネルボンディング（複数のチャネルを結合）により実現されます。MIMOは、複数のアンテナを使用して同時に複数のデータストリームを送受信することで、伝送速度を向上させる技術です。802.11nは2.4GHz帯と5GHz帯の両方を使用でき、最大4ストリームのMIMOをサポートします。無線LAN規格の変遷：802.11a（最大54Mbps、5GHz帯）、802.11b（最大11Mbps、2.4GHz帯）、802.11g（最大54Mbps、2.4GHz帯）、802.11n（最大600Mbps、2.4/5GHz帯）、802.11ac（Wi-Fi 5、最大約6.9Gbps、5GHz帯）、802.11ax（Wi-Fi 6、最大約9.6Gbps、2.4/5GHz帯）です。実際の通信速度は、理論値より低くなることが多く、距離、障害物、干渉、接続機器数などの要因に影響されます。',
        'options': [
            {'option_text': '約600Mbps', 'is_correct': True},
            {'option_text': '約54Mbps', 'is_correct': False},
            {'option_text': '約6.9Gbps', 'is_correct': False},
            {'option_text': '約9.6Gbps', 'is_correct': False},
        ]
    },
    
    # データベース関連
    {
        'question_text': 'SQL文「SELECT * FROM employees WHERE department = \'IT\' ORDER BY salary DESC;」において、結果の並び順はどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'easy',
        'explanation': 'ORDER BY句でDESC（降順：Descending）を指定しているため、salary（給与）の高い順に並びます。SQL文の構造を理解することが重要です。SELECT句で取得する列を指定し、FROM句で対象テーブルを指定し、WHERE句で条件を指定し、ORDER BY句で並び順を指定します。DESCは降順（大きい順）、ASC（Ascending）は昇順（小さい順）で、デフォルトはASCです。このSQL文では、department（部署）が「IT」の従業員を抽出し、salary（給与）の高い順に並べ替えます。ORDER BY句では複数の列を指定でき、最初の列で同じ値の場合、次の列で並び替えます（例：ORDER BY department ASC, salary DESC）。また、列名の代わりに列の位置番号（例：ORDER BY 5 DESC）や式（例：ORDER BY salary * 1.1 DESC）も使用できます。',
        'options': [
            {'option_text': '給与の高い順', 'is_correct': True},
            {'option_text': '給与の低い順', 'is_correct': False},
            {'option_text': '入社日の古い順', 'is_correct': False},
            {'option_text': '名前のアルファベット順', 'is_correct': False},
        ]
    },
    {
        'question_text': 'リレーショナルデータベースにおいて、第2正規形（2NF）の条件はどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'hard',
        'explanation': '第2正規形（2NF）は、第1正規形を満たし、かつ部分関数従属を排除した状態です。正規化は、データベースの設計において、データの冗長性を排除し、整合性を保つための重要な手法です。第1正規形（1NF）は、すべての属性が原子値（これ以上分割できない値）であることを要求します。第2正規形（2NF）は、第1正規形を満たし、かつ部分関数従属を排除します。部分関数従属とは、複合主キーを持つテーブルで、非キー属性が主キーの一部にのみ従属している状態です。例えば、注文テーブルで（注文ID、商品ID）が主キーで、商品名が商品IDのみに従属している場合、部分関数従属が発生します。これを排除するには、商品情報を別テーブルに分離します。第3正規形（3NF）は、第2正規形を満たし、かつ推移的関数従属を排除します。推移的関数従属とは、非キー属性が他の非キー属性に従属している状態です。正規化により、データの更新時の不整合を防ぎ、ストレージ効率を向上させることができます。',
        'options': [
            {'option_text': '第1正規形を満たし、部分関数従属を排除する', 'is_correct': True},
            {'option_text': 'すべての属性が原子値である', 'is_correct': False},
            {'option_text': '第2正規形を満たし、推移的関数従属を排除する', 'is_correct': False},
            {'option_text': '主キーが存在する', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SQLの集約関数において、NULL値を除外して計算する関数はどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': 'COUNT(*)はNULLを含むすべての行をカウントしますが、COUNT(列名)はNULL値を除外してカウントします。SQLの集約関数は、複数の行から1つの値を計算する関数です。COUNT(*)は、条件に一致するすべての行をカウントし、NULL値の有無に関係なく行数を返します。一方、COUNT(列名)は、指定した列がNULLでない行のみをカウントします。例えば、10行のテーブルで3行がNULLの場合、COUNT(*)は10、COUNT(列名)は7を返します。SUM（合計）、AVG（平均）、MAX（最大値）、MIN（最小値）も、NULL値を除外して計算します。NULL値は「不明」や「存在しない」を表す特殊な値で、算術演算の結果もNULLになります。NULL値の扱いは、データベース設計において重要な考慮事項です。IS NULLやIS NOT NULLを使用してNULL値をチェックできます。',
        'options': [
            {'option_text': 'COUNT(列名)', 'is_correct': True},
            {'option_text': 'COUNT(*)', 'is_correct': False},
            {'option_text': 'SUM(*)', 'is_correct': False},
            {'option_text': 'AVG(*)', 'is_correct': False},
        ]
    },
    {
        'question_text': 'データベースのトランザクションにおいて、ACID特性の「I」は何を表すか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': 'ACID特性の「I」はIsolation（独立性、分離性）を表します。ACID特性は、データベースのトランザクション処理において、データの整合性を保証するための4つの重要な特性です。A（Atomicity：原子性）は、トランザクションがすべて実行されるか、すべて実行されないかのどちらかであることを保証します。途中でエラーが発生した場合、すべての変更がロールバックされます。C（Consistency：一貫性）は、トランザクションの前後でデータベースの整合性制約が満たされることを保証します。I（Isolation：独立性）は、複数のトランザクションが同時に実行されても、互いに影響を与えないことを保証します。これは、トランザクションの分離レベル（READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ、SERIALIZABLE）によって制御されます。D（Durability：永続性）は、トランザクションがコミットされた後、システム障害が発生しても変更が失われないことを保証します。これらの特性により、データベースの信頼性が確保されます。',
        'options': [
            {'option_text': 'Isolation（独立性）', 'is_correct': True},
            {'option_text': 'Integrity（整合性）', 'is_correct': False},
            {'option_text': 'Index（インデックス）', 'is_correct': False},
            {'option_text': 'Inheritance（継承）', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SQLのJOIN操作において、左外部結合（LEFT OUTER JOIN）の説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': 'LEFT OUTER JOINは、左側のテーブルのすべての行を保持し、右側のテーブルに一致する行がない場合はNULLを返します。SQLのJOIN操作は、複数のテーブルから関連するデータを結合して取得する操作です。INNER JOIN（内部結合）は、両方のテーブルに一致する行のみを返します。LEFT OUTER JOIN（左外部結合）は、左側のテーブルのすべての行を保持し、右側のテーブルに一致する行がない場合は、右側の列にNULLを返します。RIGHT OUTER JOIN（右外部結合）は、右側のテーブルのすべての行を保持し、左側のテーブルに一致する行がない場合は、左側の列にNULLを返します。FULL OUTER JOIN（完全外部結合）は、両方のテーブルのすべての行を保持し、一致しない場合はNULLを返します。LEFT OUTER JOINは、顧客テーブルと注文テーブルを結合して、注文がない顧客も含めて取得する場合などに使用されます。実務では、LEFT OUTER JOINが最もよく使用されます。',
        'options': [
            {'option_text': '左側のテーブルのすべての行を保持し、右側に一致がない場合はNULLを返す', 'is_correct': True},
            {'option_text': '両方のテーブルに一致する行のみを返す', 'is_correct': False},
            {'option_text': '右側のテーブルのすべての行を保持し、左側に一致がない場合はNULLを返す', 'is_correct': False},
            {'option_text': '両方のテーブルのすべての行を返す', 'is_correct': False},
        ]
    },
    
    # セキュリティ関連
    {
        'question_text': '公開鍵暗号方式において、RSA暗号の鍵長として、現在推奨される最小値はどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'hard',
        'explanation': 'RSA暗号の鍵長は、セキュリティ要件に応じて選択されます。現在、2048ビットが推奨される最小値です。RSA暗号は、公開鍵暗号方式の一つで、大きな数の素因数分解の困難性に基づいています。鍵長が長いほど、暗号を解読するのに必要な計算量が指数関数的に増加します。1024ビットのRSA鍵は、2010年頃から安全ではないとされ、現在では使用が推奨されていません。2048ビットのRSA鍵は、現在の標準的な鍵長で、一般的な用途に適しています。3072ビットや4096ビットは、より高いセキュリティが必要な場合（例：長期にわたる機密情報の保護、政府機関など）に使用されます。ただし、鍵長が長いほど、暗号化・復号化の処理時間が増加します。実務では、用途に応じて適切な鍵長を選択する必要があります。また、RSA暗号は計算コストが高いため、実際の通信では、RSAで共通鍵を交換し、その後は高速な共通鍵暗号（AESなど）で通信することが一般的です。',
        'options': [
            {'option_text': '2048ビット', 'is_correct': True},
            {'option_text': '1024ビット', 'is_correct': False},
            {'option_text': '512ビット', 'is_correct': False},
            {'option_text': '256ビット', 'is_correct': False},
        ]
    },
    {
        'question_text': 'ハッシュ関数SHA-256の出力ビット数はどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'easy',
        'explanation': 'SHA-256は、入力データから256ビット（32バイト）の固定長のハッシュ値を生成するハッシュ関数です。ハッシュ関数は、任意の長さのデータから固定長のハッシュ値（メッセージダイジェスト）を生成する一方向関数です。SHA-256は、SHA-2（Secure Hash Algorithm 2）ファミリーの一つで、2001年にNIST（米国国立標準技術研究所）によって標準化されました。SHA-1（160ビット）は、2005年に理論的な脆弱性が発見され、2017年に実用的な衝突攻撃が成功したため、現在では使用が推奨されていません。SHA-512は512ビットの出力を生成し、SHA-256より長いハッシュ値を提供しますが、計算コストも高くなります。MD5（128ビット）は、1996年に脆弱性が発見され、現在では暗号学的な用途には使用されていません。SHA-256は、デジタル署名、メッセージ認証コード（HMAC）、パスワードのハッシュ化、ブロックチェーンなど、様々な用途で使用されています。ハッシュ関数の重要な性質は、一方向性（逆算が困難）、衝突耐性（異なる入力から同じハッシュ値が生成されにくい）、雪崩効果（入力の小さな変更でハッシュ値が大きく変わる）です。',
        'options': [
            {'option_text': '256ビット', 'is_correct': True},
            {'option_text': '128ビット', 'is_correct': False},
            {'option_text': '512ビット', 'is_correct': False},
            {'option_text': '1024ビット', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SSL/TLSプロトコルにおいて、サーバー証明書の検証で確認する項目として、適切でないものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'medium',
        'explanation': 'サーバー証明書の検証では、有効期限、発行者（CA：認証局）の信頼性、ドメイン名の一致を確認します。SSL/TLSプロトコルでは、サーバーがクライアントにサーバー証明書を送信し、クライアントがその証明書を検証することで、サーバーの身元を確認します。証明書の有効期限を確認することで、期限切れの証明書を拒否できます。発行者（CA）の信頼性を確認することで、信頼できる認証局によって発行された証明書であることを確認します。ドメイン名の一致を確認することで、接続先のサーバーが証明書に記載されたドメイン名と一致することを確認します（例：www.example.comに接続している場合、証明書のCommon Name（CN）またはSubject Alternative Name（SAN）にwww.example.comが含まれている必要があります）。サーバーのIPアドレスは証明書に含まれていないため、検証項目ではありません。IPアドレスは動的に変更される可能性があるため、証明書には含めません。証明書の検証に失敗した場合、ブラウザは警告を表示し、ユーザーに接続を続行するか確認します。',
        'options': [
            {'option_text': 'サーバーのIPアドレス', 'is_correct': True},
            {'option_text': '証明書の有効期限', 'is_correct': False},
            {'option_text': '発行者（CA）の信頼性', 'is_correct': False},
            {'option_text': 'ドメイン名の一致', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SQLインジェクション攻撃を防ぐための対策として、最も適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'medium',
        'explanation': 'SQLインジェクション攻撃を防ぐには、プリペアドステートメント（パラメータ化クエリ）を使用することが最も効果的です。SQLインジェクション攻撃は、悪意のあるSQL文をユーザー入力に注入して、データベースを不正に操作する攻撃です。例えば、ログイン画面で「admin\' OR \'1\'=\'1」と入力すると、「SELECT * FROM users WHERE username = \'admin\' OR \'1\'=\'1\'」となり、常に真となる条件が追加されてしまいます。プリペアドステートメントは、SQL文の構造を事前に定義し、ユーザー入力をパラメータとして後からバインドする方式です。これにより、ユーザー入力をSQL文の一部として解釈されないようにします。例えば、「SELECT * FROM users WHERE username = ?」というSQL文を定義し、ユーザー入力を「?」にバインドします。入力値の検証（ホワイトリスト、長さ制限など）やエスケープ処理も有効ですが、完全ではない可能性があります。プリペアドステートメントは、すべての主要なデータベース（MySQL、PostgreSQL、SQLiteなど）でサポートされており、実務では必須の対策です。OWASP（Open Web Application Security Project）のTop 10でも、SQLインジェクションは重要なセキュリティリスクとして挙げられています。',
        'options': [
            {'option_text': 'プリペアドステートメント（パラメータ化クエリ）の使用', 'is_correct': True},
            {'option_text': '入力値の長さ制限のみ', 'is_correct': False},
            {'option_text': 'データベースへのアクセス権限の削除', 'is_correct': False},
            {'option_text': 'SQL文の暗号化', 'is_correct': False},
        ]
    },
    {
        'question_text': 'XSS（Cross-Site Scripting）攻撃の説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'medium',
        'explanation': 'XSS（Cross-Site Scripting）攻撃は、悪意のあるスクリプトをWebページに注入し、他のユーザーのブラウザで実行させる攻撃です。XSS攻撃には、反射型XSS（Reflected XSS）、格納型XSS（Stored XSS）、DOM-based XSSの3種類があります。反射型XSSは、ユーザー入力が即座にページに反映される場合に発生します。格納型XSSは、悪意のあるスクリプトがデータベースに保存され、後から他のユーザーに表示される場合に発生します。DOM-based XSSは、クライアント側のJavaScriptでDOMを操作する際に発生します。XSS攻撃により、セッション情報（Cookie）の窃取、ユーザーになりすましての操作、個人情報の窃取、フィッシング攻撃などが可能になります。対策としては、ユーザー入力を適切にエスケープ処理する（HTMLエスケープ、JavaScriptエスケープなど）、Content Security Policy（CSP）を設定する、HttpOnly属性をCookieに設定するなどがあります。SQLインジェクションはデータベースへの攻撃、CSRF（Cross-Site Request Forgery）は別のサイトからのリクエストを利用してユーザーに操作を実行させる攻撃です。OWASP Top 10では、XSSは重要なセキュリティリスクとして挙げられています。',
        'options': [
            {'option_text': '悪意のあるスクリプトをWebページに注入し、ユーザーのブラウザで実行させる攻撃', 'is_correct': True},
            {'option_text': 'SQL文を注入してデータベースを操作する攻撃', 'is_correct': False},
            {'option_text': '別のサイトからのリクエストを利用してユーザーに操作を実行させる攻撃', 'is_correct': False},
            {'option_text': 'パスワードを総当たりで試行する攻撃', 'is_correct': False},
        ]
    },
    
    # ハードウェア関連
    {
        'question_text': 'CPUのキャッシュメモリにおいて、L2キャッシュの特徴として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': 'L2キャッシュは、L1キャッシュと主記憶装置の中間にあるキャッシュです。CPUのキャッシュメモリは、CPUと主記憶装置の速度差を埋めるために使用される高速なメモリです。L1キャッシュ（一次キャッシュ）は、CPUに最も近く、最も高速ですが容量が小さいです（通常、命令用とデータ用に分かれています）。L2キャッシュ（二次キャッシュ）は、L1より遅いが容量が大きく、主記憶より高速です。L3キャッシュ（三次キャッシュ）は、さらに容量が大きく、複数のCPUコアで共有されることが多いです。キャッシュの階層構造により、CPUは頻繁にアクセスするデータを高速なキャッシュに保持し、メモリアクセスの待ち時間を削減します。キャッシュミス（必要なデータがキャッシュにない場合）が発生すると、主記憶装置からデータを取得する必要があり、処理が遅くなります。L2キャッシュは、通常、CPUコアごとまたは複数コアで共有されます。キャッシュのサイズは、CPUの性能に大きく影響し、一般的に大きいほど性能が向上しますが、コストも増加します。',
        'options': [
            {'option_text': 'L1より遅いが容量が大きく、主記憶より高速', 'is_correct': True},
            {'option_text': 'L1より高速で容量も大きい', 'is_correct': False},
            {'option_text': '主記憶装置と同じ速度', 'is_correct': False},
            {'option_text': 'L3キャッシュより高速', 'is_correct': False},
        ]
    },
    {
        'question_text': 'RAID 1の特徴として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': 'RAID 1（ミラーリング）は、同じデータを2台以上のディスクに書き込むことで、1台のディスク障害に耐えられる冗長性を提供します。RAID（Redundant Array of Independent Disks）は、複数のディスクを組み合わせて、性能向上や冗長性を実現する技術です。RAID 1では、2台以上のディスクに同じデータを書き込むため、1台のディスクが故障しても、もう1台のディスクからデータを読み取ることができます。読み取り性能は向上します（複数のディスクから並列に読み取れるため）が、書き込み性能は向上しません（すべてのディスクに書き込む必要があるため）。使用可能な容量は、ディスクの合計容量の半分になります（2台の場合）。RAID 0（ストライピング）は高速化のみで冗長性はなく、RAID 5はパリティによる冗長化とストライピングによる高速化を実現し、RAID 6は2つのパリティを使用して2台のディスク障害に耐えられます。RAID 1は、データの可用性が重要な場合（例：データベースサーバー、ファイルサーバー）に使用されます。',
        'options': [
            {'option_text': 'ミラーリングによる冗長化で、1台のディスク障害に耐えられる', 'is_correct': True},
            {'option_text': 'ストライピングによる高速化のみで、冗長性はない', 'is_correct': False},
            {'option_text': 'パリティによる冗長化で、2台以上のディスク障害に耐えられる', 'is_correct': False},
            {'option_text': 'データの圧縮による容量削減', 'is_correct': False},
        ]
    },
    {
        'question_text': 'メモリの種類において、SRAMの特徴として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'hard',
        'explanation': 'SRAM（Static Random Access Memory）は、フリップフロップ回路を使用した高速なメモリです。SRAMは、データを保持するために電源を必要としますが、リフレッシュ（定期的なデータの再書き込み）が不要です。DRAM（Dynamic Random Access Memory）は、コンデンサに電荷を蓄える方式で、定期的なリフレッシュが必要ですが、SRAMより安価で大容量です。SRAMは、DRAMより高速ですが、高価で容量が小さく、主にCPUのキャッシュメモリ（L1、L2、L3キャッシュ）として使用されます。DRAMは、主記憶装置（RAM）として使用されます。SRAMのアクセス時間は数ナノ秒、DRAMのアクセス時間は数十ナノ秒です。SRAMは、フリップフロップ回路を使用するため、セルあたり6個のトランジスタが必要で、DRAM（1個のトランジスタと1個のコンデンサ）より複雑です。そのため、SRAMは高価で、大容量化が困難です。不揮発性メモリ（ROM、フラッシュメモリなど）は、電源を切ってもデータが保持されますが、SRAMとDRAMは揮発性メモリです。',
        'options': [
            {'option_text': 'DRAMより高速だが高価で、主にキャッシュメモリとして使用', 'is_correct': True},
            {'option_text': 'DRAMより低速だが安価で、主記憶装置として使用', 'is_correct': False},
            {'option_text': '不揮発性メモリで、電源を切ってもデータが保持される', 'is_correct': False},
            {'option_text': 'フラッシュメモリの一種', 'is_correct': False},
        ]
    },
    {
        'question_text': 'CPUの命令実行において、スーパースカラ方式の説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'hard',
        'explanation': 'スーパースカラ方式は、複数の命令を同時に実行できる実行ユニットを複数持つことで、1クロックサイクルあたりに複数の命令を処理できる方式です。CPUの性能向上技術には、パイプライン、スーパースカラ、アウトオブオーダー実行、マルチコアなどがあります。パイプライン処理は、命令の実行を複数のステージ（命令フェッチ、デコード、実行、メモリアクセス、書き戻しなど）に分割し、異なる命令を各ステージで並列に処理することで、スループットを向上させます。スーパースカラ方式は、複数の実行ユニット（ALU：算術論理演算装置など）を持ち、1クロックサイクルあたりに複数の命令を同時に実行します。アウトオブオーダー実行は、命令の依存関係を解析し、実行可能な命令から順に実行することで、実行ユニットのアイドル時間を削減します。マルチコアは、1つのCPUパッケージに複数のCPUコアを搭載することで、真の並列処理を実現します。これらの技術を組み合わせることで、CPUの性能が大幅に向上します。現代のCPU（例：Intel Core、AMD Ryzen）は、これらの技術をすべて使用しています。',
        'options': [
            {'option_text': '複数の実行ユニットを持ち、1クロックサイクルあたりに複数の命令を処理', 'is_correct': True},
            {'option_text': '命令を複数ステージに分割して並列処理', 'is_correct': False},
            {'option_text': '複数のCPUコアを持つ', 'is_correct': False},
            {'option_text': '命令の順序を変更して実行', 'is_correct': False},
        ]
    },
    
    # アルゴリズム・データ構造関連
    {
        'question_text': '二分探索アルゴリズムの時間計算量はどれか。',
        'question_type': 'multiple_choice',
        'category': 'アルゴリズム',
        'difficulty': 'medium',
        'explanation': '二分探索は、ソート済みの配列から要素を探索するアルゴリズムで、各ステップで探索範囲を半分に削減します。時間計算量はO(log n)です。二分探索の手順は、1）配列の中央の要素を確認、2）目的の値と比較、3）目的の値が中央より小さい場合は左半分、大きい場合は右半分を探索、4）見つかるか探索範囲がなくなるまで繰り返す、です。線形探索は、配列の先頭から順に要素を確認するアルゴリズムで、時間計算量はO(n)です。二分探索は、ソート済みの配列に対してのみ使用でき、ソートにO(n log n)の時間がかかりますが、探索回数が多い場合は、二分探索の方が効率的です。バブルソートは、隣接する要素を比較して交換するソートアルゴリズムで、時間計算量はO(n²)です。マージソートは、配列を分割してソートし、マージするソートアルゴリズムで、時間計算量はO(n log n)です。実務では、データ構造によって適切な探索アルゴリズムを選択する必要があります。ハッシュテーブルはO(1)の探索が可能ですが、メモリを多く消費します。',
        'options': [
            {'option_text': 'O(log n)', 'is_correct': True},
            {'option_text': 'O(n)', 'is_correct': False},
            {'option_text': 'O(n log n)', 'is_correct': False},
            {'option_text': 'O(n²)', 'is_correct': False},
        ]
    },
    {
        'question_text': 'データ構造において、スタックの特徴として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'アルゴリズム',
        'difficulty': 'easy',
        'explanation': 'スタックは、LIFO（Last In First Out：後入れ先出し）のデータ構造です。最後に追加した要素が最初に取り出されます。スタックの操作は、push（要素の追加）とpop（要素の取り出し）です。スタックは、関数呼び出し、再帰処理、式の評価（逆ポーランド記法）、Undo/Redo機能などに使用されます。キューは、FIFO（First In First Out：先入れ先出し）のデータ構造で、最初に追加した要素が最初に取り出されます。キューの操作は、enqueue（要素の追加）とdequeue（要素の取り出し）です。キューは、タスクスケジューリング、メッセージキュー、幅優先探索などに使用されます。ヒープは、優先度付きキューを実装するためのデータ構造で、親ノードの値が子ノードの値より大きい（または小さい）という性質を持ちます。ヒープは、優先度付きスケジューリング、ヒープソートなどに使用されます。ハッシュテーブルは、キーと値のペアを格納するデータ構造で、キーからハッシュ値を計算して、その位置に値を格納します。ハッシュテーブルは、O(1)の探索が可能ですが、衝突処理が必要です。',
        'options': [
            {'option_text': 'LIFO（後入れ先出し）のデータ構造', 'is_correct': True},
            {'option_text': 'FIFO（先入れ先出し）のデータ構造', 'is_correct': False},
            {'option_text': '優先度に基づいて要素を取り出すデータ構造', 'is_correct': False},
            {'option_text': 'キーと値のペアを格納するデータ構造', 'is_correct': False},
        ]
    },
    {
        'question_text': 'ソートアルゴリズムにおいて、クイックソートの平均時間計算量はどれか。',
        'question_type': 'multiple_choice',
        'category': 'アルゴリズム',
        'difficulty': 'medium',
        'explanation': 'クイックソートの平均時間計算量はO(n log n)です。クイックソートは、ピボット（基準値）を選択し、ピボットより小さい要素を左に、大きい要素を右に分割し、再帰的にソートするアルゴリズムです。最悪の場合（ピボットが常に最小値や最大値の場合）はO(n²)ですが、平均的には高速です。ピボットの選択方法（ランダム、中央値など）により、最悪ケースを回避できます。クイックソートは、in-placeソート（追加のメモリをほとんど使用しない）で、実装が比較的簡単です。バブルソートは、隣接する要素を比較して交換するアルゴリズムで、時間計算量はO(n²)です。実装が簡単ですが、効率が悪いため、実務では使用されません。マージソートは、配列を分割してソートし、マージするアルゴリズムで、時間計算量はO(n log n)で、最悪の場合もO(n log n)です。安定ソート（同じ値の要素の順序が保たれる）ですが、追加のメモリが必要です。挿入ソートは、要素を適切な位置に挿入するアルゴリズムで、時間計算量はO(n²)ですが、データがほぼソート済みの場合は高速です。実務では、データの特性に応じて適切なソートアルゴリズムを選択します。',
        'options': [
            {'option_text': 'O(n log n)', 'is_correct': True},
            {'option_text': 'O(n)', 'is_correct': False},
            {'option_text': 'O(n²)', 'is_correct': False},
            {'option_text': 'O(log n)', 'is_correct': False},
        ]
    },
    {
        'question_text': 'データ構造において、連結リストの特徴として、適切でないものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'アルゴリズム',
        'difficulty': 'medium',
        'explanation': '連結リストは、要素がポインタで連結されたデータ構造です。連結リストの各ノードは、データと次のノードへのポインタ（リンク）を持ちます。先頭からの順次アクセスはO(1)ですが、任意の位置へのアクセスはO(n)です（先頭から順にたどる必要があるため）。配列とは異なり、メモリ上で連続していないため、ランダムアクセスは効率的ではありません。連結リストの利点は、要素の追加・削除がO(1)で可能（先頭の場合）で、メモリの動的確保が容易なことです。配列は、ランダムアクセスがO(1)で高速ですが、要素の追加・削除がO(n)で、サイズの変更が困難です。連結リストには、単方向リスト、双方向リスト、循環リストなどの種類があります。実務では、データのアクセスパターンに応じて、配列と連結リストを選択します。スタックやキューは、連結リストで実装することもできます。また、ハッシュテーブルの衝突処理にも連結リストが使用されることがあります。',
        'options': [
            {'option_text': '任意の位置へのアクセスがO(1)で高速', 'is_correct': True},
            {'option_text': '要素の追加・削除がO(1)で可能（先頭の場合）', 'is_correct': False},
            {'option_text': 'メモリ上で連続していない', 'is_correct': False},
            {'option_text': '要素がポインタで連結されている', 'is_correct': False},
        ]
    },
    
    # ソフトウェア開発関連
    {
        'question_text': 'アジャイル開発手法において、スクラムの役割として、適切でないものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': 'スクラムの主要な役割は、プロダクトオーナー（要求の管理）、スクラムマスター（プロセスの促進）、開発チーム（開発の実行）です。スクラムは、アジャイル開発手法の一つで、複雑な問題を解決するためのフレームワークです。プロダクトオーナーは、プロダクトのビジョンを定義し、プロダクトバックログ（要求のリスト）を管理し、優先順位を決定します。スクラムマスターは、スクラムのプロセスを促進し、チームを支援し、障害を取り除きます。開発チームは、自己組織化されたチームで、スプリント（通常1〜4週間）ごとに機能を開発します。プロジェクトマネージャーはスクラムの役割ではありません。スクラムでは、階層的な管理ではなく、自己組織化されたチームが重要です。スクラムのイベントには、スプリントプランニング、デイリースクラム、スプリントレビュー、スプリントレトロスペクティブがあります。スクラムの成果物には、プロダクトバックログ、スプリントバックログ、インクリメントがあります。スクラムは、変化に対応しやすく、顧客価値を早期に提供できる開発手法として、多くの組織で採用されています。',
        'options': [
            {'option_text': 'プロジェクトマネージャー', 'is_correct': True},
            {'option_text': 'プロダクトオーナー', 'is_correct': False},
            {'option_text': 'スクラムマスター', 'is_correct': False},
            {'option_text': '開発チーム', 'is_correct': False},
        ]
    },
    {
        'question_text': 'バージョン管理システムGitにおいて、ブランチをマージするコマンドはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'easy',
        'explanation': 'git mergeは、指定したブランチを現在のブランチにマージするコマンドです。Gitは、分散バージョン管理システムで、ソースコードの変更履歴を管理します。git mergeは、2つのブランチの変更を統合します。マージには、Fast-forwardマージ（履歴が一直線の場合）と3-wayマージ（分岐した履歴を統合する場合）があります。git branchは、ブランチの作成・一覧表示・削除を行うコマンドです。git checkoutは、ブランチの切り替え、ファイルの復元などを行うコマンドです（Git 2.23以降では、git switchとgit restoreに分離されました）。git rebaseは、ブランチの履歴を書き換えて、別のブランチの上に再適用するコマンドです。rebaseにより、履歴が一直線になり、見やすくなりますが、既に公開されたブランチに対しては使用を避けるべきです。Git FlowやGitHub Flowなどのブランチ戦略では、featureブランチをdevelopブランチやmainブランチにマージする際にgit mergeを使用します。マージコンフリクト（競合）が発生した場合は、手動で解決する必要があります。',
        'options': [
            {'option_text': 'git merge', 'is_correct': True},
            {'option_text': 'git branch', 'is_correct': False},
            {'option_text': 'git checkout', 'is_correct': False},
            {'option_text': 'git rebase', 'is_correct': False},
        ]
    },
    {
        'question_text': 'テスト手法において、ブラックボックステストの説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': 'ブラックボックステストは、プログラムの内部構造を知らずに、入力と出力のみに基づいてテストする手法です。ブラックボックステストは、仕様書に基づいてテストケースを作成し、プログラムが仕様を満たしているかを確認します。テスト設計技法には、同値分割（等価クラス）、境界値分析、デシジョンテーブル、状態遷移テストなどがあります。ホワイトボックステストは、プログラムの内部構造（コード）に基づいてテストする手法で、コードカバレッジ（命令網羅、分岐網羅、条件網羅など）を測定します。統合テストは、複数のモジュールを組み合わせてテストする手法で、モジュール間のインターフェースを確認します。単体テストは、個々のモジュール（関数、クラスなど）を独立してテストする手法です。テストのピラミッドでは、単体テストが最も多く、統合テスト、システムテスト、E2Eテストの順に少なくなります。実務では、これらのテスト手法を組み合わせて、ソフトウェアの品質を確保します。',
        'options': [
            {'option_text': 'プログラムの内部構造を知らずに、入力と出力のみに基づいてテスト', 'is_correct': True},
            {'option_text': 'プログラムの内部構造に基づいてテスト', 'is_correct': False},
            {'option_text': '複数のモジュールを組み合わせてテスト', 'is_correct': False},
            {'option_text': '個々のモジュールを独立してテスト', 'is_correct': False},
        ]
    },
    {
        'question_text': '設計パターンにおいて、Singletonパターンの説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'hard',
        'explanation': 'Singletonパターンは、クラスのインスタンスが1つだけ存在することを保証するデザインパターンです。Singletonパターンは、Creational Patterns（生成に関するパターン）の一つで、グローバルなアクセスポイントを提供します。実装方法には、Eager Initialization（早期初期化）、Lazy Initialization（遅延初期化）、Thread-Safe Singleton（スレッドセーフな実装）などがあります。データベース接続プール、設定管理、ログ管理、キャッシュ管理など、アプリケーション全体で1つのインスタンスを共有したい場合に使用されます。Singletonパターンの利点は、リソースの節約、グローバルなアクセス、状態の一元管理などです。欠点は、テストが困難、グローバル状態による結合度の増加、マルチスレッド環境での注意が必要などです。実務では、DI（Dependency Injection）コンテナを使用して、Singletonのライフサイクルを管理することも多いです。GoF（Gang of Four）のデザインパターンには、他にFactory、Observer、Strategy、Adapterなどがあります。',
        'options': [
            {'option_text': 'クラスのインスタンスが1つだけ存在することを保証する', 'is_correct': True},
            {'option_text': 'オブジェクトの生成と使用を分離する', 'is_correct': False},
            {'option_text': 'アルゴリズムをカプセル化して交換可能にする', 'is_correct': False},
            {'option_text': 'オブジェクト間の一対多の依存関係を定義する', 'is_correct': False},
        ]
    },
    
    # OS・システム関連
    {
        'question_text': 'OSのプロセス管理において、デッドロックが発生するための必要条件として、適切でないものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'OS',
        'difficulty': 'hard',
        'explanation': 'デッドロックの4つの必要条件は、相互排除（Mutual Exclusion）、保持と待機（Hold and Wait）、非先取り（No Preemption）、循環待機（Circular Wait）です。デッドロックは、複数のプロセスが互いにリソースを待ち続け、処理が進まなくなる状態です。相互排除は、リソースが排他的に使用されること、保持と待機は、プロセスがリソースを保持したまま他のリソースを待つこと、非先取りは、リソースを強制的に奪えないこと、循環待機は、プロセス間で循環的な待機関係が発生することです。これらの4つの条件がすべて満たされると、デッドロックが発生する可能性があります。デッドロックの対策には、予防（4つの条件のいずれかを排除）、回避（リソースの割り当て順序を制御）、検出と回復（デッドロックを検出して解除）があります。優先度の高いプロセスが優先的に実行されることは、プロセススケジューリングの話で、デッドロックの必要条件ではありません。実務では、リソースの割り当て順序を統一する、タイムアウトを設定する、デッドロック検出アルゴリズムを使用するなどの対策が取られます。',
        'options': [
            {'option_text': '優先度の高いプロセスが優先的に実行される', 'is_correct': True},
            {'option_text': '相互排除（排他制御）', 'is_correct': False},
            {'option_text': '保持と待機', 'is_correct': False},
            {'option_text': '循環待機', 'is_correct': False},
        ]
    },
    {
        'question_text': 'OSのメモリ管理において、ページング方式の説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'OS',
        'difficulty': 'medium',
        'explanation': 'ページング方式は、メモリと補助記憶装置を固定サイズのページに分割し、ページ単位で管理する方式です。ページング方式では、仮想アドレス空間と物理アドレス空間をページ（通常4KB）に分割し、ページテーブルで仮想アドレスを物理アドレスに変換します。これにより、メモリの断片化（フラグメンテーション）を防ぎ、効率的なメモリ管理が可能になります。セグメンテーション方式は、メモリを可変サイズのセグメントに分割し、セグメント単位で管理する方式です。ページング方式の利点は、外部フラグメンテーションが発生しない、ページ単位でのスワッピング（仮想メモリ）が容易、メモリ保護が容易などです。欠点は、内部フラグメンテーションが発生する可能性、ページテーブルの管理コストなどです。現代のOS（Windows、Linux、macOSなど）は、ページング方式を使用しています。仮想メモリにより、物理メモリより大きなアドレス空間を使用でき、メモリが不足した場合は、使用頻度の低いページを補助記憶装置（ハードディスク、SSD）にスワップアウトします。ページフォルト（必要なページがメモリにない場合）が発生すると、OSがページをスワップインします。',
        'options': [
            {'option_text': 'メモリを固定サイズのページに分割し、ページ単位で管理', 'is_correct': True},
            {'option_text': 'メモリを可変サイズのセグメントに分割し、セグメント単位で管理', 'is_correct': False},
            {'option_text': 'メモリを連続した領域として割り当てる', 'is_correct': False},
            {'option_text': 'メモリを階層的に管理する', 'is_correct': False},
        ]
    },
]

