# 実際の基本情報技術者試験に近い問題データ
# より実践的で具体的な問題を定義

REAL_QUESTIONS = [
    # ネットワーク関連の実践的な問題
    {
        'question_text': 'IPv4アドレス 192.168.1.0/24 のサブネットマスクはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': '/24は、ネットワーク部が24ビット、ホスト部が8ビットであることを意味します。CIDR表記（Classless Inter-Domain Routing）では、スラッシュの後の数字がネットワーク部のビット数を示します。サブネットマスクは255.255.255.0（2進数で11111111.11111111.11111111.00000000）となります。サブネットマスクは、IPアドレスのどの部分がネットワーク部で、どの部分がホスト部かを示す32ビットの値です。ネットワーク部のビットは1、ホスト部のビットは0で表されます。/24の場合、最初の24ビットがネットワーク部、最後の8ビットがホスト部です。このネットワークでは、192.168.1.1から192.168.1.254までがホストとして使用可能です（合計254台）。192.168.1.0はネットワークアドレス、192.168.1.255はブロードキャストアドレスとして予約されています。',
        'options': [
            {'option_text': '255.255.255.0', 'is_correct': True},
            {'option_text': '255.255.0.0', 'is_correct': False},
            {'option_text': '255.0.0.0', 'is_correct': False},
            {'option_text': '255.255.255.255', 'is_correct': False},
        ]
    },
    {
        'question_text': 'TCP/IPネットワークにおいて、MTU（Maximum Transmission Unit）のデフォルト値はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': 'イーサネット（Ethernet）のMTUのデフォルト値は1500バイトです。MTU（Maximum Transmission Unit）は、1回の転送で送信できるデータの最大サイズです。これは、イーサネットフレームのペイロード部分（IPパケット）の最大サイズを表します。イーサネットフレーム全体のサイズは、ペイロード（最大1500バイト）+ イーサネットヘッダー（14バイト）+ FCS（Frame Check Sequence、4バイト）= 最大1518バイトです。MTUが大きすぎると、フラグメンテーション（分割）が発生し、パフォーマンスが低下する可能性があります。MTUが小さすぎると、オーバーヘッドが増加します。1500バイトは、イーサネットの標準的な値で、多くのネットワークで使用されています。Jumbo Frame（ジャンボフレーム）は、9000バイトなどの大きなMTUを使用し、高性能ネットワークで使用されますが、すべての機器でサポートされているわけではありません。',
        'options': [
            {'option_text': '1500バイト', 'is_correct': True},
            {'option_text': '1024バイト', 'is_correct': False},
            {'option_text': '2048バイト', 'is_correct': False},
            {'option_text': '4096バイト', 'is_correct': False},
        ]
    },
    {
        'question_text': 'HTTPステータスコード404の意味はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'easy',
        'explanation': 'HTTPステータスコード404は「Not Found」を意味し、リクエストされたリソース（ファイル、ページなど）が見つからないことを示します。HTTPステータスコードは、3桁の数字で、最初の桁がカテゴリを表します。2xx（成功）：200 OK（リクエスト成功）、201 Created（リソース作成成功）、204 No Content（成功だが内容なし）など。3xx（リダイレクト）：301 Moved Permanently（永続的なリダイレクト）、302 Found（一時的なリダイレクト）、304 Not Modified（変更なし）など。4xx（クライアントエラー）：400 Bad Request（不正なリクエスト）、401 Unauthorized（認証が必要）、403 Forbidden（アクセス拒否）、404 Not Found（リソースが見つからない）、408 Request Timeout（タイムアウト）など。5xx（サーバーエラー）：500 Internal Server Error（サーバー内部エラー）、502 Bad Gateway（ゲートウェイエラー）、503 Service Unavailable（サービス利用不可）、504 Gateway Timeout（ゲートウェイタイムアウト）など。404エラーは、URLが間違っている、ファイルが削除された、サーバーの設定ミスなどが原因で発生します。',
        'options': [
            {'option_text': 'Not Found（リソースが見つからない）', 'is_correct': True},
            {'option_text': 'OK（リクエスト成功）', 'is_correct': False},
            {'option_text': 'Moved Permanently（永続的なリダイレクト）', 'is_correct': False},
            {'option_text': 'Internal Server Error（サーバー内部エラー）', 'is_correct': False},
        ]
    },
    {
        'question_text': 'OSI参照モデルの第2層（データリンク層）で使用されるプロトコルはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'medium',
        'explanation': 'OSI参照モデルの第2層（データリンク層）では、Ethernet、PPP、HDLCなどのプロトコルが使用されます。データリンク層は、物理層の上に位置し、同一ネットワーク内でのデータ転送を担当します。Ethernetは、最も広く使用されている有線LANのプロトコルで、CSMA/CD（Carrier Sense Multiple Access with Collision Detection）方式を使用します。PPP（Point-to-Point Protocol）は、2点間の直接接続で使用されるプロトコルで、ダイヤルアップ接続などで使用されます。HDLC（High-Level Data Link Control）は、WAN（Wide Area Network）で使用されるプロトコルです。IPは第3層（ネットワーク層）で、異なるネットワーク間でのルーティングを担当します。TCPは第4層（トランスポート層）で、信頼性のあるデータ転送を提供します。HTTPは第7層（アプリケーション層）で、WebブラウザとWebサーバー間の通信に使用されます。OSI参照モデルは、ネットワークの機能を7層に分けて理解するための概念モデルです。',
        'options': [
            {'option_text': 'Ethernet', 'is_correct': True},
            {'option_text': 'IP', 'is_correct': False},
            {'option_text': 'TCP', 'is_correct': False},
            {'option_text': 'HTTP', 'is_correct': False},
        ]
    },
    {
        'question_text': '無線LAN規格IEEE 802.11acの最大伝送速度はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ネットワーク',
        'difficulty': 'hard',
        'explanation': 'IEEE 802.11ac（Wi-Fi 5）の最大伝送速度は約6.9Gbpsです。802.11acは、2013年に標準化された無線LAN規格で、5GHz帯のみを使用します。MIMO（Multiple Input Multiple Output）技術により、最大8ストリームの同時送受信が可能で、チャネルボンディング（複数のチャネルを結合）により、最大160MHzの帯域幅を使用できます。802.11n（Wi-Fi 4）は最大600Mbps、802.11gは最大54Mbps、802.11aは最大54Mbpsです。802.11ax（Wi-Fi 6）は、2019年に標準化され、最大約9.6Gbpsの伝送速度を実現します。実際の通信速度は、理論値より低くなることが多く、距離、障害物、干渉、接続機器数、使用しているチャネルの帯域幅などの要因に影響されます。802.11acは、高解像度動画のストリーミング、大容量ファイルの転送など、高速通信が必要な用途で使用されます。',
        'options': [
            {'option_text': '約6.9Gbps', 'is_correct': True},
            {'option_text': '約600Mbps', 'is_correct': False},
            {'option_text': '約54Mbps', 'is_correct': False},
            {'option_text': '約11Mbps', 'is_correct': False},
        ]
    },
    # データベース関連の実践的な問題
    {
        'question_text': 'SQL文「SELECT COUNT(*) FROM employees WHERE salary > 50000;」の実行結果として、返される値はどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': 'COUNT(*)は、条件に一致する行の数を返す集約関数です。このSQL文は、salary（給与）が50000を超える従業員の数を返します。COUNT(*)は、NULL値を含むすべての行をカウントします。WHERE句で「salary > 50000」という条件を指定しているため、給与が50000より大きい従業員のみがカウントされます。COUNT(列名)は、指定した列がNULLでない行のみをカウントします。集約関数には、他にSUM（合計）、AVG（平均）、MAX（最大値）、MIN（最小値）があります。これらの関数は、GROUP BY句と組み合わせて使用することで、グループごとの集計が可能です。例えば、「SELECT department, COUNT(*) FROM employees GROUP BY department;」とすると、部署ごとの従業員数を取得できます。',
        'options': [
            {'option_text': 'salaryが50000を超える従業員の数', 'is_correct': True},
            {'option_text': 'salaryが50000以下の従業員の数', 'is_correct': False},
            {'option_text': '全従業員のsalaryの合計', 'is_correct': False},
            {'option_text': '全従業員のsalaryの平均', 'is_correct': False},
        ]
    },
    {
        'question_text': 'リレーショナルデータベースにおいて、外部キー制約の主な目的はどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': '外部キー制約は、参照整合性を保証するために使用されます。外部キーは、他のテーブルの主キーまたは一意キーを参照する列です。これにより、存在しないレコードを参照することを防ぎ、データの整合性を維持できます。例えば、注文テーブルに顧客IDの外部キーがある場合、存在しない顧客IDを参照する注文を作成することはできません。外部キー制約には、ON DELETE CASCADE（親レコードが削除されたら子レコードも削除）、ON DELETE SET NULL（親レコードが削除されたら子レコードの外部キーをNULLに設定）、ON DELETE RESTRICT（親レコードが削除されないようにする）などのオプションがあります。参照整合性により、データの不整合を防ぎ、データベースの信頼性が向上します。ただし、外部キー制約は、パフォーマンスに影響を与える可能性があるため、適切にインデックスを設定する必要があります。',
        'options': [
            {'option_text': '参照整合性の保証', 'is_correct': True},
            {'option_text': 'データの暗号化', 'is_correct': False},
            {'option_text': '検索速度の向上', 'is_correct': False},
            {'option_text': 'データの圧縮', 'is_correct': False},
        ]
    },
    {
        'question_text': 'データベースの正規化において、第3正規形（3NF）の条件はどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'hard',
        'explanation': '第3正規形（3NF）は、第2正規形を満たし、かつ非キー属性が他の非キー属性に関数従属していないことを要求します。つまり、推移的関数従属を排除します。推移的関数従属とは、A→B、B→Cという関係がある場合、A→Cという間接的な従属関係が発生することです。例えば、従業員テーブルで（従業員ID→部署ID、部署ID→部署名）という関係がある場合、従業員ID→部署名という推移的関数従属が発生します。これを排除するには、部署情報を別テーブルに分離します。第3正規形により、データの更新時の不整合を防ぎ、ストレージ効率を向上させることができます。ただし、正規化を進めすぎると、JOINが増加し、パフォーマンスが低下する可能性があるため、実務では、用途に応じて適切な正規化レベルを選択する必要があります。非正規化（デノーマライゼーション）は、パフォーマンスを優先する場合に使用されます。',
        'options': [
            {'option_text': '第2正規形を満たし、推移的関数従属を排除する', 'is_correct': True},
            {'option_text': '第1正規形を満たし、部分関数従属を排除する', 'is_correct': False},
            {'option_text': 'すべての属性が原子値である', 'is_correct': False},
            {'option_text': '主キーが存在する', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SQLのトランザクション制御文で、変更を確定するコマンドはどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'easy',
        'explanation': 'COMMITは、トランザクション内で行われたすべての変更を確定するコマンドです。トランザクションは、複数のSQL文を1つの単位として実行し、すべて成功するか、すべて失敗するかのどちらかを保証します。COMMITを実行すると、トランザクション内のすべての変更（INSERT、UPDATE、DELETEなど）がデータベースに永続的に保存されます。ROLLBACKは、トランザクション内の変更を取り消すコマンドです。エラーが発生した場合や、変更を取り消したい場合に使用します。BEGIN（またはSTART TRANSACTION）は、トランザクションを開始するコマンドです。多くのデータベースでは、トランザクションは自動的に開始されますが、明示的に開始することもできます。SAVEPOINTは、トランザクション内に保存点を設定し、その時点までロールバックできるようにするコマンドです。ACID特性（原子性、一貫性、独立性、永続性）により、データベースの信頼性が確保されます。',
        'options': [
            {'option_text': 'COMMIT', 'is_correct': True},
            {'option_text': 'ROLLBACK', 'is_correct': False},
            {'option_text': 'BEGIN', 'is_correct': False},
            {'option_text': 'SAVEPOINT', 'is_correct': False},
        ]
    },
    {
        'question_text': 'データベースのインデックスに関する説明として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'データベース',
        'difficulty': 'medium',
        'explanation': 'インデックスは、データベースの検索速度を向上させるために使用されますが、インデックスの作成や更新にはコストがかかります。インデックスは、本の索引のように、データの位置を高速に検索できるようにするデータ構造です。B-treeインデックスが最も一般的で、O(log n)の時間でデータを検索できます。インデックスの利点は、検索速度の向上（特にWHERE句、JOIN、ORDER BY句での使用）、一意性の保証（UNIQUEインデックス）などです。欠点は、ストレージ容量の消費、INSERT、UPDATE、DELETEの処理時間の増加（インデックスの更新が必要なため）、メンテナンスコストなどです。インデックスは、検索頻度が高い列、JOINで使用される列、ORDER BYで使用される列などに設定します。ただし、インデックスを増やしすぎると、更新処理が遅くなるため、適切なバランスを取る必要があります。実務では、クエリの実行計画を確認し、適切なインデックスを設計します。',
        'options': [
            {'option_text': '検索速度を向上させるが、更新処理のコストが増加する', 'is_correct': True},
            {'option_text': '検索速度と更新速度の両方を向上させる', 'is_correct': False},
            {'option_text': 'ストレージ容量を削減する', 'is_correct': False},
            {'option_text': 'データの整合性を保証する', 'is_correct': False},
        ]
    },
    # セキュリティ関連の実践的な問題
    {
        'question_text': '公開鍵暗号方式において、RSA暗号の安全性の根拠はどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'hard',
        'explanation': 'RSA暗号の安全性は、大きな数の素因数分解の困難性に基づいています。大きな合成数を素因数分解することは、現在のコンピュータ技術では非常に時間がかかるため、暗号として安全です。',
        'options': [
            {'option_text': '大きな数の素因数分解の困難性', 'is_correct': True},
            {'option_text': '離散対数問題の困難性', 'is_correct': False},
            {'option_text': '楕円曲線上の離散対数問題の困難性', 'is_correct': False},
            {'option_text': 'ハッシュ関数の一方向性', 'is_correct': False},
        ]
    },
    {
        'question_text': 'パスワードポリシーにおいて、推奨される最小文字数はどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'easy',
        'explanation': '一般的に、パスワードは8文字以上が推奨されますが、より長いパスワード（12文字以上）の方が安全です。また、大文字、小文字、数字、記号を組み合わせることで、セキュリティが向上します。',
        'options': [
            {'option_text': '8文字以上', 'is_correct': True},
            {'option_text': '4文字以上', 'is_correct': False},
            {'option_text': '6文字以上', 'is_correct': False},
            {'option_text': '10文字以上', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SSL/TLSプロトコルにおいて、使用される暗号化アルゴリズムの組み合わせとして、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'hard',
        'explanation': 'SSL/TLSでは、公開鍵暗号（RSA、ECDSAなど）と共通鍵暗号（AES、ChaCha20など）を組み合わせて使用します。公開鍵暗号で共通鍵を交換し、その後は共通鍵暗号で高速に通信します。',
        'options': [
            {'option_text': '公開鍵暗号と共通鍵暗号の組み合わせ', 'is_correct': True},
            {'option_text': '公開鍵暗号のみ', 'is_correct': False},
            {'option_text': '共通鍵暗号のみ', 'is_correct': False},
            {'option_text': 'ハッシュ関数のみ', 'is_correct': False},
        ]
    },
    {
        'question_text': 'ファイアウォールの機能として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'medium',
        'explanation': 'ファイアウォールは、ネットワークトラフィックを監視し、許可された通信のみを通すことで、不正なアクセスを防ぎます。パケットフィルタリング、ステートフルインスペクション、アプリケーションゲートウェイなどの機能があります。',
        'options': [
            {'option_text': 'ネットワークトラフィックの制御と監視', 'is_correct': True},
            {'option_text': 'ウイルスの検出と駆除', 'is_correct': False},
            {'option_text': 'データの暗号化', 'is_correct': False},
            {'option_text': 'パスワードの管理', 'is_correct': False},
        ]
    },
    {
        'question_text': '二要素認証（2FA）において、使用される認証要素の組み合わせとして、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'セキュリティ',
        'difficulty': 'medium',
        'explanation': '二要素認証では、知識（パスワード）、所有物（スマートフォン、トークン）、生体認証（指紋、顔認証）のうち、異なる2つの要素を組み合わせて使用します。',
        'options': [
            {'option_text': '知識（パスワード）と所有物（スマートフォン）', 'is_correct': True},
            {'option_text': '知識（パスワード）と知識（秘密の質問）', 'is_correct': False},
            {'option_text': '所有物（スマートフォン）と所有物（トークン）', 'is_correct': False},
            {'option_text': '知識（パスワード）のみ', 'is_correct': False},
        ]
    },
    # ハードウェア関連の実践的な問題
    {
        'question_text': 'CPUのキャッシュメモリにおいて、L1キャッシュの特徴として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': 'L1キャッシュは、CPUに最も近いキャッシュで、最も高速ですが容量が小さいです。L2、L3キャッシュはより遅いですが、より大きな容量を持ちます。',
        'options': [
            {'option_text': '最も高速だが容量が小さい', 'is_correct': True},
            {'option_text': '最も低速だが容量が大きい', 'is_correct': False},
            {'option_text': '速度と容量のバランスが取れている', 'is_correct': False},
            {'option_text': '主記憶装置と同じ速度', 'is_correct': False},
        ]
    },
    {
        'question_text': 'RAID 5の特徴として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'hard',
        'explanation': 'RAID 5は、パリティ情報を分散して保存することで、1台のディスク障害に耐えられる冗長性を提供しつつ、ストライピングによる高速化も実現します。最低3台のディスクが必要です。',
        'options': [
            {'option_text': 'パリティによる冗長化とストライピングによる高速化', 'is_correct': True},
            {'option_text': 'ミラーリングのみ', 'is_correct': False},
            {'option_text': 'ストライピングのみ（冗長性なし）', 'is_correct': False},
            {'option_text': 'データの圧縮', 'is_correct': False},
        ]
    },
    {
        'question_text': 'メモリの種類において、DRAMの特徴として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': 'DRAM（Dynamic Random Access Memory）は、主記憶装置として使用される揮発性メモリです。定期的なリフレッシュが必要ですが、SRAMより安価で大容量です。',
        'options': [
            {'option_text': '揮発性メモリで、定期的なリフレッシュが必要', 'is_correct': True},
            {'option_text': '不揮発性メモリで、リフレッシュが不要', 'is_correct': False},
            {'option_text': 'SRAMより高速だが高価', 'is_correct': False},
            {'option_text': 'フラッシュメモリの一種', 'is_correct': False},
        ]
    },
    {
        'question_text': 'CPUの命令実行において、パイプライン処理の主な目的はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'medium',
        'explanation': 'パイプライン処理は、命令の実行を複数のステージに分割し、異なる命令を並列に処理することで、CPUのスループットを向上させます。',
        'options': [
            {'option_text': '命令の並列処理によるスループットの向上', 'is_correct': True},
            {'option_text': 'メモリアクセスの高速化', 'is_correct': False},
            {'option_text': '消費電力の削減', 'is_correct': False},
            {'option_text': 'メモリ容量の増加', 'is_correct': False},
        ]
    },
    {
        'question_text': 'SSDとHDDの主な違いとして、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ハードウェア',
        'difficulty': 'easy',
        'explanation': 'SSD（Solid State Drive）は半導体メモリを使用し、HDD（Hard Disk Drive）は磁気ディスクを使用します。SSDの方が高速で、衝撃に強く、消費電力が少ないですが、容量あたりのコストは高いです。',
        'options': [
            {'option_text': 'SSDは半導体メモリ、HDDは磁気ディスクを使用', 'is_correct': True},
            {'option_text': 'SSDは磁気ディスク、HDDは半導体メモリを使用', 'is_correct': False},
            {'option_text': 'SSDとHDDは同じ技術を使用', 'is_correct': False},
            {'option_text': 'SSDは光ディスクを使用', 'is_correct': False},
        ]
    },
    # ソフトウェア開発関連の実践的な問題
    {
        'question_text': 'アジャイル開発手法において、スクラムのスプリントの期間として、一般的なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': 'スクラムのスプリントは、通常1〜4週間の期間で設定されます。2週間が最も一般的です。スプリント期間中は、スプリントゴールに向かって開発を進めます。',
        'options': [
            {'option_text': '1〜4週間（通常2週間）', 'is_correct': True},
            {'option_text': '1日', 'is_correct': False},
            {'option_text': '6ヶ月', 'is_correct': False},
            {'option_text': '1年', 'is_correct': False},
        ]
    },
    {
        'question_text': 'Gitのブランチ戦略において、Git Flowで使用されるブランチの組み合わせとして、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'hard',
        'explanation': 'Git Flowでは、main（master）、develop、feature、release、hotfixのブランチを使用します。mainは本番環境、developは開発環境、featureは機能開発、releaseはリリース準備、hotfixは緊急修正に使用されます。',
        'options': [
            {'option_text': 'main、develop、feature、release、hotfix', 'is_correct': True},
            {'option_text': 'mainのみ', 'is_correct': False},
            {'option_text': 'mainとdevelopのみ', 'is_correct': False},
            {'option_text': 'featureのみ', 'is_correct': False},
        ]
    },
    {
        'question_text': 'コードレビューの主な目的として、適切なものはどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'easy',
        'explanation': 'コードレビューは、コードの品質向上、バグの早期発見、知識の共有、コーディング規約の遵守などを目的としています。',
        'options': [
            {'option_text': 'コードの品質向上とバグの早期発見', 'is_correct': True},
            {'option_text': '開発速度の向上のみ', 'is_correct': False},
            {'option_text': 'メモリ使用量の削減のみ', 'is_correct': False},
            {'option_text': 'セキュリティの強化のみ', 'is_correct': False},
        ]
    },
    {
        'question_text': '継続的デリバリー（CD）の主な目的はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': '継続的デリバリー（CD）は、コードの変更を自動的にビルド、テスト、デプロイすることで、ソフトウェアを常に本番環境にデプロイ可能な状態に保つことを目的としています。',
        'options': [
            {'option_text': 'ソフトウェアを常に本番環境にデプロイ可能な状態に保つ', 'is_correct': True},
            {'option_text': '開発速度の向上のみ', 'is_correct': False},
            {'option_text': 'メモリ使用量の削減のみ', 'is_correct': False},
            {'option_text': 'セキュリティの強化のみ', 'is_correct': False},
        ]
    },
    {
        'question_text': 'ユニットテストのカバレッジとして、一般的に推奨される値はどれか。',
        'question_type': 'multiple_choice',
        'category': 'ソフトウェア開発',
        'difficulty': 'medium',
        'explanation': 'ユニットテストのカバレッジは、一般的に80%以上が推奨されます。100%を目指すこともありますが、カバレッジだけでなく、テストの質も重要です。',
        'options': [
            {'option_text': '80%以上', 'is_correct': True},
            {'option_text': '50%以上', 'is_correct': False},
            {'option_text': '30%以上', 'is_correct': False},
            {'option_text': '10%以上', 'is_correct': False},
        ]
    },
]

