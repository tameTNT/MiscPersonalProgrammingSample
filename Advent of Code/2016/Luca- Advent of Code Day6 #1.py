import collections

messages = ["ewqplnag",  "qchqvvsf",  "jdhaqbeu",  "jsgoijzv",  "iwgxjyxi",  "yzeeuwoi",  "gmgisfmd",  "vdtezvan",  "secfljup",  "dngzexve",  "xzanwmgd",  "ziobunnv",  "ennaiqiz",  "jgrnzpzi",  "huwrnmnw",  "qeibstlk",  "qegqmijn",  "gpwfokjg",  "gsmfeqmm",  "hlytxgti",  "idyjagzt",  "mlaztojc",  "xqokrslk",  "gkigkibl",  "feobhvwi",  "xxylgrpe",  "uivfbbbz",  "lekmcifg",  "ngcwvese",  "tgyvzlkg",  "pysjumnt",  "bmeepsda",  "svbznlid",  "hcwlvtyg",  "tjdzsiqu",  "cadtkxut",  "msirmtzs",  "cxgahqib",  "dtfdkzss",  "nrnodqjy",  "ptwvbmtq",  "ywkqyulp",  "ciszkcnx",  "ahxtwnnk",  "dlwvcsfc",  "uewwndje",  "ocdgocqk",  "auanolri",  "pfqyjyja",  "uypwzjjo",  "zaidpezv",  "tjtwiftf",  "fnrzsyhp",  "hfyqsxfu",  "nigauqsd",  "xonhbtpx",  "wcjciqgn",  "kdgvmzox",  "zbweztcm",  "irrmwyux",  "zmqblmfm",  "chcqxrqm",  "qjnahphi",  "hvkxgyeu",  "uqcsxxix",  "lhzkoydb",  "oyukomwi",  "prjjkctn",  "nsjvcthj",  "bivdsubf",  "galbvbof",  "emrnviig",  "bnpuofwt",  "shsutaeo",  "xkhargbp",  "swunowfn",  "dzohfvtr",  "kbsvqoor",  "dtkjgajx",  "bcjgfstl",  "jlgouhim",  "xmbqsvjx",  "brcvmnqc",  "eyphcrec",  "flnxhhzm",  "blrixjdy",  "msxlfmop",  "eaawcbkp",  "mgxiemxl",  "pfxtpuvh",  "vulefkxn",  "tlxfigbc",  "iktsstzd",  "qdycwpat",  "yjfhllyu",  "mmcxxloe",  "xpwpjnuy",  "sziveuyv",  "rmkmyqyl",  "hqywtzhu",  "pouceqty",  "kvfdzahj",  "ltiledbc",  "pcajwpht",  "kcsxqksn",  "bfmdmqyf",  "luxbaaqq",  "nptsvniz",  "aawfrzxw",  "keeyyptq",  "ryicuhie",  "yjvclzac",  "bveorbeo",  "ohmbvpmu",  "cvxejdwb",  "ziyffdnx",  "gwjxdbaq",  "unnrfnqh",  "kvicaaai",  "jkkiuvxj",  "cjviyayl",  "drbielvb",  "nulynluk",  "eixugugc",  "fxfzuonn",  "ludhzktb",  "tmqvbqfm",  "nzzjdxph",  "ukzvvges",  "ejplrckc",  "ocawtnmd",  "svqsxbrf",  "sfdfgohg",  "bnjrokxk",  "frulcpng",  "fjuhbzfb",  "wpwytpzh",  "jqstbhff",  "wkzichey",  "uygpxxgb",  "laemchta",  "vgjcyumm",  "hhloaorn",  "iviwosqf",  "kudumnei",  "ntfvtoay",  "xcimluam",  "wypytwno",  "cqboftdd",  "mwfcdwzw",  "tgwmjxfp",  "jysdwspw",  "cnsoamld",  "fyznzrpo",  "skvorpwt",  "plpwsuih",  "aysqbwem",  "rutkdrnn",  "llxxyaqe",  "vfhsvtxv",  "lgtmtjmj",  "ypfcjnbb",  "tdvnfrtv",  "obpdwotj",  "zreanciv",  "mfexhuff",  "hodukcbc",  "rjqrgxgn",  "xpmtiaec",  "roavlcvt",  "rabhqwct",  "ojkdtbsz",  "pztezpmw",  "qefgwtbf",  "ocdtbmop",  "dlfgvkmh",  "ddpzjrqc",  "ounagflg",  "vrtrakwj",  "ekcrcvtl",  "hrvghvmq",  "yphmhigf",  "nbmwllxs",  "gmcfdvvw",  "yafshyuo",  "hpbrminb",  "lwmuprvy",  "rajyhedj",  "qtrxbxal",  "wcqfjvfg",  "pvzefquu",  "juizosne",  "qbnrfgpp",  "muyjpylx",  "ljftujim",  "ssrjqzhi",  "isolpxai",  "lpazyyse",  "znrlwzhc",  "tvcbgplx",  "ecdcsjuq",  "axzsjwnm",  "edogmygw",  "gfbqksky",  "bekioiyr",  "nyhxmwmx",  "murhyrrk",  "rwlfdeve",  "trlmfwjy",  "zzanjgdz",  "bwscvdxk",  "tsmrttcq",  "fmmizwrz",  "cqneezoq",  "dhuwkslc",  "jwzrdomv",  "wxrleoed",  "fivvxash",  "ioygsjhc",  "qdpwprez",  "tagvmlbn",  "pqtaqcot",  "bdmdrheh",  "pfmsjlpa",  "hiafczzf",  "ovjrntwt",  "eoytrczw",  "ekcuhuur",  "wmqzzebk",  "awczvbtm",  "vnxrniiy",  "kaayoxlt",  "xhjtpiju",  "ceffyfww",  "vdnoycxw",  "pmebcukw",  "swbogemw",  "affewhdj",  "inbpzraz",  "ttjkvylh",  "khiljslo",  "ixmjrdom",  "wfnmgcqr",  "pntkncna",  "ezbtngtx",  "dxgoiwtq",  "gcorhdwq",  "mtnxxcfn",  "lguoqhpp",  "mydgtldv",  "dcautedv",  "aqxafodz",  "abvyoomx",  "qdpyeshc",  "eslyxatb",  "sxhhruer",  "fyudfdpl",  "mvbfwmhk",  "upmzmdmz",  "rqxugbwh",  "lubhqmre",  "vhpzyerz",  "ljyexgma",  "vpshuvyr",  "pxvuccyv",  "ppesevpl",  "mjcyazgy",  "mthxasgs",  "zkeinsxs",  "emehvnsz",  "icawtxzi",  "rxrpyaji",  "jxoxevxd",  "adewmqba",  "jcypwkfv",  "wspbxbnf",  "sjagbbna",  "ubfllkvq",  "hsecqidv",  "bztzbswf",  "udhthpya",  "hbpqvrrg",  "glnwntfm",  "ghpsmdjt",  "fgwxpvkx",  "sadgtywm",  "ipcrkfuv",  "tctyqmko",  "livzojbr",  "yejzdarn",  "aqqnctjm",  "emgcphcq",  "nkqfubfl",  "qojeklqt",  "kvsnebgk",  "whbowpmx",  "brmttrog",  "dyecglha",  "bjhyzrqq",  "vtkhzeyk",  "loopqwmv",  "pycecyfy",  "riswpqzb",  "fpukakic",  "jbyjandt",  "pgmqyhho",  "rkovglxj",  "gyoamarg",  "zffmcdgz",  "vajaeirw",  "mewxbrpv",  "akullmcy",  "hnhhlxto",  "vrzuwzzd",  "oqudtfol",  "hjbadzse",  "pttmnoan",  "bgvmjudu",  "cfrowrpy",  "xapmrpde",  "uvoxhgwo",  "ogzbapqj",  "slkplnas",  "nzidxmos",  "ymfjsfcx",  "celkhenj",  "mjsysfzp",  "piduvvdb",  "jhjlhnai",  "vuqwliaq",  "kwxnhphe",  "kttkiutd",  "kbxdqmdi",  "syokthzk",  "hgzkmhvv",  "zhwusjfg",  "qsozuerb",  "obyswgci",  "aosbzjnt",  "vtriuhuy",  "ewwggfad",  "ntpassqj",  "ggvooetp",  "hhmyywmv",  "rzhrqkvx",  "zapkliel",  "mfrgyvgw",  "ziwaqzun",  "vdpqztyc",  "wgxbjzxa",  "azvotolg",  "nskteyaj",  "mxoustqy",  "wfsrmtrk",  "xoqecgrl",  "dluzpwur",  "lokaxykx",  "xyqouhxb",  "udaqkoqf",  "hbvsdvkk",  "omqymecg",  "zpdwrwin",  "gaaprkiw",  "qrljdsgr",  "yzqzxlsu",  "lwxzzesm",  "fogpmgrb",  "ahahsyet",  "xbshcjlp",  "kqjnqfns",  "dirbsjvo",  "ivvuvzde",  "uuktpjjo",  "xjyqnzuz",  "gocimeia",  "qgznojog",  "gliwbekp",  "bqgakwkl",  "emewklsz",  "nrsbhxls",  "ksqxptkx",  "qayiikzs",  "ypulgpll",  "zpgbguze",  "oxttgrkk",  "usubcozu",  "vfdfaqdf",  "aijdqnws",  "zrafskka",  "qevegolp",  "limniayp",  "ufiiffly",  "npadruup",  "euamdite",  "plzaivpj",  "akqqvlro",  "foknpolu",  "yzvvtjwz",  "svhqjfpq",  "zsceoycs",  "fueralpo",  "dmwobiiv",  "nwmjvxxj",  "qvypxtyn",  "ycfkrxge",  "bdlrfvxh",  "ilkjiske",  "nebvkegk",  "stclxlsh",  "dzcomxfy",  "xnqqcilu",  "fwtpdqok",  "xcwpngxi",  "jhzgpgmd",  "gxfgyecr",  "ifzqihyl",  "rtdjzika",  "eeqqbdrn",  "bcxcqoif",  "sxdiaauc",  "rwfkuhka",  "abixxudr",  "aexxbgvm",  "ibnckfvl",  "wpnguagh",  "ukicjzms",  "rjcdglsa",  "wbbbwedq",  "gszpbdcd",  "uuliinia",  "oroolcgs",  "dbrutctl",  "clhhguog",  "jhttewcr",  "nudiqqvi",  "onpwamga",  "kztklrsm",  "moqperyh",  "wrlcyfwl",  "hsnkrqrz",  "jctpxrsp",  "dgyjdbaj",  "yxamrvae",  "cubkcqah",  "yvecuhqs",  "vvbcmhdf",  "mcosktuq",  "uonxvxhd",  "zileeeyl",  "jxebsrqb",  "rvkudgsu",  "yiflvdar",  "hefezoyf",  "vlhprvnx",  "gnlmhfzj",  "fdzgbpei",  "evisboku",  "eiultlcz",  "ttrpqdch",  "bnujwmwg",  "kxkijfkb",  "frzqsuvg",  "yzbrwmhf",  "tbytnypt",  "wizbqixp",  "sqofdzfw",  "gkiddyod",  "tqzyncjl",  "vfsjagyy",  "xkcvhice",  "nkkipbzd",  "murubxvr",  "aalgekbr",  "qzhgpqiz",  "rtxmuasx",  "vznzbbuq",  "bdpaucup",  "byzeajgv",  "dpedjbke",  "ksmynpqq",  "zocacvlb",  "zymffjwb",  "cegodbwk",  "qggqsxoo",  "uziyisoh",  "oatngkya",  "caumywbn",  "lqbnhdpj",  "fszkqnop",  "tnhssbbg",  "jyltqque",  "uwwsazxg",  "mwujixlj",  "wrslfkst",  "shmhlagd",  "rgdphggr",  "korsrnbu",  "rzjnunxy",  "rnjypyeo",  "gtvnifwz",  "uapadqvb",  "ovipnngd",  "dkehomjw",  "eaiejnmq",  "jeikkciu",  "oftckfsk",  "klydfonj",  "igglmwfo",  "fyubwdnh",  "ngzkhkpd",  "yuglfalc",  "jhjuufhh",  "dxemyuqq",  "skxsfkuf",  "bngixdvm",  "ibetxweu",  "vhkddick",  "yphvckps",  "vsfjvfuc",  "yslnkljn",  "owpmzvtw",  "hwqxmdkm",  "xedywgaa",  "gxspaddo",  "fgtuqtzz",  "lmdgicyj",  "wormnkqh",  "odjjjnjs",  "upwsehpy",  "cdnoenbr",  "palgbqbo",  "cxhtopct",  "atyclmda",  "sqqsghaw",  "kphxnffp",  "snajohsd",  "fgoqdmya",  "qukeyclq",  "ridnraeu",  "xxnrgycg",  "ithdkict",  "xkkvoupr",  "jdxzaowb",  "wsrakjua",  "tnlfvefb",  "tkopftbw",  "fflhizvk",  "qlviiyxs",  "tqlkpdji",  "wbkizspo",  "qfcnlwzy",  "icnypchf",  "rmcrtzhx",  "ibghzcrx",  "nwjeakcj",  "ozubzsep",  "thevuhvq",  "drmvjqbr",  "zlsxyeqi",  "kfbaywmd",  "uxpkilwv",  "nifwejqs",  "yjlhwrhl",  "jsotkgry",  "tnjboxch",  "loaljerf",  "howfiujr",  "zmqsffwn",  "uqrsbamt",  "othunkcr",  "ylhkojxs",  "kzldescv",  "irwynsjs",  "cytlwbvv",  "iqvupsei",  "wemgrrnj",  "akrqrpis",  "vocnluer",  "wjnscmyh",  "hekwlgim",  "ilmqutgu",  "qtnurohl",  "cjuclgbg",  "yivdapow",  "jrbhdxku",  "xholfbuw",  "grgfxaho",  "lquojibn",  "cbdendkb",  "mdurkdvz",  "dqdixboo",  "wvopazpt",  "xbxclroc",  "zjxgejjk",  "tmbfyyvz",  "cosjhwru",  "aqwtipsw",  "pmympjrh"]

