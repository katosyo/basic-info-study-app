<template>
  <div class="study-materials">
    <h1>対策問題集・ノート作成</h1>
    
    <div class="materials-content">
      <div class="period-selection">
        <h2>期間を選択</h2>
        <div class="period-options">
          <label 
            v-for="period in periods" 
            :key="period.value"
            class="period-option"
            :class="{ 'selected': selectedPeriod === period.value }"
          >
            <input 
              type="radio" 
              :value="period.value" 
              v-model="selectedPeriod"
              @change="loadIncorrectQuestions"
            >
            <span>{{ period.label }}</span>
          </label>
        </div>
      </div>

      <div v-if="loading" class="loading">読み込み中...</div>
      <div v-else-if="incorrectQuestions.length === 0" class="no-data">
        選択した期間に間違えた問題はありません。
      </div>
      <div v-else class="materials-section">
        <div class="materials-header">
          <h2>間違えた問題: {{ incorrectQuestions.length }}問</h2>
          <div class="action-buttons">
            <button @click="generateProblemSet" class="generate-button">
              対策問題集を作成
            </button>
            <button @click="generateNote" class="generate-button">
              ノートを作成
            </button>
          </div>
        </div>

        <div v-if="showProblemSet" class="problem-set-compact">
          <div class="problem-set-header-compact">
            <h3>対策問題集</h3>
            <div class="sort-mode-selection-compact">
              <select v-model="sortMode" @change="sortProblems">
                <option value="incorrect_count">間違えた回数順</option>
                <option value="accuracy_low">正答率低い順</option>
                <option value="weakness_score">苦手度スコア順</option>
                <option value="original">元の順序</option>
              </select>
            </div>
          </div>
          <div class="problem-list-compact">
            <div 
              v-for="(question, index) in sortedProblems" 
              :key="question.id"
              class="problem-item-compact"
            >
              <div class="problem-header-compact">
                <span class="problem-number-compact">Q{{ index + 1 }}</span>
                <span class="problem-category-compact">{{ question.category }}</span>
                <span class="problem-stats-compact">
                  <span class="stat-badge">正答率{{ question.accuracy }}%</span>
                  <span class="stat-badge">誤答{{ question.incorrect_count }}回</span>
                  <span class="stat-badge">総{{ question.total_attempts }}回</span>
                </span>
              </div>
              <p class="problem-text-compact">{{ question.question_text }}</p>
              <div class="problem-options-compact">
                <div 
                  v-for="(option, optIndex) in question.options" 
                  :key="option.id"
                  class="option-item-compact"
                  :class="{ 'correct': option.is_correct }"
                >
                  <span class="option-label-compact">{{ String.fromCharCode(65 + optIndex) }}.</span>
                  <span class="option-text-compact">{{ option.option_text }}</span>
                  <span v-if="option.is_correct" class="correct-mark-compact">✓</span>
                </div>
              </div>
              <div class="explanations-compact">
                <div v-if="question.explanation" class="explanation-compact">
                  <strong>解説:</strong> {{ question.explanation }}
                </div>
                <div class="option-explanations-compact">
                  <div 
                    v-for="(option, optIndex) in question.options" 
                    :key="option.id"
                    class="option-explanation-item"
                    :class="{ 'correct': option.is_correct }"
                  >
                    <strong>{{ String.fromCharCode(65 + optIndex) }}:</strong>
                    <span v-if="option.is_correct">{{ getCorrectOptionExplanation(question, option) }}</span>
                    <span v-else>{{ getIncorrectOptionExplanation(question, option) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="showNote" class="note-textbook">
          <div class="note-header-textbook">
            <h3>対策ノート - 覚えるべき知識</h3>
            <button @click="printNote" class="print-button-compact">📄 印刷</button>
          </div>
          <div class="textbook-pages">
            <div 
              v-for="(chapterGroup, chapterKey) in organizedTextbookContent" 
              :key="chapterKey"
              class="textbook-chapter-page"
            >
              <div class="chapter-page-header">
                <h2 class="chapter-page-number">第{{ chapterGroup.chapter }}章</h2>
                <h2 class="chapter-page-title">{{ chapterGroup.chapterTitle }}</h2>
              </div>
              <div 
                v-for="(sectionGroup, sectionKey) in chapterGroup.sections" 
                :key="sectionKey"
                class="textbook-section-page"
              >
                <div class="section-page-header">
                  <h3 class="section-page-number">第{{ sectionGroup.section }}節</h3>
                  <h3 class="section-page-title">{{ sectionGroup.sectionTitle }}</h3>
                </div>
                <div class="section-page-description">
                  <p>{{ sectionGroup.sectionDescription }}</p>
                </div>
                <div 
                  v-for="(topic, topicIndex) in sectionGroup.topics" 
                  :key="topicIndex"
                  class="topic-content-block"
                >
                  <h4 class="topic-title">{{ topic.name }}</h4>
                  <div v-if="topic.content" class="topic-content">
                    <p>{{ topic.content }}</p>
                  </div>
                  <div v-if="topic.keyPoints && topic.keyPoints.length > 0" class="topic-key-points">
                    <strong class="key-points-label">重要ポイント:</strong>
                    <ul class="key-points-list">
                      <li v-for="(point, pointIndex) in topic.keyPoints" :key="pointIndex">{{ point }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QuestionService from '@/services/question.service';

export default {
  name: 'StudyMaterials',
  data() {
    return {
      selectedPeriod: 'all',
      periods: [
        { value: '1hour', label: '1時間' },
        { value: '1day', label: '1日' },
        { value: '1week', label: '1週間' },
        { value: '2weeks', label: '2週間' },
        { value: '1month', label: '1ヶ月' },
        { value: 'all', label: '全期間' }
      ],
      incorrectQuestions: [],
      loading: false,
      showProblemSet: false,
      showNote: false,
      sortMode: 'weakness_score'
    };
  },
  computed: {
    textbookStructure() {
      // 基本情報技術者試験の標準的な教科書構造を定義
      return this.getTextbookStructure();
    },
    sortedProblems() {
      if (!this.showProblemSet || this.incorrectQuestions.length === 0) {
        return this.incorrectQuestions;
      }
      
      const sorted = [...this.incorrectQuestions];
      
      switch (this.sortMode) {
        case 'incorrect_count':
          return sorted.sort((a, b) => b.incorrect_count - a.incorrect_count);
        case 'accuracy_low':
          return sorted.sort((a, b) => a.accuracy - b.accuracy);
        case 'weakness_score':
          // 苦手度スコア = 間違えた回数 × (100 - 正答率)
          return sorted.sort((a, b) => {
            const scoreA = a.incorrect_count * (100 - a.accuracy);
            const scoreB = b.incorrect_count * (100 - b.accuracy);
            return scoreB - scoreA;
          });
        case 'original':
        default:
          return sorted;
      }
    },
    organizedTextbookContent() {
      // 間違えた問題から関連する教科書の内容を収集し、章・節・トピックごとに整理
      const contentMap = {};
      
      // すべての間違えた問題から参照を収集
      this.incorrectQuestions.forEach(question => {
        const references = this.getTextbookReferences(question);
        references.forEach(ref => {
          const chapterKey = `chapter-${ref.chapter}`;
          const sectionKey = `section-${ref.section}`;
          
          if (!contentMap[chapterKey]) {
            contentMap[chapterKey] = {
              chapter: ref.chapter,
              chapterTitle: this.getChapterTitle(ref.chapter),
              sections: {}
            };
          }
          
          if (!contentMap[chapterKey].sections[sectionKey]) {
            contentMap[chapterKey].sections[sectionKey] = {
              section: ref.section,
              sectionTitle: this.getSectionTitle(ref.chapter, ref.section),
              sectionDescription: this.getSectionDescription(ref.chapter, ref.section),
              topics: []
            };
          }
          
          // トピックが既に追加されていない場合のみ追加
          const section = contentMap[chapterKey].sections[sectionKey];
          const topicExists = section.topics.some(t => t.name === ref.topic);
          
          if (!topicExists && ref.topic) {
            const topicContent = this.getTopicContent(ref.chapter, ref.section, ref.topic);
            const topicKeyPoints = this.getTopicKeyPoints(ref.chapter, ref.section, ref.topic);
            
            section.topics.push({
              name: ref.topic,
              content: topicContent,
              keyPoints: topicKeyPoints
            });
          }
        });
      });
      
      // オブジェクトを配列に変換し、章・節の順序でソート
      return Object.keys(contentMap)
        .sort((a, b) => contentMap[a].chapter - contentMap[b].chapter)
        .map(key => {
          const chapter = contentMap[key];
          // 節も順序でソート
          chapter.sections = Object.keys(chapter.sections)
            .sort((a, b) => chapter.sections[a].section - chapter.sections[b].section)
            .reduce((acc, sectionKey) => {
              acc[sectionKey] = chapter.sections[sectionKey];
              return acc;
            }, {});
          return chapter;
        });
    }
  },
  created() {
    this.loadIncorrectQuestions();
  },
  methods: {
    async loadIncorrectQuestions() {
      this.loading = true;
      this.showProblemSet = false;
      this.showNote = false;
      try {
        this.incorrectQuestions = await QuestionService.getIncorrectQuestions(this.selectedPeriod);
      } catch (error) {
        console.error('Error loading incorrect questions:', error);
      } finally {
        this.loading = false;
      }
    },
    generateProblemSet() {
      this.showProblemSet = true;
      this.showNote = false;
      // ページの先頭にスクロール
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    generateNote() {
      this.showNote = true;
      this.showProblemSet = false;
      // ページの先頭にスクロール
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    sortProblems() {
      // 並び替えはcomputedプロパティで自動的に行われるため、何もしない
      // このメソッドは@changeイベント用に残しておく
    },
    getCorrectOptionExplanation(question, option) {
      // 正解の選択肢がなぜ正しいかを説明
      const category = question.category;
      const questionText = question.question_text.toLowerCase();
      const optionText = option.option_text;
      
      // 既存の解説がある場合はそれを活用
      if (question.explanation) {
        // 解説から正解に関する部分を抽出
        const explanation = question.explanation;
        if (explanation.includes(optionText) || explanation.includes('正解') || explanation.includes('正しい')) {
          return explanation;
        }
      }
      
      // カテゴリと問題文に基づいて説明を生成
      let explanation = '';
      
      if (category === 'ネットワーク') {
        if (questionText.includes('ポート') || questionText.includes('port')) {
          explanation = `${optionText}は、このポート番号で使用される標準的なプロトコルです。ポート番号は、TCP/IP通信においてアプリケーションを識別するために使用され、Well-Knownポート（0-1023）には特定のサービスが割り当てられています。`;
        } else if (questionText.includes('ipアドレス') || questionText.includes('サブネット')) {
          explanation = `${optionText}は、IPアドレスのネットワーク部とホスト部を正しく識別するためのサブネットマスクです。CIDR表記と組み合わせて、ネットワークの範囲を正確に指定できます。`;
        } else if (questionText.includes('tcp') || questionText.includes('udp')) {
          explanation = `${optionText}は、TCP/IPプロトコルスタックにおける正しい説明です。TCPは信頼性の高い通信を提供し、UDPは高速な通信を提供します。`;
        } else {
          explanation = `${optionText}は、ネットワークの仕組みやプロトコルに関する正しい説明です。この選択肢が問題文の要件を満たしています。`;
        }
      } else if (category === 'データベース') {
        if (questionText.includes('sql') || questionText.includes('select') || questionText.includes('join')) {
          explanation = `${optionText}は、SQL文の正しい使用方法やデータベース操作の適切な説明です。リレーショナルデータベースの設計原則に従っています。`;
        } else if (questionText.includes('正規化') || questionText.includes('正規形')) {
          explanation = `${optionText}は、データベースの正規化に関する正しい説明です。正規化により、データの冗長性を排除し、整合性を保つことができます。`;
        } else if (questionText.includes('トランザクション') || questionText.includes('acid')) {
          explanation = `${optionText}は、トランザクションのACID特性（原子性、一貫性、独立性、永続性）に関する正しい説明です。`;
        } else {
          explanation = `${optionText}は、データベースの設計や操作に関する正しい説明です。`;
        }
      } else if (category === 'セキュリティ') {
        if (questionText.includes('暗号') || questionText.includes('暗号化')) {
          explanation = `${optionText}は、暗号化技術に関する正しい説明です。公開鍵暗号、共通鍵暗号、ハッシュ関数などの適切な使用方法を表しています。`;
        } else if (questionText.includes('攻撃') || questionText.includes('インジェクション') || questionText.includes('xss') || questionText.includes('csrf')) {
          explanation = `${optionText}は、セキュリティ攻撃に対する適切な対策方法です。この対策により、該当する攻撃を効果的に防ぐことができます。`;
        } else {
          explanation = `${optionText}は、情報セキュリティの原則や対策に関する正しい説明です。`;
        }
      } else {
        // デフォルトの説明
        explanation = `${optionText}は、問題文の要件を満たす正しい選択肢です。この選択肢が最も適切な説明または答えとなっています。`;
      }
      
      return explanation;
    },
    getIncorrectOptionExplanation(question, option) {
      // 間違った選択肢がなぜ間違っているかを説明
      const category = question.category;
      const questionText = question.question_text.toLowerCase();
      const optionText = option.option_text;
      
      // 正解の選択肢を取得
      const correctOption = question.options.find(opt => opt.is_correct);
      
      // カテゴリと問題文に基づいて説明を生成
      let explanation = '';
      
      if (category === 'ネットワーク') {
        if (questionText.includes('ポート') || questionText.includes('port')) {
          explanation = `${optionText}は、このポート番号で使用されるプロトコルではありません。ポート番号とプロトコルの対応関係が誤っています。正しくは${correctOption ? correctOption.option_text : '別のプロトコル'}が使用されます。`;
        } else if (questionText.includes('ipアドレス') || questionText.includes('サブネット')) {
          explanation = `${optionText}は、IPアドレスのネットワーク部とホスト部の識別方法が誤っています。サブネットマスクの計算やCIDR表記の理解が不足している可能性があります。`;
        } else if (questionText.includes('tcp') || questionText.includes('udp')) {
          explanation = `${optionText}は、TCP/IPプロトコルの特性に関する誤った説明です。TCPとUDPの違いや、各プロトコルの役割を正しく理解する必要があります。`;
        } else {
          explanation = `${optionText}は、ネットワークの仕組みやプロトコルに関する誤った説明です。正解は${correctOption ? correctOption.option_text : '別の選択肢'}です。`;
        }
      } else if (category === 'データベース') {
        if (questionText.includes('sql') || questionText.includes('select') || questionText.includes('join')) {
          explanation = `${optionText}は、SQL文の使用方法やデータベース操作に関する誤った説明です。SQLの構文やJOINの種類、集約関数の使い方を再確認する必要があります。`;
        } else if (questionText.includes('正規化') || questionText.includes('正規形')) {
          explanation = `${optionText}は、データベースの正規化に関する誤った説明です。正規化の目的や各正規形の定義を正しく理解する必要があります。`;
        } else if (questionText.includes('トランザクション') || questionText.includes('acid')) {
          explanation = `${optionText}は、トランザクションのACID特性に関する誤った説明です。原子性、一貫性、独立性、永続性のそれぞれの意味を正確に把握する必要があります。`;
        } else {
          explanation = `${optionText}は、データベースの設計や操作に関する誤った説明です。`;
        }
      } else if (category === 'セキュリティ') {
        if (questionText.includes('暗号') || questionText.includes('暗号化')) {
          explanation = `${optionText}は、暗号化技術に関する誤った説明です。公開鍵暗号と共通鍵暗号の違い、ハッシュ関数の特性などを正しく理解する必要があります。`;
        } else if (questionText.includes('攻撃') || questionText.includes('インジェクション') || questionText.includes('xss') || questionText.includes('csrf')) {
          explanation = `${optionText}は、セキュリティ攻撃に対する対策として不適切です。この対策では、該当する攻撃を効果的に防ぐことができません。正しくは${correctOption ? correctOption.option_text : '別の対策方法'}が必要です。`;
        } else {
          explanation = `${optionText}は、情報セキュリティの原則や対策に関する誤った説明です。`;
        }
      } else if (category === 'ハードウェア') {
        if (questionText.includes('cpu') || questionText.includes('プロセッサ')) {
          explanation = `${optionText}は、CPUやプロセッサの仕組みに関する誤った説明です。命令の実行サイクル、パイプライン処理、キャッシュメモリの役割などを正しく理解する必要があります。`;
        } else if (questionText.includes('メモリ')) {
          explanation = `${optionText}は、メモリの種類や階層構造に関する誤った説明です。DRAM、SRAM、ROM、フラッシュメモリの違いや、メモリ階層の仕組みを再確認する必要があります。`;
        } else {
          explanation = `${optionText}は、ハードウェアの仕組みに関する誤った説明です。`;
        }
      } else if (category === 'アルゴリズム' || category === 'データ構造') {
        if (questionText.includes('探索') || questionText.includes('ソート')) {
          explanation = `${optionText}は、アルゴリズムの計算量や動作に関する誤った説明です。時間計算量（O記法）やアルゴリズムの特性を正しく理解する必要があります。`;
        } else if (questionText.includes('スタック') || questionText.includes('キュー') || questionText.includes('リスト')) {
          explanation = `${optionText}は、データ構造の特性に関する誤った説明です。LIFO（スタック）やFIFO（キュー）の原則、各データ構造の操作を正しく理解する必要があります。`;
        } else {
          explanation = `${optionText}は、アルゴリズムやデータ構造に関する誤った説明です。`;
        }
      } else {
        // デフォルトの説明
        explanation = `${optionText}は、問題文の要件を満たしていない誤った選択肢です。正解は${correctOption ? correctOption.option_text : '別の選択肢'}であり、その理由を理解することが重要です。`;
      }
      
      return explanation;
    },
    organizeSections(questions) {
      // 問題から知識を抽出してセクションに整理
      const sections = [];
      
      // 各問題から知識を抽出
      questions.forEach(question => {
        const section = {
          title: this.extractTitle(question),
          keyPoints: [],
          terms: [],
          formulas: [],
          explanations: [],
          diagrams: [],
          relatedKnowledge: []
        };

        // 解説から重要ポイントを抽出
        if (question.explanation) {
          section.explanations.push(question.explanation);
          section.keyPoints.push(...this.extractKeyPoints(question.explanation));
        }

        // 正解の選択肢から重要用語を抽出
        const correctOption = question.options.find(opt => opt.is_correct);
        if (correctOption) {
          section.terms.push({
            term: this.extractTerm(correctOption.option_text),
            definition: correctOption.option_text
          });
        }

        // 問題文から重要な概念を抽出
        const concept = this.extractConcept(question.question_text);
        if (concept) {
          section.keyPoints.push(concept);
        }

        // 数値や公式を抽出
        const formula = this.extractFormula(question);
        if (formula) {
          section.formulas.push(formula);
        }

        // 図や表を生成
        const diagrams = this.generateDiagrams(question);
        if (diagrams && diagrams.length > 0) {
          section.diagrams = diagrams;
        }

        // 周辺知識を生成
        const relatedKnowledge = this.generateRelatedKnowledge(question);
        if (relatedKnowledge && relatedKnowledge.length > 0) {
          section.relatedKnowledge = relatedKnowledge;
        }

        if (section.keyPoints.length > 0 || section.terms.length > 0 || 
            section.formulas.length > 0 || section.explanations.length > 0 ||
            section.diagrams.length > 0 || section.relatedKnowledge.length > 0) {
          sections.push(section);
        }
      });

      return sections;
    },
    extractTitle(question) {
      // 問題文からタイトルを抽出（最初の30文字程度）
      const text = question.question_text;
      if (text.length > 50) {
        return text.substring(0, 50) + '...';
      }
      return text;
    },
    extractKeyPoints(explanation) {
      // 解説から重要ポイントを抽出（簡易版）
      const points = [];
      const sentences = explanation.split(/[。！？]/).filter(s => s.trim().length > 10);
      
      // 重要な文を抽出（「です」「ます」「である」で終わる文、数値を含む文など）
      sentences.forEach(sentence => {
        const trimmed = sentence.trim();
        if (trimmed.length > 15 && trimmed.length < 100) {
          // 数値、用語、重要な概念を含む文を優先
          if (/\d+/.test(trimmed) || /とは|である|です|ます/.test(trimmed)) {
            points.push(trimmed);
          }
        }
      });

      return points.slice(0, 3); // 最大3つまで
    },
    extractTerm(optionText) {
      // 選択肢から用語を抽出
      // 簡易版：最初の10文字程度を用語として使用
      const match = optionText.match(/^[^。、]+/);
      if (match && match[0].length < 20) {
        return match[0];
      }
      return optionText.substring(0, 15) + '...';
    },
    extractConcept(questionText) {
      // 問題文から重要な概念を抽出
      const concepts = ['IPアドレス', 'TCP/IP', 'データベース', 'アルゴリズム', 'セキュリティ', 
                        'プロトコル', 'OS', 'CPU', 'メモリ', 'ストレージ'];
      for (const concept of concepts) {
        if (questionText.includes(concept)) {
          return `${concept}に関する重要な概念`;
        }
      }
      return null;
    },
    extractFormula(question) {
      // 数値や公式を抽出
      const text = question.question_text + ' ' + (question.explanation || '');
      const numberMatches = text.match(/(\d+)\s*(バイト|ビット|MHz|GHz|GB|MB|KB|秒|分|時間)/g);
      if (numberMatches && numberMatches.length > 0) {
        return {
          name: '重要な数値',
          value: numberMatches[0]
        };
      }
      return null;
    },
    getCurrentDate() {
      const now = new Date();
      return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`;
    },
    printNote() {
      window.print();
    },
    getTextbookStructure() {
      // 基本情報技術者試験の標準的な教科書構造
      return [
        {
          chapterNumber: 1,
          title: '基礎理論',
          introduction: 'コンピュータの基礎となる理論について学習します。',
          sections: [
            {
              sectionNumber: 1,
              title: '数値表現とデータ',
              description: '2進数、16進数、文字コードなどの数値表現とデータの扱い方を学習します。',
              topics: [
                { name: '2進数・10進数・16進数の変換', description: '基数変換の方法と計算' },
                { name: '文字コード', description: 'ASCII、Unicode、UTF-8などの文字コード体系' },
                { name: 'データの表現', description: '整数、浮動小数点、論理演算' }
              ]
            },
            {
              sectionNumber: 2,
              title: '論理演算と集合',
              description: '論理演算、集合、ベン図などの基礎的な数学的概念を学習します。',
              topics: [
                { name: '論理演算', description: 'AND、OR、NOT、XORなどの論理演算' },
                { name: '集合', description: '集合の基本操作とベン図' },
                { name: '真理値表', description: '論理式の真理値表の作成方法' }
              ]
            },
            {
              sectionNumber: 3,
              title: 'アルゴリズムとデータ構造',
              description: 'アルゴリズムの基本とデータ構造について学習します。アルゴリズムは問題を解決するための手順であり、データ構造はデータを効率的に扱うための構造です。',
              topics: [
                { 
                  name: 'アルゴリズムの基本', 
                  description: 'アルゴリズムは、問題を解決するための明確な手順です。アルゴリズムの評価には、時間計算量と空間計算量が用いられます。',
                  content: '時間計算量は、アルゴリズムの実行時間を入力サイズnの関数として表したものです。O記法（ビッグオー記法）を使用して表現します。O(1)は定数時間、O(log n)は対数時間、O(n)は線形時間、O(n log n)は線形対数時間、O(n²)は2乗時間です。空間計算量は、アルゴリズムが使用するメモリ量を表します。'
                },
                { 
                  name: 'データ構造', 
                  description: 'データ構造は、データを効率的に格納・操作するための構造です。用途に応じて適切なデータ構造を選択することが重要です。',
                  content: '配列は、連続したメモリ領域にデータを格納し、O(1)でランダムアクセスが可能です。連結リストは、ポインタで連結されたデータ構造で、動的なサイズ変更が可能です。スタックはLIFO（後入れ先出し）、キューはFIFO（先入れ先出し）のデータ構造です。木構造は、階層的なデータを表現するのに適しています。'
                },
                { 
                  name: '探索アルゴリズム', 
                  description: '探索アルゴリズムは、データから目的の要素を見つけるためのアルゴリズムです。',
                  content: '線形探索は、配列の先頭から順に要素を確認するアルゴリズムで、時間計算量はO(n)です。二分探索は、ソート済みの配列に対して使用でき、時間計算量はO(log n)です。ハッシュ探索は、ハッシュテーブルを使用して、平均的にO(1)で探索できますが、衝突処理が必要です。'
                },
                { 
                  name: 'ソートアルゴリズム', 
                  description: 'ソートアルゴリズムは、データを一定の順序に並べ替えるためのアルゴリズムです。',
                  content: 'バブルソートは、隣接する要素を比較して交換するアルゴリズムで、時間計算量はO(n²)です。クイックソートは、ピボットを選択して分割するアルゴリズムで、平均時間計算量はO(n log n)です。マージソートは、配列を分割してソートし、マージするアルゴリズムで、時間計算量はO(n log n)で、最悪の場合もO(n log n)です。'
                }
              ]
            }
          ]
        },
        {
          chapterNumber: 2,
          title: 'コンピュータシステム',
          introduction: 'コンピュータのハードウェアとソフトウェアの仕組みについて学習します。',
          sections: [
            {
              sectionNumber: 1,
              title: 'プロセッサ',
              description: 'CPUの構造と動作原理について学習します。CPU（Central Processing Unit）は、コンピュータの頭脳として、命令を解釈・実行します。',
              topics: [
                { 
                  name: 'CPUの構成', 
                  description: 'CPUは、制御装置、演算装置、レジスタから構成されます。',
                  content: '制御装置は、命令を解釈し、他の装置に制御信号を送ります。演算装置（ALU: Arithmetic Logic Unit）は、算術演算と論理演算を実行します。レジスタは、CPU内部の高速な記憶装置で、命令レジスタ、プログラムカウンタ、汎用レジスタなどがあります。'
                },
                { 
                  name: '命令の実行', 
                  description: '命令の実行は、フェッチ、デコード、実行、メモリアクセス、書き戻しの5つのステージで行われます。',
                  content: '命令フェッチ: メモリから命令を読み込む。命令デコード: 命令を解釈し、必要な制御信号を生成する。実行: 演算装置で演算を実行する。メモリアクセス: 必要に応じてメモリにアクセスする。書き戻し: 結果をレジスタに書き込む。このサイクルを命令実行サイクルと呼びます。'
                },
                { 
                  name: 'パイプライン処理', 
                  description: 'パイプライン処理は、命令の実行を複数のステージに分割し、異なる命令を各ステージで並列に処理することで、スループットを向上させます。',
                  content: 'パイプライン処理により、1つの命令の実行時間は変わらないが、複数の命令を並列に処理できるため、全体のスループットが向上します。パイプラインの深さ（ステージ数）が深いほど、理論的な性能向上が期待できますが、パイプラインハザード（データハザード、制御ハザード、構造ハザード）が発生する可能性があります。'
                },
                { 
                  name: 'キャッシュメモリ', 
                  description: 'キャッシュメモリは、CPUと主記憶装置の速度差を埋めるために使用される高速なメモリです。',
                  content: 'L1キャッシュは、CPUに最も近く、最も高速ですが容量が小さいです（通常、命令用とデータ用に分かれています）。L2キャッシュは、L1より遅いが容量が大きく、主記憶より高速です。L3キャッシュは、さらに容量が大きく、複数のCPUコアで共有されることが多いです。キャッシュの階層構造により、CPUは頻繁にアクセスするデータを高速なキャッシュに保持し、メモリアクセスの待ち時間を削減します。'
                }
              ]
            },
            {
              sectionNumber: 2,
              title: 'メモリ',
              description: '主記憶装置と補助記憶装置について学習します。メモリは、データやプログラムを格納するための記憶装置です。',
              topics: [
                { 
                  name: 'メモリの種類', 
                  description: 'メモリには、揮発性メモリと不揮発性メモリがあります。',
                  content: 'DRAM（Dynamic Random Access Memory）は、主記憶装置として使用される揮発性メモリで、定期的なリフレッシュが必要ですが、SRAMより安価で大容量です。SRAM（Static Random Access Memory）は、フリップフロップ回路を使用した高速なメモリで、リフレッシュが不要ですが、高価で容量が小さく、主にキャッシュメモリとして使用されます。ROM（Read-Only Memory）は、不揮発性メモリで、BIOSなどが格納されます。フラッシュメモリは、不揮発性メモリで、SSDやUSBメモリなどに使用されます。'
                },
                { 
                  name: 'メモリ階層', 
                  description: 'メモリ階層は、速度と容量のトレードオフを考慮した階層構造です。',
                  content: 'メモリ階層は、上から下に向かって速度が遅くなり、容量が大きくなります。レジスタ（最速、最小）→ L1キャッシュ → L2キャッシュ → L3キャッシュ → 主記憶装置（DRAM）→ 補助記憶装置（SSD/HDD）。この階層構造により、頻繁にアクセスするデータを高速なメモリに保持し、全体の性能を向上させます。'
                },
                { 
                  name: '仮想メモリ', 
                  description: '仮想メモリは、物理メモリより大きなアドレス空間を使用できるようにする技術です。',
                  content: 'ページング方式は、メモリと補助記憶装置を固定サイズのページに分割し、ページ単位で管理する方式です。セグメンテーション方式は、メモリを可変サイズのセグメントに分割し、セグメント単位で管理する方式です。仮想メモリにより、物理メモリが不足した場合でも、使用頻度の低いページを補助記憶装置にスワップアウトすることで、より多くのプログラムを実行できます。'
                }
              ]
            },
            {
              sectionNumber: 3,
              title: '入出力装置',
              description: '各種入出力装置とそのインターフェースについて学習します。入出力装置は、コンピュータと外部環境との情報のやり取りを行う装置です。',
              topics: [
                { 
                  name: '入出力インターフェース', 
                  description: '入出力インターフェースは、コンピュータと周辺機器を接続するための規格です。',
                  content: 'USB（Universal Serial Bus）は、汎用的なシリアルインターフェースで、USB 3.0は最大5Gbpsの転送速度です。HDMI（High-Definition Multimedia Interface）は、映像と音声をデジタルで伝送するインターフェースです。PCIe（PCI Express）は、拡張カード用の高速なシリアルインターフェースで、x1、x4、x8、x16などのレーン数があります。'
                },
                { 
                  name: 'ストレージ', 
                  description: 'ストレージは、データを永続的に保存するための記憶装置です。',
                  content: 'HDD（Hard Disk Drive）は、磁気ディスクを使用したストレージで、大容量で安価ですが、アクセス速度が遅いです。SSD（Solid State Drive）は、半導体メモリを使用したストレージで、高速で衝撃に強いですが、容量あたりのコストが高いです。RAID（Redundant Array of Independent Disks）は、複数のディスクを組み合わせて、性能向上や冗長性を実現する技術です。RAID 0は高速化のみ、RAID 1はミラーリングによる冗長化、RAID 5はパリティによる冗長化とストライピングによる高速化を実現します。'
                },
                { 
                  name: 'ディスプレイ', 
                  description: 'ディスプレイは、情報を視覚的に表示するための出力装置です。',
                  content: '解像度は、画面に表示できる画素数で、1920×1080（Full HD）、2560×1440（2K）、3840×2160（4K）などがあります。色深度は、1ピクセルあたりの色情報のビット数で、24ビット（約1677万色）が一般的です。リフレッシュレートは、1秒間に画面を更新する回数で、60Hz、120Hz、144Hzなどがあります。'
                }
              ]
            },
            {
              sectionNumber: 4,
              title: 'オペレーティングシステム',
              description: 'OSの機能とプロセス管理について学習します。OS（Operating System）は、コンピュータのリソースを管理し、アプリケーションの実行環境を提供するシステムソフトウェアです。',
              topics: [
                { 
                  name: 'OSの機能', 
                  description: 'OSは、リソース管理、プロセス管理、メモリ管理、ファイル管理などの機能を提供します。',
                  content: 'リソース管理: CPU、メモリ、入出力装置などのリソースを効率的に割り当てます。プロセス管理: 複数のプロセスを同時に実行し、CPU時間を割り当てます。メモリ管理: メモリの割り当てと解放、仮想メモリの管理を行います。ファイル管理: ファイルシステムを通じて、ファイルの作成、読み書き、削除を管理します。'
                },
                { 
                  name: 'プロセスとスレッド', 
                  description: 'プロセスとスレッドは、OSの実行単位ですが、異なる特徴があります。',
                  content: 'プロセスは、独立したメモリ空間を持つ実行単位で、重いですが、クラッシュの影響が局所化されます。スレッドは、同じメモリ空間を共有する実行単位で、軽いですが、共有リソースの同期が必要です。マルチプロセスは、独立性が高いが、プロセス間通信にコストがかかります。マルチスレッドは、効率的ですが、共有リソースの競合に注意が必要です。'
                },
                { 
                  name: 'デッドロック', 
                  description: 'デッドロックは、複数のプロセスが互いにリソースを待ち続け、処理が進まなくなる状態です。',
                  content: 'デッドロックの4つの必要条件: 相互排除（リソースが排他的に使用される）、保持と待機（リソースを保持したまま他のリソースを待つ）、非先取り（リソースを強制的に奪えない）、循環待機（プロセス間で循環的な待機関係が発生）。デッドロックの対策には、予防（4つの条件のいずれかを排除）、回避（リソースの割り当て順序を制御）、検出と回復があります。'
                },
                { 
                  name: 'メモリ管理', 
                  description: 'メモリ管理は、限られた物理メモリを効率的に使用するための技術です。',
                  content: 'ページング方式は、メモリと補助記憶装置を固定サイズのページに分割し、ページ単位で管理する方式です。外部フラグメンテーションが発生しませんが、内部フラグメンテーションが発生する可能性があります。セグメンテーション方式は、メモリを可変サイズのセグメントに分割し、セグメント単位で管理する方式です。柔軟ですが、外部フラグメンテーションが発生します。現代のOSは主にページング方式を使用しています。'
                }
              ]
            }
          ]
        },
        {
          chapterNumber: 3,
          title: '技術要素',
          introduction: 'ソフトウェア開発とデータベース、ネットワークなどの技術要素について学習します。',
          sections: [
            {
              sectionNumber: 1,
              title: 'ソフトウェア',
              description: 'ソフトウェアの種類と開発手法について学習します。',
              topics: [
                { name: 'ソフトウェアの種類', description: 'システムソフトウェアとアプリケーションソフトウェア' },
                { name: '開発手法', description: 'ウォーターフォール、アジャイル、スクラム' },
                { name: '設計手法', description: '構造化設計、オブジェクト指向設計' },
                { name: 'テスト', description: '単体テスト、統合テスト、システムテスト' }
              ]
            },
            {
              sectionNumber: 2,
              title: 'データベース',
              description: 'リレーショナルデータベースの設計と操作について学習します。データベースは、データを効率的に管理し、検索・更新・削除を行うためのシステムです。',
              topics: [
                { 
                  name: 'データベースの基礎', 
                  description: 'リレーショナルデータベースは、表（テーブル）の形式でデータを管理します。正規化により、データの冗長性を排除し、整合性を保ちます。',
                  content: 'リレーショナルモデルでは、データを行（レコード）と列（カラム）の表形式で表現します。主キーは各行を一意に識別する列で、外部キーは他のテーブルへの参照です。正規化は、第1正規形（原子値）、第2正規形（部分関数従属の排除）、第3正規形（推移的関数従属の排除）の順に進めます。正規化により、データの更新時の不整合を防ぎ、ストレージ効率を向上させますが、JOINが増加し、パフォーマンスが低下する可能性もあります。'
                },
                { 
                  name: 'SQL', 
                  description: 'SQL（Structured Query Language）は、データベースを操作するための言語です。データの取得、挿入、更新、削除が可能です。',
                  content: 'SELECT文はデータの取得に使用します。WHERE句で条件を指定し、ORDER BY句で並び替え、GROUP BY句でグループ化、HAVING句でグループ化後の条件を指定できます。JOINは複数のテーブルを結合します。INNER JOINは両方のテーブルに一致する行のみ、LEFT OUTER JOINは左テーブルの全行を保持し、RIGHT OUTER JOINは右テーブルの全行を保持します。集約関数（COUNT、SUM、AVG、MAX、MIN）は、複数の行から1つの値を計算します。'
                },
                { 
                  name: 'トランザクション', 
                  description: 'トランザクションは、複数のSQL文を1つの単位として実行し、すべて成功するか、すべて失敗するかを保証します。',
                  content: 'ACID特性: Atomicity（原子性）- すべて実行されるか、すべて実行されないか。Consistency（一貫性）- データの整合性が保たれる。Isolation（独立性）- 複数のトランザクションが互いに影響しない。Durability（永続性）- コミット後は変更が失われない。COMMITは変更を確定し、ROLLBACKは変更を取り消します。トランザクションの分離レベル（READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ、SERIALIZABLE）により、独立性の程度を制御できます。'
                },
                { 
                  name: 'インデックス', 
                  description: 'インデックスは、データベースの検索速度を向上させるためのデータ構造です。本の索引のように、データの位置を高速に検索できます。',
                  content: 'インデックスは、B-treeなどのデータ構造を使用して、O(log n)の時間でデータを検索できます。インデックスの利点は、検索速度の向上（特にWHERE句、JOIN、ORDER BY句での使用）です。欠点は、ストレージ容量の消費、INSERT、UPDATE、DELETEの処理時間の増加（インデックスの更新が必要なため）です。インデックスは、検索頻度が高い列、JOINで使用される列、ORDER BYで使用される列などに設定します。'
                }
              ]
            },
            {
              sectionNumber: 3,
              title: 'ネットワーク',
              description: 'ネットワークの基礎とプロトコルについて学習します。ネットワークは、複数のコンピュータやデバイスを接続して、データを共有・通信するための仕組みです。',
              topics: [
                { 
                  name: 'ネットワークの基礎', 
                  description: 'LAN（Local Area Network）は同一建物内のネットワーク、WAN（Wide Area Network）は広域ネットワーク、インターネットは世界中のネットワークを接続したものです。ネットワークの構成要素には、ルーター、スイッチ、ハブなどがあります。',
                  content: 'ネットワークは、物理的な接続（有線・無線）と論理的な接続（プロトコル）によって実現されます。LANは同一セグメント内の通信、WANは異なるセグメント間の通信を可能にします。'
                },
                { 
                  name: 'OSI参照モデル', 
                  description: 'OSI参照モデルは、ネットワーク通信を7層に分けて定義した理論的なモデルです。第7層（アプリケーション層）から第1層（物理層）まで、各層が異なる役割を持ちます。',
                  content: '第7層（アプリケーション層）: HTTP、FTP、SMTP、DNSなどのアプリケーションプロトコル。第6層（プレゼンテーション層）: データの変換と暗号化。第5層（セッション層）: セッションの確立と管理。第4層（トランスポート層）: TCP、UDPによるエンドツーエンドの通信制御。第3層（ネットワーク層）: IPによるルーティング。第2層（データリンク層）: Ethernet、PPPによる同一ネットワーク内の通信。第1層（物理層）: ケーブルや信号による物理的な伝送。'
                },
                { 
                  name: 'TCP/IP', 
                  description: 'TCP/IPは、実際のインターネットで使用されているプロトコルスタックです。4層構造で、OSI参照モデルと対応関係があります。',
                  content: 'アプリケーション層: HTTP、FTP、SMTP、DNSなど。トランスポート層: TCP（信頼性のある通信、順序保証、再送制御）とUDP（高速な通信、信頼性は低い）。インターネット層（IP層）: IP（ルーティング、パケット転送）、ICMP（エラー通知）、ARP（IPアドレスとMACアドレスの対応）。ネットワークインターフェース層: Ethernet、Wi-Fiなどの物理的な通信規格。'
                },
                { 
                  name: 'IPアドレス', 
                  description: 'IPアドレスは、ネットワーク上の各デバイスを一意に識別するための32ビット（IPv4）または128ビット（IPv6）の数値です。',
                  content: 'IPv4アドレスは32ビットで、通常は「192.168.1.1」のように4つの10進数で表記されます。CIDR表記（例: 192.168.1.0/24）では、スラッシュの後の数字がネットワーク部のビット数を示します。/24の場合、最初の24ビットがネットワーク部、最後の8ビットがホスト部です。サブネットマスクは、ネットワーク部とホスト部を区別するための32ビットの値で、ネットワーク部のビットは1、ホスト部のビットは0で表されます。プライベートIPアドレス（10.0.0.0/8、172.16.0.0/12、192.168.0.0/16）は、組織内のネットワークで使用され、インターネット上では直接使用されません。'
                },
                { 
                  name: 'ポート番号', 
                  description: 'ポート番号は、1つのIPアドレス上で複数のアプリケーションを識別するための16ビットの数値（0〜65535）です。',
                  content: 'Well-Known Ports（0-1023）は、よく知られたアプリケーション用に予約されています。主要なポート番号: HTTP（80）、HTTPS（443）、FTP（20、21）、SSH（22）、SMTP（25）、DNS（53）、POP3（110）、IMAP（143）など。ポート番号により、同じIPアドレス上で複数のサービスを同時に提供できます。'
                },
                { 
                  name: 'DNS', 
                  description: 'DNS（Domain Name System）は、人間が覚えやすいドメイン名（例: www.example.com）を、コンピュータが理解できるIPアドレス（例: 192.0.2.1）に変換する分散データベースシステムです。',
                  content: 'DNSレコードの種類: Aレコード（IPv4アドレス）、AAAAレコード（IPv6アドレス）、MXレコード（メールサーバー）、CNAMEレコード（別名）、NSレコード（ネームサーバー）、PTRレコード（逆引き）など。DNSは階層構造で、ルートサーバーから順に問い合わせを行います。DNSクエリには、再帰問い合わせと反復問い合わせがあります。'
                }
              ]
            },
            {
              sectionNumber: 4,
              title: 'セキュリティ',
              description: '情報セキュリティの基礎と対策について学習します。情報セキュリティは、情報の機密性、完全性、可用性を保護するための技術と対策です。',
              topics: [
                { 
                  name: '暗号化', 
                  description: '暗号化は、データを第三者に読まれないように変換する技術です。',
                  content: '公開鍵暗号方式（RSA、ECDSAなど）は、公開鍵と秘密鍵のペアを使用します。公開鍵で暗号化し、秘密鍵で復号します。鍵交換やデジタル署名に使用されますが、計算コストが高いです。共通鍵暗号方式（AES、ChaCha20など）は、同じ鍵で暗号化と復号を行います。高速ですが、鍵の安全な交換が必要です。ハッシュ関数（SHA-256など）は、任意の長さのデータから固定長のハッシュ値を生成する一方向関数です。メッセージダイジェストやパスワードのハッシュ化に使用されます。'
                },
                { 
                  name: '認証', 
                  description: '認証は、ユーザーの身元を確認するための技術です。',
                  content: 'パスワード認証は、知識（パスワード）に基づく認証です。強力なパスワードポリシー（8文字以上、大文字・小文字・数字・記号の組み合わせ）が推奨されます。2要素認証（2FA）は、知識（パスワード）と所有物（スマートフォン、トークン）の2つの要素を組み合わせて使用します。生体認証は、指紋、顔認証、虹彩など、個人の生体的特徴を使用する認証です。'
                },
                { 
                  name: 'セキュリティ攻撃', 
                  description: 'セキュリティ攻撃は、システムの脆弱性を利用して不正にアクセスしたり、データを改ざんしたりする攻撃です。',
                  content: 'SQLインジェクション攻撃は、悪意のあるSQL文をユーザー入力に注入して、データベースを不正に操作する攻撃です。対策として、プリペアドステートメント（パラメータ化クエリ）の使用が最も効果的です。XSS（Cross-Site Scripting）攻撃は、悪意のあるスクリプトをWebページに注入し、他のユーザーのブラウザで実行させる攻撃です。対策として、入力値の適切なエスケープ処理が必要です。CSRF（Cross-Site Request Forgery）攻撃は、別のサイトからのリクエストを利用してユーザーに操作を実行させる攻撃です。対策として、CSRFトークンの使用が必要です。DoS攻撃は、大量のリクエストを送信してサービスを停止させる攻撃です。'
                },
                { 
                  name: 'セキュリティ対策', 
                  description: 'セキュリティ対策は、セキュリティ攻撃からシステムを保護するための技術と対策です。',
                  content: 'ファイアウォールは、ネットワークトラフィックを監視し、許可された通信のみを通すことで、不正なアクセスを防ぎます。パケットフィルタリング、ステートフルインスペクション、アプリケーションゲートウェイなどの機能があります。IDS（Intrusion Detection System）は、不正なアクセスを検出するシステムです。IPS（Intrusion Prevention System）は、不正なアクセスを検出し、自動的にブロックするシステムです。SSL/TLSは、Web通信を暗号化するプロトコルで、公開鍵暗号と共通鍵暗号を組み合わせて使用します。'
                }
              ]
            }
          ]
        },
        {
          chapterNumber: 4,
          title: '開発技術',
          introduction: 'プログラミングと開発環境について学習します。',
          sections: [
            {
              sectionNumber: 1,
              title: 'プログラミング',
              description: 'プログラミング言語の基礎とアルゴリズムの実装について学習します。',
              topics: [
                { name: 'プログラミング言語', description: '手続き型、オブジェクト指向、関数型' },
                { name: '制御構造', description: '条件分岐、繰り返し、例外処理' },
                { name: 'データ構造', description: '配列、リスト、スタック、キュー、木構造' }
              ]
            },
            {
              sectionNumber: 2,
              title: '開発環境',
              description: '開発ツールとバージョン管理について学習します。',
              topics: [
                { name: 'IDE', description: '統合開発環境の機能と使い方' },
                { name: 'バージョン管理', description: 'Gitの基本操作とブランチ戦略' },
                { name: 'デバッグ', description: 'デバッグ手法とツール' }
              ]
            }
          ]
        }
      ];
    },
    getTextbookReferences(question) {
      // 問題の内容に基づいて、関連する教科書の箇所を返す
      const references = [];
      const category = question.category;
      const text = question.question_text + ' ' + (question.explanation || '');

      // ネットワーク関連
      if (category === 'ネットワーク') {
        if (text.includes('OSI参照モデル') || text.includes('OSI') || (text.includes('第') && text.includes('層'))) {
          references.push({
            chapter: 3,
            section: 3,
            topic: 'OSI参照モデル',
            description: 'OSI参照モデルの7層構造と各層の役割について、第3章第3節の「OSI参照モデル」を参照してください。',
            keyPoints: [
              '第7層（アプリケーション層）から第1層（物理層）までの各層の役割',
              'TCP/IPプロトコルスタックとの対応関係',
              '各層で使用される主要なプロトコル'
            ]
          });
        }
        if (text.includes('ポート') || text.includes('ポート番号')) {
          references.push({
            chapter: 3,
            section: 3,
            topic: 'ポート番号',
            description: 'ポート番号の役割と主要なポート番号について、第3章第3節の「ポート番号」を参照してください。',
            keyPoints: [
              'ポート番号の役割（アプリケーションの識別）',
              '主要なポート番号（HTTP: 80、HTTPS: 443、SSH: 22など）',
              'Well-Known Ports（0-1023）の範囲'
            ]
          });
        }
        if (text.includes('IPアドレス') || text.includes('サブネット') || text.includes('/24') || text.includes('CIDR')) {
          references.push({
            chapter: 3,
            section: 3,
            topic: 'IPアドレス',
            description: 'IPアドレスの構造とサブネットマスクについて、第3章第3節の「IPアドレス」を参照してください。',
            keyPoints: [
              'IPv4アドレスの構造（32ビット）',
              'CIDR表記とサブネットマスク',
              'ネットワーク部とホスト部の区別',
              'プライベートIPアドレスの範囲'
            ]
          });
        }
        if (text.includes('TCP') || text.includes('UDP') || text.includes('TCP/IP')) {
          references.push({
            chapter: 3,
            section: 3,
            topic: 'TCP/IP',
            description: 'TCP/IPプロトコルスタックについて、第3章第3節の「TCP/IP」を参照してください。',
            keyPoints: [
              'TCPとUDPの違い（信頼性 vs 高速性）',
              'TCP/IPプロトコルスタックの4層構造',
              '各層の主要なプロトコル'
            ]
          });
        }
        if (text.includes('DNS') || text.includes('ドメイン名')) {
          references.push({
            chapter: 3,
            section: 3,
            topic: 'DNS',
            description: 'DNSの仕組みとドメイン名解決について、第3章第3節の「DNS」を参照してください。',
            keyPoints: [
              'DNSの役割（ドメイン名とIPアドレスの変換）',
              'DNSレコードの種類（A、AAAA、MX、CNAMEなど）',
              'DNSの階層構造'
            ]
          });
        }
      }

      // データベース関連
      if (category === 'データベース') {
        if (text.includes('正規化') || text.includes('第') && text.includes('正規形')) {
          references.push({
            chapter: 3,
            section: 2,
            topic: 'データベースの基礎',
            description: 'データベースの正規化について、第3章第2節の「データベースの基礎」を参照してください。',
            keyPoints: [
              '第1正規形から第3正規形までの正規化の手順',
              '部分関数従属と推移的関数従属の排除',
              '正規化のメリットとデメリット'
            ]
          });
        }
        if (text.includes('SQL') || text.includes('SELECT') || text.includes('JOIN')) {
          references.push({
            chapter: 3,
            section: 2,
            topic: 'SQL',
            description: 'SQL文の書き方について、第3章第2節の「SQL」を参照してください。',
            keyPoints: [
              'SELECT文の基本構文',
              'WHERE句、ORDER BY句、GROUP BY句の使い方',
              'JOINの種類（INNER、LEFT、RIGHT、FULL OUTER JOIN）',
              '集約関数（COUNT、SUM、AVG、MAX、MIN）'
            ]
          });
        }
        if (text.includes('トランザクション') || text.includes('ACID') || text.includes('COMMIT')) {
          references.push({
            chapter: 3,
            section: 2,
            topic: 'トランザクション',
            description: 'トランザクションとACID特性について、第3章第2節の「トランザクション」を参照してください。',
            keyPoints: [
              'ACID特性（原子性、一貫性、独立性、永続性）',
              'COMMITとROLLBACKの使い方',
              'トランザクションの分離レベル'
            ]
          });
        }
        if (text.includes('インデックス')) {
          references.push({
            chapter: 3,
            section: 2,
            topic: 'インデックス',
            description: 'インデックスの役割と設計について、第3章第2節の「インデックス」を参照してください。',
            keyPoints: [
              'インデックスの役割（検索速度の向上）',
              'インデックスのメリットとデメリット',
              'インデックスの設計指針'
            ]
          });
        }
      }

      // セキュリティ関連
      if (category === 'セキュリティ') {
        if (text.includes('暗号') || text.includes('RSA') || text.includes('AES') || text.includes('ハッシュ')) {
          references.push({
            chapter: 3,
            section: 4,
            topic: '暗号化',
            description: '暗号化の基礎について、第3章第4節の「暗号化」を参照してください。',
            keyPoints: [
              '公開鍵暗号と共通鍵暗号の違い',
              'RSA暗号の仕組みと鍵長',
              'ハッシュ関数（SHA-256など）の役割',
              'SSL/TLSでの暗号化の使い分け'
            ]
          });
        }
        if (text.includes('SQLインジェクション') || text.includes('XSS') || text.includes('CSRF') || text.includes('攻撃')) {
          references.push({
            chapter: 3,
            section: 4,
            topic: 'セキュリティ攻撃',
            description: '主要なセキュリティ攻撃と対策について、第3章第4節の「セキュリティ攻撃」を参照してください。',
            keyPoints: [
              'SQLインジェクション攻撃と対策（プリペアドステートメント）',
              'XSS攻撃と対策（入力値のエスケープ）',
              'CSRF攻撃と対策（CSRFトークン）',
              'OWASP Top 10の主要なセキュリティリスク'
            ]
          });
        }
      }

      // ハードウェア関連
      if (category === 'ハードウェア') {
        if (text.includes('CPU') || text.includes('プロセッサ') || text.includes('パイプライン')) {
          references.push({
            chapter: 2,
            section: 1,
            topic: 'プロセッサ',
            description: 'CPUの構造と動作について、第2章第1節の「プロセッサ」を参照してください。',
            keyPoints: [
              'CPUの構成要素（制御装置、演算装置、レジスタ）',
              '命令の実行サイクル',
              'パイプライン処理による高速化',
              'スーパースカラ方式とアウトオブオーダー実行'
            ]
          });
        }
        if (text.includes('キャッシュ') || text.includes('メモリ') || text.includes('L1') || text.includes('L2')) {
          references.push({
            chapter: 2,
            section: 2,
            topic: 'メモリ',
            description: 'メモリの種類と階層構造について、第2章第2節の「メモリ」を参照してください。',
            keyPoints: [
              'メモリの種類（DRAM、SRAM、ROM）',
              'キャッシュメモリの階層（L1、L2、L3）',
              'メモリ階層とアクセス速度の関係',
              '仮想メモリの仕組み'
            ]
          });
        }
        if (text.includes('RAID')) {
          references.push({
            chapter: 2,
            section: 3,
            topic: 'ストレージ',
            description: 'RAID構成について、第2章第3節の「ストレージ」を参照してください。',
            keyPoints: [
              'RAID 0、RAID 1、RAID 5、RAID 6の特徴',
              '冗長性と性能のバランス',
              '使用可能容量の計算方法'
            ]
          });
        }
      }

      // アルゴリズム関連
      if (category === 'アルゴリズム') {
        if (text.includes('探索') || text.includes('ソート') || text.includes('計算量') || text.includes('O(')) {
          references.push({
            chapter: 1,
            section: 3,
            topic: 'アルゴリズムとデータ構造',
            description: 'アルゴリズムの基本とデータ構造について、第1章第3節の「アルゴリズムとデータ構造」を参照してください。',
            keyPoints: [
              '時間計算量の表記法（O記法）',
              '探索アルゴリズム（線形探索、二分探索）',
              'ソートアルゴリズム（バブルソート、クイックソート、マージソート）',
              'データ構造の選択指針'
            ]
          });
        }
        if (text.includes('データ構造') || text.includes('スタック') || text.includes('キュー')) {
          references.push({
            chapter: 1,
            section: 3,
            topic: 'データ構造',
            description: 'データ構造の種類と特徴について、第1章第3節の「データ構造」を参照してください。',
            keyPoints: [
              '配列、リスト、スタック、キュー、木構造の特徴',
              '各データ構造の操作の時間計算量',
              '用途に応じたデータ構造の選択'
            ]
          });
        }
      }

      // OS関連
      if (category === 'OS' || category === 'オペレーティングシステム') {
        if (text.includes('プロセス') || text.includes('スレッド') || text.includes('マルチタスク')) {
          references.push({
            chapter: 2,
            section: 4,
            topic: 'プロセスとスレッド',
            description: 'プロセスとスレッドの違いについて、第2章第4節の「プロセスとスレッド」を参照してください。',
            keyPoints: [
              'プロセスとスレッドの違い',
              'マルチプロセスとマルチスレッド',
              'プロセスの状態遷移',
              'コンテキストスイッチの仕組み'
            ]
          });
        }
        if (text.includes('デッドロック')) {
          references.push({
            chapter: 2,
            section: 4,
            topic: 'デッドロック',
            description: 'デッドロックの発生条件と対策について、第2章第4節の「デッドロック」を参照してください。',
            keyPoints: [
              'デッドロックの4つの必要条件',
              'デッドロックの予防、回避、検出と回復',
              'リソースの割り当て順序の統一'
            ]
          });
        }
        if (text.includes('ページング') || text.includes('仮想メモリ')) {
          references.push({
            chapter: 2,
            section: 4,
            topic: 'メモリ管理',
            description: 'メモリ管理の仕組みについて、第2章第4節の「メモリ管理」を参照してください。',
            keyPoints: [
              'ページング方式とセグメンテーション方式',
              '仮想メモリの仕組み',
              'ページフォルトとスワッピング'
            ]
          });
        }
      }

      // ソフトウェア開発関連
      if (category === 'ソフトウェア開発') {
        if (text.includes('スクラム') || text.includes('アジャイル')) {
          references.push({
            chapter: 3,
            section: 1,
            topic: '開発手法',
            description: 'アジャイル開発とスクラムについて、第3章第1節の「開発手法」を参照してください。',
            keyPoints: [
              'アジャイル開発の原則',
              'スクラムの役割（プロダクトオーナー、スクラムマスター、開発チーム）',
              'スプリントの流れ',
              'スクラムのイベントと成果物'
            ]
          });
        }
        if (text.includes('Git') || text.includes('バージョン管理')) {
          references.push({
            chapter: 4,
            section: 2,
            topic: 'バージョン管理',
            description: 'Gitの基本操作について、第4章第2節の「バージョン管理」を参照してください。',
            keyPoints: [
              'Gitの主要なコマンド（clone、add、commit、push、pull）',
              'ブランチの作成とマージ',
              'Git Flowなどのブランチ戦略'
            ]
          });
        }
        if (text.includes('テスト') || text.includes('単体') || text.includes('統合')) {
          references.push({
            chapter: 3,
            section: 1,
            topic: 'テスト',
            description: 'テスト手法について、第3章第1節の「テスト」を参照してください。',
            keyPoints: [
              'テストの種類（単体、統合、システム、E2E）',
              'ブラックボックステストとホワイトボックステスト',
              'テストのピラミッド',
              'テストカバレッジ'
            ]
          });
        }
      }

      // デフォルト: カテゴリに基づく参照
      if (references.length === 0) {
        const categoryMap = {
          'ネットワーク': { chapter: 3, section: 3, topic: 'ネットワークの基礎' },
          'データベース': { chapter: 3, section: 2, topic: 'データベースの基礎' },
          'セキュリティ': { chapter: 3, section: 4, topic: 'セキュリティの基礎' },
          'ハードウェア': { chapter: 2, section: 1, topic: 'コンピュータシステムの基礎' },
          'アルゴリズム': { chapter: 1, section: 3, topic: 'アルゴリズムとデータ構造' },
          'OS': { chapter: 2, section: 4, topic: 'オペレーティングシステム' },
          'オペレーティングシステム': { chapter: 2, section: 4, topic: 'オペレーティングシステム' },
          'ソフトウェア開発': { chapter: 3, section: 1, topic: 'ソフトウェア開発の基礎' }
        };

        const defaultRef = categoryMap[category];
        if (defaultRef) {
          references.push({
            chapter: defaultRef.chapter,
            section: defaultRef.section,
            topic: defaultRef.topic,
            description: `${category}に関する基礎知識について、第${defaultRef.chapter}章第${defaultRef.section}節の「${defaultRef.topic}」を参照してください。`,
            keyPoints: []
          });
        }
      }

      return references;
    },
    getChapterTitle(chapterNumber) {
      const chapter = this.textbookStructure.find(c => c.chapterNumber === chapterNumber);
      return chapter ? chapter.title : '';
    },
    getSectionTitle(chapterNumber, sectionNumber) {
      const chapter = this.textbookStructure.find(c => c.chapterNumber === chapterNumber);
      if (!chapter) return '';
      const section = chapter.sections.find(s => s.sectionNumber === sectionNumber);
      return section ? section.title : '';
    },
    getSectionDescription(chapterNumber, sectionNumber) {
      const chapter = this.textbookStructure.find(c => c.chapterNumber === chapterNumber);
      if (!chapter) return '';
      const section = chapter.sections.find(s => s.sectionNumber === sectionNumber);
      return section ? section.description : '';
    },
    getTopicContent(chapterNumber, sectionNumber, topicName) {
      const chapter = this.textbookStructure.find(c => c.chapterNumber === chapterNumber);
      if (!chapter) return '';
      const section = chapter.sections.find(s => s.sectionNumber === sectionNumber);
      if (!section || !section.topics) return '';
      // トピック名に一致する項目を探す
      const topic = section.topics.find(t => 
        t.name === topicName || 
        t.name.includes(topicName) || 
        topicName.includes(t.name)
      );
      return topic && topic.content ? topic.content : '';
    },
    getTopicKeyPoints(chapterNumber, sectionNumber, topicName) {
      const chapter = this.textbookStructure.find(c => c.chapterNumber === chapterNumber);
      if (!chapter) return [];
      const section = chapter.sections.find(s => s.sectionNumber === sectionNumber);
      if (!section || !section.topics) return [];
      // トピック名に一致する項目を探す
      const topic = section.topics.find(t => 
        t.name === topicName || 
        t.name.includes(topicName) || 
        topicName.includes(t.name)
      );
      return topic && topic.keyPoints ? topic.keyPoints : [];
    },
    getTopicDetails(chapterNumber, sectionNumber, topicName) {
      const chapter = this.textbookStructure.find(c => c.chapterNumber === chapterNumber);
      if (!chapter) return null;
      const section = chapter.sections.find(s => s.sectionNumber === sectionNumber);
      if (!section || !section.topics) return null;
      // トピック名に一致する項目を返す
      const topic = section.topics.find(t => 
        t.name === topicName || 
        t.name.includes(topicName) || 
        topicName.includes(t.name)
      );
      if (topic) {
        return [topic];
      }
      // 一致しない場合は、その節のすべての項目を返す
      return section.topics;
    },
    generateDiagrams(question) {
      const diagrams = [];
      const category = question.category;
      const text = question.question_text + ' ' + (question.explanation || '');

      // ネットワーク関連の図表
      if (category === 'ネットワーク') {
        // OSI参照モデルの図
        if (text.includes('OSI参照モデル') || text.includes('OSI') || text.includes('第') && text.includes('層')) {
          diagrams.push({
            type: 'ascii',
            title: 'OSI参照モデル（7層構造）',
            content: `┌─────────────────────────────────────┐
│ 第7層  アプリケーション層 (Application)  │  HTTP, FTP, SMTP, DNS
├─────────────────────────────────────┤
│ 第6層  プレゼンテーション層 (Presentation)│  SSL/TLS, データ変換
├─────────────────────────────────────┤
│ 第5層  セッション層 (Session)         │  セッション管理
├─────────────────────────────────────┤
│ 第4層  トランスポート層 (Transport)    │  TCP, UDP
├─────────────────────────────────────┤
│ 第3層  ネットワーク層 (Network)       │  IP, ICMP, ARP
├─────────────────────────────────────┤
│ 第2層  データリンク層 (Data Link)     │  Ethernet, PPP
├─────────────────────────────────────┤
│ 第1層  物理層 (Physical)             │  ケーブル, 信号
└─────────────────────────────────────┘`
          });
        }

        // ポート番号の表
        if (text.includes('ポート') || text.includes('ポート番号')) {
          diagrams.push({
            type: 'table',
            title: '主要なポート番号一覧',
            headers: ['ポート番号', 'プロトコル', '用途'],
            rows: [
              ['20, 21', 'FTP', 'ファイル転送'],
              ['22', 'SSH', 'セキュアなリモートログイン'],
              ['23', 'Telnet', 'リモートログイン'],
              ['25', 'SMTP', 'メール送信'],
              ['53', 'DNS', 'ドメイン名解決'],
              ['80', 'HTTP', 'Web通信'],
              ['110', 'POP3', 'メール受信'],
              ['143', 'IMAP', 'メール受信'],
              ['443', 'HTTPS', '暗号化Web通信'],
              ['3306', 'MySQL', 'データベース'],
              ['5432', 'PostgreSQL', 'データベース']
            ]
          });
        }

        // TCP/IPプロトコルスタック
        if (text.includes('TCP/IP') || text.includes('TCP') || text.includes('UDP')) {
          diagrams.push({
            type: 'ascii',
            title: 'TCP/IPプロトコルスタック',
            content: `┌─────────────────────────────┐
│  アプリケーション層              │
│  (HTTP, FTP, SMTP, DNS等)       │
├─────────────────────────────┤
│  トランスポート層                │
│  TCP (信頼性) / UDP (高速)      │
├─────────────────────────────┤
│  インターネット層 (IP層)         │
│  IP (ルーティング)              │
├─────────────────────────────┤
│  ネットワークインターフェース層  │
│  Ethernet, Wi-Fi等             │
└─────────────────────────────┘`
          });
        }

        // IPアドレスの構造
        if (text.includes('IPアドレス') || text.includes('/24') || text.includes('サブネット')) {
          diagrams.push({
            type: 'table',
            title: 'CIDR表記とサブネットマスク',
            headers: ['CIDR表記', 'サブネットマスク', 'ネットワーク部', 'ホスト部', '使用可能ホスト数'],
            rows: [
              ['/24', '255.255.255.0', '24ビット', '8ビット', '254'],
              ['/25', '255.255.255.128', '25ビット', '7ビット', '126'],
              ['/26', '255.255.255.192', '26ビット', '6ビット', '62'],
              ['/27', '255.255.255.224', '27ビット', '5ビット', '30'],
              ['/28', '255.255.255.240', '28ビット', '4ビット', '14']
            ]
          });
        }
      }

      // データベース関連の図表
      if (category === 'データベース') {
        // 正規化の図
        if (text.includes('正規化') || text.includes('第') && text.includes('正規形')) {
          diagrams.push({
            type: 'ascii',
            title: 'データベース正規化の階層',
            content: `非正規形 (UNF)
    ↓ 第1正規形 (1NF): 原子値にする
第1正規形 (1NF)
    ↓ 第2正規形 (2NF): 部分関数従属を排除
第2正規形 (2NF)
    ↓ 第3正規形 (3NF): 推移的関数従属を排除
第3正規形 (3NF)
    ↓ ボイス・コッド正規形 (BCNF)
ボイス・コッド正規形 (BCNF)
    ↓ 第4正規形 (4NF): 多値従属を排除
第4正規形 (4NF)
    ↓ 第5正規形 (5NF): 結合従属を排除
第5正規形 (5NF)`
          });
        }

        // SQL JOINの図
        if (text.includes('JOIN') || text.includes('結合')) {
          diagrams.push({
            type: 'table',
            title: 'SQL JOINの種類',
            headers: ['JOINの種類', '説明', '結果'],
            rows: [
              ['INNER JOIN', '両方のテーブルに一致する行のみ', '共通部分'],
              ['LEFT OUTER JOIN', '左テーブルの全行 + 右テーブルの一致行', '左テーブル優先'],
              ['RIGHT OUTER JOIN', '右テーブルの全行 + 左テーブルの一致行', '右テーブル優先'],
              ['FULL OUTER JOIN', '両方のテーブルの全行', 'すべての行'],
              ['CROSS JOIN', 'すべての行の組み合わせ', '直積']
            ]
          });
        }

        // ACID特性の表
        if (text.includes('ACID') || text.includes('トランザクション')) {
          diagrams.push({
            type: 'table',
            title: 'ACID特性の詳細',
            headers: ['特性', '英語名', '説明'],
            rows: [
              ['原子性', 'Atomicity', 'すべて実行されるか、すべて実行されないか'],
              ['一貫性', 'Consistency', 'データの整合性が保たれる'],
              ['独立性', 'Isolation', '複数のトランザクションが互いに影響しない'],
              ['永続性', 'Durability', 'コミット後は変更が失われない']
            ]
          });
        }
      }

      // セキュリティ関連の図表
      if (category === 'セキュリティ') {
        // 暗号化方式の比較
        if (text.includes('暗号') || text.includes('RSA') || text.includes('AES')) {
          diagrams.push({
            type: 'table',
            title: '暗号化方式の比較',
            headers: ['方式', '種類', '特徴', '用途'],
            rows: [
              ['RSA', '公開鍵暗号', '鍵長: 2048bit以上推奨', '鍵交換、デジタル署名'],
              ['AES', '共通鍵暗号', '鍵長: 128/192/256bit', 'データ暗号化'],
              ['SHA-256', 'ハッシュ関数', '256bit出力', 'メッセージダイジェスト'],
              ['SSL/TLS', 'プロトコル', '公開鍵+共通鍵の組み合わせ', 'Web通信の暗号化']
            ]
          });
        }

        // 攻撃手法の分類
        if (text.includes('攻撃') || text.includes('インジェクション') || text.includes('XSS')) {
          diagrams.push({
            type: 'list',
            title: '主要なセキュリティ攻撃と対策',
            items: [
              { label: 'SQLインジェクション', value: '対策: プリペアドステートメントの使用' },
              { label: 'XSS (Cross-Site Scripting)', value: '対策: 入力値のエスケープ処理' },
              { label: 'CSRF (Cross-Site Request Forgery)', value: '対策: CSRFトークンの使用' },
              { label: 'パスワードクラック', value: '対策: 強力なパスワード、2要素認証' },
              { label: 'DoS攻撃', value: '対策: レート制限、DDoS対策サービス' }
            ]
          });
        }
      }

      // ハードウェア関連の図表
      if (category === 'ハードウェア') {
        // メモリ階層
        if (text.includes('キャッシュ') || text.includes('メモリ') || text.includes('L1') || text.includes('L2')) {
          diagrams.push({
            type: 'ascii',
            title: 'メモリ階層（速度と容量の関係）',
            content: `速度 ↑
│
│  L1キャッシュ (最小、最速)
│  L2キャッシュ
│  L3キャッシュ
│  主記憶装置 (DRAM)
│  補助記憶装置 (SSD/HDD)
│
容量 →`
          });
        }

        // RAID構成の表
        if (text.includes('RAID')) {
          diagrams.push({
            type: 'table',
            title: 'RAIDレベル比較',
            headers: ['RAIDレベル', '構成', '冗長性', '性能', '使用可能容量'],
            rows: [
              ['RAID 0', 'ストライピング', 'なし', '高速', '100%'],
              ['RAID 1', 'ミラーリング', '1台まで', '読み取り高速', '50%'],
              ['RAID 5', 'パリティ分散', '1台まで', '高速', 'n-1台分'],
              ['RAID 6', '2重パリティ', '2台まで', '高速', 'n-2台分'],
              ['RAID 10', 'RAID 1+0', '各グループ1台まで', '最高速', '50%']
            ]
          });
        }
      }

      // OS関連の図表
      if (category === 'OS' || category === 'オペレーティングシステム') {
        // プロセス状態遷移
        if (text.includes('プロセス') || text.includes('スレッド')) {
          diagrams.push({
            type: 'ascii',
            title: 'プロセスの状態遷移',
            content: `新規作成
    ↓
実行可能 (Ready)
    ↓ ← スケジューラ選択
実行中 (Running)
    ↓ ← タイムスライス終了
    ↓ ← I/O待ち
待機 (Waiting/Blocked)
    ↓ ← I/O完了
    ↓
終了 (Terminated)`
          });
        }

        // デッドロックの条件
        if (text.includes('デッドロック')) {
          diagrams.push({
            type: 'list',
            title: 'デッドロックの4つの必要条件',
            items: [
              { label: '相互排除 (Mutual Exclusion)', value: 'リソースが排他的に使用される' },
              { label: '保持と待機 (Hold and Wait)', value: 'リソースを保持したまま他のリソースを待つ' },
              { label: '非先取り (No Preemption)', value: 'リソースを強制的に奪えない' },
              { label: '循環待機 (Circular Wait)', value: 'プロセス間で循環的な待機関係が発生' }
            ]
          });
        }
      }

      // ソフトウェア開発関連の図表
      if (category === 'ソフトウェア開発') {
        // スクラムの流れ
        if (text.includes('スクラム') || text.includes('アジャイル')) {
          diagrams.push({
            type: 'ascii',
            title: 'スクラムの開発フロー',
            content: `プロダクトバックログ
    ↓
スプリントプランニング
    ↓
スプリントバックログ
    ↓
スプリント (1-4週間)
    ├─ デイリースクラム
    ├─ 開発作業
    └─ スプリントレビュー
    ↓
インクリメント (完成した機能)
    ↓
スプリントレトロスペクティブ
    ↓
次のスプリント`
          });
        }

        // テストのピラミッド
        if (text.includes('テスト') || text.includes('単体') || text.includes('統合')) {
          diagrams.push({
            type: 'ascii',
            title: 'テストのピラミッド',
            content: `        E2Eテスト
      (少ない、高コスト)
    ────────────────
     統合テスト
    ────────────────
   単体テスト
  (多い、低コスト)`
          });
        }
      }

      // アルゴリズム関連の図表
      if (category === 'アルゴリズム') {
        // 時間計算量の比較
        if (text.includes('計算量') || text.includes('O(') || text.includes('時間')) {
          diagrams.push({
            type: 'table',
            title: 'アルゴリズムの時間計算量',
            headers: ['アルゴリズム', '最良', '平均', '最悪', '備考'],
            rows: [
              ['線形探索', 'O(1)', 'O(n)', 'O(n)', 'ソート不要'],
              ['二分探索', 'O(1)', 'O(log n)', 'O(log n)', 'ソート済み必要'],
              ['バブルソート', 'O(n)', 'O(n²)', 'O(n²)', '安定ソート'],
              ['クイックソート', 'O(n log n)', 'O(n log n)', 'O(n²)', '高速'],
              ['マージソート', 'O(n log n)', 'O(n log n)', 'O(n log n)', '安定ソート']
            ]
          });
        }

        // データ構造の比較
        if (text.includes('データ構造') || text.includes('スタック') || text.includes('キュー')) {
          diagrams.push({
            type: 'table',
            title: '主要なデータ構造の特徴',
            headers: ['データ構造', 'アクセス', '追加', '削除', '用途'],
            rows: [
              ['配列', 'O(1)', 'O(n)', 'O(n)', 'ランダムアクセス'],
              ['連結リスト', 'O(n)', 'O(1)', 'O(1)', '動的サイズ'],
              ['スタック', 'O(1)', 'O(1)', 'O(1)', 'LIFO'],
              ['キュー', 'O(1)', 'O(1)', 'O(1)', 'FIFO'],
              ['ハッシュテーブル', 'O(1)', 'O(1)', 'O(1)', '高速検索']
            ]
          });
        }
      }

      return diagrams;
    },
    generateRelatedKnowledge(question) {
      const knowledge = [];
      const category = question.category;
      const text = question.question_text + ' ' + (question.explanation || '');

      // ネットワーク関連の周辺知識
      if (category === 'ネットワーク') {
        if (text.includes('OSI参照モデル')) {
          knowledge.push({
            title: 'OSI参照モデルとTCP/IPの対応関係',
            content: 'OSI参照モデルは理論的な7層モデルですが、実際のインターネットではTCP/IP（4層モデル）が使用されています。OSIの第5〜7層がTCP/IPのアプリケーション層に、第4層がトランスポート層に、第3層がインターネット層に、第1〜2層がネットワークインターフェース層に対応します。',
            points: [
              'OSI参照モデルは学習用の概念モデル',
              'TCP/IPは実装されたプロトコルスタック',
              '実際のネットワークではTCP/IPが主流'
            ]
          });
        }

        if (text.includes('ポート')) {
          knowledge.push({
            title: 'ポート番号の覚え方',
            content: 'よく使用されるポート番号は語呂合わせで覚えると便利です。',
            points: [
              'HTTP (80): ハッピー（80）なWeb閲覧',
              'HTTPS (443): よっしー（443）安全に',
              'SSH (22): にーにー（22）セキュアに',
              'FTP (21): ふーとー（21）ファイル転送',
              'DNS (53): ごーさん（53）名前解決'
            ]
          });
        }

        if (text.includes('IPアドレス') || text.includes('サブネット')) {
          knowledge.push({
            title: 'プライベートIPアドレス',
            content: 'プライベートIPアドレスは、インターネット上で直接使用されず、組織内のネットワークで使用されるIPアドレスです。',
            points: [
              '10.0.0.0/8: 大規模ネットワーク用',
              '172.16.0.0/12: 中規模ネットワーク用',
              '192.168.0.0/16: 小規模ネットワーク用（家庭用ルーターなど）',
              'NAT（Network Address Translation）でグローバルIPに変換'
            ]
          });
        }
      }

      // データベース関連の周辺知識
      if (category === 'データベース') {
        if (text.includes('正規化')) {
          knowledge.push({
            title: '正規化のメリット・デメリット',
            content: '正規化はデータの整合性を保つために重要ですが、過度な正規化はパフォーマンスを低下させる可能性があります。',
            points: [
              'メリット: データの冗長性削減、更新時の不整合防止、ストレージ効率向上',
              'デメリット: JOINが増加、クエリが複雑化、パフォーマンス低下の可能性',
              '実務では、用途に応じて適切な正規化レベルを選択',
              '非正規化（デノーマライゼーション）も有効な手段'
            ]
          });
        }

        if (text.includes('インデックス')) {
          knowledge.push({
            title: 'インデックスの設計指針',
            content: 'インデックスは検索速度を向上させますが、適切に設計する必要があります。',
            points: [
              'WHERE句で頻繁に使用される列に設定',
              'JOINで使用される外部キーに設定',
              'ORDER BYで使用される列に設定',
              '更新頻度が高い列には慎重に設定',
              '複合インデックスは列の順序が重要'
            ]
          });
        }
      }

      // セキュリティ関連の周辺知識
      if (category === 'セキュリティ') {
        if (text.includes('RSA') || text.includes('暗号')) {
          knowledge.push({
            title: '暗号化の実務での使い分け',
            content: '暗号化方式は用途に応じて使い分けます。',
            points: [
              '公開鍵暗号（RSA）: 鍵交換、デジタル署名に使用（計算コストが高い）',
              '共通鍵暗号（AES）: データ暗号化に使用（高速）',
              'ハイブリッド方式: 公開鍵で共通鍵を交換し、その後は共通鍵で通信',
              'SSL/TLSはハイブリッド方式を採用'
            ]
          });
        }

        if (text.includes('SQLインジェクション') || text.includes('XSS')) {
          knowledge.push({
            title: 'OWASP Top 10',
            content: 'OWASP（Open Web Application Security Project）が発表する、Webアプリケーションの主要なセキュリティリスクです。',
            points: [
              '1. インジェクション（SQL、OS、LDAP等）',
              '2. 認証の不備',
              '3. 機密データの露出',
              '4. XML外部エンティティ（XXE）',
              '5. アクセス制御の不備',
              '6. セキュリティ設定の不備',
              '7. XSS（Cross-Site Scripting）',
              '8. 安全でないデシリアライゼーション',
              '9. 既知の脆弱性のあるコンポーネント',
              '10. 不十分なロギングとモニタリング'
            ]
          });
        }
      }

      // ハードウェア関連の周辺知識
      if (category === 'ハードウェア') {
        if (text.includes('キャッシュ') || text.includes('メモリ')) {
          knowledge.push({
            title: 'キャッシュメモリの重要性',
            content: 'CPUと主記憶装置の速度差を埋めるために、キャッシュメモリが重要な役割を果たします。',
            points: [
              'CPUの速度: 数GHz（数ナノ秒）',
              '主記憶装置の速度: 数十ナノ秒',
              'キャッシュヒット率が高いほど性能が向上',
              'キャッシュミスが発生すると、主記憶からデータを取得する必要があり遅延が発生',
              '最近使用されたデータ（時間的局所性）や近くのデータ（空間的局所性）がキャッシュに保持される'
            ]
          });
        }
      }

      // アルゴリズム関連の周辺知識
      if (category === 'アルゴリズム') {
        if (text.includes('ソート') || text.includes('探索')) {
          knowledge.push({
            title: 'アルゴリズムの選択指針',
            content: 'データの特性や要件に応じて、適切なアルゴリズムを選択することが重要です。',
            points: [
              'データ量が少ない場合: シンプルなアルゴリズム（バブルソート、線形探索）',
              'データ量が多い場合: 効率的なアルゴリズム（クイックソート、二分探索）',
              '安定性が必要な場合: マージソート、バブルソート',
              'メモリ制約がある場合: インプレースソート（クイックソート）',
              '既にソート済みの場合: 挿入ソートが高速'
            ]
          });
        }
      }

      // OS関連の周辺知識
      if (category === 'OS' || category === 'オペレーティングシステム') {
        if (text.includes('プロセス') || text.includes('スレッド')) {
          knowledge.push({
            title: 'プロセスとスレッドの違い',
            content: 'プロセスとスレッドは、OSの実行単位ですが、異なる特徴があります。',
            points: [
              'プロセス: 独立したメモリ空間を持つ、重い、通信にコストがかかる',
              'スレッド: 同じメモリ空間を共有、軽い、通信が容易',
              'マルチプロセス: 独立性が高い、クラッシュの影響が局所化',
              'マルチスレッド: 効率的、共有リソースの同期が必要',
              '実務では、用途に応じて使い分ける'
            ]
          });
        }

        if (text.includes('ページング') || text.includes('仮想メモリ')) {
          knowledge.push({
            title: 'ページングとセグメンテーション',
            content: 'メモリ管理には、ページング方式とセグメンテーション方式があります。',
            points: [
              'ページング: 固定サイズ、外部フラグメンテーションなし、内部フラグメンテーションあり',
              'セグメンテーション: 可変サイズ、外部フラグメンテーションあり、柔軟',
              '現代のOSは主にページング方式を使用',
              '仮想メモリにより、物理メモリより大きなアドレス空間を使用可能',
              'ページフォルトが発生すると、OSがページをスワップイン'
            ]
          });
        }
      }

      // ソフトウェア開発関連の周辺知識
      if (category === 'ソフトウェア開発') {
        if (text.includes('スクラム') || text.includes('アジャイル')) {
          knowledge.push({
            title: 'アジャイル開発の原則',
            content: 'アジャイル開発は、変化に対応し、顧客価値を早期に提供する開発手法です。',
            points: [
              '個人と対話がプロセスやツールより重要',
              '動くソフトウェアが包括的なドキュメントより重要',
              '顧客との協調が契約交渉より重要',
              '変化への対応が計画に従うことより重要',
              '短いスプリントで継続的に価値を提供'
            ]
          });
        }

        if (text.includes('Git') || text.includes('バージョン管理')) {
          knowledge.push({
            title: 'Gitの主要なコマンド',
            content: 'Gitは分散バージョン管理システムで、効率的な開発を支援します。',
            points: [
              'git clone: リポジトリをクローン',
              'git add: 変更をステージング',
              'git commit: 変更をコミット',
              'git push: リモートにプッシュ',
              'git pull: リモートから取得',
              'git branch: ブランチ管理',
              'git merge: ブランチをマージ',
              'git rebase: 履歴を書き換え'
            ]
          });
        }
      }

      return knowledge;
    }
  }
};
</script>

<style scoped>
.study-materials {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
}

h1 {
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.materials-content {
  background-color: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.period-selection {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: white;
  border-radius: 5px;
}

.period-selection h2 {
  color: #007bff;
  margin-bottom: 1rem;
}

.period-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.period-option {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
}

.period-option:hover {
  border-color: #007bff;
  background-color: #f0f7ff;
}

.period-option.selected {
  border-color: #007bff;
  background-color: #e7f3ff;
}

.period-option input {
  margin-right: 0.5rem;
}

.loading, .no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.materials-section {
  margin-top: 2rem;
}

.materials-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.materials-header h2 {
  color: #333;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.generate-button {
  padding: 0.75rem 1.5rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.generate-button:hover {
  background-color: #218838;
}

/* コンパクトな対策問題集 */
.problem-set-compact {
  background-color: white;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 0.5rem;
}

.problem-set-header-compact {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #ddd;
}

.problem-set-header-compact h3 {
  color: #007bff;
  margin: 0;
  font-size: 1.1rem;
}

.sort-mode-selection-compact select {
  padding: 0.3rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 3px;
  font-size: 0.85rem;
  background-color: white;
  cursor: pointer;
}

.problem-list-compact {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.problem-item-compact {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fafafa;
  font-size: 0.85rem;
}

.problem-header-compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.problem-number-compact {
  font-weight: bold;
  color: #007bff;
  font-size: 0.9rem;
}

.problem-category-compact {
  background-color: #007bff;
  color: white;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
}

.problem-stats-compact {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
  margin-left: auto;
}

.stat-badge {
  background-color: #6c757d;
  color: white;
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  font-size: 0.7rem;
}

.problem-text-compact {
  color: #333;
  margin: 0.5rem 0;
  line-height: 1.5;
  font-size: 0.9rem;
}

.problem-options-compact {
  margin: 0.5rem 0;
}

.option-item-compact {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.5rem;
  margin-bottom: 0.3rem;
  border: 1px solid #ddd;
  border-radius: 3px;
  background-color: white;
  font-size: 0.85rem;
}

.option-item-compact.correct {
  border-color: #28a745;
  background-color: #d4edda;
}

.option-label-compact {
  font-weight: bold;
  color: #333;
  min-width: 1.2rem;
  font-size: 0.85rem;
}

.option-text-compact {
  flex-grow: 1;
  color: #555;
}

.correct-mark-compact {
  color: #28a745;
  font-weight: bold;
  font-size: 0.9rem;
}

.explanations-compact {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
}

.explanation-compact {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background-color: #e7f3ff;
  border-left: 2px solid #007bff;
  border-radius: 3px;
  font-size: 0.8rem;
  line-height: 1.5;
}

.explanation-compact strong {
  color: #007bff;
}

.option-explanations-compact {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.option-explanation-item {
  padding: 0.4rem;
  border-radius: 3px;
  font-size: 0.75rem;
  line-height: 1.4;
}

.option-explanation-item.correct {
  background-color: #e8f5e9;
  border-left: 2px solid #28a745;
}

.option-explanation-item:not(.correct) {
  background-color: #ffebee;
  border-left: 2px solid #dc3545;
}

.option-explanation-item strong {
  color: #333;
  margin-right: 0.3rem;
}

/* 教科書形式のノート */
.note-textbook {
  background-color: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 0.5rem;
}

.note-header-textbook {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #007bff;
}

.note-header-textbook h3 {
  color: #007bff;
  margin: 0;
  font-size: 1.2rem;
}

.textbook-pages {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.textbook-chapter-page {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fafafa;
  margin-bottom: 0.5rem;
}

.chapter-page-header {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #007bff;
}

.chapter-page-number {
  color: #007bff;
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0;
}

.chapter-page-title {
  color: #333;
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0;
}

.textbook-section-page {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background-color: white;
  border-left: 3px solid #28a745;
  border-radius: 3px;
}

.section-page-header {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.section-page-number {
  color: #28a745;
  font-size: 1rem;
  font-weight: bold;
  margin: 0;
}

.section-page-title {
  color: #333;
  font-size: 1rem;
  font-weight: bold;
  margin: 0;
}

.section-page-description {
  margin-bottom: 0.75rem;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 3px;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #555;
}

.topic-content-block {
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 3px;
}

.topic-title {
  color: #333;
  font-size: 0.95rem;
  font-weight: bold;
  margin: 0 0 0.5rem 0;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #e0e0e0;
}

.topic-content {
  margin: 0.5rem 0;
  font-size: 0.85rem;
  line-height: 1.7;
  color: #555;
}

.topic-content p {
  margin: 0.5rem 0;
}

.topic-key-points {
  margin-top: 0.75rem;
  padding: 0.5rem;
  background-color: #fff9e6;
  border-left: 3px solid #ffc107;
  border-radius: 3px;
}

.key-points-label {
  color: #856404;
  font-size: 0.85rem;
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
}

.key-points-list {
  margin: 0;
  padding-left: 1.5rem;
  color: #555;
  font-size: 0.85rem;
  line-height: 1.6;
}

.key-points-list li {
  margin-bottom: 0.3rem;
}

/* コンパクトなノート（旧スタイル - 互換性のため残す） */
.note-compact {
  background-color: white;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 0.5rem;
}

.note-header-compact {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #ddd;
}

.note-header-compact h3 {
  color: #007bff;
  margin: 0;
  font-size: 1.1rem;
}

.print-button-compact {
  padding: 0.4rem 0.8rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.85rem;
}

.print-button-compact:hover {
  background-color: #5a6268;
}

.note-list-compact {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.note-item-compact {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fafafa;
  font-size: 0.85rem;
}

.note-question-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.note-question-number {
  font-weight: bold;
  color: #007bff;
  font-size: 0.9rem;
}

.note-category-badge {
  background-color: #007bff;
  color: white;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
}

.note-stats-badge {
  background-color: #dc3545;
  color: white;
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  font-size: 0.7rem;
  margin-left: auto;
}

.note-question-text {
  color: #333;
  margin: 0.5rem 0;
  line-height: 1.5;
  font-size: 0.9rem;
}

.note-options-compact {
  margin: 0.5rem 0;
}

.note-option-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.5rem;
  margin-bottom: 0.3rem;
  border: 1px solid #ddd;
  border-radius: 3px;
  background-color: white;
  font-size: 0.85rem;
}

.note-option-item.correct {
  border-color: #28a745;
  background-color: #d4edda;
}

.note-option-label {
  font-weight: bold;
  color: #333;
  min-width: 1.2rem;
  font-size: 0.85rem;
}

.note-option-text {
  flex-grow: 1;
  color: #555;
}

.note-correct-mark {
  color: #28a745;
  font-weight: bold;
  font-size: 0.9rem;
}

.note-explanation-compact {
  margin: 0.5rem 0;
  padding: 0.5rem;
  background-color: #e7f3ff;
  border-left: 2px solid #007bff;
  border-radius: 3px;
  font-size: 0.8rem;
  line-height: 1.5;
}

.note-explanation-compact strong {
  color: #007bff;
}

.note-textbook-ref-compact {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
}

.note-textbook-ref-compact strong {
  color: #007bff;
  font-size: 0.85rem;
  display: block;
  margin-bottom: 0.3rem;
}

.textbook-ref-item {
  margin-bottom: 0.5rem;
  padding: 0.4rem;
  background-color: #f8f9fa;
  border-left: 2px solid #ffc107;
  border-radius: 3px;
  font-size: 0.75rem;
}

.ref-chapter {
  font-weight: bold;
  color: #007bff;
}

.ref-section {
  color: #666;
  margin-left: 0.3rem;
}

.ref-content {
  margin-top: 0.3rem;
  padding-left: 0.5rem;
  color: #555;
  line-height: 1.4;
  font-size: 0.75rem;
}

.problem-set, .note {
  background-color: white;
  padding: 2rem;
  border-radius: 5px;
  margin-top: 1rem;
}

.problem-set-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.problem-set-header h3 {
  color: #007bff;
  margin: 0;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.sort-mode-selection {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-mode-selection label {
  font-weight: bold;
  color: #555;
}

.sort-mode-selection select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
}

.problem-set h3, .note h3 {
  color: #007bff;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.problem-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.problem-item {
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.problem-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.problem-number {
  font-weight: bold;
  color: #333;
}

.problem-category {
  background-color: #007bff;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
}

.problem-stats {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.problem-accuracy {
  background-color: #6c757d;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
}

.problem-incorrect-count {
  background-color: #dc3545;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
}

.problem-total-attempts {
  background-color: #17a2b8;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
}

.problem-text {
  color: #555;
  margin-bottom: 1rem;
  line-height: 1.6;
  font-size: 1.1rem;
}

.problem-options {
  margin-bottom: 1rem;
}

.option-item {
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.option-item.correct {
  border-color: #28a745;
  background-color: #d4edda;
}

.option-item-detailed {
  padding: 1rem;
  margin-bottom: 1rem;
  border: 2px solid #ddd;
  border-radius: 5px;
  background-color: white;
}

.option-item-detailed.correct {
  border-color: #28a745;
  background-color: #f0f9f4;
}

.option-item-detailed.incorrect {
  border-color: #dc3545;
  background-color: #fff5f5;
}

.option-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.option-label {
  font-weight: bold;
  color: #333;
  min-width: 1.5rem;
}

.option-text {
  flex-grow: 1;
  color: #555;
}

.option-explanation {
  margin-top: 0.75rem;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.95rem;
  line-height: 1.6;
}

.correct-explanation {
  background-color: #e8f5e9;
  border-left: 3px solid #28a745;
}

.correct-explanation strong {
  color: #28a745;
  display: block;
  margin-bottom: 0.5rem;
}

.incorrect-explanation {
  background-color: #ffebee;
  border-left: 3px solid #dc3545;
}

.incorrect-explanation strong {
  color: #dc3545;
  display: block;
  margin-bottom: 0.5rem;
}

.correct-mark {
  color: #28a745;
  font-weight: bold;
  background-color: #28a745;
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

.explanation {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #e7f3ff;
  border-left: 4px solid #007bff;
  border-radius: 5px;
}

.explanation strong {
  color: #007bff;
}

.explanation p {
  margin-top: 0.5rem;
  color: #555;
  line-height: 1.6;
}

/* 教科書形式のスタイル */
.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #007bff;
}

.print-button {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  font-size: 1rem;
}

.print-button:hover {
  background-color: #5a6268;
}

.textbook-content {
  background-color: white;
  padding: 3rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 0 auto;
}

.textbook-cover {
  text-align: center;
  padding: 4rem 2rem;
  border: 2px solid #333;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.textbook-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1rem;
  font-weight: bold;
  line-height: 1.4;
}

.textbook-subtitle {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 2rem;
}

.textbook-date {
  font-size: 1rem;
  color: #888;
}

.textbook-toc {
  margin-bottom: 3rem;
  padding: 2rem;
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
}

.textbook-toc h2 {
  color: #007bff;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.textbook-toc ul {
  list-style: none;
  padding: 0;
}

.textbook-toc li {
  padding: 0.5rem 0;
  border-bottom: 1px dotted #ddd;
}

.textbook-toc a {
  color: #333;
  text-decoration: none;
  transition: color 0.2s;
}

.textbook-toc a:hover {
  color: #007bff;
}

.textbook-chapter {
  margin-bottom: 4rem;
  page-break-inside: avoid;
}

.chapter-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #007bff;
}

.chapter-number {
  font-size: 3rem;
  color: #007bff;
  margin-right: 1rem;
  font-weight: bold;
  min-width: 60px;
}

.chapter-title {
  font-size: 2rem;
  color: #333;
  margin: 0;
}

.chapter-intro {
  background-color: #e7f3ff;
  padding: 1.5rem;
  border-radius: 5px;
  margin-bottom: 2rem;
  border-left: 4px solid #007bff;
}

.chapter-intro p {
  margin: 0;
  color: #555;
  line-height: 1.8;
}

.chapter-section {
  margin-bottom: 3rem;
  padding: 2rem;
  background-color: #fafafa;
  border-radius: 5px;
}

.section-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #ddd;
}

.subsection-title {
  font-size: 1.2rem;
  color: #007bff;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-weight: bold;
}

.key-points, .terms-section, .formulas-section, .explanations-section {
  margin-bottom: 2rem;
}

.points-list {
  list-style: none;
  padding: 0;
}

.points-list li {
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  background-color: white;
  border-left: 4px solid #28a745;
  border-radius: 3px;
  line-height: 1.6;
}

.terms-list {
  margin: 0;
  padding: 0;
}

.terms-list div {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: white;
  border-radius: 5px;
  border-left: 4px solid #ffc107;
}

.terms-list dt {
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.terms-list dd {
  margin: 0;
  color: #555;
  line-height: 1.6;
  padding-left: 1rem;
}

.formulas-list {
  list-style: none;
  padding: 0;
}

.formulas-list li {
  padding: 1rem;
  margin-bottom: 0.75rem;
  background-color: white;
  border-left: 4px solid #dc3545;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  line-height: 1.8;
}

.explanation-block {
  padding: 1.5rem;
  margin-bottom: 1rem;
  background-color: white;
  border-left: 4px solid #17a2b8;
  border-radius: 3px;
}

.explanation-block p {
  margin: 0;
  line-height: 1.8;
  color: #555;
}

.textbook-footer {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 2px solid #ddd;
  text-align: center;
  color: #666;
  font-style: italic;
}

.textbook-footer p {
  margin: 0.5rem 0;
}

/* 図表のスタイル */
.diagrams-section {
  margin-bottom: 2rem;
}

.diagram-block {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: white;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.diagram-title {
  font-size: 1.1rem;
  color: #007bff;
  margin-bottom: 1rem;
  font-weight: bold;
}

.diagram-table {
  overflow-x: auto;
}

.diagram-table table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-size: 0.95rem;
}

.diagram-table th {
  background-color: #007bff;
  color: white;
  padding: 0.75rem;
  text-align: left;
  border: 1px solid #0056b3;
  font-weight: bold;
}

.diagram-table td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

.diagram-table tr:nth-child(even) td {
  background-color: #f0f0f0;
}

.diagram-table tr:hover td {
  background-color: #e7f3ff;
}

.diagram-ascii {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 5px;
  overflow-x: auto;
}

.diagram-ascii pre {
  margin: 0;
  font-family: 'Courier New', 'Monaco', 'Consolas', monospace;
  font-size: 0.9rem;
  line-height: 1.4;
  color: #333;
  white-space: pre;
}

.diagram-list {
  margin-top: 1rem;
}

.diagram-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.diagram-list li {
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
  border-radius: 3px;
  line-height: 1.6;
}

.diagram-list li strong {
  color: #007bff;
  margin-right: 0.5rem;
}

/* 周辺知識のスタイル */
.related-knowledge-section {
  margin-bottom: 2rem;
}

.knowledge-block {
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background-color: #fff9e6;
  border-left: 4px solid #ffc107;
  border-radius: 5px;
}

.knowledge-title {
  font-size: 1.1rem;
  color: #856404;
  margin-bottom: 0.75rem;
  font-weight: bold;
}

.knowledge-content {
  margin: 0 0 1rem 0;
  color: #555;
  line-height: 1.8;
}

.knowledge-points {
  margin: 1rem 0 0 0;
  padding-left: 1.5rem;
  color: #555;
}

.knowledge-points li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

/* 間違えた問題と教科書参照のスタイル */
.incorrect-questions-section {
  margin-bottom: 4rem;
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.section-main-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #007bff;
}

.question-reference-block {
  margin-bottom: 3rem;
  padding: 2rem;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.question-header {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.question-number {
  font-size: 0.95rem;
  font-weight: bold;
  color: #007bff;
}

.question-category-badge {
  background-color: #007bff;
  color: white;
  padding: 0.3rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.question-accuracy-badge {
  background-color: #dc3545;
  color: white;
  padding: 0.3rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.question-text-block {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-left: 3px solid #007bff;
  border-radius: 5px;
}

.question-text {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #333;
}

.question-options-block {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.options-label {
  display: block;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.option-item-small {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 3px;
  font-size: 0.85rem;
  line-height: 1.5;
}

.option-item-small.correct-option {
  border-color: #28a745;
  background-color: #d4edda;
}

.option-item-small.incorrect-option {
  border-color: #dc3545;
  background-color: #f8d7da;
  opacity: 0.8;
}

.option-number {
  font-weight: bold;
  color: #666;
  min-width: 1.5rem;
}

.option-text-small {
  flex: 1;
  color: #555;
}

.correct-mark-small {
  color: #28a745;
  font-weight: bold;
  font-size: 0.8rem;
  margin-left: auto;
}

.textbook-references {
  margin-bottom: 1.5rem;
}

.textbook-content-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #ddd;
}

.textbook-content-title {
  font-size: 1.3rem;
  color: #007bff;
  margin-bottom: 1.5rem;
  font-weight: bold;
}

.textbook-content-block {
  margin-bottom: 2.5rem;
  padding: 2rem;
  background-color: #f8f9fa;
  border-left: 5px solid #007bff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.textbook-content-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #007bff;
}

.content-chapter-title {
  font-size: 1.4rem;
  color: #007bff;
  margin: 0;
  font-weight: bold;
}

.textbook-content-body {
  margin-top: 1.5rem;
}

.content-section-description {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: white;
  border-radius: 5px;
  border-left: 3px solid #6c757d;
}

.content-section-description p {
  margin: 0;
  color: #555;
  line-height: 1.8;
  font-size: 1rem;
}

.content-topic-section {
  margin-top: 1.5rem;
}

.content-topic-title {
  font-size: 1.2rem;
  color: #28a745;
  margin-bottom: 1rem;
  font-weight: bold;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #28a745;
}

.content-topic-details {
  padding: 1.5rem;
  background-color: white;
  border-radius: 5px;
}

.content-topic-details > p {
  margin: 0 0 1rem 0;
  color: #555;
  line-height: 1.8;
  font-size: 1rem;
}

.content-key-points {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #fff9e6;
  border-left: 4px solid #ffc107;
  border-radius: 5px;
}

.content-key-points strong {
  color: #856404;
  display: block;
  margin-bottom: 0.75rem;
  font-size: 1.05rem;
}

.content-key-points ul {
  margin: 0.5rem 0 0 0;
  padding-left: 1.5rem;
  color: #555;
}

.content-key-points li {
  margin-bottom: 0.75rem;
  line-height: 1.7;
}

.content-topic-items {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #e7f3ff;
  border-left: 4px solid #007bff;
  border-radius: 5px;
}

.content-topic-items ul {
  margin: 0;
  padding-left: 1.5rem;
  list-style-type: disc;
}

.content-topic-items li {
  margin-bottom: 0.75rem;
  line-height: 1.7;
  color: #555;
}

.content-topic-items li strong {
  color: #007bff;
  margin-right: 0.5rem;
}

.topic-item-detail {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: white;
  border-radius: 5px;
  border-left: 4px solid #28a745;
}

.topic-item-name {
  font-size: 1.15rem;
  color: #28a745;
  margin: 0 0 1rem 0;
  font-weight: bold;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #28a745;
}

.topic-item-description {
  margin: 0 0 1rem 0;
  color: #555;
  line-height: 1.8;
  font-size: 1rem;
  font-weight: 500;
}

.topic-item-content {
  margin: 1rem 0 0 0;
  color: #666;
  line-height: 1.9;
  font-size: 0.95rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 5px;
  border-left: 3px solid #6c757d;
}

.question-explanation {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #e7f3ff;
  border-left: 3px solid #007bff;
  border-radius: 5px;
}

.question-explanation strong {
  color: #007bff;
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.question-explanation p {
  margin: 0;
  color: #555;
  line-height: 1.7;
  font-size: 0.85rem;
}

.section-description {
  margin: 1rem 0;
  color: #666;
  line-height: 1.8;
}

.section-topics {
  margin-top: 1.5rem;
}

.topics-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0 0;
}

.topics-list li {
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  background-color: #f8f9fa;
  border-left: 4px solid #6c757d;
  border-radius: 3px;
  line-height: 1.6;
}

.topics-list li strong {
  color: #495057;
  margin-right: 0.5rem;
}

/* 印刷用スタイル */
@media print {
  .note-header {
    position: fixed;
    top: 0;
    width: 100%;
    background: white;
    z-index: 1000;
  }

  .print-button {
    display: none;
  }

  .textbook-content {
    box-shadow: none;
    padding: 0;
  }

  .textbook-chapter {
    page-break-after: auto;
    page-break-inside: avoid;
  }

  .chapter-section {
    page-break-inside: avoid;
  }

  .textbook-toc {
    page-break-after: always;
  }

  .textbook-cover {
    page-break-after: always;
  }

  .diagram-block {
    page-break-inside: avoid;
  }

  .knowledge-block {
    page-break-inside: avoid;
  }

  .diagram-table {
    page-break-inside: avoid;
  }
}
</style>

