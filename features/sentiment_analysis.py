class SentimentAnalysis:
    def __init__(self):
        self.positive_words = set(['happy', 'good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'love', 'like', 'enjoy'])
        self.negative_words = set(['sad', 'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'angry', 'upset', 'disappointed'])

    def analyze(self, text):
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'