### 1. 环境准备

Purpose: Load the core language resources required for preprocessing.
Key point: Ensure the local availability of basic dictionaries and machine learning models.

```Python
nltk.download('punkt')   # 分词模型
nltk.download('stopwords')  # 停用词库
nltk.download('wordnet')    # 词形还原词典
nltk.download('averaged_perceptron_tagger')  # 词性标注模型
```

### 2. 流程框架

Modular Design: Separate text processing from file operation logic.
Scalability: Allow independent optimization of text processing or I/O workflows.

```Python
def preprocess_text(text):
    # 8 core processing steps...
def process_articles(input_dir, output_dir):
    # File traversal and data integration...
```

### 3. 文本清洗核心步骤

#### 3.1 原始文本净化

```Python
text = re.sub(r'<.*?>', '', text)  # 去除HTML标签
text = re.sub(r'[^a-zA-Z\s]', '', text)  # 移除非字母字符
```

Example: "Biden's 2023 plan `<br>`..." → "Bidens plan"

#### 3.2 智能分词

```Python
tokenizer = RegexpTokenizer(r'\b[a-zA-Z-]{2,}\b')  # 保留≥2字母的单词 
tokens = tokenizer.tokenize(text.lower())
```

但是这里第一条不能删除单个字母，在后续会再次处理

#### 3.3 上下文感知停用词过滤

Innovation: Customize the filter word library based on domain knowledge (international political news)
Linguistic considerations: Remove meaningless prepositional structures

```Python
stop_words = set(stopwords.words('english'))     # 英语（english）的停用词
tokens = [word for word in tokens if word not in stop_words]     #总共198个，package所包含的
```

根据向量情况反馈，清洗不够干净，有所遗留

因此 `custom`了两次：

```Python
custom_prepositions = {'above', 'across',...
                       }
custom_stop_words = {
    'china', 'usa', 'jan', 'feb', ...  # 自定义政治/时间相关停用词
}
stop_words.update(custom_prepositions)
stop_words.update(custom_prepositions)  # 添加50+介词
```

#### 3.4 词形还原优化

```Python
pos_tags = pos_tag(tokens)  # 词性标注
wn_tag = get_wordnet_pos(tag)  # 转换标注体系
lemmatizer.lemmatize(word, wn_tag)  # 基于词性的还原
```

#### 3.5 特殊处理，remove specific words

1. Remove words longer than 10 letters：
   经过最初的几次试验，发现‘body’部分每篇处理完的文章都有一个很长的单词，推测应该属于与文章不相关的其他部分，选择删除

```Python
tokens = [word for word in tokens if len(word) <= 10]
```

2. Remove specific words (performed after lemmatization):
   同上，发现每篇文章都有相同的word，属于干扰因素，直接选择删去(V1)；
   但是，在试过一版的时候，发现有遗留 `{'principle', 'open', 'new'}`，更改代码为after lemmatization之后再处理(V2);
   最后，根据向量反馈，删除数字相关。

```Python
words_to_remove = {'licensing', 'right',
                  }
 words_to_remove.update(['one', 
                         )
```

3. Remove single-letter words：
   3.2已经提到过使用去除单个字母，但是在body部分依旧残留很多 `‘u’`

```Python
lemmatized_tokens = [word for word in lemmatized_tokens if len(word) >= 2]
```

关键修改说明：
在预处理函数的最后（返回 `lemmatized_tokens`之前），添加了一个过滤步骤，确保所有保留的单词长度至少为2。这样可以有效移除在词形还原等步骤中可能生成的单个字母（如 `'u'`），确保输出结果中不再包含这类单词。

### 4. 数据流水线设计

process_articles() 函数工作流程：

1. 递归遍历目录树
2. JSON文件解析与语言检测（隐式通过内容存在性检查）
3. 标题/正文独立处理
4. 基于标题的重复检测
5. 结构化存储为CSV

输出格式优化：

```csv
"title", "date", "body"
"us, china, trade...", "2023-01-01", "negotiation, tariff..."
```

### 5. 创新性设计亮点

混合停用词策略：
基础停用词(179) + 自定义停用词(120+) + 介词库(50+)

领域定制过滤：
政治实体词（china/usa/russia）
时间相关词（jan/mon/week）

预处理后验证：
空内容检测、标题重复检测

#### 6. P.S.

- The directory must contain a folder named `'articles'` that includes the JSON files, where the collected text is included. After running the code, a folder named `'processed_articles'` will be automatically created, and the output CSV file will be saved in this folder.
