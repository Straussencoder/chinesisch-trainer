# Die gültigen Silben des Hochchinesischen (ohne Ton), nach Anlaut geordnet. ü wird als v geschrieben.
T = {
"": "a o e ai ei ao ou an en ang eng er yi ya ye yao you yan yin yang ying yong wu wa wo wai wei wan wen wang weng yu yue yuan yun",
"b": "ba bo bai bei bao ban ben bang beng bi bie biao bian bin bing bu",
"p": "pa po pai pei pao pou pan pen pang peng pi pie piao pian pin ping pu",
"m": "ma mo me mai mei mao mou man men mang meng mi mie miao miu mian min ming mu",
"f": "fa fo fei fou fan fen fang feng fu",
"d": "da de dai dei dao dou dan den dang deng dong di die diao diu dian ding du duo dui duan dun",
"t": "ta te tai tao tou tan tang teng tong ti tie tiao tian ting tu tuo tui tuan tun",
"n": "na ne nai nei nao nou nan nen nang neng nong ni nie niao niu nian nin niang ning nu nuo nuan nv nve",
"l": "la le lai lei lao lou lan lang leng long li lia lie liao liu lian lin liang ling lu luo luan lun lv lve",
"g": "ga ge gai gei gao gou gan gen gang geng gong gu gua guo guai gui guan gun guang",
"k": "ka ke kai kao kou kan ken kang keng kong ku kua kuo kuai kui kuan kun kuang",
"h": "ha he hai hei hao hou han hen hang heng hong hu hua huo huai hui huan hun huang",
"j": "ji jia jie jiao jiu jian jin jiang jing jiong ju jue juan jun",
"q": "qi qia qie qiao qiu qian qin qiang qing qiong qu que quan qun",
"x": "xi xia xie xiao xiu xian xin xiang xing xiong xu xue xuan xun",
"zh": "zha zhe zhi zhai zhei zhao zhou zhan zhen zhang zheng zhong zhu zhua zhuo zhuai zhui zhuan zhun zhuang",
"ch": "cha che chi chai chao chou chan chen chang cheng chong chu chua chuo chuai chui chuan chun chuang",
"sh": "sha she shi shai shei shao shou shan shen shang sheng shu shua shuo shuai shui shuan shun shuang",
"r": "re ri rao rou ran ren rang reng rong ru ruo rui ruan run",
"z": "za ze zi zai zei zao zou zan zen zang zeng zong zu zuo zui zuan zun",
"c": "ca ce ci cai cao cou can cen cang ceng cong cu cuo cui cuan cun",
"s": "sa se si sai sao sou san sen sang seng song su suo sui suan sun",
}
ALL = [s for k in T for s in T[k].split()]
if __name__ == "__main__":
    print(len(ALL), len(set(ALL)))
    open("/tmp/pylist.txt", "w").write("\n".join(ALL) + "\n")
