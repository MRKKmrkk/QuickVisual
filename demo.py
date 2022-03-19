import pandas

df = pandas.DataFrame({
    "word": ["a", "b", "c"],
    "num": [11, 22, 33]
})

words = df['word'].tolist()
nums = df['num'].tolist()

datas = []
for i in range(len(words)):
    datas.append((words[i], nums[i]))
print(datas)
