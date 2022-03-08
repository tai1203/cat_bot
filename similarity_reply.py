from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
from collections import defaultdict



class tf_idf:
    def __init__(self):
        self.corpus = []
        self.labels = []
        self.vectorizer = TfidfVectorizer(token_pattern= '\S+') # -> token pattern 是 把詞斷開的依據 (\S+ : 空格以外的詞都當一個詞)
        self.vocabs = None
        self.train_set = None

    def add_sentence(self, sentence, label):
        self.corpus.append(' '.join(self.cut_sentence(sentence))) # -> use join function 變成一個句子並以空格格開）
        self.labels.append(label)
        
    def cut_sentence(self,sentence):
        return list(jieba.cut(sentence)) # -> return a list （出來是個list)

    def train(self):
        self.train_set = self.vectorizer.fit_transform(self.corpus)
        self.vocabs = self.vectorizer.get_feature_names()

    def inference(self,sentence): #sentence is user's sentence
        # 先斷詞
        cut_str = ' '.join(self.cut_sentence(sentence)) # 字串
        # 重新對新詞訓練
        tr_sents = self.vectorizer.transform([cut_str]) # 0, 0, 0, 0.4, ...的vector
        #計算 cosine similarity
        similarities = cosine_similarity(self.train_set.A, tr_sents) #.A 的功用是 從 sparse matrix 轉乘 matrix , vector
        # [                 similarities 的型態長這樣
        #     [0.1], 
        #     [0.2], 
        #     ...
        # ]
        print(similarities)
        aggregate_map = defaultdict(list) #defaultdict 內每個東西都是list 型態
        for i, value in enumerate(similarities): # 0 -> self.labels index : 0
            aggregate_map[self.labels[i]].append(value[0])
            print(i,' ',aggregate_map)
                 #dict['天氣'] = [0.1, 0.3, 0.2 ...] -> avg : 0.2
                 #dict['餐廳'] = [0.9, 0.1] -> avg : 0.5  使用者的話與餐廳最接近
        sorted_label = []
        for key in aggregate_map.keys():
            print(aggregate_map)
            sorted_label.append([key, sum(aggregate_map[key])/len(aggregate_map[key])])

        sorted_label = sorted(sorted_label, key = lambda x: x[1] , reverse=True) #從key 的第一個數字 由大排到小
        return sorted_label[0][0]




