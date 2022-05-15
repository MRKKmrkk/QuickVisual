c = '<li id="province_num" side-bar-model="true"> <a href="#">  <i class="fa fa-dashboard">  </i>  <span>   qv-side-bar-model-content  </span> </a></li>'

ans = ""

i = 0
while (c[i] != ">"):
    i += 1
i += 1

print(c[i])
print(i)

e = len(c) - 1
while (c[e] != "<"):
    e -= 1

print(c[i:e])
