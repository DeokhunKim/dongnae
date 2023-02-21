import pandas as pd

readfile = pd.read_table('/Users/thekoon/Downloads/juso.txt', sep='	')
writefile = open("/Users/thekoon/Downloads/juso_.txt", "w")

region_code ={}

for i in readfile.itertuples():
    code = str(i[1])
    #print(f"{code[:5]} / {i[2]}")
    if region_code.get(code[:5]) is None:
        region_code[code[:5]] = i[2]


'''
print("{")
for k in region_code:
    print(f"   '{k}': '{region_code[k]}',")
print("}")
'''

writefile.write("{")
for k in region_code:
    writefile.write(f"   {k}: '{region_code[k]}',\n")
writefile.write("}")


writefile.close()