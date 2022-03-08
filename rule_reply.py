class rule_plattern:
    def __init__(self):
        self.keyword_pair = {}

    def set_keyword_pair(self, keyword, reply):
        self.keyword_pair[keyword] = reply
        #keyword_pair['天氣'] = ‘天氣很好’
    
    def reply(self, sentence):
        #sentence: '可以告訴我明天天氣嗎？'
        for key in self.keyword_pair.keys():
            #天氣 in 可以告訴我明天天氣嗎？
            if key in sentence:
                #回傳 keyword_pair['天氣'] = ‘天氣很好’
                return self.keyword_pair[key]
        return None 