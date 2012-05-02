class item():
    def __init__(self,guid,title):
        self.guid = guid
        self.title = title
l1=[item(title='a',guid='a'),item(title='b',guid='b')]

l2=[item(title='a',guid='a'),item(title='c',guid='c'),item(title='d',guid='d')]

l3=[item(title='a',guid='a'),item(title='c',guid='c')]

l4=[item(title='a',guid='a')]

for x in l1:
	print x.title