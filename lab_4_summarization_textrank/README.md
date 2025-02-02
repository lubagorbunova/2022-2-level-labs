# Лабораторная работа №4
  
## Дано  

1. Несколько текстов на русском языке, они находятся в папке [assets](./assets/texts).
2. Список стоп слов (предлоги, союзы, местоимения и другие неполнозначные слова русского языка). [Ссылка](./assets/stop_words.txt). 
    * Данный список взят из библиотеки для работы с естественным языком [NLTK](https://www.nltk.org/index.html).

Необходимо реализовать алгоритм, способный для случайного текста создавать его краткое содержание (*суммаризовать*).

Код, считывающий _некоторые_ материалы, уже написан для вас в `start.py`.

вы найдете эти ресурсы в следующих переменных:
* `text` - текст о жизни первого космонавта [Юрия Гагарина](https://ru.wikipedia.org/wiki/Гагарин,_Юрий_Алексеевич)
* `stop_words` - список стоп слов
* `paths_to_texts` - список из **путей** до текстов из папки [assets](./assets/texts).

**Важно:** В рамках данной лабораторной работы **нельзя использовать сторонние модули и модуль collections.**

**Важно:** вы *можете* использовать функции из предыдущих лабораторных работ.

Тексты статей взяты из [датасета статей сайта Газета.ру](https://www.kaggle.com/datasets/phoenix120/gazeta-summaries).

Следующее правило применяется ко всем функциям, которые необходимо реализовать в лабораторной работе:

Если на вход в функцию подаются некорректные аргументы, поднимается ошибка `ValueError`.
  * Некорректным аргумент считается в следующих случаях:
    * его тип отличается от ожидаемого типа
    * у него нет содержимого

## Подходы к выделению краткого содержания текста

У большинства задач есть несколько решений. Это применимо и к выделению краткого содержания.

В зависимости от желаемой структуры краткого содержания, выделяют два подхода:
1. _Извлекающий_ (_extraction-based_) - из исходного текста выбираются наиболее важные фразы, предложения или абзацы, совокупность которых образует краткое содержание. При этом данные фрагменты не обрабатывают, а извлекают в том порядке и виде, в каком они приведены в исходном тексте. 
   * **Достоинства**: независимость от предметной области, сравнительная простота разработки. 
   * **Недостатки**: бессвязность результата.
2. _Генерирующий_ (_abstractive-based_) - генерирующие методы основаны на лингвистических правилах обработки естественного языка или методах искусственного интеллекта. Они содержательно обобщают исходный документ, создавая текст, явно в нём не представленный.
   * **Достоинства**: лучшее качество результата.
   * **Недостатки**: сложность практической реализации, необходимость сбора большого количества лингвистических знаний.

В данной работе мы будем реализовывать алгоритм, основанный на извлекающем подходе.

Также, чтобы избежать путаницы, определим, что мы будем считать кратким содержанием:
* _Краткое содержание_ или _summary_ для текста - несколько наиболее важных для текста предложений.

Критерии важности предложений мы рассмотрим в следующих пунктах.

В [лабораторной работе №3](../lab_3_keywords_textrank/README.md) вы познакомились с выделением ключевых слов с помощью алгоритма _TextRank_.
Этот метод выделял отдельные ключевые слова из документа с помощью построения графов совместной встречаемости.

В данной лабораторной работе вы _модифицируете_ данный алгоритм, чтобы он мог выделять наиболее важные предложения из текста.

## Что надо сделать  

### Шаг 1. Творческое задание, будет анонсировано преподавателем на практике. Выполнение Шага 1 соответствует 4 баллам

### Шаг 2. Создать абстракцию для предложения

Так как в данной работе мы будем оперировать предложениями, причём в разных его проявлениях (сырой текст, предобработанный, закодированный), 
имеет смысл создать _абстракцию_, которая будет представлять предложение из реального мира в коде. 

За это будет отвечать класс `Sentence`.

#### Шаг 2.1 Инициализатор класса

Для создания объекта `Sentence` нам необходимо знать сам текст предложения, который мы будем передавать с помощью аргумента `text`, и его позицию в тексте.

Внутри инициализатора необходимо сохранить пришедшие на вход `text` и `position` в одноименные **защищённые** атрибуты класса.

Дополнительно необходимо создать два защищённых поля класса: `_preprocessed` и `_encoded`, 
отвечающие за предобработанную и закодированную версии предложения. Они должны быть инициализированы пустыми кортежами. 

Таким образом, у объекта класса `Sentence` должны быть следующие поля: `_text`, `_position`, `_preprocessed`, `_encoded`.

Интерфейс:   
```py
class Sentence:
    def __init__(self, text: str, position: int) -> None:
        pass
```  

#### Шаг 2.2 Методы `set_attribute` и `get_attribute`

Чтобы была возможность обращаться к защищённым атрибутам класса, необходимо реализовать соответствующие 
методы присваивания (`set_preprocessed`, `set_encoded`) и обращения (`get_text`, `get_preprocessed`, `get_encoded`, `get_position`) к ним.

Методы `set_preprocessed` и `set_encoded` принимают на вход соответствующее значение и 
присваивают его соответствующему атрибуту экземпляра класса.

**Важно**: должна происходить проверка элементов на соответствие типа:
* для `set_preprocessed` - то, что все элементы строки
* для `set_encoded` - то, что все элементы числа

Если это условие не выполняется, то должна подниматься ошибка `ValueError`.

Пример интерфейса:
```py
def set_encoded(self, encoded_sentence: EncodedSentence):
    pass
```  

Методы `get_text`, `get_preprocessed`, `get_encoded` и `get_position` не принимают ничего на вход и возвращают текущее 
значение соответствующего атрибута.

Пример интерфейса:
```py
def get_encoded(self) -> EncodedSentence:
    pass
```  

### Шаг 3. Выделить из текста предложения

В рамках [лабораторной работы №3](../lab_3_keywords_textrank/README.md) вы реализовали класс `TextPreprocessor`, позволяющий предобрабатывать текст.
В данной работе вы модифицируете функционал этого класса с помощью наследования и переопределения методов, чтобы можно было работать с предложениями.

В этом шаге вы будете реализовывать `SentencePreprocessor`.

#### Шаг 3.1 Инициализатор класса

Для создания объекта `SentencePreprocessor` нам необходимо знать: список стоп слов (аргумент `stop_words`) и пунктуационные знаки (аргумент `punctuation`).

Внутри инициализатора необходимо вызвать инициализатор родительского класса с пришедшими аргументами.

Таким образом, у объекта класса `SentencePreprocessor` должны быть как минимум следующие поля: `_stop_words`, `_punctuation`.

Интерфейс:   
```py
class SentencePreprocessor(TextPreprocessor):
    def __init__(self, stop_words: tuple[str, ...], punctuation: tuple[str, ...]):
        pass
```  

**Важно**: должна происходить проверка элементов на соответствие типа:
* для `stop_words` - то, что все элементы строки
* для `punctuation` - то, что все элементы строки

Если это условие не выполняется, то должна подниматься ошибка `ValueError`.


#### Шаг 3.2 Разделение текста на предложение. Метод `_split_by_sentence`

Этот метод, как вытекает из названия, разделяет текст на отдельные предложения. 

Метод принимает на вход неочищенный текст. 

Возвращаемым значением метода является кортеж предложений.

**Важно**: каждый элемент возвращаемого кортежа - экземпляр класса `Sentence`.

**Важно №2**: критерий разделения текста на предложения: знак препинания (`.!?`), за которым следуют пробел(ы) или символ(ы) новой строки и заглавная буква.

Интерфейс:   
```py
def _split_by_sentence(self, text: str) -> tuple[Sentence, ...]:
    pass
```  

#### Шаг 3.3 Предобработка предложений. Метод `_preprocess_sentences`

Этот метод предобрабатывает (разделяет на отдельные токены и очищает от специальных символов) предложения. 

Метод принимает на вход последовательность предложений. 

Метод добавляет к каждому предложению его предобработанную версию с помощью метода `set_preprocessed`.

**Важно**: необходимо использовать метод `preprocess_text` родительского класса.

**Важно №2**: необходимо использовать методы `get_text` и `set_preprocessed` для взаимодействия с экземплярами класса `Sentence`.

Интерфейс:   
```py
def _preprocess_sentences(self, sentences: tuple[Sentence, ...]) -> None:
    pass
```  

#### Шаг 3.4 Извлечение предложений из текста. Метод `get_sentences`

Этот метод является частью интерфейса класса `SentencePreprocessor`. 

Метод принимает на вход текст. 

Возвращаемым значением метода является кортеж предложений.

**Важно**: каждый элемент возвращаемого кортежа - экземпляр класса `Sentence`, у которого заполнены поля `_text` & `_preprocessed`.

**Важно №2**: необходимо использовать методы `_split_by_sentence` & `_preprocess_sentences`.

Интерфейс:   
```py
def get_sentences(self, text: str) -> tuple[Sentence, ...]:
    pass
```  

### Шаг 4. Закодировать предложения

В рамках [лабораторной работы №3](../lab_3_keywords_textrank/README.md) вы реализовали класс `TextEncoder`, позволяющий кодировать текст.
В данной работе вы модифицируете функционал этого класса с помощью наследования и переопределения методов, чтобы можно было работать с предложениями.

В этом шаге вы будете реализовывать `SentenceEncoder`.

#### Шаг 4.1 Инициализатор класса

Инициализатор класса `SentenceEncoder` не принимает аргументов.

Внутри инициализатора необходимо вызвать инициализатор родительского класса.

Таким образом, у объекта класса `SentenceEncoder` должны быть как минимум следующие поля: `_word2id`, `_id2word`.

Интерфейс:   
```py
class SentenceEncoder(TextEncoder):
    def __init__(self) -> None:
        pass
```  

#### Шаг 4.2 Заполнение атрибутов класса. Метод `_learn_indices`

Данный метод кодировщика принимает на вход кортеж из строк и соответствующим образом заполняет атрибуты `_word2id` и `_id2word`. Метод ничего не возвращает.
Каждой строке должно быть присвоено целое число. Одной строке присваивается ровно одно уникальное число. **Значения `word_id` должны начинаться с `1000`.**

Рассмотрим пример. Пусть дана следующая последовательность токенов: `('в', 'лесу', 'родилась', 'ёлочка', 'в', 'лесу', 'она', 'росла')`
В этой последовательности всего 6 разных строк: `'в'`, `'лесу'`, `'она'`, `'родилась'`, `'росла'`, `'ёлочка'`. 
Присвоим каждой из этих строк по одному уникальному числу больше 1000. Допустим, соответствие получается такое:

* `'в'` - `1009`
* `'лесу'` - `1001`
* `'она'` - `1005`
* `'родилась'` - `1101`
* `'росла'` - `1061`
* `'ёлочка'` - `1041`

Тогда атрибут `_word2id` должен выглядеть следующим образом: `{'в': 1009, 'лесу': 1001, 'она': 1005, 'родилась': 1101, 'росла': 1061, 'ёлочка': 1041}`. 
В `_id2word`, соответственно, ключи и значения меняются местами: `{1009: 'в', 1001: 'лесу', 1005: 'она', 1101: 'родилась', 1061: 'росла', 1041: 'ёлочка'}`.

Если вы все сделали правильно, то длина данных атрибутов должна совпадать.

**Важно**: в рамках данной лабораторной работы метод должен **дополнять** атрибуты `_word2id` и `_id2word`, а не переписывать их. 
Модифицируйте поведение метода, чтобы этот момент учитывался.

Интерфейс:   
```py
def _learn_indices(self, tokens: tuple[str, ...]) -> None:
    pass
```

#### Шаг 4.3 Кодирование предложений. Метод `encode_sentences`

Этот метод кодирует предложения, то есть заменяет каждый токен на число. 

Метод принимает последовательность предложений. 

Метод добавляет к каждому предложению его закодированную версию.

**Важно**: метод ничего не возвращает.

**Важно №2**: на входящих предложениях необходимо использовать метод `_learn_indicies`.

**Важно №3**: необходимо использовать методы `set_encoded` и `get_preprocessed` для взаимодействия с атрибутами экземпляров `Sentence`.  

Интерфейс:   
```py
def encode_sentences(self, tokens: tuple[Sentence, ...]) -> None:
    pass
```  

### Шаг 5. Продемонстрировать выделение и кодирование предложений. Выполнение Шагов 1-5 соответствует 6 баллам

В файле `start.py` в переменной `text` находится одна из статей. Выделите из неё предложения и закодируйте их.

#### Шаг 6. Вычисление метрики похожести 

Предобработанное предложение - последовательность из токенов. Существует [множество способов](https://aircconline.com/mlaij/V3N1/3116mlaij03.pdf) узнать, 
насколько две последовательности элементов похожи друг на друга.

В данной работе вы реализуете _меру Жаккара_ (_Jaccard Similarity/Index_), которая позволяет понять, насколько два множества элементов похожи.

Формула выглядит следующим образом:

```math
J(A, B) = \frac{|A\cap B|}{|A\cup B|}
```

Объяснение:
* $A$ & $B$ - множества элементов
* $|A\cap B|$ - количество элементов, которые являются общими для обоих множеств
* $|A\cup B|$ - общее количество уникальных элементов в обоих множествах

Пример:
* Множество $A$ - ${0, 1, 2, 5, 6}$
* Множество $B$ - ${0, 2, 3, 4, 5, 7, 9}$

```math
J(A, B) = \frac{|A\cap B|}{|A\cup B|} = \frac{|\{0, 2, 5\}|}{|\{0, 1, 2, 3, 4, 5, 6, 7, 9\}|} = \frac{3}{9} = 0.3(3)
```

Реализуйте функцию, рассчитывающую значение меры Жаккара для двух последовательностей элементов.

Функция принимает на вход две последовательности элементов.

Функция возвращает значение меры Жаккара.

Интерфейс:
```py
def calculate_similarity(sequence: Sequence, other_sequence: Sequence) -> float:
    pass
```

### Шаг 7. Представить текст в виде графа. Матрица схожести предложений

В рамках [лабораторной работы №3](../lab_3_keywords_textrank/README.md) вы реализовали класс `AdjacencyMatrixGraph`, позволяющий строить граф на основе совстречаемости токенов.
Токены были вершинами, а связи между ними - рёбрами.

В данной работе вы модифицируете функционал этого класса, чтобы можно было работать с предложениями:
* Вершинами будут предложения
* Рёбрами будут значения похожести между предложениями
  * Расчёт похожести между предложениями будет рассмотрен в следующих шагах

В этом шаге вы будете реализовывать `SimilarityMatrix`.

Матрица смежности представляет собой не что иное, как таблицу. В нашем случае незаполненная матрица выглядит вот так.

|   |A   |B   |C   |D   |
|---|---|---|---|---|
|A   |   |   |   |   |
|B   |   |   |   |   |
|C   |   |   |   |   |
|D   |   |   |   |   |

В ней одинаковое количество столбцов и строк. При этом каждая строка и каждый столбец соответствуют одной какой-либо вершине графа. Например, на пересечении строки, соответствующей вершине А, и столбца, соответствующего вершине В, будет записано число, 
отражающее значение похожести между этими вершинами, являющимися предложениями. Давайте посмотрим, как она может выглядеть в заполненном виде.

|   | A   | B   | C | D   |
|---|-----|-----|---|-----|
| A | 1   | 0.2 | 0 | 0.3 |
| B | 0.2 | 1   | 0 | 0.7 |
| C | 0   | 0   | 1 | 0   |
| D | 0.3 | 0.7 | 0 | 1   |

Ниже описаны шаги реализации матрицы похожести.

**Важно**: в матрице, которую вы реализуете, должны быть только столбцы и строки с числами.

#### Шаг 7.1 Инициализатор

Инициализация матрицы похожести не требует никаких входных аргументов. Конструктор задает необходимые атрибуты класса.

У каждого объекта графа **обязательно** должен быть следующий атрибут:
* `_matrix` - таблица, кодирующая связи между вершинами. Ожидаемый тип данных, хранящийся в этом атрибуте: `list[list[float]]]`.

```py
class SimilarityMatrix:
    def __init__(self) -> None:
        pass
```

#### Шаг 7.2 Добавление ребра

В данной лабораторной граф является изменяемой структурой данных: мы можем добавлять вершины и ребра после инициализации объекта.

Ответственным за это является метод `add_edge`. Он принимает на вход две вершины (предложения). 

В рамках класса `AdjacencyMatrixGraph` метод записывал в матрицу единицу, если вершины имеют ребро.

Здесь, в классе `SimilarityMatrix`, вместо единицы, необходимо записать значение метрики похожести для пришедших на вход вершин (предложений). 
Это значение необходимо вычислить с помощью функции `calculate_similarity`.

В случае, если вершины, пришедшей в качестве аргумента, в графе еще нет, необходимо ее добавить. 

**Важно**: Петли, то есть ребра, соединяющие вершину с самой собой, добавлять нельзя. 

**Важно №2**: два предложения являются одинаковыми, если у них одинаковые возвращаемые значения метода `get_encoded`.

Если в качестве обоих входных аргументов выступила одна и та же вершина, то поднимается ошибка `ValueError`.

Интерфейс:
```py
def add_edge(self, vertex1: Sentence, vertex2: Sentence):
    pass
```

#### Шаг 7.3 Получение значения метрики похожести

Для использования графа необходимо иметь возможность запросить у него информацию о том, насколько похожи два предложения друг на друга. 
Для этого нужно определить метод `get_similarity_score`. Метод принимает на вход два аргумента: вершина №1 и вершина №2. 

Метод возвращает значение похожести между двумя предложения из матрицы.

Если какая-либо из запрошенных вершин отсутствует в графе, поднимается ошибка `ValueError`.

Интерфейс:
```py
def get_similarity_score(self, sentence: Sentence, other_sentence: Sentence) -> float:
    pass
```

#### Шаг 7.4 Получение информации обо всех вершинах

Также необходимо реализовать возможность узнать, какие вершины есть в графе. Для этого следует реализовать метод `get_vertices`. 
Он не принимает никаких дополнительных аргументов. Возвращаемым значением является кортеж вершин сохраненного графа.

Интерфейс:
```py
def get_vertices(self) -> tuple[Sentence, ...]:
    pass
```

#### Шаг 7.5 Подсчет количества похожих вершин

Для работы алгоритма `TextRank` очень важно знать, с каким количеством вершин каждая конкретная вершина имеет общие ребра. Это называется `InOut score`. 
При суммаризации мы говорим, что два предложения (или вершины) имеют общее ребро, если значение метрики похожести для них > 0.

Метод принимает на вход вершину и возвращает количество похожих на неё вершин. Если на вход приходит вершина, которой нет в графе, поднимается ошибка `ValueError`.

Интерфейс:
```py
def calculate_inout_score(self, vertex: Sentence) -> int:
    pass
```

#### Шаг 7.6. Заполнение экземпляра графа 

Для упрощения работы с экземпляром графа реализуем метод, который заполнит его всеми вершинами и ребрами, которые можно извлечь из последовательности предложений.

Метод принимает на вход последовательность предложений. Внутри метода происходит выделение пар предложений и добавление соответствующих ребер в граф. 
Необходимо обращаться к методу `add_edge`. Метод ничего не возвращает.

Интерфейс:
```py
def fill_from_sentences(self, sentences: tuple[Sentence, ...]) -> None:
    pass
```

### Шаг 8. Алгоритм TextRank для суммаризации

В рамках [лабораторной работы №3](../lab_3_keywords_textrank/README.md) вы реализовали класс `TextRank`, 
позволяющий оценить важность токенов путем анализа их совстречаемости.

Данный алгоритм оперировал словами и находил ключевые слова для текста. Чтобы позволить этому алгоритму находить наиболее важные предложения, 
необходимо внести несколько модификаций (модификации выделены жирным шрифтом): 

* $V$ - вершина графа (то есть **предложение**)
* $d$ - damping factor, то есть вероятность перейти от этой вершины к любой другой, его значение обычно равно `0.85`
* $InOut(V)$ - вершины, **похожие на вершину** $V$
* $|InOut(V)|$ - количество вершин, **похожих на** $V$ (то есть, как мы назвали это в предыдущем пункте, `InOut score`)
* $k$ - это номер итерации: при переподсчёте веса вершины мы опираемся на веса инцидентных с ней вершин с *прошлых итераций*
    
Таким образом, чтобы посчитать новый вес для новой вершины, нужно:
* перебрать все вершины, инцидентные с данной вершиной
* для каждой из таких вершин найти ее `InOut score`, использовать его как знаменатель в дроби $\frac{1}{|InOut(V_{j})|}$ и умножить полученное значение на вес этой же вершины
* полученные значения просуммировать и умножить на $d$
* далее результат умножения сложить с $(1 - d)$; результат такого сложения становится новым весом рассматриваемой вершины

В этом шаге вы будете реализовывать `TextRankSummarizer`.

#### Шаг 8.1 Инициализатор класса

Инициализатор класса `TextRankSummarizer` принимает на вход только заполненный экземпляр класса `SimilarityMatrix`.

У каждого объекта `TextRankSummarizer` **обязательно** должны быть следующие атрибуты:
* `_graph` - здесь хранится пришедший на вход заполненная матрица
* `_damping_factor` - как упоминалось ранее, это константное значение, нужное для того, чтобы алгоритм не зациклился и отражающее вероятность перейти от конкретной вершины к любой другой; установите значение данного атрибута как `0.85`
* `_convergence_threshold` - это константное значение, отражающее максимально допустимую разницу между весами до и после обновления: если после очередной итерации пересчета весов вершин сумма разностей вершин не превышает этот порог, то мы считаем, что оптимальные веса найдены; установите значение данного атрибута как `0.0001`
* `_max_iter` - это константное значение, отражающее максимально допустимое количество итераций обновления весов: теоретически на вход может прийти очень сложный граф, в котором невозможно подобрать стабильные веса, и чтобы не попасть в бесконечный цикл, мы ограничиваем максимальное количество итераций; установите значение данного атрибута как `50`
* `_scores` - веса вершин, здесь ключами являются вершины (предложения), а значениями их вес, отражающий их важность

Интерфейс:
```py
class TextRankSummarizer:
    def __init__(self, graph: SimilarityMatrix) -> None:
        pass
```

#### Шаг 8.2 Обновление веса конкретной вершины

Модифицируйте обновление веса конкретной вершины. Метод принимает на вход вершину, вес которой необходимо пересчитать, 
список похожих на неё вершин и словарь с весами вершин после предыдущей итерации обновления. 

Новый вес вершины необходимо рассчитать по формуле из Шага №5 (то есть модифицировать уже существующий в классе `VanillaTextRank` метод расчёта, взяв код из реализации предыдущей лабораторной работы). 
Для получения информации о значении $d$ необходимо обратиться к соответствующему атрибуту класса, 
информацию о количестве похожих вершин нужно взять при помощи метода матрицы похожести `calculate_inout_score`. Доступ к матрице также происходит через атрибуты класса.

Метод ничего не возвращает. Вместо этого он перезаписывает вес вершины в словаре, хранящемся в атрибуте `_scores`. 

Интерфейс: 
```py
def update_vertex_score(self, 
                        vertex: Sentence,
                        incidental_vertices: list[Sentence],
                        scores: dict[Sentence, float]) -> None:
    pass
```

#### Шаг 8.3 Итеративное обновление весов вершин

Модифицируйте метод итеративного переподсчёта важности предложений `train`, взяв код из предыдущей лабораторной работы.

Метод должен работать с предложениями и передавать в метод `update_vertex_score` предложения, похожие на то, для которого происходит переоценка важности.

Метод ничего не принимает на вход и ничего не возвращает. Вместо этого он изменяет атрибут `_scores`.

#### Шаг 8.4 Получение наиболее важных предложений

Реализуйте метод, возвращающий наиболее важные предложения для текста. 

Метод принимает на вход аргумент, обозначающий требуемое количество предложений. Метод возвращает последовательность из `n_sentences` предложений по убыванию их значимости.

Интерфейс:
```py
def get_top_sentences(self, n_sentences: int) -> tuple[Sentence, ...]:
    pass
```

#### Шаг 8.5 Создание краткого содержания

Как было описано ранее, краткое содержание для текста - несколько наиболее важных предложений. 

Реализуйте метод, возвращающий краткое содержание.

Метод принимает на вход аргумент, обозначающий требуемое количество предложений.

Формат краткого содержания:
```python
{SENTENCE_1}
{SENTENCE_2}
{SENTENCE_3}
...
{SENTENCE_N}
```

Наиболее важные предложения, соединённые символом новой строки.

Метод принимает на вход аргумент, обозначающий требуемое количество предложений. Метод возвращает краткое содержание.

**Важно**: предложения должны идти в хронологическом порядке! То есть так, как они шли в оригинальном тексте.

Интерфейс:
```py
def make_summary(self, n_sentences: int) -> str:
    pass
```

### Шаг 9. Продемонстрировать выделение краткого содержания. Выполнение Шагов 1-9 соответствует 8 баллам

Продемонстрируйте выделение краткого содержания для текста, хранящегося в переменной `text`, в файле `start.py`. 

Не забудьте предобработать текст, закодировать его, создать экземпляр матрицы похожести, заполнить её, итеративно вычислить вес вершин и выделить краткое содержание.

### Шаг 10. Создать всезнающего помощника

Голосовые и текстовые помощники (боты) очень популярны: 
от назойливых всплывающих окон на веб-сайтах до вполне полезных ботов в банковских приложениях - они пытаются помочь.

Откуда у них, помощников, находится информация, необходимая пользователю и как они выбирают нужный ответ (то есть соотносящийся со входным запросом) из этой информации?
Как можно представить работу простого текстового помощника?

Сегодня множество компаний используют машинное обучение для тренировки голосовых и текстовых помощников: нейронная сеть получает огромный объём информации, который она обобщает и затем использует для ответа на запросы.

Однако, так было (и иногда есть) не всегда. Есть и более простые способы создания помощника.

В предыдущих пунктах мы разобрались, как понять, насколько тексты похожи друг на друга с помощью подсчёта совпадающих ключевых слов.

Запрос пользователя тоже можно рассматривать как текст, из него можно выделить ключевые слова и, соответственно, сравнивать с другими текстами на предмет сходства.
Те тексты, которые будут максимально похожи на запрос, и будут ответом. Но что, если тексты довольно длинные? Пользователь вряд ли захочет читать ~5 страниц информации для получения простого ответа.

Здесь на помощь приходит возможность выделять краткое содержание из текстов (и как кстати, что мы уже знаем, как это сделать).

Если суммаризовать сказанное выше, то для создания помощника нужно:
1. Взять некоторое количество текстов
2. Выделить из них ключевые слова
3. Создать для текстов краткие содержания

Ключевые слова и краткие содержания будут _базой знаний_ помощника.

Затем, когда пользователь делает запрос к помощнику, процесс конструирования ответа выглядит следующим образом:
1. Запрос проходит предобработку
2. Из запроса выделяются ключевые слова
3. Ключевые слова запроса сравниваются с ключевыми словами текстов из базы знаний
4. Те тексты, ключевые слова которых наиболее похожи на ключевые слова из запроса, запоминаются как потенциальный ответ
5. Соответствующие этим текстам краткие содержания форматируются и выдаются пользователю как ответ

Каждый из шагов будет более подробно рассмотрен далее.

В коде помощника будет представлять класс `Buddy`.

Для помощника нам нужно будет следующее:
* `paths_to_texts` - список путей до текстов, которые будут составлять базу знаний помощника
* `stop_words` - список стоп слов
* `punctuation` - список пунктуационных знаков
* `idf_values` - предобученные значения IDF для выделения ключевых слов с помощью `TFIDFAdapter`

Интерфейс: 
```py
class Buddy:
        def __init__(self,
                     paths_to_texts: list[str],
                     stop_words: tuple[str, ...],
                     punctuation: tuple[str, ...],
                     idf_values: dict[str, float]):
        pass
```

У каждого экземпляра `Buddy` должны быть как минимум следующие атрибуты:
* `_stop_words` - список стоп слов
* `_punctuation` - список пунктуационных знаков
* `_idf_values` - предобученные значения IDF для выделения ключевых слов с помощью `TFIDFAdapter`
* `_text_preprocessor` - экземпляр класса `TextPreprocessor`, необходимый для предобработки текста
* `_sentence_encoder` - экземпляр класса `SentenceEncoder`, необходимый для кодирования предложений
* `_sentence_preprocessor` - экземпляр класса `SentencePreprocessor`, необходимый для предобработки предложений
* `_paths_to_texts` - путь до текстов, которые будут составлять базу знаний помощника 
* `_knowledge_database` - база знаний помощника со следующей структурой:
  * Ключи - путь до текста
  * Значения - словари со следующей структурой: `{'sentences': sentences, 'keywords': keywords, 'summary': summary}`
    * `sentences` - предобработанные и закодированные предложения (каждый элемент - экземпляр `Sentence`) 
    * `keywords` - ключевые слова для данного текста (кортеж из строк)
    * `summary` - краткое содержание текста

Значение по умолчанию для `_knowledge_database` - пустой словарь.

При создании экземпляра класса `Buddy` база знаний должна заполняться информацией на основе текстов, переданных в аргументе `paths_to_texts`, с помощью метода `add_text_to_database`, о котором далее.

#### Шаг 10.1 Заполнение базы знаний помощника

Для заполнения базы знаний Вам необходимо реализовать метод `add_text_to_database`.

Метод принимает на вход путь до текста.

Метод:
1. Считывает текст
2. Извлекает из текста предложения
   1. Предобрабатывает предложения
   2. Кодирует предложения
3. Извлекает из текста ключевые слова с помощью `TFIDFAdapter`. `TFIDFAdapter` необходимо импортировать из третьей лабораторной работы.
4. Создаёт краткое содержание для текста с помощью `TextRankSummarizer`
5. Записывает в переменную `_knowledge_database` пару ключ-значение, где ключ - уникальный идентификатор текста (путь до него); 
значение - словарь со структурой, описанной ранее:
    ```py
    self._knowledge_database[text_id] = {
        'sentences': sentences,
        'keywords': keywords,
        'summary': summary
    }
    ```

**Важно**: 
* `sentences` - последовательность экземпляров класс `Sentence`, у каждого из которых заполнены поля `_text`, `_preprocessed`, `_encoded`
* `keywords` - последовательность из 100 ключевых слов для текста, извлечённых с помощью `TFIDFAdapter`
* `summary` - краткое содержание текста, состоящее из 5 предложений, извлечённых с помощью `TextRankSummarizer`

Интерфейс:
```py
def add_text_to_database(self, path_to_text: str) -> None:
    pass
```

**Важно №2**: этот метод должен быть вызван для **каждого** текста из списка `paths_to_texts` при создании экземпляра класса `Buddy`.

#### Шаг 10.2 Нахождение текстов, похожих на ключевые слова

Как было описано в Шаге №7, мы можем рассматривать запрос пользователя как текст и, соответственно, выделять из него ключевые слова. 

Ключевыми словами в контексте запроса мы будем считать те, которые не являются стоп словами.   

В качестве ответа на вопрос пользователя должны выбираться краткие содержания тех текстов, ключевые слова которых близки (согласно мере Жаккара) 
к ключевым словам из запроса.

Чтобы находить тексты, ключевые слова которых похожи на ключевые слова из запроса, Вам нужно реализовать метод `_find_texts_close_to_keywords`.

Метод принимает на вход список ключевых слов из запроса и количество необходимых текстов.

Метод возвращает список уникальных идентификаторов текстов (их пути) из базы знаний, которые наиболее похожи на ключевые слова. 
Степень похожести нужно вычислить с помощью функции `calculate_similarity`. 

**Важно**: в ситуации, когда у текстов одинаковые значения метрики похожести, необходимо сортировать значения по пути до текста в **обратном** (по убыванию) лексикографическом порядке.

Интерфейс:
```py
def _find_texts_close_to_keywords(self,
                                  keywords: tuple[str, ...],
                                  n_texts: int) -> tuple[str, ...]:
    pass
```

**Важно №2**: в ситуации, когда у всех текстов значение метрики похожести на ключевые слова равняется 0, необходимо поднять 
_пользовательское исключение_ с сообщением `Texts that are related to the query were not found. Try another query.`.

Создайте пользовательское исключение с именем `NoRelevantTextsError`. Что такое пользовательские исключения и как их создавать, вы можете
найти [здесь](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions).

#### Шаг 10.3 Внешний интерфейс помощника

Теперь, когда вы знаете, как находить наиболее похожие на запрос тексты и имеете доступ к их кратким содержаниям, необходимо
создать внешний интерфейс помощника, который будет использовать реализованное выше.

Конечная цель, обозначенная ранее: создание помощника, который может отвечать на запрос пользователя определённым количеством кратких содержаний.
Эти краткие содержания должны быть релевантны запросу.

Для того чтобы помощник мог взаимодействовать с пользователем, Вам нужно реализовать метод `reply`.

Метод принимает на вход запрос и количество кратких содержаний, которые будут в ответе (по умолчанию - три). 
Если в базе данных количество текстов меньше, чем количество необходимых кратких содержаний, поднимается ошибка `ValueError`. 

Метод возвращает ответ со следующим форматированием:
```python
Ответ:
{SUMMARY_1}

{SUMMARY_2}
...

{SUMMARY_N}
```

Краткие содержания, соединённые двумя символами новой строки.

**Важно**: количество предложений в кратких содержаниях должно равняться 5.

Интерфейс:
```py
def reply(self, query: str, n_summaries: int = 3) -> str:
    pass
```

**Важно №2**: в ситуации, когда запрос пользователя имеет некорректный тип или является пустой строкой, необходимо поднять 
_пользовательское исключение_ с сообщением `Incorrect query. Use string as input.`.

Создайте пользовательское исключение с именем `IncorrectQueryError`. Что такое пользовательские исключения и как их создавать, вы можете
найти [здесь](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions).

### Шаг 11. Продемонстрировать работу всезнающего помощника. Выполнение Шагов 1-11 соответствует 10 баллам

Продемонстрируйте взаимодействие с помощником: обучите его с помощью текстов, хранящихся в папке [texts](./assets/texts), 
задайте несколько вопросов и оцените, насколько полезными оказались ответы.

**Важно**: переменная `paths_to_texts` хранит список **путей** до текстов, используйте её при инициализации помощника.

## Узнать больше

* [Подходы к суммаризации текста](https://arxiv.org/pdf/1904.00688.pdf)
* [Метрики похожести последовательностей](https://aircconline.com/mlaij/V3N1/3116mlaij03.pdf)
* [TextRank для суммаризации](https://arxiv.org/pdf/1602.03606.pdf)
