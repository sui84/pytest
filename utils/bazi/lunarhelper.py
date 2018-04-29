#encoding=utf-8
#http://www.cnblogs.com/hhh5460/p/4302499.html
import datetime
import pdb

class Lunar(object):
    #******************************************************************************
    # 下面为阴历计算所需的数据,为节省存储空间,所以采用下面比较变态的存储方法.
    #******************************************************************************
    #数组g_lunar_month_day存入阴历1901年到2050年每年中的月天数信息，
    #阴历每月只能是29或30天，一年用12（或13）个二进制位表示，对应位为1表30天，否则为29天
    g_lunar_month_day = [
        0x4ae0, 0xa570, 0x5268, 0xd260, 0xd950, 0x6aa8, 0x56a0, 0x9ad0, 0x4ae8, 0x4ae0,   #1910
        0xa4d8, 0xa4d0, 0xd250, 0xd548, 0xb550, 0x56a0, 0x96d0, 0x95b0, 0x49b8, 0x49b0,   #1920
        0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada8, 0x2b60, 0x9570, 0x4978, 0x4970, 0x64b0,   #1930
        0xd4a0, 0xea50, 0x6d48, 0x5ad0, 0x2b60, 0x9370, 0x92e0, 0xc968, 0xc950, 0xd4a0,   #1940
        0xda50, 0xb550, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950, 0xb4a8, 0x6ca0,   #1950
        0xb550, 0x55a8, 0x4da0, 0xa5b0, 0x52b8, 0x52b0, 0xa950, 0xe950, 0x6aa0, 0xad50,   #1960
        0xab50, 0x4b60, 0xa570, 0xa570, 0x5260, 0xe930, 0xd950, 0x5aa8, 0x56a0, 0x96d0,   #1970
        0x4ae8, 0x4ad0, 0xa4d0, 0xd268, 0xd250, 0xd528, 0xb540, 0xb6a0, 0x96d0, 0x95b0,   #1980
        0x49b0, 0xa4b8, 0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada0, 0xab60, 0x9370, 0x4978,   #1990
        0x4970, 0x64b0, 0x6a50, 0xea50, 0x6b28, 0x5ac0, 0xab60, 0x9368, 0x92e0, 0xc960,   #2000
        0xd4a8, 0xd4a0, 0xda50, 0x5aa8, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950,   #2010
        0xb4a0, 0xb550, 0xb550, 0x55a8, 0x4ba0, 0xa5b0, 0x52b8, 0x52b0, 0xa930, 0x74a8,   #2020
        0x6aa0, 0xad50, 0x4da8, 0x4b60, 0x9570, 0xa4e0, 0xd260, 0xe930, 0xd530, 0x5aa0,   #2030
        0x6b50, 0x96d0, 0x4ae8, 0x4ad0, 0xa4d0, 0xd258, 0xd250, 0xd520, 0xdaa0, 0xb5a0,   #2040
        0x56d0, 0x4ad8, 0x49b0, 0xa4b8, 0xa4b0, 0xaa50, 0xb528, 0x6d20, 0xada0, 0x55b0,   #2050
    ]

    #数组gLanarMonth存放阴历1901年到2050年闰月的月份，如没有则为0，每字节存两年
    g_lunar_month = [
        0x00, 0x50, 0x04, 0x00, 0x20,   #1910
        0x60, 0x05, 0x00, 0x20, 0x70,   #1920
        0x05, 0x00, 0x40, 0x02, 0x06,   #1930
        0x00, 0x50, 0x03, 0x07, 0x00,   #1940
        0x60, 0x04, 0x00, 0x20, 0x70,   #1950
        0x05, 0x00, 0x30, 0x80, 0x06,   #1960
        0x00, 0x40, 0x03, 0x07, 0x00,   #1970
        0x50, 0x04, 0x08, 0x00, 0x60,   #1980
        0x04, 0x0a, 0x00, 0x60, 0x05,   #1990
        0x00, 0x30, 0x80, 0x05, 0x00,   #2000
        0x40, 0x02, 0x07, 0x00, 0x50,   #2010
        0x04, 0x09, 0x00, 0x60, 0x04,   #2020
        0x00, 0x20, 0x60, 0x05, 0x00,   #2030
        0x30, 0xb0, 0x06, 0x00, 0x50,   #2040
        0x02, 0x07, 0x00, 0x50, 0x03    #2050
    ]

    START_YEAR = 1901

    # 天干
    gan = u'甲乙丙丁戊己庚辛壬癸'
    # 地支
    zhi = u'子丑寅卯辰巳午未申酉戌亥'
    # 生肖
    xiao = u'鼠牛虎兔龙蛇马羊猴鸡狗猪'
    # 月份
    lm = u'正二三四五六七八九十冬腊'
    # 日份
    ld = u'初一初二初三初四初五初六初七初八初九初十十一十二十三十四十五十六十七十八十九二十廿一廿二廿三廿四廿五廿六廿七廿八廿九三十'
    # 节气
    jie = u'小寒大寒立春雨水惊蛰春分清明谷雨立夏小满芒种夏至小暑大暑立秋处暑白露秋分寒露霜降立冬小雪大雪冬至'

    jieqi_mins = [{"jieqiid":0,"zhiid":1,"mins":0},{"jieqiid":1,"zhiid":1,"mins":21208}
                  ,{"jieqiid":2,"zhiid":2,"mins":42467},{"jieqiid":3,"zhiid":2,"mins":63836}
                  ,{"jieqiid":4,"zhiid":3,"mins":85337},{"jieqiid":5,"zhiid":3,"mins":107014}
                  ,{"jieqiid":6,"zhiid":4,"mins":128867},{"jieqiid":7,"zhiid":4,"mins":150921}
                  ,{"jieqiid":8,"zhiid":5,"mins":173149},{"jieqiid":9,"zhiid":5,"mins":195551}
                  ,{"jieqiid":10,"zhiid":6,"mins":218072},{"jieqiid":11,"zhiid":6,"mins":240693}
                  ,{"jieqiid":12,"zhiid":7,"mins":263343},{"jieqiid":13,"zhiid":7,"mins":285989}
                  ,{"jieqiid":14,"zhiid":8,"mins":308563},{"jieqiid":15,"zhiid":8,"mins":331033}
                  ,{"jieqiid":16,"zhiid":9,"mins":353350},{"jieqiid":17,"zhiid":9,"mins":375494}
                  ,{"jieqiid":18,"zhiid":10,"mins":397447},{"jieqiid":19,"zhiid":10,"mins":419210}
                  ,{"jieqiid":20,"zhiid":11,"mins":440795},{"jieqiid":21,"zhiid":11,"mins":462224}
                  ,{"jieqiid":22,"zhiid":0,"mins":483532},{"jieqiid":23,"zhiid":0,"mins":504758}]

    # regsion
    '''
    yearno	bitdt	bitdata	leapmon	ydays	fromdays	todays
    1900	0x004BD8	19416	8	384	NULL	384
    1901	0x004AE0	19168	0	354	384	738
    1902	0x00A570	42352	0	355	738	1093
    1903	0x0054D5	21717	5	383	1093	1476
    1904	0x00D260	53856	0	354	1476	1830
    1905	0x00D950	55632	0	355	1830	2185
    1906	0x016554	91476	4	384	2185	2569
    1907	0x0056A0	22176	0	354	2569	2923
    1908	0x009AD0	39632	0	355	2923	3278
    1909	0x0055D2	21970	2	384	3278	3662
    1910	0x004AE0	19168	0	354	3662	4016
    1911	0x00A5B6	42422	6	384	4016	4400
    1912	0x00A4D0	42192	0	354	4400	4754
    1913	0x00D250	53840	0	354	4754	5108
    1914	0x01D255	119381	5	384	5108	5492
    1915	0x00B540	46400	0	354	5492	5846
    1916	0x00D6A0	54944	0	355	5846	6201
    1917	0x00ADA2	44450	2	384	6201	6585
    1918	0x0095B0	38320	0	355	6585	6940
    1919	0x014977	84343	7	384	6940	7324
    1920	0x004970	18800	0	354	7324	7678
    1921	0x00A4B0	42160	0	354	7678	8032
    1922	0x00B4B5	46261	5	384	8032	8416
    1923	0x006A50	27216	0	354	8416	8770
    1924	0x006D40	27968	0	354	8770	9124
    1925	0x01AB54	109396	4	385	9124	9509
    1926	0x002B60	11104	0	354	9509	9863
    1927	0x009570	38256	0	355	9863	10218
    1928	0x0052F2	21234	2	384	10218	10602
    1929	0x004970	18800	0	354	10602	10956
    1930	0x006566	25958	6	383	10956	11339
    1931	0x00D4A0	54432	0	354	11339	11693
    1932	0x00EA50	59984	0	355	11693	12048
    1933	0x006E95	28309	5	384	12048	12432
    1934	0x005AD0	23248	0	355	12432	12787
    1935	0x002B60	11104	0	354	12787	13141
    1936	0x0186E3	100067	3	384	13141	13525
    1937	0x0092E0	37600	0	354	13525	13879
    1938	0x01C8D7	116951	7	384	13879	14263
    1939	0x00C950	51536	0	354	14263	14617
    1940	0x00D4A0	54432	0	354	14617	14971
    1941	0x01D8A6	120998	6	384	14971	15355
    1942	0x00B550	46416	0	355	15355	15710
    1943	0x0056A0	22176	0	354	15710	16064
    1944	0x01A5B4	107956	4	385	16064	16449
    1945	0x0025D0	9680	0	354	16449	16803
    1946	0x0092D0	37584	0	354	16803	17157
    1947	0x00D2B2	53938	2	384	17157	17541
    1948	0x00A950	43344	0	354	17541	17895
    1949	0x00B557	46423	7	384	17895	18279
    1950	0x006CA0	27808	0	354	18279	18633
    1951	0x00B550	46416	0	355	18633	18988
    1952	0x015355	86869	5	384	18988	19372
    1953	0x004DA0	19872	0	354	19372	19726
    1954	0x00A5B0	42416	0	355	19726	20081
    1955	0x014573	83315	3	384	20081	20465
    1956	0x0052B0	21168	0	354	20465	20819
    1957	0x00A9A8	43432	8	383	20819	21202
    1958	0x00E950	59728	0	355	21202	21557
    1959	0x006AA0	27296	0	354	21557	21911
    1960	0x00AEA6	44710	6	384	21911	22295
    1961	0x00AB50	43856	0	355	22295	22650
    1962	0x004B60	19296	0	354	22650	23004
    1963	0x00AAE4	43748	4	384	23004	23388
    1964	0x00A570	42352	0	355	23388	23743
    1965	0x005260	21088	0	353	23743	24096
    1966	0x00F263	62051	3	384	24096	24480
    1967	0x00D950	55632	0	355	24480	24835
    1968	0x005B57	23383	7	384	24835	25219
    1969	0x0056A0	22176	0	354	25219	25573
    1970	0x0096D0	38608	0	355	25573	25928
    1971	0x004DD5	19925	5	384	25928	26312
    1972	0x004AD0	19152	0	354	26312	26666
    1973	0x00A4D0	42192	0	354	26666	27020
    1974	0x00D4D4	54484	4	384	27020	27404
    1975	0x00D250	53840	0	354	27404	27758
    1976	0x00D558	54616	8	384	27758	28142
    1977	0x00B540	46400	0	354	28142	28496
    1978	0x00B6A0	46752	0	355	28496	28851
    1979	0x0195A6	103846	6	384	28851	29235
    1980	0x0095B0	38320	0	355	29235	29590
    1981	0x0049B0	18864	0	354	29590	29944
    1982	0x00A974	43380	4	384	29944	30328
    1983	0x00A4B0	42160	0	354	30328	30682
    1984	0x00B27A	45690	10	384	30682	31066
    1985	0x006A50	27216	0	354	31066	31420
    1986	0x006D40	27968	0	354	31420	31774
    1987	0x00AF46	44870	6	384	31774	32158
    1988	0x00AB60	43872	0	355	32158	32513
    1989	0x009570	38256	0	355	32513	32868
    1990	0x004AF5	19189	5	384	32868	33252
    1991	0x004970	18800	0	354	33252	33606
    1992	0x0064B0	25776	0	354	33606	33960
    1993	0x0074A3	29859	3	383	33960	34343
    1994	0x00EA50	59984	0	355	34343	34698
    1995	0x006B58	27480	8	384	34698	35082
    1996	0x0055C0	21952	0	354	35082	35436
    1997	0x00AB60	43872	0	355	35436	35791
    1998	0x0096D5	38613	5	384	35791	36175
    1999	0x0092E0	37600	0	354	36175	36529
    2000	0x00C960	51552	0	354	36529	36883
    2001	0x00D954	55636	4	384	36883	37267
    2002	0x00D4A0	54432	0	354	37267	37621
    2003	0x00DA50	55888	0	355	37621	37976
    2004	0x007552	30034	2	384	37976	38360
    2005	0x0056A0	22176	0	354	38360	38714
    2006	0x00ABB7	43959	7	385	38714	39099
    2007	0x0025D0	9680	0	354	39099	39453
    2008	0x0092D0	37584	0	354	39453	39807
    2009	0x00CAB5	51893	5	384	39807	40191
    2010	0x00A950	43344	0	354	40191	40545
    2011	0x00B4A0	46240	0	354	40545	40899
    2012	0x00BAA4	47780	4	384	40899	41283
    2013	0x00AD50	44368	0	355	41283	41638
    2014	0x0055D9	21977	9	384	41638	42022
    2015	0x004BA0	19360	0	354	42022	42376
    2016	0x00A5B0	42416	0	355	42376	42731
    2017	0x015176	86390	6	384	42731	43115
    2018	0x0052B0	21168	0	354	43115	43469
    2019	0x00A930	43312	0	354	43469	43823
    2020	0x007954	31060	4	384	43823	44207
    2021	0x006AA0	27296	0	354	44207	44561
    2022	0x00AD50	44368	0	355	44561	44916
    2023	0x005B52	23378	2	384	44916	45300
    2024	0x004B60	19296	0	354	45300	45654
    2025	0x00A6E6	42726	6	384	45654	46038
    2026	0x00A4E0	42208	0	354	46038	46392
    2027	0x00D260	53856	0	354	46392	46746
    2028	0x00EA65	60005	5	384	46746	47130
    2029	0x00D530	54576	0	355	47130	47485
    2030	0x005AA0	23200	0	354	47485	47839
    2031	0x0076A3	30371	3	384	47839	48223
    2032	0x0096D0	38608	0	355	48223	48578
    2033	0x004BD7	19415	7	384	48578	48962
    2034	0x004AD0	19152	0	354	48962	49316
    2035	0x00A4D0	42192	0	354	49316	49670
    2036	0x01D0B6	118966	6	384	49670	50054
    2037	0x00D250	53840	0	354	50054	50408
    2038	0x00D520	54560	0	354	50408	50762
    2039	0x00DD45	56645	5	384	50762	51146
    2040	0x00B5A0	46496	0	355	51146	51501
    2041	0x0056D0	22224	0	355	51501	51856
    2042	0x0055B2	21938	2	384	51856	52240
    2043	0x0049B0	18864	0	354	52240	52594
    2044	0x00A577	42359	7	384	52594	52978
    2045	0x00A4B0	42160	0	354	52978	53332
    2046	0x00AA50	43600	0	354	53332	53686
    2047	0x01B255	111189	5	384	53686	54070
    2048	0x006D20	27936	0	354	54070	54424
    2049	0x00ADA0	44448	0	355	54424	54779
    2050	0x014B63	84835	3	384	54779	55163

    JieQiId	JieQiMonth	JieQi	ZhiId	Minutes
    1	12	小寒	2	0
    2	12	大寒	2	21208
    3	1	立春	3	42467
    4	1	雨水	3	63836
    5	2	惊蛰	4	85337
    6	2	春分	4	107014
    7	3	清明	5	128867
    8	3	谷雨	5	150921
    9	4	立夏	6	173149
    10	4	小满	6	195551
    11	5	芒种	7	218072
    12	5	夏至	7	240693
    13	6	小暑	8	263343
    14	6	大暑	8	285989
    15	7	立秋	9	308563
    16	7	处暑	9	331033
    17	8	白露	10	353350
    18	8	秋分	10	375494
    19	9	寒露	11	397447
    20	9	霜降	11	419210
    21	10	立冬	12	440795
    22	10	小雪	12	462224
    23	11	大雪	1	483532
    24	11	冬至	1	504758
    '''


    #endregion

    def __init__(self, dt = None):
        '''初始化：参数为datetime.datetime类实例，默认当前时间'''
        self.localtime = dt if dt else datetime.datetime.today()

    def sx_year(self): # 返回生肖年
        ct = self.localtime #取当前时间

        year = self.ln_year() - 3 - 1 # 农历年份减3 （说明：补减1）
        year = year % 12 # 模12，得到地支数
        return self.xiao[year]

    def gzid_year(self): # 返回干支纪年
        ct = self.localtime #取当前时间
        year = self.ln_year() - 3 - 1 # 农历年份减3 （说明：补减1）
        G = year % 10 # 模10，得到天干数
        Z = year % 12 # 模12，得到地支数
        return G,Z

    def gz_year(self): # 返回干支纪年
        G,Z = self.gzid_year()
        return self.gan[G] + self.zhi[Z]

    def get_index(self,G):
        #根据年上起月表，日上起时表，返回index
        if G ==0 or G == 5:
            index=0
        elif G ==1 or G == 6:
            index=2
        elif G ==2 or G == 7:
            index=4
        elif G ==3 or G == 8:
            index=6
        elif G ==4 or G == 9:
            index=8
        return index

    def gzid_month(self): # 返回干支纪月
        jieqiid,MZ,jieqi,jqstart,jqend=self._get_jieqi()
        YG,YZ=self.gzid_year()
        index = self.get_index(YG)
        MG = (index+MZ)%10
        return MG,MZ

    def gz_month(self): # 返回干支纪月
        G,Z = self.gzid_month()
        return self.gan[G]+self.zhi[Z]

    def gzid_day(self): # 返回干支纪日
        ct = self.localtime #取当前时间
        C = ct.year // 100 #取世纪数，减一
        y = ct.year % 100 #取年份后两位（若为1月、2月则当前年份减一）
        y = y - 1 if ct.month == 1 or ct.month == 2 else y
        M = ct.month #取月份（若为1月、2月则分别按13、14来计算）
        M = M + 12 if ct.month == 1 or ct.month == 2 else M
        d = ct.day #取日数
        i = 0 if ct.month % 2 == 1 else 6 #取i （奇数月i=0，偶数月i=6）

        #下面两个是网上的公式
        # http://baike.baidu.com/link?url=MbTKmhrTHTOAz735gi37tEtwd29zqE9GJ92cZQZd0X8uFO5XgmyMKQru6aetzcGadqekzKd3nZHVS99rewya6q
        # 计算干（说明：补减1）
        G = 4 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d - 3 - 1
        G = G % 10
        # 计算支（说明：补减1）
        Z = 8 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d + 7 + i - 1
        Z = Z % 12
        return G,Z

    def gz_day(self): # 返回干支纪日
        G,Z = self.gzid_day()
        return self.gan[G] + self.zhi[Z]

    def gzid_hour(self): # 返回干支纪时（时辰）
        ct = self.localtime #取当前时间
        #计算支
        Z = round((ct.hour/2) + 0.1) % 12 # 之所以加0.1是因为round的bug!!
        Z = int(Z)
        RG,RZ = self.gzid_day()
        index = self.get_index(RG)
        G =  (index+Z)%10
        return G,Z

    def gz_hour(self): #返回 干支纪时（时辰）
        G,Z = self.gzid_hour()
        return self.gan[G]+self.zhi[Z]

    def ln_year(self): # 返回农历年
        year, _, _ = self.ln_date()
        return year

    def ln_month(self): # 返回农历月
        _, month, _ = self.ln_date()
        return month

    def ln_day(self): # 返回农历日
        _, _, day = self.ln_date()
        return day

    def ln_date(self): # 返回农历日期整数元组（年、月、日）（查表法）
        delta_days = self._date_diff()

        #阳历1901年2月19日为阴历1901年正月初一
        #阳历1901年1月1日到2月19日共有49天
        if (delta_days < 49):
            year = self.START_YEAR - 1
            if (delta_days <19):
              month = 11;
              day = 11 + delta_days
            else:
                month = 12;
                day = delta_days - 18
            return (year, month, day)

        #下面从阴历1901年正月初一算起
        delta_days -= 49
        year, month, day = self.START_YEAR, 1, 1
        #计算年
        tmp = self._lunar_year_days(year)
        while delta_days >= tmp:
            delta_days -= tmp
            year += 1
            tmp = self._lunar_year_days(year)
            #print year,tmp

        #计算月
        (foo, tmp) = self._lunar_month_days(year, month)
        while delta_days >= tmp:
            delta_days -= tmp
            if (month == self._get_leap_month(year)):
                (tmp, foo) = self._lunar_month_days(year, month)
                if (delta_days < tmp):
                    return (0, 0, 0)
                delta_days -= tmp
            month += 1
            (foo, tmp) = self._lunar_month_days(year, month)

        #计算日
        day += delta_days
        return (year, month, day)

    def ln_date_str(self):# 返回农历日期字符串，形如：农历正月初九
        _, month, day = self.ln_date()
        return u'农历{}月{}'.format(self.lm[month-1], self.ld[(day-1)*2:day*2])

    def ln_jie(self): # 返回农历节气
        ct = self.localtime #取当前时间
        year = ct.year
        for i in range(24):
            #因为两个都是浮点数，不能用相等表示
            delta = self._julian_day() - self._julian_day_of_ln_jie(year, i)
            if -.5 <= delta <= .5:
                print i
                return self.jie[i*2:(i+1)*2]
        return ''

    #显示日历
    def calendar(self):
        pass

    #######################################################
    #            下面皆为私有函数
    #######################################################

    def _date_diff(self):
        '''返回基于1901/01/01日差数'''
        return (self.localtime - datetime.datetime(1901, 1, 1)).days

    def _get_leap_month(self, lunar_year):
        flag = self.g_lunar_month[(lunar_year - self.START_YEAR) // 2]
        if (lunar_year - self.START_YEAR) % 2:
            return flag & 0x0f
        else:
            return flag >> 4

    def _lunar_month_days(self, lunar_year, lunar_month):
        if (lunar_year < self.START_YEAR):
            return 30

        high, low = 0, 29
        iBit = 16 - lunar_month;

        if (lunar_month > self._get_leap_month(lunar_year) and self._get_leap_month(lunar_year)):
            iBit -= 1

        if (self.g_lunar_month_day[lunar_year - self.START_YEAR] & (1 << iBit)):
            low += 1

        if (lunar_month == self._get_leap_month(lunar_year)):
            if (self.g_lunar_month_day[lunar_year - self.START_YEAR] & (1 << (iBit -1))):
                 high = 30
            else:
                 high = 29

        return (high, low)

    def _lunar_year_days(self, year):
        days = 0
        for i in range(1, 13):
            (high, low) = self._lunar_month_days(year, i)
            days += high
            days += low
        return days

    # 返回指定公历日期的儒略日（http://blog.csdn.net/orbit/article/details/9210413）
    def _julian_day(self):
        ct = self.localtime #取当前时间
        year = ct.year
        month = ct.month
        day = ct.day

        if month <= 2:
            month += 12
            year -= 1

        B = year / 100
        B = 2 - B + year / 400

        dd = day + 0.5000115740 #本日12:00后才是儒略日的开始(过一秒钟)*/
        return int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + B - 1524.5

    # 返回指定年份的节气的儒略日数（http://blog.csdn.net/orbit/article/details/9210413）
    def _julian_day_of_ln_jie(self, year, st):
        s_stAccInfo =[
             0.00, 1272494.40, 2548020.60, 3830143.80, 5120226.60, 6420865.80,
             7732018.80, 9055272.60, 10388958.00, 11733065.40, 13084292.40, 14441592.00,
             15800560.80, 17159347.20, 18513766.20, 19862002.20, 21201005.40, 22529659.80,
             23846845.20, 25152606.00, 26447687.40, 27733451.40, 29011921.20, 30285477.60]

        #已知1900年小寒时刻为1月6日02:05:00
        base1900_SlightColdJD = 2415025.5868055555

        if (st < 0) or (st > 24):
            return 0.0

        stJd = 365.24219878 * (year - 1900) + s_stAccInfo[st] / 86400.0

        return base1900_SlightColdJD + stJd

    def _get_jieqi(self):
        #	set @jieQiStartDt = convert(datetime,'1900-01-06 02:05:00',20)
	    #update #JieQi set fromDt = dateadd(minute,525948.76 * (@solarY - 1900) + Minutes,@jieQiStartDt)
        #已知1900年小寒时刻为1月6日02:05:00
        basedt = datetime.datetime(1900,1,6,2,5,0)
        ystart =basedt+ datetime.timedelta(minutes=int(525948.76 *(self.localtime.year - 1900)))
        i=0
        for jm in self.jieqi_mins:
            jqstart = ystart+datetime.timedelta(minutes=int(jm.get('mins')))
            #上年最后一个月
            if(self.localtime < jqstart):
                jieqiid = 23
                lastyearjq = basedt+ datetime.timedelta(minutes=int(525948.76 *(self.localtime.year - 1900-1)))+datetime.timedelta(minutes=int(504758))
                return jieqiid,0,self.jie[jieqiid*2:(jieqiid+1)*2],lastyearjq,ystart
            if(i+1 < len(self.jieqi_mins)):
                jqend = ystart+datetime.timedelta(minutes=int(self.jieqi_mins[i+1].get('mins')))
            else:
                jqend = basedt+datetime.timedelta(minutes=525948.76 *(self.localtime.year - 1900+1))
            #print self.localtime,jqstart,jqend
            if self.localtime >= jqstart and self.localtime < jqend:
                jieqiid = jm.get('jieqiid')
                return jieqiid,jm.get('zhiid'),self.jie[jieqiid*2:(jieqiid+1)*2],jqstart,jqend
            i+=1


if __name__ == '__main__':
    ct = datetime.datetime(1984,10,8,8,0,0)
    ln = Lunar(ct)
    print ln
    print(u'公历 {}  北京时间 {}'.format(ln.localtime.date(), ln.localtime.time()))
    print(u'{} {} {}年 {}月 {}日 {}时'.format(ln.ln_date_str(), ln.sx_year(), ln.gz_year(),ln.gz_month(), ln.gz_day(), ln.gz_hour()))
    jieqiid,zhiid,jieqi,jqstart,jqend=ln._get_jieqi()
    print(u'节气：{} 从 {} 到 {} '.format(jieqi,jqstart,jqend))