letter1 = []
letter2 = []
letter3 = []
letter4 = []
letter5 = []
letter6 = []
letter7 = []
letter8 = []

for w in range(len(messages)):
    letter1.append(str((messages[w])[0]))

letter1 = "".join(letter1)

for w in range(len(messages)):
    letter2.append(str((messages[w])[1]))

letter2 = "".join(letter2)

for w in range(len(messages)):
    letter3.append(str((messages[w])[2]))

letter3 = "".join(letter3)

for w in range(len(messages)):
    letter4.append(str((messages[w])[3]))

letter4 = "".join(letter4)

for w in range(len(messages)):
    letter5.append(str((messages[w])[4]))

letter5 = "".join(letter5)

for w in range(len(messages)):
    letter6.append(str((messages[w])[5]))

letter6 = "".join(letter6)

for w in range(len(messages)):
    letter7.append(str((messages[w])[6]))

letter7 = "".join(letter7)

for w in range(len(messages)):
    letter8.append(str((messages[w])[7]))

letter8 = "".join(letter8)

letter1 = (str(collections.Counter(letter1)))[10]
letter2 = (str(collections.Counter(letter2)))[10]
letter3 = (str(collections.Counter(letter3)))[10]
letter4 = (str(collections.Counter(letter4)))[10]
letter5 = (str(collections.Counter(letter5)))[10]
letter6 = (str(collections.Counter(letter6)))[10]
letter7 = (str(collections.Counter(letter7)))[10]
letter8 = (str(collections.Counter(letter8)))[10]

print("The word is...")
print("".join(letter1+letter2+letter3+letter4+letter5+letter6+letter7+letter8))
