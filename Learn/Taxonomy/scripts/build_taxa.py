"""Build data/taxa.json from a compact Python tree definition.

Scope:
- 界: 5 (Monera, Protista, Fungi, Plantae, Animalia, 五界系统)
- 门: comprehensive, all major phyla across kingdoms
- 纲: comprehensive, major classes in each phylum
- 目: comprehensive, major orders in each class
- 科/属/种: common, well-known representatives
"""
import json
from pathlib import Path


def N(zh, latin, children=None, wiki_zh=None, wiki_en=None, note=None, dist=None):
    """Create a taxon node (dict) in the canonical shape.

    dist: short text distinguishing this taxon from its siblings.
    """
    d = {"zh": zh, "latin": latin}
    if wiki_zh:
        d["wiki_zh"] = wiki_zh
    if wiki_en:
        d["wiki_en"] = wiki_en
    if note:
        d["note"] = note
    if dist:
        d["distinction"] = dist
    if children:
        d["children"] = children
    return d


# Helper builders
def genus_species(gen_zh, gen_latin, species_list, wiki_zh_gen=None):
    """species_list: list of (zh, latin, wiki_zh or None)"""
    return N(gen_zh, gen_latin, wiki_zh=wiki_zh_gen, children=[
        N(s[0], s[1], wiki_zh=s[2] if len(s) > 2 else None) for s in species_list
    ])


# ============================================================
# 原核生物界 Monera (细菌 + 古菌)
# ============================================================
kingdom_monera = N(
    "原核生物界", "Monera",
    wiki_zh="原核生物", wiki_en="Prokaryote",
    note="无细胞核；含细菌域与古菌域",
    dist="原核：无真正细胞核、无膜细胞器，单细胞",
    children=[
        # --- 细菌 Bacteria ---
        N("蓝菌门", "Cyanobacteria", wiki_zh="藍菌門", note="含光合色素，旧称蓝绿藻"),
        N("变形菌门", "Pseudomonadota", wiki_zh="變形菌門", note="原 Proteobacteria；革兰阴性最大门",
          children=[
              N("α-变形菌纲", "Alphaproteobacteria", wiki_zh="α-變形菌綱", note="根瘤菌、立克次体"),
              N("β-变形菌纲", "Betaproteobacteria", wiki_zh="β-變形菌綱"),
              N("γ-变形菌纲", "Gammaproteobacteria", wiki_zh="γ-變形菌綱",
                children=[
                    N("肠杆菌目", "Enterobacterales",
                      children=[
                          N("肠杆菌科", "Enterobacteriaceae", wiki_zh="腸桿菌科",
                            children=[
                                N("埃希氏菌属", "Escherichia", wiki_zh="埃希氏菌屬",
                                  children=[N("大肠杆菌", "Escherichia coli", wiki_zh="大腸桿菌")]),
                                N("沙门氏菌属", "Salmonella", wiki_zh="沙門氏菌屬",
                                  children=[N("肠道沙门氏菌", "Salmonella enterica", wiki_zh="腸道沙門氏菌")]),
                                genus_species("志贺氏菌属", "Shigella", [("福氏志贺菌", "Shigella flexneri", "福氏志賀菌")], wiki_zh_gen="志賀氏菌屬"),
                                genus_species("克雷伯氏菌属", "Klebsiella", [("肺炎克雷伯菌", "Klebsiella pneumoniae", "肺炎克雷伯菌")], wiki_zh_gen="克雷伯氏菌屬"),
                            ])
                      ]),
                    N("假单胞菌目", "Pseudomonadales"),
                    N("弧菌目", "Vibrionales", wiki_zh="弧菌目", note="霍乱弧菌"),
                ]),
              N("δ-变形菌纲", "Deltaproteobacteria", wiki_zh="δ-變形菌綱"),
              N("ε-变形菌纲", "Epsilonproteobacteria", wiki_zh="ε-變形菌綱", note="幽门螺杆菌",
                children=[
                    N("弯曲菌目", "Campylobacterales", wiki_zh="彎曲菌目",
                      children=[
                          N("螺杆菌科", "Helicobacteraceae", wiki_zh="螺桿菌科",
                            children=[
                                genus_species("螺杆菌属", "Helicobacter", [("幽门螺杆菌", "Helicobacter pylori", "幽門螺桿菌")], wiki_zh_gen="螺桿菌屬"),
                            ]),
                      ]),
                ]),
          ]),
        N("厚壁菌门", "Bacillota", wiki_zh="厚壁菌門", note="原 Firmicutes；革兰阳性",
          children=[
              N("芽孢杆菌纲", "Bacilli", wiki_zh="芽孢桿菌綱",
                children=[
                    N("乳杆菌目", "Lactobacillales", note="乳酸菌、链球菌",
                      children=[
                          N("乳杆菌科", "Lactobacillaceae", wiki_zh="乳桿菌科",
                            children=[
                                genus_species("乳杆菌属", "Lactobacillus", [("保加利亚乳杆菌", "Lactobacillus delbrueckii", "德氏乳桿菌")], wiki_zh_gen="乳桿菌屬"),
                            ]),
                          N("链球菌科", "Streptococcaceae", wiki_zh="鏈球菌科",
                            children=[
                                genus_species("链球菌属", "Streptococcus", [("化脓性链球菌", "Streptococcus pyogenes", "化膿性鏈球菌")], wiki_zh_gen="鏈球菌屬"),
                            ]),
                      ]),
                    N("芽孢杆菌目", "Bacillales", note="炭疽杆菌、金黄色葡萄球菌",
                      children=[
                          N("芽孢杆菌科", "Bacillaceae", wiki_zh="芽孢桿菌科",
                            children=[
                                genus_species("芽孢杆菌属", "Bacillus", [
                                    ("枯草芽孢杆菌", "Bacillus subtilis", "枯草芽孢桿菌"),
                                    ("炭疽杆菌", "Bacillus anthracis", "炭疽桿菌"),
                                ], wiki_zh_gen="芽孢桿菌屬"),
                            ]),
                          N("葡萄球菌科", "Staphylococcaceae", wiki_zh="葡萄球菌科",
                            children=[
                                genus_species("葡萄球菌属", "Staphylococcus", [("金黄色葡萄球菌", "Staphylococcus aureus", "金黃色葡萄球菌")], wiki_zh_gen="葡萄球菌屬"),
                            ]),
                      ]),
                ]),
              N("梭菌纲", "Clostridia", wiki_zh="梭菌綱", note="破伤风、肉毒梭菌",
                children=[
                    N("梭菌目", "Clostridiales", wiki_zh="梭菌目",
                      children=[
                          N("梭菌科", "Clostridiaceae", wiki_zh="梭菌科",
                            children=[
                                genus_species("梭菌属", "Clostridium", [
                                    ("破伤风梭菌", "Clostridium tetani", "破傷風梭菌"),
                                    ("肉毒梭菌", "Clostridium botulinum", "肉毒桿菌"),
                                ], wiki_zh_gen="梭菌屬"),
                            ]),
                      ])
                ]),
          ]),
        N("放线菌门", "Actinomycetota", wiki_zh="放線菌門", note="链霉菌、结核杆菌、双歧杆菌",
          children=[
              N("放线菌纲", "Actinomycetia", wiki_zh="放線菌綱", dist="高GC革兰阳性；多产抗生素",
                children=[
                    N("棒状杆菌目", "Corynebacteriales", wiki_zh="棒狀桿菌目",
                      children=[
                          N("分枝杆菌科", "Mycobacteriaceae", wiki_zh="分枝桿菌科",
                            children=[
                                genus_species("分枝杆菌属", "Mycobacterium", [
                                    ("结核分枝杆菌", "Mycobacterium tuberculosis", "結核分枝桿菌"),
                                ], wiki_zh_gen="分枝桿菌屬"),
                            ]),
                      ]),
                    N("链霉菌目", "Streptomycetales", wiki_zh="鏈黴菌目",
                      children=[
                          N("链霉菌科", "Streptomycetaceae", wiki_zh="鏈黴菌科",
                            children=[
                                genus_species("链霉菌属", "Streptomyces", [("灰色链霉菌", "Streptomyces griseus", "灰色鏈黴菌")], wiki_zh_gen="鏈黴菌屬"),
                            ]),
                      ]),
                    N("双歧杆菌目", "Bifidobacteriales", wiki_zh="雙歧桿菌目",
                      children=[
                          N("双歧杆菌科", "Bifidobacteriaceae", wiki_zh="雙歧桿菌科",
                            children=[
                                genus_species("双歧杆菌属", "Bifidobacterium", [("两歧双歧杆菌", "Bifidobacterium bifidum", "兩歧雙歧桿菌")], wiki_zh_gen="雙歧桿菌屬"),
                            ]),
                      ]),
                ]),
          ]),
        N("拟杆菌门", "Bacteroidota", wiki_zh="擬桿菌門", note="肠道常见菌群"),
        N("螺旋体门", "Spirochaetota", wiki_zh="螺旋體門", note="梅毒螺旋体、钩端螺旋体"),
        N("衣原体门", "Chlamydiota", wiki_zh="衣原體門", note="沙眼衣原体"),
        N("疣微菌门", "Verrucomicrobiota", wiki_zh="疣微菌門"),
        N("绿弯菌门", "Chloroflexota", wiki_zh="綠彎菌門", note="光合自养"),
        N("梭杆菌门", "Fusobacteriota", wiki_zh="梭桿菌門"),
        N("脱硫杆菌门", "Desulfobacterota", wiki_zh="脫硫桿菌門"),
        N("酸杆菌门", "Acidobacteriota", wiki_zh="酸桿菌門"),
        # --- 古菌 Archaea ---
        N("广古菌门", "Euryarchaeota", wiki_zh="廣古菌門", note="古菌；甲烷菌、盐杆菌"),
        N("泉古菌门", "Crenarchaeota", wiki_zh="泉古菌門", note="古菌；嗜热嗜酸"),
        N("奇古菌门", "Thaumarchaeota", wiki_zh="奇古菌門", note="古菌；氨氧化"),
    ]
)

# ============================================================
# 原生生物界 Protista
# ============================================================
kingdom_protista = N(
    "原生生物界", "Protista",
    wiki_zh="原生生物",
    note="并系类群；单细胞真核生物的统称",
    dist="真核、单细胞（或简单多细胞），不归入动植菌",
    children=[
        N("纤毛虫门", "Ciliophora", wiki_zh="纖毛蟲門",
          note="草履虫、钟虫",
          children=[
              N("寡膜纲", "Oligohymenophorea",
                children=[
                    N("膜口目", "Peniculida",
                      children=[
                          N("草履虫科", "Parameciidae",
                            children=[
                                N("草履虫属", "Paramecium", wiki_zh="草履蟲屬",
                                  children=[N("大草履虫", "Paramecium caudatum", wiki_zh="草履蟲")])
                            ])
                      ])
                ])
          ]),
        N("变形虫门", "Amoebozoa", wiki_zh="變形蟲門", note="变形虫、黏菌"),
        N("眼虫门", "Euglenozoa", wiki_zh="眼蟲門", note="眼虫、锥虫"),
        N("顶复门", "Apicomplexa", wiki_zh="頂複門", note="疟原虫、弓形虫"),
        N("鞭毛虫门", "Sarcomastigophora", wiki_zh="鞭毛蟲", note="历史类群；已拆分"),
        N("红藻门", "Rhodophyta", wiki_zh="紅藻門", note="紫菜、石花菜"),
        N("褐藻门", "Phaeophyta", wiki_zh="褐藻", note="海带、裙带菜"),
        N("硅藻门", "Bacillariophyta", wiki_zh="硅藻", note="浮游植物主力"),
        N("绿藻门", "Chlorophyta", wiki_zh="綠藻", note="衣藻、石莼；与陆生植物同源"),
        N("甲藻门", "Dinoflagellata", wiki_zh="甲藻", note="赤潮主因"),
        N("卵菌门", "Oomycota", wiki_zh="卵菌", note="疫霉、霜霉"),
        N("有孔虫门", "Foraminifera", wiki_zh="有孔蟲"),
        N("放射虫门", "Radiolaria", wiki_zh="放射蟲"),
    ]
)

# ============================================================
# 真菌界 Fungi
# ============================================================
kingdom_fungi = N(
    "真菌界", "Fungi", wiki_zh="真菌",
    note="异养，细胞壁含几丁质",
    dist="真核、异养（腐生/寄生），细胞壁含几丁质；无叶绿体",
    children=[
        N("担子菌门", "Basidiomycota", wiki_zh="擔子菌門", note="蘑菇、木耳、灵芝",
          dist="产担孢子(棒状担子外生4孢)；菌褶/菌孔典型；子实体可见",
          children=[
              N("伞菌纲", "Agaricomycetes", wiki_zh="傘菌綱",
                children=[
                    N("伞菌目", "Agaricales", wiki_zh="傘菌目",
                      children=[
                          N("蘑菇科", "Agaricaceae", wiki_zh="蘑菇科",
                            children=[
                                N("蘑菇属", "Agaricus", wiki_zh="蘑菇屬",
                                  children=[N("双孢蘑菇", "Agaricus bisporus", wiki_zh="雙孢蘑菇")]),
                            ]),
                          N("侧耳科", "Pleurotaceae",
                            children=[
                                N("侧耳属", "Pleurotus", wiki_zh="側耳屬",
                                  children=[
                                      N("平菇", "Pleurotus ostreatus", wiki_zh="糙皮側耳"),
                                      N("杏鲍菇", "Pleurotus eryngii", wiki_zh="杏鮑菇"),
                                  ]),
                            ]),
                          N("口蘑科", "Tricholomataceae", wiki_zh="口蘑科", dist="菌褶自由或附生；含香菇、松茸",
                            children=[
                                genus_species("香菇属", "Lentinula", [("香菇", "Lentinula edodes", "香菇")], wiki_zh_gen="香菇屬"),
                                genus_species("口蘑属", "Tricholoma", [("松茸", "Tricholoma matsutake", "松茸")], wiki_zh_gen="口蘑屬"),
                            ]),
                          N("膨瑚菌科", "Physalacriaceae", wiki_zh="膨瑚菌科",
                            children=[
                                genus_species("金钱菌属", "Flammulina", [("金针菇", "Flammulina filiformis", "金針菇")], wiki_zh_gen="金針菇屬"),
                            ]),
                      ]),
                    N("多孔菌目", "Polyporales", wiki_zh="多孔菌目",
                      children=[
                          N("灵芝科", "Ganodermataceae",
                            children=[
                                N("灵芝属", "Ganoderma", wiki_zh="靈芝屬",
                                  children=[N("赤芝", "Ganoderma lucidum", wiki_zh="靈芝")]),
                            ])
                      ]),
                    N("木耳目", "Auriculariales", wiki_zh="木耳目",
                      children=[
                          N("木耳科", "Auriculariaceae",
                            children=[
                                N("木耳属", "Auricularia", wiki_zh="木耳屬",
                                  children=[N("黑木耳", "Auricularia auricula-judae", wiki_zh="木耳")]),
                            ])
                      ]),
                    N("红菇目", "Russulales", note="松乳菇、红菇"),
                    N("牛肝菌目", "Boletales", note="牛肝菌",
                      children=[
                          N("牛肝菌科", "Boletaceae", wiki_zh="牛肝菌科",
                            children=[
                                genus_species("牛肝菌属", "Boletus", [("美味牛肝菌", "Boletus edulis", "美味牛肝菌")], wiki_zh_gen="牛肝菌屬"),
                            ]),
                      ]),
              ]),
          ]),
        N("子囊菌门", "Ascomycota", wiki_zh="子囊菌門", note="酵母、青霉、冬虫夏草、羊肚菌",
          dist="产子囊孢子(囊内通常8个)；形态最多样；酵母/霉菌多在此",
          children=[
              N("酵母菌纲", "Saccharomycetes", wiki_zh="酵母菌綱",
                children=[
                    N("酵母目", "Saccharomycetales",
                      children=[
                          N("酵母科", "Saccharomycetaceae",
                            children=[
                                N("酵母属", "Saccharomyces", wiki_zh="酵母屬",
                                  children=[N("酿酒酵母", "Saccharomyces cerevisiae", wiki_zh="釀酒酵母")])
                            ])
                      ])
                ]),
              N("散囊菌纲", "Eurotiomycetes", wiki_zh="散囊菌綱",
                children=[
                    N("散囊菌目", "Eurotiales",
                      children=[
                          N("发菌科", "Trichocomaceae",
                            children=[
                                N("青霉属", "Penicillium", wiki_zh="青黴屬",
                                  children=[N("产黄青霉", "Penicillium chrysogenum", wiki_zh="產黃青黴")]),
                                N("曲霉属", "Aspergillus", wiki_zh="曲黴屬",
                                  children=[N("黄曲霉", "Aspergillus flavus", wiki_zh="黃曲黴")]),
                            ])
                      ])
                ]),
              N("盘菌纲", "Pezizomycetes", wiki_zh="盤菌綱", note="羊肚菌",
                children=[
                    N("盘菌目", "Pezizales", wiki_zh="盤菌目", dist="子实体盘/杯/皱褶状",
                      children=[
                          N("羊肚菌科", "Morchellaceae", wiki_zh="羊肚菌科",
                            children=[
                                genus_species("羊肚菌属", "Morchella", [("羊肚菌", "Morchella esculenta", "羊肚菌")], wiki_zh_gen="羊肚菌屬"),
                            ]),
                          N("块菌科", "Tuberaceae", wiki_zh="塊菌科", dist="地下生长；与树根共生；松露即此",
                            children=[
                                genus_species("块菌属", "Tuber", [("佩里戈尔黑松露", "Tuber melanosporum", "黑孢塊菌")], wiki_zh_gen="塊菌屬"),
                            ]),
                      ]),
                ]),
              N("粪壳菌纲", "Sordariomycetes", note="冬虫夏草归属",
                children=[
                    N("肉座菌目", "Hypocreales", wiki_zh="肉座菌目", dist="含麦角菌、木霉、虫草",
                      children=[
                          N("线虫草科", "Ophiocordycipitaceae", wiki_zh="線蟲草科",
                            children=[
                                genus_species("线虫草属", "Ophiocordyceps", [("冬虫夏草", "Ophiocordyceps sinensis", "冬蟲夏草")], wiki_zh_gen="線蟲草屬"),
                            ]),
                      ]),
                ]),
          ]),
        N("接合菌门", "Zygomycota", wiki_zh="接合菌門", note="根霉；并系"),
        N("球囊菌门", "Glomeromycota", wiki_zh="球囊菌門", note="与植物根共生(菌根)"),
        N("壶菌门", "Chytridiomycota", wiki_zh="壺菌門", note="水生真菌"),
        N("微孢子虫门", "Microsporidia", wiki_zh="微孢子蟲門"),
        N("地衣门", "Lichenes", wiki_zh="地衣", note="真菌+藻共生体；非真分类群"),
    ]
)

# ============================================================
# 植物界 Plantae
# ============================================================
kingdom_plantae = N(
    "植物界", "Plantae", wiki_zh="植物",
    note="多细胞真核自养；具叶绿体",
    dist="真核、自养（光合），细胞壁含纤维素；有叶绿体",
    children=[
        N("苔藓植物门", "Bryophyta", wiki_zh="苔蘚植物",
          dist="无维管束；无真正根茎叶；靠水受精；配子体发达",
          children=[
              N("藓纲", "Bryopsida", wiki_zh="真蘚綱",
                dist="有茎叶分化；叶螺旋排列；孢蒴具蒴盖与蒴齿；如葫芦藓"),
              N("苔纲", "Marchantiopsida", wiki_zh="苔綱",
                dist="叶状体或具两列叶；假根单细胞；无蒴盖蒴齿；如地钱"),
              N("角苔纲", "Anthocerotopsida", wiki_zh="角苔綱",
                dist="孢子体呈细长角状；质地革质；少见类群"),
          ]),
        N("蕨类植物门", "Pteridophyta", wiki_zh="蕨類植物門",
          note="孢子繁殖，有维管束",
          dist="有维管束；无种子(孢子繁殖)；孢子体发达",
          children=[
              N("真蕨纲", "Polypodiopsida", wiki_zh="水龍骨綱",
                dist="叶大型(大叶型)，幼时拳卷；多数常见蕨类；孢子囊群在叶背",
                children=[
                    N("水龙骨目", "Polypodiales", wiki_zh="水龍骨目", dist="真蕨最大目；现代蕨类主体",
                      children=[
                          N("鳞毛蕨科", "Dryopteridaceae", wiki_zh="鱗毛蕨科",
                            dist="叶柄密被鳞片；孢子囊群圆形带膜盖；常见林下蕨"),
                          N("水龙骨科", "Polypodiaceae", wiki_zh="水龍骨科",
                            dist="多附生；叶革质；孢子囊群圆形无盖"),
                      ]),
                    N("紫萁目", "Osmundales", wiki_zh="紫萁目", dist="原始真蕨；孢子囊大肉质；如紫萁"),
                ]),
              N("松叶蕨纲", "Psilotopsida",
                dist="无真正的叶和根，二叉分枝；原始形态"),
              N("木贼纲", "Equisetopsida", wiki_zh="木賊綱",
                dist="茎中空具节，小型叶轮生呈鞘状；如问荆",
                children=[
                    N("木贼目", "Equisetales", wiki_zh="木賊目", dist="茎具纵棱、节、鞘",
                      children=[
                          N("木贼科", "Equisetaceae", wiki_zh="木賊科",
                            children=[
                                N("木贼属", "Equisetum", wiki_zh="木賊屬",
                                  children=[N("问荆", "Equisetum arvense", wiki_zh="問荊")])
                            ])
                      ])
                ]),
              N("石松纲", "Lycopodiopsida", wiki_zh="石松綱",
                dist="小型叶螺旋排列；茎匍匐分叉；孢子囊穗顶生",
                children=[
                    N("石松目", "Lycopodiales", wiki_zh="石松目", dist="茎常匍匐分枝；小型叶鳞状"),
                    N("卷柏目", "Selaginellales", wiki_zh="卷柏目", dist="叶两种大小；多旱生能复苏；如卷柏"),
                ]),
          ]),
        N("裸子植物门", "Pinophyta", wiki_zh="裸子植物",
          note="种子裸露",
          dist="有种子但无果皮包裹(裸露于球果)；多为针叶常绿",
          children=[
              N("松杉纲", "Pinopsida", wiki_zh="松柏綱",
                dist="针叶或鳞叶；球果；常绿为主；裸子植物中种类最多",
                children=[
                    N("松柏目", "Pinales", wiki_zh="松柏目",
                      dist="叶针形或鳞形；雌雄球花；含树脂道",
                      children=[
                          N("松科", "Pinaceae", wiki_zh="松科",
                            dist="针叶2~5针一束或单针；大型球果木质鳞片；含树脂",
                            children=[
                                N("松属", "Pinus", wiki_zh="松屬",
                                  dist="针叶2/3/5一束(看束数辨种)；鳞叶基部有叶鞘",
                                  children=[
                                    N("油松", "Pinus tabuliformis", wiki_zh="油松",
                                      dist="2针一束；华北常见；树皮裂片灰红褐色"),
                                    N("马尾松", "Pinus massoniana", wiki_zh="馬尾松",
                                      dist="2针一束但细长柔软(马尾状)；华南常见"),
                                    N("华山松", "Pinus armandii", wiki_zh="華山松"),
                                    N("白皮松", "Pinus bungeana", wiki_zh="白皮松"),
                                    N("红松", "Pinus koraiensis", wiki_zh="紅松"),
                                  ]),
                                genus_species("云杉属", "Picea", [
                                    ("白扦", "Picea meyeri", None),
                                    ("云杉", "Picea asperata", "雲杉"),
                                ], wiki_zh_gen="雲杉屬"),
                                genus_species("冷杉属", "Abies", [("冷杉", "Abies fabri", "冷杉")], wiki_zh_gen="冷杉屬"),
                                genus_species("落叶松属", "Larix", [("落叶松", "Larix gmelinii", "落葉松")], wiki_zh_gen="落葉松屬"),
                                genus_species("雪松属", "Cedrus", [("雪松", "Cedrus deodara", "雪松")], wiki_zh_gen="雪松屬"),
                                genus_species("铁杉属", "Tsuga", [("铁杉", "Tsuga chinensis", "鐵杉")], wiki_zh_gen="鐵杉屬"),
                            ]),
                          N("柏科", "Cupressaceae", wiki_zh="柏科",
                            dist="叶多为鳞片状(或针状)贴生；球果较小、果鳞木质或肉质(桧柏)；无树脂道",
                            children=[
                                genus_species("柏木属", "Cupressus", [("柏木", "Cupressus funebris", "柏木")], wiki_zh_gen="柏木屬"),
                                genus_species("刺柏属", "Juniperus", [
                                    ("圆柏", "Juniperus chinensis", "圓柏"),
                                    ("侧柏", "Platycladus orientalis", "側柏"),
                                ], wiki_zh_gen="刺柏屬"),
                                genus_species("水杉属", "Metasequoia", [("水杉", "Metasequoia glyptostroboides", "水杉")], wiki_zh_gen="水杉屬"),
                                genus_species("柳杉属", "Cryptomeria", [("日本柳杉", "Cryptomeria japonica", "日本柳杉")], wiki_zh_gen="柳杉屬"),
                            ]),
                      ])
                ]),
              N("苏铁纲", "Cycadopsida", wiki_zh="蘇鐵綱",
                dist="形似棕榈但羽状叶硬革质；顶生大型孢子叶球；生长极慢",
                children=[
                    N("苏铁目", "Cycadales", wiki_zh="蘇鐵目", dist="茎干粗短不分枝；雌雄异株",
                      children=[
                          N("苏铁科", "Cycadaceae", wiki_zh="蘇鐵科",
                            children=[
                                N("苏铁属", "Cycas", wiki_zh="蘇鐵屬",
                                  children=[N("苏铁", "Cycas revoluta", wiki_zh="蘇鐵")])
                            ])
                      ])
                ]),
              N("银杏纲", "Ginkgoopsida", wiki_zh="銀杏綱",
                dist="叶扇形二裂；仅存1目1科1属1种；活化石",
                children=[
                    N("银杏目", "Ginkgoales",
                      children=[
                          N("银杏科", "Ginkgoaceae",
                            children=[
                                genus_species("银杏属", "Ginkgo", [
                                    ("银杏", "Ginkgo biloba", "銀杏"),
                                ], wiki_zh_gen="銀杏屬")
                            ])
                      ])
                ]),
              N("买麻藤纲", "Gnetopsida", wiki_zh="買麻藤綱",
                dist="介于裸/被子植物之间；叶常似被子植物；含麻黄、百岁兰",
                children=[
                    N("麻黄目", "Ephedrales", wiki_zh="麻黃目", dist="小灌木；鳞叶小对生；药用(含麻黄碱)",
                      children=[
                          N("麻黄科", "Ephedraceae", wiki_zh="麻黃科",
                            children=[
                                N("麻黄属", "Ephedra", wiki_zh="麻黃屬",
                                  children=[N("草麻黄", "Ephedra sinica", wiki_zh="草麻黃")])
                            ])
                      ])
                ]),
          ]),
        N("被子植物门", "Magnoliophyta", wiki_zh="被子植物",
          note="花果实最发达；最丰富的植物类群",
          dist="有真花；种子包被于果实内；植物界种类最多",
          children=[
              N("单子叶植物纲", "Liliopsida", wiki_zh="單子葉植物",
                dist="子叶1片；叶脉平行；花部3基数；多须根；茎维管束散生",
                children=[
                    N("禾本目", "Poales", wiki_zh="禾本目",
                      dist="草本；风媒花退化不显；含禾本科与莎草科等",
                      children=[
                          N("禾本科", "Poaceae", wiki_zh="禾本科",
                            note="稻、麦、玉米等主粮",
                            dist="茎圆、节明显、中空(竹除外)；叶片线形、叶鞘抱茎；颖花无显著花被",
                            children=[
                                genus_species("稻属", "Oryza", [("稻", "Oryza sativa", "稻")], wiki_zh_gen="稻屬"),
                                genus_species("小麦属", "Triticum", [
                                    ("普通小麦", "Triticum aestivum", "小麥"),
                                ], wiki_zh_gen="小麥屬"),
                                genus_species("玉蜀黍属", "Zea", [("玉米", "Zea mays", "玉蜀黍")], wiki_zh_gen="玉蜀黍屬"),
                                genus_species("竹属", "Bambusa", [("青皮竹", "Bambusa textilis", None)], wiki_zh_gen="簕竹屬"),
                                genus_species("高粱属", "Sorghum", [("高粱", "Sorghum bicolor", "高粱")], wiki_zh_gen="高粱屬"),
                                genus_species("狗尾草属", "Setaria", [("粟", "Setaria italica", "粟")], wiki_zh_gen="狗尾草屬"),
                                genus_species("大麦属", "Hordeum", [("大麦", "Hordeum vulgare", "大麥")], wiki_zh_gen="大麥屬"),
                                genus_species("燕麦属", "Avena", [("燕麦", "Avena sativa", "燕麥")], wiki_zh_gen="燕麥屬"),
                                genus_species("甘蔗属", "Saccharum", [("甘蔗", "Saccharum officinarum", "甘蔗")], wiki_zh_gen="甘蔗屬"),
                            ]),
                      ]),
                    N("百合目", "Liliales",
                      dist="多具鳞茎或根状茎；花被片6常鲜艳；百合、郁金香归此",
                      children=[
                          N("百合科", "Liliaceae", wiki_zh="百合科",
                            dist="鳞茎；花被片6(外3内3类似)；雄蕊6；常大花",
                            children=[
                                N("百合属", "Lilium", wiki_zh="百合屬",
                                  dist="鳞茎大；叶互生或轮生；花喇叭或反卷，带斑点(常)",
                                  children=[
                                    N("卷丹", "Lilium lancifolium", wiki_zh="卷丹",
                                      dist="花橙红有紫黑斑点，强烈反卷；叶腋有珠芽"),
                                  ]),
                                N("郁金香属", "Tulipa", wiki_zh="鬱金香屬",
                                  dist="鳞茎大；每茎单花杯状；花被无斑或底部有斑",
                                  children=[
                                    N("郁金香", "Tulipa gesneriana", wiki_zh="鬱金香",
                                      dist="花单生直立杯状，颜色丰富；叶2~3枚基生"),
                                  ]),
                                genus_species("萱草属", "Hemerocallis", [
                                    ("黄花菜", "Hemerocallis citrina", "黃花菜"),
                                    ("萱草", "Hemerocallis fulva", "萱草"),
                                ], wiki_zh_gen="萱草屬"),
                                genus_species("贝母属", "Fritillaria", [("川贝母", "Fritillaria cirrhosa", "川貝母")], wiki_zh_gen="貝母屬"),
                            ])
                      ]),
                    N("天门冬目", "Asparagales", wiki_zh="天門冬目",
                      note="洋葱、韭、兰花",
                      dist="多具鳞茎、根状茎或肉质根；很多种类有硫化物气味；兰科归此",
                      children=[
                          N("兰科", "Orchidaceae", wiki_zh="蘭科",
                            dist="花两侧对称、有唇瓣；雄蕊/雌蕊合生为合蕊柱；种子极细；种类极多",
                            children=[
                                genus_species("兰属", "Cymbidium", [
                                    ("春兰", "Cymbidium goeringii", "春蘭"),
                                    ("蕙兰", "Cymbidium faberi", "蕙蘭"),
                                ], wiki_zh_gen="蘭屬"),
                                genus_species("蝴蝶兰属", "Phalaenopsis", [("蝴蝶兰", "Phalaenopsis aphrodite", "蝴蝶蘭")], wiki_zh_gen="蝴蝶蘭屬"),
                                genus_species("石斛属", "Dendrobium", [("石斛", "Dendrobium nobile", "石斛")], wiki_zh_gen="石斛屬"),
                            ]),
                          N("石蒜科", "Amaryllidaceae", wiki_zh="石蒜科",
                            dist="鳞茎；花序顶生伞形；葱属特有硫化物气味",
                            children=[
                                genus_species("葱属", "Allium", [
                                    ("洋葱", "Allium cepa", "洋蔥"),
                                    ("大蒜", "Allium sativum", "大蒜"),
                                    ("韭", "Allium tuberosum", "韭"),
                                    ("葱", "Allium fistulosum", "蔥"),
                                ], wiki_zh_gen="蔥屬"),
                                genus_species("石蒜属", "Lycoris", [
                                    ("石蒜", "Lycoris radiata", "石蒜"),
                                ], wiki_zh_gen="石蒜屬"),
                                genus_species("水仙属", "Narcissus", [
                                    ("水仙", "Narcissus tazetta", "水仙"),
                                ], wiki_zh_gen="水仙屬"),
                            ]),
                          N("鸢尾科", "Iridaceae", wiki_zh="鳶尾科",
                            dist="多年生草本有根茎/球茎；叶剑形基生；花被片6基数3",
                            children=[
                                genus_species("鸢尾属", "Iris", [("鸢尾", "Iris tectorum", "鳶尾")], wiki_zh_gen="鳶尾屬"),
                                genus_species("唐菖蒲属", "Gladiolus", [("唐菖蒲", "Gladiolus × gandavensis", "唐菖蒲")], wiki_zh_gen="唐菖蒲屬"),
                            ]),
                      ]),
                    N("棕榈目", "Arecales",
                      dist="热带/亚热带大型单子叶木本；茎不分枝；顶生大叶羽状或掌状",
                      children=[
                          N("棕榈科", "Arecaceae", wiki_zh="棕櫚科",
                            dist="树干无次生生长；顶冠叶；花小三基数，果浆果/核果",
                            children=[
                                genus_species("椰子属", "Cocos", [("椰子", "Cocos nucifera", "椰子")], wiki_zh_gen="椰子屬")
                            ])
                      ]),
                    N("薯蓣目", "Dioscoreales", wiki_zh="薯蕷目", note="山药、薯蓣",
                      dist="多藤本草质；块茎储淀粉；叶心形互生",
                      children=[
                          N("薯蓣科", "Dioscoreaceae", wiki_zh="薯蕷科",
                            children=[
                                N("薯蓣属", "Dioscorea", wiki_zh="薯蕷屬",
                                  children=[N("山药", "Dioscorea polystachya", wiki_zh="山藥")])
                            ])
                      ]),
                    N("鸭跖草目", "Commelinales", wiki_zh="鴨跖草目", note="鸭跖草、雨久花",
                      dist="多草本；花部3基数色艳；含鸭跖草科、雨久花科"),
                    N("泽泻目", "Alismatales", wiki_zh="澤瀉目", note="水生(泽泻、慈菇)",
                      dist="多水生/湿生；叶柄长；花3基数"),
                    N("姜目", "Zingiberales", note="香蕉、姜、芭蕉",
                      dist="草本或假茎(由叶鞘组成)；叶大具鞘；花两侧对称常艳丽",
                      children=[
                          N("芭蕉科", "Musaceae", wiki_zh="芭蕉科",
                            dist="假茎由叶鞘构成；叶片巨大易撕裂；花序下垂苞片肉质鲜艳",
                            children=[
                                genus_species("芭蕉属", "Musa", [("香蕉", "Musa × paradisiaca", "香蕉")], wiki_zh_gen="芭蕉屬")
                            ]),
                          N("姜科", "Zingiberaceae", wiki_zh="薑科",
                            dist="根状茎含挥发油(姜辣素)；叶二列；花唇瓣醒目",
                            children=[
                                genus_species("姜属", "Zingiber", [("姜", "Zingiber officinale", "薑")], wiki_zh_gen="薑屬"),
                                genus_species("姜黄属", "Curcuma", [("姜黄", "Curcuma longa", "薑黃")], wiki_zh_gen="薑黃屬"),
                                genus_species("砂仁属", "Amomum", [("砂仁", "Amomum villosum", "砂仁")], wiki_zh_gen="豆蔻屬"),
                            ]),
                      ]),
                ]),
              N("双子叶植物纲", "Magnoliopsida", wiki_zh="雙子葉植物綱",
                dist="子叶2片；网状叶脉；花部4/5基数；主根直根系；茎维管束环状",
                children=[
                    N("蔷薇目", "Rosales", wiki_zh="薔薇目",
                      dist="花常5基数；含蔷薇科(蔷薇、李、苹果)与桑科等",
                      children=[
                          N("蔷薇科", "Rosaceae", wiki_zh="薔薇科",
                            dist="叶多互生有托叶；花托发达；常见果类型：核果(桃李)、梨果(苹果梨)、聚合瘦果(草莓)",
                            children=[
                                N("苹果属", "Malus", wiki_zh="蘋果屬",
                                  dist="叶缘有锯齿；花先叶或与叶同开；果为梨果，花萼宿存形成凹心",
                                  children=[N("苹果", "Malus domestica", wiki_zh="蘋果")]),
                                N("李属", "Prunus", wiki_zh="李屬",
                                  dist="核果属；'桃樱梅李杏'五兄弟；区分看花期/果/叶/树皮",
                                  children=[
                                    N("桃", "Prunus persica", wiki_zh="桃",
                                      dist="花3-4月，单朵粉红色无梗或极短；果表面有绒毛；叶披针形"),
                                    N("樱花", "Prunus serrulata", wiki_zh="櫻花",
                                      dist="花3-4月成簇下垂有长梗；花瓣顶端有缺刻；果小不可食"),
                                    N("杏", "Prunus armeniaca", wiki_zh="杏",
                                      dist="花最早2-3月，单朵贴枝无梗粉白带红；叶宽卵圆形"),
                                    N("梅", "Prunus mume", wiki_zh="梅",
                                      dist="花冬末早春1-2月，单朵芳香无梗；树皮灰褐；果表有绒毛味酸"),
                                    N("李", "Prunus salicina", wiki_zh="李",
                                      dist="花3-4月成簇白色；果光滑无绒毛，紫红或黄；叶倒卵形"),
                                    N("甜樱桃", "Prunus avium", wiki_zh="歐洲甜櫻桃"),
                                    N("扁桃", "Prunus dulcis", wiki_zh="扁桃"),
                                  ]),
                                N("梨属", "Pyrus", wiki_zh="梨屬",
                                  dist="叶互生多卵圆；花白色5瓣；果为梨果，果皮常有石细胞(沙粒感)",
                                  children=[
                                      N("梨", "Pyrus pyrifolia", wiki_zh="梨"),
                                      N("西洋梨", "Pyrus communis", wiki_zh="西洋梨"),
                                  ]),
                                genus_species("山楂属", "Crataegus", [("山楂", "Crataegus pinnatifida", "山楂")], wiki_zh_gen="山楂屬"),
                                genus_species("枇杷属", "Eriobotrya", [("枇杷", "Eriobotrya japonica", "枇杷")], wiki_zh_gen="枇杷屬"),
                                N("蔷薇属", "Rosa", wiki_zh="薔薇屬",
                                  dist="茎有皮刺；羽状复叶有托叶；花5基数(单/重瓣)；果为蔷薇果",
                                  children=[
                                    N("月季", "Rosa chinensis", wiki_zh="月季花",
                                      dist="四季开花；小叶3-5片亮绿无皱；花较大常重瓣；刺较少"),
                                    N("玫瑰", "Rosa rugosa", wiki_zh="玫瑰",
                                      dist="花期春夏各一次；小叶5-9片革质多皱；茎密生刺毛；花紫红香浓"),
                                  ]),
                                N("草莓属", "Fragaria", wiki_zh="草莓屬",
                                  dist="多年生草本，匍匐茎；叶三出复叶；花托膨大为肉质'果'",
                                  children=[N("草莓", "Fragaria × ananassa", wiki_zh="草莓")]),
                            ]),
                          N("桑科", "Moraceae", wiki_zh="桑科",
                            dist="多含乳汁；叶互生；花极小无花被或单被；聚花果",
                            children=[
                                genus_species("桑属", "Morus", [("桑", "Morus alba", "桑")], wiki_zh_gen="桑屬")
                            ]),
                      ]),
                    N("豆目", "Fabales", wiki_zh="豆目",
                      dist="豆科为主；多数为草/木本，具荚果；花5基数多呈蝶形",
                      children=[
                          N("豆科", "Fabaceae", wiki_zh="豆科",
                            dist="果为豆荚；复叶(常羽状或三出)；花多蝶形(旗/翼/龙骨瓣)；根瘤固氮",
                            children=[
                                genus_species("大豆属", "Glycine", [("大豆", "Glycine max", "大豆")], wiki_zh_gen="大豆屬"),
                                genus_species("豌豆属", "Pisum", [("豌豆", "Pisum sativum", "豌豆")], wiki_zh_gen="豌豆屬"),
                                genus_species("花生属", "Arachis", [("花生", "Arachis hypogaea", "花生")], wiki_zh_gen="花生屬"),
                                genus_species("菜豆属", "Phaseolus", [
                                    ("菜豆", "Phaseolus vulgaris", "菜豆"),
                                    ("绿豆", "Vigna radiata", None),
                                ], wiki_zh_gen="菜豆屬"),
                                genus_species("蚕豆属", "Vicia", [("蚕豆", "Vicia faba", "蠶豆")], wiki_zh_gen="野豌豆屬"),
                                genus_species("扁豆属", "Lablab", [("扁豆", "Lablab purpureus", "扁豆")], wiki_zh_gen="扁豆屬"),
                                genus_species("紫荆属", "Cercis", [("紫荆", "Cercis chinensis", "紫荊")], wiki_zh_gen="紫荊屬"),
                                genus_species("槐属", "Styphnolobium", [("国槐", "Styphnolobium japonicum", "槐")], wiki_zh_gen="槐屬"),
                                genus_species("刺槐属", "Robinia", [("刺槐", "Robinia pseudoacacia", "刺槐")], wiki_zh_gen="刺槐屬"),
                                genus_species("含羞草属", "Mimosa", [("含羞草", "Mimosa pudica", "含羞草")], wiki_zh_gen="含羞草屬"),
                                genus_species("合欢属", "Albizia", [("合欢", "Albizia julibrissin", "合歡")], wiki_zh_gen="合歡屬"),
                            ])
                      ]),
                    N("十字花目", "Brassicales", wiki_zh="十字花目",
                      dist="多含芥子油(辛辣)；花常4瓣十字形；长角果或短角果",
                      children=[
                          N("十字花科", "Brassicaceae", wiki_zh="十字花科",
                            dist="花瓣4呈十字；雄蕊6(4长2短)；果为长/短角果",
                            children=[
                                genus_species("芸薹属", "Brassica", [
                                    ("白菜", "Brassica rapa", "蕪菁"),
                                    ("甘蓝", "Brassica oleracea", "野甘藍"),
                                    ("芥菜", "Brassica juncea", "芥菜"),
                                    ("油菜", "Brassica napus", "油菜"),
                                ], wiki_zh_gen="蕓薹屬"),
                                genus_species("萝卜属", "Raphanus", [("萝卜", "Raphanus sativus", "蘿蔔")], wiki_zh_gen="蘿蔔屬"),
                            ])
                      ]),
                    N("葫芦目", "Cucurbitales",
                      dist="多藤本攀缘，具卷须；单性花；果常为瓠果",
                      children=[
                          N("葫芦科", "Cucurbitaceae", wiki_zh="葫蘆科",
                            dist="茎匍匐/攀缘；掌状叶；单性花黄色；瓠果",
                            children=[
                                genus_species("西瓜属", "Citrullus", [("西瓜", "Citrullus lanatus", "西瓜")], wiki_zh_gen="西瓜屬"),
                                genus_species("黄瓜属", "Cucumis", [
                                    ("黄瓜", "Cucumis sativus", "黃瓜"),
                                    ("甜瓜", "Cucumis melo", "甜瓜"),
                                ], wiki_zh_gen="黃瓜屬"),
                                genus_species("南瓜属", "Cucurbita", [
                                    ("南瓜", "Cucurbita moschata", "南瓜"),
                                    ("笋瓜", "Cucurbita maxima", "筍瓜"),
                                ], wiki_zh_gen="南瓜屬"),
                                genus_species("冬瓜属", "Benincasa", [("冬瓜", "Benincasa hispida", "冬瓜")], wiki_zh_gen="冬瓜屬"),
                                genus_species("苦瓜属", "Momordica", [("苦瓜", "Momordica charantia", "苦瓜")], wiki_zh_gen="苦瓜屬"),
                                genus_species("丝瓜属", "Luffa", [("丝瓜", "Luffa aegyptiaca", "絲瓜")], wiki_zh_gen="絲瓜屬"),
                            ])
                      ]),
                    N("茄目", "Solanales", wiki_zh="茄目",
                      dist="多含生物碱(可药可毒)；花冠常合瓣钟状或轮状；浆果/蒴果",
                      children=[
                          N("茄科", "Solanaceae", wiki_zh="茄科",
                            dist="花合瓣5裂；雄蕊5贴生花冠；浆果(番茄/茄)或蒴果(烟草)",
                            children=[
                                genus_species("茄属", "Solanum", [
                                    ("番茄", "Solanum lycopersicum", "番茄"),
                                    ("马铃薯", "Solanum tuberosum", "馬鈴薯"),
                                    ("茄", "Solanum melongena", "茄"),
                                ], wiki_zh_gen="茄屬"),
                                genus_species("辣椒属", "Capsicum", [("辣椒", "Capsicum annuum", "辣椒")], wiki_zh_gen="辣椒屬"),
                                genus_species("烟草属", "Nicotiana", [("烟草", "Nicotiana tabacum", "菸草")], wiki_zh_gen="菸草屬"),
                                genus_species("枸杞属", "Lycium", [("宁夏枸杞", "Lycium barbarum", "寧夏枸杞")], wiki_zh_gen="枸杞屬"),
                            ])
                      ]),
                    N("菊目", "Asterales",
                      dist="以菊科为主；花小聚成头状花序；多为'一朵花其实是几百朵'",
                      children=[
                          N("菊科", "Asteraceae", wiki_zh="菊科", note="种类最多的科之一",
                            dist="头状花序(看似一朵其实多朵)；下具总苞；瘦果带冠毛；全科种类极多",
                            children=[
                                N("向日葵属", "Helianthus", wiki_zh="向日葵屬",
                                  dist="头状花序大型，中心盘花、外轮舌状花；茎直立高大",
                                  children=[N("向日葵", "Helianthus annuus", wiki_zh="向日葵")]),
                                N("菊属", "Chrysanthemum", wiki_zh="菊屬",
                                  dist="叶羽状深裂；头状花序中等大小；品种繁多，秋季开花",
                                  children=[N("菊花", "Chrysanthemum morifolium", wiki_zh="菊花")]),
                                N("雏菊属", "Bellis", wiki_zh="雛菊屬",
                                  dist="小型多年生草本；头状花序单生于花葶；舌状花白/粉",
                                  children=[N("雏菊", "Bellis perennis", wiki_zh="雛菊")]),
                                genus_species("莴苣属", "Lactuca", [
                                    ("莴苣", "Lactuca sativa", "萵苣"),
                                ], wiki_zh_gen="萵苣屬"),
                                genus_species("蒿属", "Artemisia", [
                                    ("黄花蒿", "Artemisia annua", "黃花蒿"),
                                    ("艾", "Artemisia argyi", "艾"),
                                ], wiki_zh_gen="蒿屬"),
                                genus_species("蒲公英属", "Taraxacum", [("蒲公英", "Taraxacum mongolicum", "蒲公英")], wiki_zh_gen="蒲公英屬"),
                                genus_species("大丽花属", "Dahlia", [("大丽花", "Dahlia pinnata", "大麗花")], wiki_zh_gen="大麗花屬"),
                                genus_species("非洲菊属", "Gerbera", [("非洲菊", "Gerbera jamesonii", "非洲菊")], wiki_zh_gen="非洲菊屬"),
                            ])
                      ]),
                    N("无患子目", "Sapindales",
                      dist="多木本；叶多为复叶(羽状);花4-5基数；芸香科含挥发油",
                      children=[
                          N("芸香科", "Rutaceae", wiki_zh="芸香科",
                            dist="叶具透明油点(揉有香味)；柑橘属果为柑果",
                            children=[
                                genus_species("柑橘属", "Citrus", [
                                    ("橘", "Citrus reticulata", "橘"),
                                    ("柠檬", "Citrus × limon", "檸檬"),
                                    ("甜橙", "Citrus × sinensis", "甜橙"),
                                    ("柚", "Citrus maxima", "柚"),
                                    ("金柑", "Citrus japonica", "金柑"),
                                ], wiki_zh_gen="柑橘屬")
                            ]),
                          N("无患子科", "Sapindaceae", wiki_zh="無患子科",
                            dist="叶多互生羽状复叶；花小；核果或蒴果；含荔枝、龙眼、枫",
                            children=[
                                genus_species("荔枝属", "Litchi", [("荔枝", "Litchi chinensis", "荔枝")], wiki_zh_gen="荔枝屬"),
                                genus_species("龙眼属", "Dimocarpus", [("龙眼", "Dimocarpus longan", "龍眼")], wiki_zh_gen="龍眼屬"),
                                genus_species("槭属", "Acer", [
                                    ("鸡爪槭", "Acer palmatum", "雞爪槭"),
                                    ("糖槭", "Acer saccharum", "糖槭"),
                                ], wiki_zh_gen="槭屬"),
                            ]),
                          N("漆树科", "Anacardiaceae", wiki_zh="漆樹科",
                            dist="多含挥发油或漆酚；核果；含芒果、腰果、漆树",
                            children=[
                                genus_species("芒果属", "Mangifera", [("芒果", "Mangifera indica", "芒果")], wiki_zh_gen="芒果屬"),
                                genus_species("腰果属", "Anacardium", [("腰果", "Anacardium occidentale", "腰果")], wiki_zh_gen="腰果屬"),
                            ]),
                          N("楝科", "Meliaceae", wiki_zh="楝科",
                            dist="多热带乔木；一回或多回羽状复叶；含楝树、香椿",
                            children=[
                                genus_species("香椿属", "Toona", [("香椿", "Toona sinensis", "香椿")], wiki_zh_gen="香椿屬"),
                            ]),
                      ]),
                    N("壳斗目", "Fagales",
                      dist="多风媒木本；花单性；雄花常柔荑花序；果坚果(橡子、栗)",
                      children=[
                          N("壳斗科", "Fagaceae", wiki_zh="殼斗科", note="橡树、栗",
                            dist="坚果被鳞状或刺状壳斗包裹(橡椀、栗苞)；叶互生常锯齿",
                            children=[
                                genus_species("栎属", "Quercus", [
                                    ("麻栎", "Quercus acutissima", "麻櫟"),
                                    ("栓皮栎", "Quercus variabilis", "栓皮櫟"),
                                ], wiki_zh_gen="櫟屬"),
                                genus_species("栗属", "Castanea", [("板栗", "Castanea mollissima", "板栗")], wiki_zh_gen="栗屬"),
                            ]),
                          N("桦木科", "Betulaceae", wiki_zh="樺木科",
                            dist="单叶互生锯齿；雄花柔荑下垂；树皮常横向剥裂(桦皮)",
                            children=[
                                genus_species("桦木属", "Betula", [("白桦", "Betula platyphylla", "白樺")], wiki_zh_gen="樺木屬"),
                                genus_species("榛属", "Corylus", [("榛", "Corylus heterophylla", "榛")], wiki_zh_gen="榛屬"),
                            ]),
                      ]),
                    N("毛茛目", "Ranunculales",
                      dist="原始双子叶类；花部数目不固定；心皮多离生；常含生物碱",
                      children=[
                          N("毛茛科", "Ranunculaceae", wiki_zh="毛茛科", note="毛茛、铁线莲、乌头",
                            dist="花部常多数且螺旋排列；雄蕊多数；聚合瘦果/蓇葖果",
                            children=[
                                genus_species("毛茛属", "Ranunculus", [("毛茛", "Ranunculus japonicus", "毛茛")], wiki_zh_gen="毛茛屬"),
                                genus_species("铁线莲属", "Clematis", [("铁线莲", "Clematis florida", "鐵線蓮")], wiki_zh_gen="鐵線蓮屬"),
                                genus_species("乌头属", "Aconitum", [("乌头", "Aconitum carmichaelii", "烏頭")], wiki_zh_gen="烏頭屬"),
                                genus_species("飞燕草属", "Delphinium", [("飞燕草", "Delphinium grandiflorum", "飛燕草")], wiki_zh_gen="翠雀屬"),
                                genus_species("银莲花属", "Anemone", [("打破碗花花", "Anemone hupehensis", "打破碗花花")], wiki_zh_gen="銀蓮花屬"),
                            ]),
                          N("芍药科", "Paeoniaceae", wiki_zh="芍藥科", note="牡丹、芍药",
                            dist="花大单生；萼片5+花瓣5~13；多心皮有肉质花盘；果为蓇葖果",
                            children=[
                                N("芍药属", "Paeonia", wiki_zh="芍藥屬",
                                  dist="区分牡丹与芍药：牡丹木本(落叶灌木)、芍药草本(地上部分冬枯)",
                                  children=[
                                      N("牡丹", "Paeonia × suffruticosa", wiki_zh="牡丹",
                                        dist="落叶灌木有木质茎；4-5月开花；花期早于芍药；花朵大"),
                                      N("芍药", "Paeonia lactiflora", wiki_zh="芍藥",
                                        dist="多年生草本无木质茎；5-6月开花；花稍晚于牡丹；花形相似但略小"),
                                  ])
                            ])
                      ]),
                    N("木兰目", "Magnoliales", wiki_zh="木蘭目", note="木兰、含笑",
                      dist="原始被子植物；花部多且螺旋排列；木兰科为代表",
                      children=[
                          N("木兰科", "Magnoliaceae", wiki_zh="木蘭科",
                            dist="大型单生花；花被片多而相似；果常为聚合蓇葖",
                            children=[
                                N("木兰属", "Magnolia", wiki_zh="木蘭屬",
                                  children=[N("玉兰", "Magnolia denudata", wiki_zh="玉蘭")])
                            ])
                      ]),
                    N("樟目", "Laurales", wiki_zh="樟目", note="樟树、月桂",
                      dist="多常绿乔灌；叶常具透明油点(揉有香气)；花三基数",
                      children=[
                          N("樟科", "Lauraceae", wiki_zh="樟科", dist="叶革质常绿；含挥发油；樟、肉桂、月桂",
                            children=[
                                N("樟属", "Cinnamomum", wiki_zh="樟屬",
                                  children=[N("樟", "Cinnamomum camphora", wiki_zh="樟")])
                            ])
                      ]),
                    N("石竹目", "Caryophyllales", wiki_zh="石竹目", note="仙人掌、苋菜、菠菜",
                      dist="多草本；常具花青苷(非花青苷类)代谢产物；含仙人掌、石竹、苋等科",
                      children=[
                          N("石竹科", "Caryophyllaceae", wiki_zh="石竹科", dist="茎节膨大；叶对生；花5基数萼宿存；石竹、康乃馨",
                            children=[
                                genus_species("石竹属", "Dianthus", [
                                    ("石竹", "Dianthus chinensis", "石竹"),
                                    ("香石竹", "Dianthus caryophyllus", "香石竹"),
                                ], wiki_zh_gen="石竹屬"),
                            ]),
                          N("仙人掌科", "Cactaceae", wiki_zh="仙人掌科", dist="茎肉质贮水；叶退化为刺；耐旱；多数美洲原产"),
                          N("苋科", "Amaranthaceae", wiki_zh="莧科", dist="花小无瓣，常具干膜质苞片；含苋菜、菠菜",
                            children=[
                                genus_species("苋属", "Amaranthus", [("苋", "Amaranthus tricolor", "莧")], wiki_zh_gen="莧屬"),
                                genus_species("菠菜属", "Spinacia", [("菠菜", "Spinacia oleracea", "菠菜")], wiki_zh_gen="菠菜屬"),
                                genus_species("藜属", "Chenopodium", [("灰绿藜", "Chenopodium album", "藜")], wiki_zh_gen="藜屬"),
                                genus_species("甜菜属", "Beta", [("甜菜", "Beta vulgaris", "甜菜")], wiki_zh_gen="甜菜屬"),
                            ]),
                      ]),
                    N("山茶目", "Ericales", wiki_zh="杜鵑花目", note="杜鹃、茶、猕猴桃、山茶",
                      dist="花5基数常显眼；含山茶科(茶)、杜鹃花科、猕猴桃科、柿科等",
                      children=[
                          N("山茶科", "Theaceae", wiki_zh="山茶科", dist="常绿乔灌；花大单生；雄蕊多；茶、油茶、山茶",
                            children=[
                                N("山茶属", "Camellia", wiki_zh="山茶屬",
                                  children=[
                                      N("茶", "Camellia sinensis", wiki_zh="茶"),
                                      N("山茶", "Camellia japonica", wiki_zh="山茶"),
                                  ])
                            ]),
                          N("杜鹃花科", "Ericaceae", wiki_zh="杜鵑花科", dist="多酸性土植物；花钟状或坛状；含杜鹃、蓝莓、越橘",
                            children=[
                                genus_species("杜鹃花属", "Rhododendron", [
                                    ("映山红", "Rhododendron simsii", "映山紅"),
                                ], wiki_zh_gen="杜鵑花屬"),
                                genus_species("越橘属", "Vaccinium", [
                                    ("蓝莓", "Vaccinium corymbosum", "藍莓"),
                                ], wiki_zh_gen="越橘屬"),
                            ]),
                          N("猕猴桃科", "Actinidiaceae", wiki_zh="獼猴桃科", dist="多藤本；花5基数；浆果多毛(猕猴桃)"),
                      ]),
                    N("龙胆目", "Gentianales", wiki_zh="龍膽目", note="咖啡、栀子",
                      dist="叶多对生；合瓣花冠；含茜草科(咖啡/栀子)、龙胆科、夹竹桃科",
                      children=[
                          N("茜草科", "Rubiaceae", wiki_zh="茜草科", dist="叶对生间有托叶；花合瓣4-5裂；咖啡、栀子",
                            children=[
                                N("栀子属", "Gardenia", wiki_zh="梔子屬",
                                  children=[N("栀子", "Gardenia jasminoides", wiki_zh="梔子")]),
                                genus_species("咖啡属", "Coffea", [
                                    ("小粒咖啡", "Coffea arabica", "阿拉比卡咖啡"),
                                    ("中粒咖啡", "Coffea canephora", "羅布斯塔咖啡"),
                                ], wiki_zh_gen="咖啡屬"),
                                genus_species("金鸡纳属", "Cinchona", [("金鸡纳树", "Cinchona officinalis", "金雞納樹")], wiki_zh_gen="金雞納屬"),
                            ]),
                          N("夹竹桃科", "Apocynaceae", wiki_zh="夾竹桃科", dist="多含乳汁；花5裂常螺旋；多有毒",
                            children=[
                                genus_species("夹竹桃属", "Nerium", [("夹竹桃", "Nerium oleander", "夾竹桃")], wiki_zh_gen="夾竹桃屬"),
                                genus_species("鸡蛋花属", "Plumeria", [("红鸡蛋花", "Plumeria rubra", "紅雞蛋花")], wiki_zh_gen="雞蛋花屬"),
                                genus_species("长春花属", "Catharanthus", [("长春花", "Catharanthus roseus", "長春花")], wiki_zh_gen="長春花屬"),
                            ]),
                      ]),
                    N("伞形目", "Apiales", wiki_zh="傘形目", note="胡萝卜、芹菜、人参",
                      dist="复伞形花序；叶多鞘状或羽裂；双悬果；含芹菜、胡萝卜、人参",
                      children=[
                          N("伞形科", "Apiaceae", wiki_zh="傘形科", dist="茎中空有纵棱；复伞花序；多具挥发油香气",
                            children=[
                                N("胡萝卜属", "Daucus", wiki_zh="胡蘿蔔屬",
                                  children=[N("胡萝卜", "Daucus carota", wiki_zh="胡蘿蔔")]),
                                N("芹属", "Apium", wiki_zh="芹屬",
                                  children=[N("芹菜", "Apium graveolens", wiki_zh="芹菜")]),
                                genus_species("芫荽属", "Coriandrum", [("芫荽", "Coriandrum sativum", "芫荽")], wiki_zh_gen="芫荽屬"),
                                genus_species("茴香属", "Foeniculum", [("茴香", "Foeniculum vulgare", "茴香")], wiki_zh_gen="茴香屬"),
                                genus_species("当归属", "Angelica", [("当归", "Angelica sinensis", "當歸")], wiki_zh_gen="當歸屬"),
                            ]),
                          N("五加科", "Araliaceae", wiki_zh="五加科", dist="掌状复叶多；花小成伞形；人参、五加、常春藤",
                            children=[
                                genus_species("人参属", "Panax", [("人参", "Panax ginseng", "人參")], wiki_zh_gen="人參屬"),
                                genus_species("常春藤属", "Hedera", [("常春藤", "Hedera nepalensis", "常春藤")], wiki_zh_gen="常春藤屬"),
                            ]),
                      ]),
                    N("葡萄目", "Vitales", wiki_zh="葡萄目",
                      dist="多木质藤本；卷须与叶对生；浆果(葡萄)",
                      children=[
                          N("葡萄科", "Vitaceae", wiki_zh="葡萄科", dist="卷须攀援；叶掌状裂；浆果聚集成串",
                            children=[
                                N("葡萄属", "Vitis", wiki_zh="葡萄屬",
                                  children=[N("葡萄", "Vitis vinifera", wiki_zh="釀酒葡萄")])
                            ])
                      ]),
                    N("锦葵目", "Malvales", wiki_zh="錦葵目", note="棉、木棉、可可",
                      dist="多星状毛或鳞片；花5基数萼瓣明显；雄蕊常合生成筒",
                      children=[
                          N("锦葵科", "Malvaceae", wiki_zh="錦葵科", dist="雄蕊合生成管；萼下常有副萼；棉、芙蓉、木棉",
                            children=[
                                N("棉属", "Gossypium", wiki_zh="棉屬",
                                  children=[N("陆地棉", "Gossypium hirsutum", wiki_zh="陸地棉")]),
                                genus_species("木槿属", "Hibiscus", [
                                    ("木槿", "Hibiscus syriacus", "木槿"),
                                    ("朱槿", "Hibiscus rosa-sinensis", "朱槿"),
                                    ("木芙蓉", "Hibiscus mutabilis", "木芙蓉"),
                                ], wiki_zh_gen="木槿屬"),
                                genus_species("可可属", "Theobroma", [("可可", "Theobroma cacao", "可可")], wiki_zh_gen="可可屬"),
                            ])
                      ]),
                    N("胡椒目", "Piperales", wiki_zh="胡椒目", note="胡椒、细辛",
                      dist="原始被子；花极简化无明显花被；含胡椒科",
                      children=[
                          N("胡椒科", "Piperaceae", wiki_zh="胡椒科",
                            dist="茎节膨大；穗状花序小花密集；含胡椒、蒌叶",
                            children=[
                                genus_species("胡椒属", "Piper", [("黑胡椒", "Piper nigrum", "黑胡椒")], wiki_zh_gen="胡椒屬")
                            ])
                      ]),
                    N("桃金娘目", "Myrtales", wiki_zh="桃金娘目", note="桉树、番石榴、石榴、紫薇",
                      dist="花瓣多4-5；雄蕊多；多常含挥发油；桉树/番石榴/石榴/紫薇",
                      children=[
                          N("桃金娘科", "Myrtaceae", wiki_zh="桃金娘科",
                            dist="叶对生革质具透明油点；花瓣脱落早雄蕊显著；多含精油",
                            children=[
                                genus_species("桉属", "Eucalyptus", [
                                    ("蓝桉", "Eucalyptus globulus", "藍桉"),
                                ], wiki_zh_gen="桉屬"),
                                genus_species("番石榴属", "Psidium", [("番石榴", "Psidium guajava", "番石榴")], wiki_zh_gen="番石榴屬"),
                                genus_species("丁子香属", "Syzygium", [("丁香(香料)", "Syzygium aromaticum", "丁子香")], wiki_zh_gen="蒲桃屬"),
                            ]),
                          N("千屈菜科", "Lythraceae", wiki_zh="千屈菜科",
                            dist="叶多对生；萼筒管状；含石榴、紫薇、散沫花",
                            children=[
                                genus_species("石榴属", "Punica", [("石榴", "Punica granatum", "石榴")], wiki_zh_gen="石榴屬"),
                                genus_species("紫薇属", "Lagerstroemia", [("紫薇", "Lagerstroemia indica", "紫薇")], wiki_zh_gen="紫薇屬"),
                            ]),
                      ]),
                    N("金虎尾目", "Malpighiales", wiki_zh="金虎尾目", note="杨柳、大戟、堇菜、柳叶菜",
                      dist="双子叶大目；含杨柳科、大戟科、堇菜科、西番莲科等",
                      children=[
                          N("杨柳科", "Salicaceae", wiki_zh="楊柳科",
                            dist="多为乔/灌木；柔荑花序；多雌雄异株；杨树、柳树",
                            children=[
                                genus_species("杨属", "Populus", [
                                    ("毛白杨", "Populus tomentosa", "毛白楊"),
                                ], wiki_zh_gen="楊屬"),
                                genus_species("柳属", "Salix", [
                                    ("垂柳", "Salix babylonica", "垂柳"),
                                ], wiki_zh_gen="柳屬"),
                            ]),
                          N("大戟科", "Euphorbiaceae", wiki_zh="大戟科",
                            dist="多含乳汁；花单性；多有毒；含大戟、蓖麻、橡胶树、木薯",
                            children=[
                                genus_species("橡胶树属", "Hevea", [("三叶橡胶树", "Hevea brasiliensis", "橡膠樹")], wiki_zh_gen="橡膠樹屬"),
                                genus_species("木薯属", "Manihot", [("木薯", "Manihot esculenta", "木薯")], wiki_zh_gen="木薯屬"),
                                genus_species("蓖麻属", "Ricinus", [("蓖麻", "Ricinus communis", "蓖麻")], wiki_zh_gen="蓖麻屬"),
                            ]),
                          N("堇菜科", "Violaceae", wiki_zh="堇菜科",
                            dist="多草本；花两侧对称具距；蒴果；三色堇、紫花地丁",
                            children=[
                                genus_species("堇菜属", "Viola", [
                                    ("三色堇", "Viola tricolor", "三色堇"),
                                    ("紫花地丁", "Viola philippica", "紫花地丁"),
                                ], wiki_zh_gen="堇菜屬"),
                            ]),
                      ]),
                    N("山龙眼目", "Proteales", wiki_zh="山龍眼目", note="莲、悬铃木、山龙眼",
                      dist="包含莲科(水生)、悬铃木科(行道树)、山龙眼科",
                      children=[
                          N("莲科", "Nelumbonaceae", wiki_zh="蓮科",
                            dist="水生；叶盾形伸出水面；花大单生；果为莲蓬",
                            children=[
                                genus_species("莲属", "Nelumbo", [("莲(荷花)", "Nelumbo nucifera", "蓮")], wiki_zh_gen="蓮屬"),
                            ]),
                          N("悬铃木科", "Platanaceae", wiki_zh="懸鈴木科",
                            dist="落叶大乔木；树皮片状剥落；叶掌状分裂；球形果序悬吊",
                            children=[
                                genus_species("悬铃木属", "Platanus", [
                                    ("二球悬铃木", "Platanus × acerifolia", "二球懸鈴木"),
                                ], wiki_zh_gen="懸鈴木屬"),
                            ]),
                      ]),
                    N("睡莲目", "Nymphaeales", wiki_zh="睡蓮目",
                      dist="水生；叶漂浮具长柄；花大单生；古老类群",
                      children=[
                          N("睡莲科", "Nymphaeaceae", wiki_zh="睡蓮科",
                            dist="根状茎伏泥；叶圆或心形漂浮；花昼开夜合",
                            children=[
                                genus_species("睡莲属", "Nymphaea", [("白睡莲", "Nymphaea alba", "白睡蓮")], wiki_zh_gen="睡蓮屬"),
                            ])
                      ]),
                    N("唇形目", "Lamiales", wiki_zh="唇形目", note="薰衣草、薄荷、橄榄、茉莉",
                      dist="花多两侧对称呈唇形；多具挥发香气；含唇形科、木樨科、玄参科等",
                      children=[
                          N("唇形科", "Lamiaceae", wiki_zh="唇形科",
                            dist="茎常方形；叶对生；花冠二唇形(上下)；多含芳香油(薄荷薰衣草)",
                            children=[
                                genus_species("薄荷属", "Mentha", [
                                    ("薄荷", "Mentha canadensis", "薄荷"),
                                    ("留兰香", "Mentha spicata", "留蘭香"),
                                ], wiki_zh_gen="薄荷屬"),
                                genus_species("薰衣草属", "Lavandula", [("狭叶薰衣草", "Lavandula angustifolia", "薰衣草")], wiki_zh_gen="薰衣草屬"),
                                genus_species("罗勒属", "Ocimum", [("罗勒", "Ocimum basilicum", "羅勒")], wiki_zh_gen="羅勒屬"),
                                genus_species("迷迭香属", "Salvia", [
                                    ("迷迭香", "Salvia rosmarinus", "迷迭香"),
                                    ("鼠尾草", "Salvia officinalis", "藥用鼠尾草"),
                                    ("丹参", "Salvia miltiorrhiza", "丹參"),
                                ], wiki_zh_gen="鼠尾草屬"),
                                genus_species("紫苏属", "Perilla", [("紫苏", "Perilla frutescens", "紫蘇")], wiki_zh_gen="紫蘇屬"),
                                genus_species("牛至属", "Origanum", [("牛至", "Origanum vulgare", "牛至")], wiki_zh_gen="牛至屬"),
                                genus_species("百里香属", "Thymus", [("百里香", "Thymus mongolicus", "百里香")], wiki_zh_gen="百里香屬"),
                            ]),
                          N("木犀科", "Oleaceae", wiki_zh="木樨科", note="橄榄、茉莉、桂花",
                            dist="叶多对生；花4裂合瓣；多芳香；果为核果(橄榄)或蒴果(连翘)",
                            children=[
                                N("茉莉属", "Jasminum", wiki_zh="茉莉屬",
                                  dist="灌木或藤本；花白或黄，浓香；叶对生或三出复叶",
                                  children=[
                                      N("茉莉", "Jasminum sambac", wiki_zh="茉莉"),
                                      N("迎春花", "Jasminum nudiflorum", wiki_zh="迎春花"),
                                  ]),
                                N("木犀属", "Osmanthus", wiki_zh="木樨屬",
                                  dist="常绿乔木或灌木；小花簇生叶腋，香味浓郁",
                                  children=[N("桂花", "Osmanthus fragrans", wiki_zh="桂花")]),
                                genus_species("橄榄属", "Olea", [("油橄榄", "Olea europaea", "油橄欖")], wiki_zh_gen="木樨欖屬"),
                                genus_species("丁香属", "Syringa", [("紫丁香", "Syringa oblata", "紫丁香")], wiki_zh_gen="丁香屬"),
                            ]),
                      ]),
                ])
          ]),
    ]
)

# ============================================================
# 动物界 Animalia
# ============================================================
# Build animal kingdom - most comprehensive
kingdom_animalia = N(
    "动物界", "Animalia", wiki_zh="动物",
    note="多细胞异养、无细胞壁",
    dist="真核、多细胞、异养；无细胞壁；一般能运动",
    children=[
        N("多孔动物门", "Porifera", wiki_zh="多孔動物門", note="海绵",
          dist="最原始的多细胞动物；无组织器官；固着滤食",
          children=[
              N("寻常海绵纲", "Demospongiae", wiki_zh="尋常海綿綱", dist="海绵门最大纲；骨针硅质或蛋白海绵丝"),
              N("钙质海绵纲", "Calcarea", wiki_zh="鈣質海綿綱", dist="骨针为碳酸钙；小型；主要浅海"),
              N("六放海绵纲", "Hexactinellida", wiki_zh="六放海綿綱", dist="玻璃海绵；三轴六放硅质骨针；深海"),
          ]),
        N("栉水母动物门", "Ctenophora", wiki_zh="櫛水母動物門", note="栉水母",
          dist="两辐射对称；8列栉板(纤毛)供游动；有胶状体"),
        N("刺胞动物门", "Cnidaria", wiki_zh="刺胞動物門", note="水母、珊瑚、海葵",
          dist="辐射对称；两胚层；具刺胞(刺细胞)；水螅体/水母体两形",
          children=[
              N("水螅纲", "Hydrozoa", wiki_zh="水螅綱",
                children=[
                    N("软水母目", "Leptothecata", wiki_zh="軟水母目"),
                    N("花裸螅目", "Anthoathecata", wiki_zh="花裸螅目", dist="典型水螅体有花状；水母体小"),
                ]),
              N("钵水母纲", "Scyphozoa", wiki_zh="缽水母綱", note="大型水母",
                children=[
                    N("旗口水母目", "Semaeostomeae", wiki_zh="旗口水母目", dist="伞宽大；口腕4长带；海月水母"),
                    N("根口水母目", "Rhizostomeae", wiki_zh="根口水母目", dist="口腕愈合为多孔口；海蜇食用品属此"),
                ]),
              N("珊瑚纲", "Anthozoa", wiki_zh="珊瑚綱", note="珊瑚、海葵",
                children=[
                    N("石珊瑚目", "Scleractinia", wiki_zh="石珊瑚目", dist="分泌石灰质外骨骼；造礁主力"),
                    N("海葵目", "Actiniaria", wiki_zh="海葵目", dist="无骨骼；单体；口盘密触手"),
                    N("软珊瑚目", "Alcyonacea", wiki_zh="軟珊瑚目", dist="有机基质肉质群体；含柳珊瑚、海鳃"),
                ]),
              N("立方水母纲", "Cubozoa", wiki_zh="立方水母綱", note="箱水母"),
          ]),
        N("扁形动物门", "Platyhelminthes", wiki_zh="扁形動物門",
          dist="两侧对称；三胚层无体腔；背腹扁平；无呼吸/循环系统",
          children=[
              N("涡虫纲", "Turbellaria", wiki_zh="渦蟲綱",
                children=[
                    N("三肠目", "Tricladida", wiki_zh="三腸目", dist="消化道三叉；常见涡虫",
                      children=[
                          N("真涡虫科", "Dugesiidae", wiki_zh="真渦蟲科",
                            children=[
                                N("真涡虫属", "Dugesia", wiki_zh="真渦蟲屬",
                                  children=[N("三角涡虫", "Dugesia japonica", wiki_zh="日本三角渦蟲")])
                            ])
                      ])
                ]),
              N("吸虫纲", "Trematoda", wiki_zh="吸蟲綱", note="血吸虫、肝吸虫",
                children=[
                    N("复殖目", "Plagiorchiida", wiki_zh="複殖目", dist="人畜寄生吸虫；血吸虫、肝吸虫均属此"),
                ]),
              N("绦虫纲", "Cestoda", wiki_zh="絛蟲綱",
                children=[
                    N("圆叶目", "Cyclophyllidea", wiki_zh="圓葉目", dist="头节4吸盘；多寄生哺乳；猪带绦、牛带绦"),
                ]),
          ]),
        N("线虫动物门", "Nematoda", wiki_zh="線蟲動物門", note="蛔虫、钩虫、线虫",
          dist="圆柱形；假体腔；有完整消化道(口+肛门)；身体不分节",
          children=[
              N("色矛纲", "Chromadorea", wiki_zh="色矛綱",
                dist="线虫动物门主要纲；多自由生活；秀丽隐杆线虫归此"),
              N("刺嘴纲", "Enoplea", wiki_zh="刺嘴綱",
                dist="多数寄生类(人蛔虫、鞭虫)；角质层较厚"),
          ]),
        N("轮虫动物门", "Rotifera", wiki_zh="輪蟲動物門",
          dist="极小；头部有轮盘状纤毛冠；多孤雌生殖"),
        N("环节动物门", "Annelida", wiki_zh="環節動物門",
          dist="身体分节(同律分节)；真体腔；闭管循环",
          children=[
              N("多毛纲", "Polychaeta", wiki_zh="多毛綱", note="沙蚕",
                children=[
                    N("叶须虫目", "Phyllodocida", wiki_zh="葉鬚蟲目", dist="活跃游泳/爬行；具明显触须和刚毛"),
                ]),
              N("寡毛纲", "Oligochaeta", wiki_zh="寡毛綱", note="蚯蚓",
                children=[
                    N("单向蚓目", "Haplotaxida", wiki_zh="單向蚓目", dist="陆生蚯蚓所在；土壤改良者",
                      children=[
                          N("正蚓科", "Lumbricidae", wiki_zh="正蚓科",
                            children=[
                                N("蚓属", "Lumbricus", wiki_zh="蚓屬",
                                  children=[N("赤子爱胜蚓", "Eisenia fetida", wiki_zh="赤子愛勝蚓")])
                            ])
                      ])
                ]),
              N("蛭纲", "Hirudinea", wiki_zh="蛭綱", note="水蛭"),
          ]),
        N("软体动物门", "Mollusca", wiki_zh="軟體動物",
          dist="身体柔软不分节；外套膜分泌贝壳(多数)；具肌肉足",
          children=[
              N("腹足纲", "Gastropoda", wiki_zh="腹足綱", note="蜗牛、螺",
                children=[
                    N("柄眼目", "Stylommatophora", wiki_zh="柄眼目", dist="陆生蜗牛代表；眼在触角顶端",
                      children=[
                          N("玛瑙螺科", "Achatinidae", wiki_zh="瑪瑙螺科",
                            children=[N("非洲大蜗牛属", "Lissachatina", wiki_zh="非洲大蝸牛屬", dist="陆生大型蜗牛；外来入侵种",
                              children=[N("非洲大蜗牛", "Lissachatina fulica", wiki_zh="非洲大蝸牛")])])
                      ])
                ]),
              N("双壳纲", "Bivalvia", wiki_zh="雙殼綱", note="蛤、牡蛎、贻贝",
                children=[
                    N("贻贝目", "Mytilida", wiki_zh="貽貝目", dist="等壳不等侧；足丝固着；贻贝",
                      children=[
                          N("贻贝科", "Mytilidae", wiki_zh="貽貝科", dist="足丝固着岩石；紫黑色贝壳",
                            children=[
                                genus_species("贻贝属", "Mytilus", [("紫贻贝", "Mytilus edulis", "紫貽貝")], wiki_zh_gen="貽貝屬"),
                            ])
                      ]),
                    N("帘蛤目", "Venerida", wiki_zh="簾蛤目", dist="壳圆或三角；肉足发达能掘沙；文蛤、蛤蜊",
                      children=[
                          N("帘蛤科", "Veneridae", wiki_zh="簾蛤科",
                            children=[
                                genus_species("文蛤属", "Meretrix", [("文蛤", "Meretrix meretrix", "文蛤")], wiki_zh_gen="文蛤屬"),
                            ])
                      ]),
                    N("牡蛎目", "Ostreida", wiki_zh="牡蠣目", dist="下壳大固着；上壳小；贝壳形状不规则；蚝",
                      children=[
                          N("牡蛎科", "Ostreidae", wiki_zh="牡蠣科", dist="下壳附石；壳厚不规则",
                            children=[
                                genus_species("巨牡蛎属", "Crassostrea", [("长牡蛎", "Crassostrea gigas", "長牡蠣")], wiki_zh_gen="巨牡蠣屬"),
                            ]),
                          N("扇贝科", "Pectinidae", wiki_zh="海扇蛤科", dist="扇形辐射肋；能喷水游动",
                            children=[
                                genus_species("栉孔扇贝属", "Mizuhopecten", [("虾夷扇贝", "Mizuhopecten yessoensis", "蝦夷扇貝")], wiki_zh_gen="栉孔扇貝屬"),
                            ]),
                      ]),
                ]),
              N("头足纲", "Cephalopoda", wiki_zh="頭足綱", note="章鱼、乌贼、鱿鱼",
                children=[
                    N("八腕目", "Octopoda", wiki_zh="八腕目", dist="8只触腕，无鳍无内壳；章鱼",
                      children=[
                          N("章鱼科", "Octopodidae", wiki_zh="章魚科",
                            children=[
                                N("章鱼属", "Octopus", wiki_zh="章魚屬",
                                  children=[N("真蛸", "Octopus vulgaris", wiki_zh="真蛸")])
                            ])
                      ]),
                    N("枪形目", "Teuthida", wiki_zh="槍形目", dist="10腕(含2长触腕)；体梭形；内壳角质透明；鱿鱼"),
                    N("乌贼目", "Sepiida", wiki_zh="烏賊目", dist="10腕；体扁椭圆；内壳石灰质(海螵蛸)；乌贼"),
                    N("鹦鹉螺目", "Nautilida", wiki_zh="鸚鵡螺目", dist="90余腕；具外壳(多室)；活化石"),
                ]),
              N("多板纲", "Polyplacophora", wiki_zh="多板綱", note="石鳖"),
          ]),
        N("节肢动物门", "Arthropoda", wiki_zh="節肢動物", note="种类最多的门",
          dist="身体分节且附肢分节；几丁质外骨骼；蜕皮生长；动物界最大门",
          children=[
              N("昆虫纲", "Insecta", wiki_zh="昆蟲",
                dist="头胸腹三部分；3对足(全在胸部)；通常2对翅；1对触角",
                children=[
                    N("鳞翅目", "Lepidoptera", wiki_zh="鱗翅目", note="蝴蝶、蛾",
                      dist="翅上覆鳞片；虹吸式口器；完全变态(卵/幼/蛹/成)",
                      children=[
                          N("凤蝶科", "Papilionidae", wiki_zh="鳳蝶科",
                            children=[
                                genus_species("凤蝶属", "Papilio", [
                                    ("柑橘凤蝶", "Papilio xuthus", "柑橘鳳蝶"),
                                    ("玉带凤蝶", "Papilio polytes", "玉帶鳳蝶"),
                                ], wiki_zh_gen="鳳蝶屬"),
                            ]),
                          N("蚕蛾科", "Bombycidae",
                            children=[
                                genus_species("蚕蛾属", "Bombyx", [("家蚕", "Bombyx mori", "蠶")], wiki_zh_gen="蠶蛾屬"),
                            ]),
                          N("粉蝶科", "Pieridae", wiki_zh="粉蝶科", dist="中小型，白/黄为主；多数幼虫取食十字花科",
                            children=[
                                genus_species("粉蝶属", "Pieris", [("菜粉蝶", "Pieris rapae", "菜粉蝶")], wiki_zh_gen="粉蝶屬"),
                            ]),
                          N("蛱蝶科", "Nymphalidae", wiki_zh="蛺蝶科", dist="蝶科最大；前足退化；翅形多变",
                            children=[
                                genus_species("斑蝶属", "Danaus", [("帝王斑蝶", "Danaus plexippus", "帝王斑蝶")], wiki_zh_gen="斑蝶屬"),
                            ]),
                          N("天蛾科", "Sphingidae", wiki_zh="天蛾科", dist="飞行极快；形似蜂鸟悬停吸蜜"),
                          N("毒蛾科", "Erebidae", wiki_zh="夜蛾科", dist="含毒蛾亚科、夜蛾亚科；幼虫多为害虫"),
                      ]),
                    N("鞘翅目", "Coleoptera", wiki_zh="鞘翅目", note="甲虫；动物界最大目",
                      dist="前翅硬化为鞘翅覆盖背部；咀嚼口器；完全变态",
                      children=[
                          N("瓢虫科", "Coccinellidae", wiki_zh="瓢蟲科",
                            children=[
                                genus_species("瓢虫属", "Coccinella", [("七星瓢虫", "Coccinella septempunctata", "七星瓢蟲")], wiki_zh_gen="瓢蟲屬"),
                            ]),
                          N("金龟科", "Scarabaeidae", wiki_zh="金龜科",
                            children=[
                                genus_species("独角仙属", "Trypoxylus", [("双叉犀金龟", "Trypoxylus dichotomus", "獨角仙")], wiki_zh_gen="獨角仙屬")
                            ]),
                          N("步甲科", "Carabidae", wiki_zh="步甲科"),
                          N("天牛科", "Cerambycidae", wiki_zh="天牛科", dist="触角特长(常超体长)；幼虫蛀木;成虫咀嚼植物",
                            children=[
                                genus_species("星天牛属", "Anoplophora", [("星天牛", "Anoplophora chinensis", "星天牛")], wiki_zh_gen="星天牛屬"),
                            ]),
                          N("锹甲科", "Lucanidae", wiki_zh="鍬形蟲科", dist="雄虫上颚发达似鹿角；腐木或汁液为食",
                            children=[
                                genus_species("深山锹甲属", "Lucanus", [("深山锹甲", "Lucanus maculifemoratus", "深山鍬甲")], wiki_zh_gen="鍬甲屬"),
                            ]),
                          N("萤科", "Lampyridae", wiki_zh="螢火蟲科", dist="腹末具发光器；夜间闪光求偶",
                            children=[
                                genus_species("萤属", "Luciola", [("黄缘萤", "Luciola ficta", None)], wiki_zh_gen="螢屬"),
                            ]),
                          N("象甲科", "Curculionidae", wiki_zh="象甲科", dist="头延伸成长吻；全球物种最多的科之一"),
                      ]),
                    N("双翅目", "Diptera", wiki_zh="雙翅目", note="蚊、蝇",
                      dist="只有前翅；后翅退化为平衡棒；刺吸/舐吸口器",
                      children=[
                          N("蚊科", "Culicidae", wiki_zh="蚊科",
                            children=[
                                genus_species("按蚊属", "Anopheles", [("中华按蚊", "Anopheles sinensis", "中華按蚊")], wiki_zh_gen="按蚊屬"),
                                genus_species("伊蚊属", "Aedes", [("白纹伊蚊", "Aedes albopictus", "白紋伊蚊")], wiki_zh_gen="斑蚊屬"),
                            ]),
                          N("家蝇科", "Muscidae", wiki_zh="家蠅科",
                            children=[
                                genus_species("家蝇属", "Musca", [("家蝇", "Musca domestica", "家蠅")], wiki_zh_gen="家蠅屬")
                            ]),
                          N("果蝇科", "Drosophilidae", wiki_zh="果蠅科", dist="小型；模式生物(遗传学)",
                            children=[
                                genus_species("果蝇属", "Drosophila", [("黑腹果蝇", "Drosophila melanogaster", "黑腹果蠅")], wiki_zh_gen="果蠅屬"),
                            ])
                      ]),
                    N("膜翅目", "Hymenoptera", wiki_zh="膜翅目", note="蜂、蚁",
                      dist="两对膜质翅(前大后小，翅钩连锁)；多具螫针；高度社会性",
                      children=[
                          N("蜜蜂科", "Apidae", wiki_zh="蜜蜂科",
                            children=[
                                genus_species("蜜蜂属", "Apis", [
                                    ("西方蜜蜂", "Apis mellifera", "西方蜜蜂"),
                                    ("东方蜜蜂", "Apis cerana", "東方蜜蜂"),
                                ], wiki_zh_gen="蜜蜂屬")
                            ]),
                          N("蚁科", "Formicidae", wiki_zh="蟻科",
                            children=[
                                genus_species("弓背蚁属", "Camponotus", [("日本弓背蚁", "Camponotus japonicus", "日本弓背蟻")], wiki_zh_gen="弓背蟻屬"),
                                genus_species("切叶蚁属", "Atta", [("切叶蚁", "Atta cephalotes", "切葉蟻")], wiki_zh_gen="切葉蟻屬"),
                            ]),
                          N("胡蜂科", "Vespidae", wiki_zh="胡蜂科",
                            children=[
                                genus_species("胡蜂属", "Vespa", [("金环胡蜂", "Vespa mandarinia", "金環胡蜂")], wiki_zh_gen="胡蜂屬"),
                            ]),
                      ]),
                    N("半翅目", "Hemiptera", wiki_zh="半翅目", note="蝉、椿象、蚜虫",
                      dist="刺吸式口器；前翅半硬化(椿象)或均匀(蝉)；不完全变态",
                      children=[
                          N("蝉科", "Cicadidae", wiki_zh="蟬科", dist="雄蝉腹基有发音器；若虫地下吸根数年",
                            children=[
                                genus_species("蚱蝉属", "Cryptotympana", [("蚱蝉", "Cryptotympana atrata", "蚱蟬")], wiki_zh_gen="蚱蟬屬"),
                            ]),
                          N("蝽科", "Pentatomidae", wiki_zh="椿象科", dist="盾形背板；具臭腺",
                            children=[
                                genus_species("蝽属", "Halyomorpha", [("茶翅蝽", "Halyomorpha halys", "茶翅蝽")], wiki_zh_gen="茶翅蝽屬"),
                            ]),
                          N("蚜科", "Aphididae", wiki_zh="蚜蟲科", dist="极小柔软；孤雌胎生；分泌蜜露"),
                      ]),
                    N("直翅目", "Orthoptera", wiki_zh="直翅目", note="蝗虫、蟋蟀、螽斯",
                      dist="后足腿节发达善跳；咀嚼口器；不完全变态；多能发声",
                      children=[
                          N("蝗科", "Acrididae", wiki_zh="蝗科", dist="触角短；后腿发达善跳；迁飞型为害重",
                            children=[
                                genus_species("飞蝗属", "Locusta", [("东亚飞蝗", "Locusta migratoria", "飛蝗")], wiki_zh_gen="飛蝗屬"),
                            ]),
                          N("蟋蟀科", "Gryllidae", wiki_zh="蟋蟀科", dist="翅短；雄虫前翅摩擦发声",
                            children=[
                                genus_species("斗蟋属", "Velarifictorus", [("迷卡斗蟋", "Velarifictorus micado", "迷卡鬥蟋")], wiki_zh_gen="斗蟋屬"),
                            ]),
                          N("螽斯科", "Tettigoniidae", wiki_zh="螽斯科", dist="触角极长；叶状翅；夜间发声"),
                      ]),
                    N("蜻蜓目", "Odonata", wiki_zh="蜻蜓目", note="蜻蜓、豆娘",
                      dist="两对透明大翅；复眼巨大；幼虫(稚虫)水生；捕食性",
                      children=[
                          N("蜻科", "Libellulidae", wiki_zh="蜻科", dist="停息时翅平展；腹粗短；常见蜻蜓",
                            children=[
                                genus_species("赤蜻属", "Sympetrum", [("红蜻", "Sympetrum pedemontanum", "紅蜻")], wiki_zh_gen="赤蜻屬"),
                            ]),
                          N("豆娘科", "Coenagrionidae", wiki_zh="蟌科", dist="停息时翅合拢；体纤细；水边常见"),
                      ]),
                    N("蜚蠊目", "Blattodea", wiki_zh="蜚蠊目", note="蟑螂、白蚁",
                      children=[
                          N("蜚蠊科", "Blattidae", wiki_zh="蜚蠊科",
                            children=[
                                genus_species("大蠊属", "Periplaneta", [("美洲大蠊", "Periplaneta americana", "美洲大蠊")], wiki_zh_gen="大蠊屬"),
                            ]),
                          N("小蠊科", "Ectobiidae", wiki_zh="家蠊科",
                            children=[
                                genus_species("小蠊属", "Blattella", [("德国小蠊", "Blattella germanica", "德國小蠊")], wiki_zh_gen="蜚蠊屬"),
                            ]),
                          N("白蚁科", "Termitidae", wiki_zh="白蟻科", dist="社会性；吃木富含纤维素；建巨大蚁冢"),
                      ]),
                    N("等翅目", "Isoptera", wiki_zh="等翅目", note="白蚁；现归入蜚蠊目"),
                    N("螳螂目", "Mantodea", wiki_zh="螳螂目",
                      children=[
                          N("螳螂科", "Mantidae", wiki_zh="螳螂科",
                            children=[
                                genus_species("斧螳属", "Hierodula", [("广斧螳", "Hierodula patellifera", "廣斧螳")], wiki_zh_gen="斧螳屬"),
                                genus_species("刀螳属", "Tenodera", [("中华刀螳", "Tenodera sinensis", "中華刀螳")], wiki_zh_gen="刀螳屬"),
                            ]),
                      ]),
                    N("竹节虫目", "Phasmatodea", wiki_zh="竹節蟲目"),
                    N("蚤目", "Siphonaptera", wiki_zh="蚤目", note="跳蚤"),
                    N("虱目", "Phthiraptera", wiki_zh="虱目"),
                    N("脉翅目", "Neuroptera", wiki_zh="脈翅目", note="草蛉、蚁蛉"),
                    N("毛翅目", "Trichoptera", wiki_zh="毛翅目"),
                    N("蜉蝣目", "Ephemeroptera", wiki_zh="蜉蝣目",
                      dist="最古老有翅昆虫；稚虫水生，成虫寿命极短(数小时至数日)；尾丝2-3根"),
                    N("缨翅目", "Thysanoptera", wiki_zh="纓翅目", note="蓟马",
                      dist="极小；两对羽状翅(缨状缘毛)；刺吸口器；农业害虫"),
                    N("革翅目", "Dermaptera", wiki_zh="革翅目", note="蠼螋",
                      dist="腹末一对钳状尾铗；前翅短革质；后翅折叠精巧"),
                    N("襀翅目", "Plecoptera", wiki_zh="襀翅目", note="石蝇",
                      dist="稚虫水生(清洁水质指示)；成虫翅膜质透明平铺；2尾丝"),
                    N("石蛃目", "Archaeognatha", wiki_zh="石蛃目",
                      dist="原始无翅昆虫；体披鳞；尾端3丝(中央特长)；潮湿环境"),
                    N("衣鱼目", "Zygentoma", wiki_zh="衣魚目",
                      dist="原始无翅昆虫；银灰色；腹末3丝；居室内食纸衣"),
                ]),
              N("蛛形纲", "Arachnida", wiki_zh="蛛形綱", note="蜘蛛、蝎子、蜱螨",
                dist="头胸+腹两部分；4对足；无翅无触角；螯肢/须肢；多陆生",
                children=[
                    N("蜘蛛目", "Araneae", wiki_zh="蜘蛛",
                      children=[
                          N("跳蛛科", "Salticidae", wiki_zh="蠅虎科", dist="复眼大而前向；视觉敏锐；善跳"),
                          N("络新妇科", "Nephilidae", wiki_zh="絡新婦科", dist="结大型金色丝网；热带常见",
                            children=[
                                genus_species("络新妇属", "Trichonephila", [("棒络新妇", "Trichonephila clavata", "棒絡新婦")], wiki_zh_gen="絡新婦屬"),
                            ]),
                          N("圆蛛科", "Araneidae", wiki_zh="金蛛科", dist="结平面圆网；腹部大多色彩鲜艳",
                            children=[
                                genus_species("园蛛属", "Araneus", [("十字园蛛", "Araneus diadematus", "十字園蛛")], wiki_zh_gen="園蛛屬"),
                            ]),
                      ]),
                    N("蝎目", "Scorpiones", wiki_zh="蠍子",
                      children=[
                          N("钳蝎科", "Buthidae", wiki_zh="鉗蠍科",
                            children=[
                                genus_species("钳蝎属", "Mesobuthus", [("东亚钳蝎", "Mesobuthus martensii", "東亞鉗蠍")], wiki_zh_gen="鉗蠍屬"),
                            ]),
                      ]),
                    N("蜱螨目", "Acari", wiki_zh="蜱螨亞綱"),
                ]),
              N("软甲纲", "Malacostraca", wiki_zh="軟甲綱", note="甲壳亚门；虾、蟹、龙虾、潮虫",
                dist="甲壳亚门代表纲；2对触角；多胸足；多水生",
                children=[
                    N("等足目", "Isopoda", wiki_zh="等足目", note="潮虫、船蛆",
                      dist="体背腹扁平；7对大小相近胸足；陆海淡水都有(潮虫)"),
                    N("端足目", "Amphipoda", wiki_zh="端足目", note="钩虾",
                      dist="体侧扁；胸足前后用途不同；广泛水生"),
                    N("磷虾目", "Euphausiacea", wiki_zh="磷蝦目",
                      dist="虾状浮游；具发光器；南极磷虾食物链关键"),
                    N("口足目", "Stomatopoda", wiki_zh="口足目", note="螳螂虾",
                      dist="第二胸足特化为强力捕捉足；视觉极复杂"),
                    N("十足目", "Decapoda", wiki_zh="十足目", note="虾、蟹、龙虾",
                      dist="胸部5对步足(共10足)；头胸部甲壳融合；多水生",
                      children=[
                          N("对虾科", "Penaeidae",
                            children=[
                                genus_species("对虾属", "Penaeus", [("中国对虾", "Penaeus chinensis", None)], wiki_zh_gen="對蝦屬")
                            ]),
                          N("弓蟹科", "Varunidae",
                            children=[
                                genus_species("绒螯蟹属", "Eriocheir", [("中华绒螯蟹", "Eriocheir sinensis", "中華絨螯蟹")], wiki_zh_gen="絨螯蟹屬")
                            ]),
                          N("螯虾科", "Cambaridae", wiki_zh="螯蝦科", dist="淡水；第一对胸足大螯",
                            children=[
                                genus_species("原螯虾属", "Procambarus", [("克氏原螯虾", "Procambarus clarkii", "克氏原螯蝦")], wiki_zh_gen="原螯蝦屬"),
                            ]),
                          N("海螯虾科", "Nephropidae", wiki_zh="海螯蝦科", dist="海生；大型螯足；食用虾",
                            children=[
                                genus_species("螯龙虾属", "Homarus", [("美洲螯龙虾", "Homarus americanus", "美洲螯龍蝦")], wiki_zh_gen="美洲螯龍蝦屬"),
                            ]),
                          N("梭子蟹科", "Portunidae", wiki_zh="梭子蟹科", dist="最后一对胸足扁平桨状善游",
                            children=[
                                genus_species("梭子蟹属", "Portunus", [("三疣梭子蟹", "Portunus trituberculatus", "三疣梭子蟹")], wiki_zh_gen="梭子蟹屬"),
                            ]),
                      ]),
                ]),
              N("鳃足纲", "Branchiopoda", wiki_zh="鰓足綱", note="甲壳亚门；水蚤、丰年虾"),
              N("桡足纲", "Copepoda", wiki_zh="橈足綱", note="甲壳亚门；浮游小型甲壳"),
              N("蔓足纲", "Cirripedia", wiki_zh="蔓足亞綱", note="甲壳亚门；藤壶"),
              N("唇足纲", "Chilopoda", wiki_zh="唇足綱", note="多足亚门；蜈蚣",
                dist="每节1对足；第一对特化为毒颚；肉食"),
              N("倍足纲", "Diplopoda", wiki_zh="倍足綱", note="多足亚门；马陆",
                dist="每节2对足(由两节融合)；圆柱形，受扰卷曲；植食腐食"),
              N("肢口纲", "Merostomata", wiki_zh="肢口綱", note="鲎(活化石)",
                dist="古老螯肢亚门类群；背甲马蹄形；长尾剑；血液含铜(蓝色)",
                children=[
                    N("剑尾目", "Xiphosura", wiki_zh="劍尾目",
                      children=[
                          N("鲎科", "Limulidae", wiki_zh="鱟科",
                            children=[
                                N("美洲鲎属", "Limulus", wiki_zh="鱟屬",
                                  children=[N("美洲鲎", "Limulus polyphemus", wiki_zh="美洲鱟")])
                            ])
                      ])
                ]),
          ]),
        N("缓步动物门", "Tardigrada", wiki_zh="緩步動物門", note="水熊虫"),
        N("纽形动物门", "Nemertea", wiki_zh="紐形動物門", note="纽虫",
          dist="两侧对称；体细长扁平；吻管可外翻捕食；海生多见"),
        N("苔藓虫门", "Bryozoa", wiki_zh="苔蘚動物", note="群体苔藓虫",
          dist="微小群体生活；每个虫室内一个个体；多固着海生；群体似苔藓"),
        N("腕足动物门", "Brachiopoda", wiki_zh="腕足動物門", note="腕足类(海豆芽)",
          dist="形似双壳贝但腹背两壳(非左右)；具肉茎固着；有触手冠"),
        N("半索动物门", "Hemichordata", wiki_zh="半索動物門", note="柱头虫",
          dist="体蠕虫状；具咽鳃裂和口索(半脊索)；为脊索动物近亲"),
        N("棘皮动物门", "Echinodermata", wiki_zh="棘皮動物門",
          dist="五辐射对称(成体)；水管系统驱动管足；内骨骼钙质骨片",
          children=[
              N("海星纲", "Asteroidea", wiki_zh="海星綱",
                children=[
                    N("瓣棘海星目", "Valvatida", wiki_zh="瓣棘海星目", dist="常见海星所在；盘与腕分界明显",
                      children=[
                          N("海燕科", "Asterinidae", wiki_zh="海燕科",
                            children=[
                                genus_species("海燕属", "Asterina", [("海燕", "Asterina pectinifera", "海燕")], wiki_zh_gen="海燕屬"),
                            ])
                      ]),
                    N("钳棘目", "Forcipulatida", wiki_zh="鉗棘目", dist="棘末端钳状；北方海域常见",
                      children=[
                          N("海盘车科", "Asteriidae", wiki_zh="海盤車科",
                            children=[
                                genus_species("海盘车属", "Asterias", [("多棘海盘车", "Asterias amurensis", "多棘海盤車")], wiki_zh_gen="海盤車屬"),
                            ])
                      ])
                ]),
              N("海胆纲", "Echinoidea", wiki_zh="海膽綱",
                children=[
                    N("拱齿目", "Camarodonta", wiki_zh="拱齒目", dist="常见球形海胆；齿咬合装置(亚氏提灯)",
                      children=[
                          N("球海胆科", "Strongylocentrotidae", wiki_zh="球海膽科",
                            children=[
                                genus_species("球海胆属", "Strongylocentrotus", [("马粪海胆", "Strongylocentrotus intermedius", "馬糞海膽")], wiki_zh_gen="球海膽屬"),
                            ])
                      ]),
                    N("盾海胆目", "Clypeasteroida", wiki_zh="盾海膽目", dist="体扁圆盘形；沙中潜居(沙钱)"),
                ]),
              N("海参纲", "Holothuroidea", wiki_zh="海參綱",
                children=[
                    N("楯手目", "Aspidochirotida", wiki_zh="楯手目", dist="口触手楯形；体壁肉质；食用海参",
                      children=[
                          N("刺参科", "Stichopodidae", wiki_zh="刺參科",
                            children=[
                                genus_species("仿刺参属", "Apostichopus", [("仿刺参", "Apostichopus japonicus", "仿刺參")], wiki_zh_gen="仿刺參屬"),
                            ])
                      ]),
                ]),
              N("海百合纲", "Crinoidea", wiki_zh="海百合綱"),
              N("蛇尾纲", "Ophiuroidea", wiki_zh="蛇尾綱"),
          ]),
        N("脊索动物门", "Chordata", wiki_zh="脊索動物",
          dist="具脊索；背神经管；咽鳃裂；肛后尾(至少胚期具备)",
          children=[
              N("软骨鱼纲", "Chondrichthyes", wiki_zh="軟骨魚綱", note="鲨、鳐",
                dist="骨骼全为软骨；鳃裂5-7对无鳃盖；体表有盾鳞",
                children=[
                    N("鼠鲨目", "Lamniformes", wiki_zh="鼠鯊目",
                      children=[
                          N("鼠鲨科", "Lamnidae",
                            children=[
                                genus_species("噬人鲨属", "Carcharodon", [("噬人鲨", "Carcharodon carcharias", "噬人鯊")], wiki_zh_gen="噬人鯊屬")
                            ])
                      ]),
                    N("虎鲨目", "Heterodontiformes"),
                    N("鳐目", "Rajiformes", wiki_zh="鰩目"),
                ]),
              N("硬骨鱼纲", "Actinopterygii", wiki_zh="輻鰭魚綱", note="大多数鱼类",
                dist="骨骼硬骨为主；有鳃盖、鱼鳔；大多数鱼",
                children=[
                    N("鲤形目", "Cypriniformes", wiki_zh="鯉形目",
                      children=[
                          N("鲤科", "Cyprinidae", wiki_zh="鯉科",
                            children=[
                                genus_species("鲤属", "Cyprinus", [("鲤", "Cyprinus carpio", "鯉")], wiki_zh_gen="鯉屬"),
                                genus_species("鲫属", "Carassius", [
                                    ("金鱼", "Carassius auratus", "金魚"),
                                    ("鲫", "Carassius gibelio", "鯽"),
                                ], wiki_zh_gen="鯽屬"),
                                genus_species("草鱼属", "Ctenopharyngodon", [("草鱼", "Ctenopharyngodon idella", "草魚")], wiki_zh_gen="草魚屬"),
                                genus_species("鲢属", "Hypophthalmichthys", [
                                    ("鲢", "Hypophthalmichthys molitrix", "鰱"),
                                    ("鳙", "Hypophthalmichthys nobilis", "鱅"),
                                ], wiki_zh_gen="鰱屬"),
                            ])
                      ]),
                    N("鲈形目", "Perciformes", wiki_zh="鱸形目", note="最大的鱼类目",
                      children=[
                          N("鲭科", "Scombridae", wiki_zh="鯖科", dist="高速远洋鱼；流线型",
                            children=[
                                genus_species("金枪鱼属", "Thunnus", [("蓝鳍金枪鱼", "Thunnus thynnus", "大西洋藍鰭金槍魚")], wiki_zh_gen="金槍魚屬"),
                                genus_species("鲭属", "Scomber", [("鲐鱼", "Scomber japonicus", "鯖")], wiki_zh_gen="鯖屬"),
                            ]),
                          N("鮨科", "Serranidae", wiki_zh="鮨科",
                            children=[
                                genus_species("石斑鱼属", "Epinephelus", [("点带石斑鱼", "Epinephelus coioides", "點帶石斑魚")], wiki_zh_gen="石斑魚屬"),
                            ]),
                          N("鲷科", "Sparidae", wiki_zh="鯛科",
                            children=[
                                genus_species("真鲷属", "Pagrus", [("真鲷", "Pagrus major", "真鯛")], wiki_zh_gen="真鯛屬"),
                            ]),
                          N("海马科", "Syngnathidae", wiki_zh="海龍科",
                            children=[
                                genus_species("海马属", "Hippocampus", [("三斑海马", "Hippocampus trimaculatus", "三斑海馬")], wiki_zh_gen="海馬屬"),
                            ]),
                      ]),
                    N("鲑形目", "Salmoniformes", wiki_zh="鮭形目", note="鲑、鳟",
                      children=[
                          N("鲑科", "Salmonidae", wiki_zh="鮭科",
                            children=[
                                genus_species("大马哈鱼属", "Oncorhynchus", [("大马哈鱼", "Oncorhynchus keta", "大麻哈魚")], wiki_zh_gen="大麻哈魚屬"),
                                genus_species("鲑属", "Salmo", [("大西洋鲑", "Salmo salar", "大西洋鮭")], wiki_zh_gen="鮭屬"),
                            ])
                      ]),
                    N("鲀形目", "Tetraodontiformes", wiki_zh="鯰形目", note="河豚",
                      children=[
                          N("鲀科", "Tetraodontidae", wiki_zh="鮋科(河魨科)",
                            children=[
                                genus_species("东方鲀属", "Takifugu", [("红鳍东方鲀", "Takifugu rubripes", "紅鰭東方魨")], wiki_zh_gen="東方魨屬"),
                            ])
                      ]),
                    N("鲇形目", "Siluriformes", wiki_zh="鯰形目", note="鲶、鲨鱼鲶",
                      children=[
                          N("鲇科", "Siluridae", wiki_zh="鯰科",
                            children=[
                                genus_species("鲇属", "Silurus", [("鲇", "Silurus asotus", "鯰")], wiki_zh_gen="鯰屬"),
                            ]),
                      ]),
                    N("鲱形目", "Clupeiformes", wiki_zh="鯡形目", note="鲱、沙丁",
                      dist="海淡水中上层鱼；体银亮；成群洄游；鲱、凤尾鱼",
                      children=[
                          N("鲱科", "Clupeidae", wiki_zh="鯡科",
                            children=[
                                genus_species("鲱属", "Clupea", [("大西洋鲱", "Clupea harengus", "大西洋鯡")], wiki_zh_gen="鯡屬"),
                                genus_species("沙丁鱼属", "Sardina", [("沙丁鱼", "Sardina pilchardus", "沙丁魚")], wiki_zh_gen="沙丁魚屬"),
                            ]),
                      ]),
                    N("鳗鲡目", "Anguilliformes", wiki_zh="鰻鱺目",
                      dist="体长蛇形无腹鳍；洄游繁殖(海出生淡水生长)",
                      children=[
                          N("鳗鲡科", "Anguillidae", wiki_zh="鰻鱺科",
                            children=[
                                genus_species("鳗鲡属", "Anguilla", [("日本鳗鲡", "Anguilla japonica", "日本鰻鱺")], wiki_zh_gen="鰻鱺屬"),
                            ]),
                      ]),
                    N("鳕形目", "Gadiformes", wiki_zh="鱈形目",
                      dist="下颌常有颏须；背鳍2-3个；冷水海鱼；鳕鱼",
                      children=[
                          N("鳕科", "Gadidae", wiki_zh="鱈科",
                            children=[
                                genus_species("鳕属", "Gadus", [("大西洋鳕", "Gadus morhua", "大西洋鱈")], wiki_zh_gen="鱈屬"),
                            ]),
                      ]),
                    N("鲟形目", "Acipenseriformes", wiki_zh="鱘形目",
                      dist="古老鱼类；骨板代替鳞；吻长下颌内凹；鲟鱼",
                      children=[
                          N("鲟科", "Acipenseridae", wiki_zh="鱘科",
                            children=[
                                genus_species("鲟属", "Acipenser", [("中华鲟", "Acipenser sinensis", "中華鱘")], wiki_zh_gen="鱘屬"),
                            ]),
                      ]),
                    N("鲉形目", "Scorpaeniformes", wiki_zh="鮋形目",
                      dist="头部多棘；常具毒刺；底栖；鲉、石头鱼",
                      children=[
                          N("鲉科", "Scorpaenidae", wiki_zh="鮋科",
                            children=[
                                genus_species("蓑鲉属", "Pterois", [("斑鳍蓑鲉", "Pterois volitans", "魔鬼蓑鮋")], wiki_zh_gen="蓑鮋屬"),
                            ]),
                      ]),
                ]),
              N("两栖纲", "Amphibia", wiki_zh="兩棲動物",
                dist="变温；幼体水生用鳃，成体陆生用肺；皮肤裸露湿润辅助呼吸",
                children=[
                    N("无尾目", "Anura", wiki_zh="無尾目", note="青蛙、蟾蜍",
                      children=[
                          N("蛙科", "Ranidae", wiki_zh="蛙科",
                            children=[
                                genus_species("蛙属", "Rana", [
                                    ("黑斑蛙", "Rana nigromaculata", None),
                                    ("中国林蛙", "Rana chensinensis", "中國林蛙"),
                                ], wiki_zh_gen="蛙屬"),
                            ]),
                          N("蟾蜍科", "Bufonidae",
                            children=[
                                genus_species("蟾蜍属", "Bufo", [("中华蟾蜍", "Bufo gargarizans", "中華蟾蜍")], wiki_zh_gen="蟾蜍屬")
                            ]),
                          N("树蛙科", "Rhacophoridae", wiki_zh="樹蛙科", dist="指趾吸盘发达；多树栖；能滑翔(部分)",
                            children=[
                                genus_species("斑腿泛树蛙属", "Polypedates", [("斑腿泛树蛙", "Polypedates megacephalus", "斑腿泛樹蛙")], wiki_zh_gen="泛樹蛙屬"),
                            ]),
                          N("姬蛙科", "Microhylidae", wiki_zh="姬蛙科",
                            children=[
                                genus_species("姬蛙属", "Microhyla", [("饰纹姬蛙", "Microhyla fissipes", "飾紋姬蛙")], wiki_zh_gen="姬蛙屬"),
                            ]),
                          N("箭毒蛙科", "Dendrobatidae", wiki_zh="箭毒蛙科", dist="中南美雨林；皮肤剧毒色彩艳丽警戒",
                            children=[
                                genus_species("箭毒蛙属", "Phyllobates", [("金色箭毒蛙", "Phyllobates terribilis", "金色箭毒蛙")], wiki_zh_gen="葉毒蛙屬"),
                            ]),
                      ]),
                    N("有尾目", "Urodela", wiki_zh="有尾目", note="蝾螈、大鲵",
                      children=[
                          N("隐鳃鲵科", "Cryptobranchidae", wiki_zh="隱鰓鯢科",
                            children=[
                                genus_species("大鲵属", "Andrias", [("中国大鲵", "Andrias davidianus", "中國大鯢")], wiki_zh_gen="大鯢屬"),
                            ]),
                          N("蝾螈科", "Salamandridae", wiki_zh="蠑螈科",
                            children=[
                                genus_species("瘰螈属", "Paramesotriton", [("中国瘰螈", "Paramesotriton chinensis", "中國瘰螈")], wiki_zh_gen="瘰螈屬"),
                            ]),
                      ]),
                    N("无足目", "Gymnophiona", wiki_zh="無足目", note="蚓螈"),
                ]),
              N("爬行纲", "Reptilia", wiki_zh="爬行動物",
                dist="变温；体表角质鳞片或甲；卵生有卵壳；完全用肺呼吸",
                children=[
                    N("有鳞目", "Squamata", wiki_zh="有鱗目", note="蛇、蜥蜴",
                      children=[
                          N("游蛇科", "Colubridae", wiki_zh="游蛇科",
                            children=[
                                genus_species("锦蛇属", "Elaphe", [("王锦蛇", "Elaphe carinata", "王錦蛇")], wiki_zh_gen="錦蛇屬"),
                            ]),
                          N("蝮蛇科", "Viperidae", wiki_zh="蝰蛇科", note="蝮蛇、响尾蛇",
                            children=[
                                genus_species("蝮属", "Gloydius", [("短尾蝮", "Gloydius brevicaudus", "短尾蝮")], wiki_zh_gen="蝮屬"),
                                genus_species("响尾蛇属", "Crotalus", [("西部菱斑响尾蛇", "Crotalus atrox", "西部菱斑響尾蛇")], wiki_zh_gen="響尾蛇屬"),
                            ]),
                          N("眼镜蛇科", "Elapidae", wiki_zh="眼鏡蛇科",
                            children=[
                                genus_species("眼镜蛇属", "Naja", [("舟山眼镜蛇", "Naja atra", "舟山眼鏡蛇")], wiki_zh_gen="眼鏡蛇屬"),
                                genus_species("银环蛇属", "Bungarus", [("银环蛇", "Bungarus multicinctus", "銀環蛇")], wiki_zh_gen="環蛇屬"),
                            ]),
                          N("蟒科", "Pythonidae", wiki_zh="蟒科",
                            children=[
                                genus_species("蟒属", "Python", [("缅甸蟒", "Python bivittatus", "緬甸蟒")], wiki_zh_gen="蟒屬"),
                            ]),
                          N("壁虎科", "Gekkonidae", wiki_zh="壁虎科",
                            children=[
                                genus_species("壁虎属", "Gekko", [("大壁虎", "Gekko gecko", "大壁虎")], wiki_zh_gen="壁虎屬"),
                            ]),
                          N("鬣蜥科", "Iguanidae", wiki_zh="鬣蜥科",
                            children=[
                                genus_species("美洲鬣蜥属", "Iguana", [("绿鬣蜥", "Iguana iguana", "綠鬣蜥")], wiki_zh_gen="美洲鬣蜥屬"),
                            ]),
                          N("避役科", "Chamaeleonidae", wiki_zh="避役科", dist="体色可变；舌极长捕虫；多足对生抓握",
                            children=[
                                genus_species("避役属", "Chamaeleo", [("普通变色龙", "Chamaeleo chamaeleon", "普通變色龍")], wiki_zh_gen="避役屬"),
                            ]),
                      ]),
                    N("龟鳖目", "Testudines", wiki_zh="龜鱉目",
                      children=[
                          N("地龟科", "Geoemydidae", wiki_zh="地龜科", dist="陆栖和半水栖淡水龟",
                            children=[
                                genus_species("乌龟属", "Mauremys", [("中华草龟", "Mauremys reevesii", "中華草龜")], wiki_zh_gen="烏龜屬"),
                            ]),
                          N("鳖科", "Trionychidae", wiki_zh="鱉科", dist="背甲革质无角板；吻长管状",
                            children=[
                                genus_species("中华鳖属", "Pelodiscus", [("中华鳖", "Pelodiscus sinensis", "中華鱉")], wiki_zh_gen="中華鱉屬"),
                            ]),
                          N("海龟科", "Cheloniidae", wiki_zh="海龜科",
                            children=[
                                genus_species("海龟属", "Chelonia", [("绿海龟", "Chelonia mydas", "綠蠵龜")], wiki_zh_gen="海龜屬"),
                            ]),
                      ]),
                    N("鳄目", "Crocodilia", wiki_zh="鱷目",
                      children=[
                          N("鳄科", "Crocodylidae", wiki_zh="鱷科",
                            children=[
                                genus_species("鳄属", "Crocodylus", [
                                    ("尼罗鳄", "Crocodylus niloticus", "尼羅鱷"),
                                    ("湾鳄", "Crocodylus porosus", "灣鱷"),
                                ], wiki_zh_gen="鱷屬"),
                            ]),
                          N("短吻鳄科", "Alligatoridae", wiki_zh="短吻鱷科",
                            children=[
                                genus_species("鼍属", "Alligator", [
                                    ("扬子鳄", "Alligator sinensis", "揚子鱷"),
                                    ("密河鼉", "Alligator mississippiensis", "密河鱷"),
                                ], wiki_zh_gen="短吻鱷屬"),
                            ]),
                      ]),
                    N("喙头目", "Rhynchocephalia", wiki_zh="喙頭目", note="楔齿蜥"),
                ]),
              N("鸟纲", "Aves", wiki_zh="鳥",
                dist="恒温；羽毛、前肢变翼；气囊辅助肺呼吸；卵生有钙质蛋壳",
                children=[
                    N("雀形目", "Passeriformes", wiki_zh="雀形目", note="最大鸟类目；燕、麻雀、乌鸦",
                      dist="三前一后的鸣禽足(跗趾肌发达)；多具鸣管；小型多样",
                      children=[
                          N("雀科", "Passeridae",
                            children=[
                                genus_species("麻雀属", "Passer", [("麻雀", "Passer montanus", "麻雀")], wiki_zh_gen="麻雀屬")
                            ]),
                          N("燕科", "Hirundinidae", wiki_zh="燕科",
                            children=[
                                genus_species("燕属", "Hirundo", [("家燕", "Hirundo rustica", "家燕")], wiki_zh_gen="燕屬"),
                            ]),
                          N("鸦科", "Corvidae", wiki_zh="鴉科",
                            children=[
                                genus_species("鸦属", "Corvus", [
                                    ("大嘴乌鸦", "Corvus macrorhynchos", "大嘴烏鴉"),
                                    ("渡鸦", "Corvus corax", "渡鴉"),
                                ], wiki_zh_gen="鴉屬"),
                                genus_species("喜鹊属", "Pica", [("喜鹊", "Pica serica", "喜鵲")], wiki_zh_gen="鵲屬"),
                            ]),
                          N("山雀科", "Paridae", wiki_zh="山雀科", dist="小型活跃鸣禽；喙短圆；林间穿梭",
                            children=[
                                genus_species("山雀属", "Parus", [("大山雀", "Parus major", "大山雀")], wiki_zh_gen="山雀屬"),
                            ]),
                          N("椋鸟科", "Sturnidae", wiki_zh="椋鳥科", dist="中型群居；善学语；黑色或彩色",
                            children=[
                                genus_species("八哥属", "Acridotheres", [("八哥", "Acridotheres cristatellus", "八哥")], wiki_zh_gen="八哥屬"),
                            ]),
                          N("画眉科", "Timaliidae", wiki_zh="畫眉科", dist="多色彩不艳但鸣声婉转；树丛活动",
                            children=[
                                genus_species("噪鹛属", "Garrulax", [("画眉", "Garrulax canorus", "畫眉")], wiki_zh_gen="噪鶥屬"),
                            ]),
                          N("百灵科", "Alaudidae", wiki_zh="百靈科", dist="中小型草原鸣禽；后爪特长；飞行中鸣叫",
                            children=[
                                genus_species("云雀属", "Alauda", [("云雀", "Alauda arvensis", "雲雀")], wiki_zh_gen="雲雀屬"),
                            ]),
                          N("伯劳科", "Laniidae", wiki_zh="伯勞科", dist="小型肉食鸣禽；喙强具钩；把猎物串刺",
                            children=[
                                genus_species("伯劳属", "Lanius", [("红尾伯劳", "Lanius cristatus", "紅尾伯勞")], wiki_zh_gen="伯勞屬"),
                            ]),
                          N("鹎科", "Pycnonotidae", wiki_zh="鵯科", dist="常见园林鸟；冠羽有无不一；声音嘈杂",
                            children=[
                                genus_species("鹎属", "Pycnonotus", [("白头鹎", "Pycnonotus sinensis", "白頭鵯")], wiki_zh_gen="鵯屬"),
                            ]),
                      ]),
                    N("鸡形目", "Galliformes", wiki_zh="雞形目", note="鸡、雉",
                      dist="陆禽；喙短强善啄；脚健壮善走；翅短拙飞",
                      children=[
                          N("雉科", "Phasianidae", wiki_zh="雉科",
                            children=[
                                genus_species("原鸡属", "Gallus", [("家鸡", "Gallus gallus domesticus", "家雞")], wiki_zh_gen="原雞屬"),
                                genus_species("孔雀属", "Pavo", [("蓝孔雀", "Pavo cristatus", "藍孔雀")], wiki_zh_gen="孔雀屬"),
                                genus_species("锦鸡属", "Chrysolophus", [("红腹锦鸡", "Chrysolophus pictus", "紅腹錦雞")], wiki_zh_gen="錦雞屬"),
                                genus_species("鹌鹑属", "Coturnix", [("鹌鹑", "Coturnix japonica", "鵪鶉")], wiki_zh_gen="鵪鶉屬"),
                            ])
                      ]),
                    N("雁形目", "Anseriformes", wiki_zh="雁形目", note="鸭、鹅、天鹅",
                      dist="游禽；喙扁而宽有嘴甲；趾间蹼；尾脂腺发达",
                      children=[
                          N("鸭科", "Anatidae", wiki_zh="鴨科",
                            children=[
                                genus_species("鸭属", "Anas", [
                                    ("家鸭", "Anas platyrhynchos domesticus", "家鴨"),
                                    ("绿头鸭", "Anas platyrhynchos", "綠頭鴨"),
                                ], wiki_zh_gen="鴨屬"),
                                genus_species("雁属", "Anser", [
                                    ("家鹅", "Anser anser domesticus", "家鵝"),
                                    ("鸿雁", "Anser cygnoid", "鴻雁"),
                                ], wiki_zh_gen="雁屬"),
                                genus_species("鸳鸯属", "Aix", [("鸳鸯", "Aix galericulata", "鴛鴦")], wiki_zh_gen="鴛鴦屬"),
                                genus_species("天鹅属", "Cygnus", [("大天鹅", "Cygnus cygnus", "大天鵝")], wiki_zh_gen="天鵝屬"),
                            ])
                      ]),
                    N("鸽形目", "Columbiformes", wiki_zh="鴿形目",
                      children=[
                          N("鸠鸽科", "Columbidae", wiki_zh="鳩鴿科",
                            children=[
                                genus_species("鸽属", "Columba", [("原鸽", "Columba livia", "原鴿")], wiki_zh_gen="鴿屬")
                            ])
                      ]),
                    N("鹦形目", "Psittaciformes", wiki_zh="鸚形目", note="鹦鹉",
                      dist="喙短钩状；对趾足(2前2后)；仿声学舌"),
                    N("鸮形目", "Strigiformes", wiki_zh="鴞形目", note="猫头鹰",
                      dist="夜行猛禽；双眼前置；面盘；爪锐羽静音",
                      children=[
                          N("鸱鸮科", "Strigidae", wiki_zh="鴟鴞科", dist="典型猫头鹰；头大无外耳",
                            children=[
                                genus_species("雕鸮属", "Bubo", [("雕鸮", "Bubo bubo", "鵰鴞")], wiki_zh_gen="雕鴞屬"),
                                genus_species("林鸮属", "Strix", [("长尾林鸮", "Strix uralensis", "長尾林鴞")], wiki_zh_gen="林鴞屬"),
                            ])
                      ]),
                    N("隼形目", "Falconiformes", wiki_zh="隼形目",
                      dist="日行小型猛禽；翅尖长善高速俯冲；上喙有齿突",
                      children=[
                          N("隼科", "Falconidae", wiki_zh="隼科", dist="翅尖长；俯冲猎鸟；喙具齿突",
                            children=[
                                genus_species("隼属", "Falco", [
                                    ("游隼", "Falco peregrinus", "遊隼"),
                                    ("红隼", "Falco tinnunculus", "紅隼"),
                                ], wiki_zh_gen="隼屬"),
                            ])
                      ]),
                    N("鹰形目", "Accipitriformes", wiki_zh="鷹形目", note="鹰、雕、鹫",
                      dist="日行大型猛禽；翅宽长善翱翔；爪强猛喙钩",
                      children=[
                          N("鹰科", "Accipitridae", wiki_zh="鷹科", dist="翅宽大善翱翔；视觉极锐；鹰、雕、鹫",
                            children=[
                                genus_species("雕属", "Aquila", [("金雕", "Aquila chrysaetos", "金鵰")], wiki_zh_gen="雕屬"),
                                genus_species("鹰属", "Accipiter", [("苍鹰", "Accipiter gentilis", "蒼鷹")], wiki_zh_gen="鷹屬"),
                            ])
                      ]),
                    N("啄木鸟目", "Piciformes", wiki_zh="鴷形目",
                      dist="对趾足；喙凿形；舌长具倒刺；凿木觅食"),
                    N("企鹅目", "Sphenisciformes", wiki_zh="企鵝目",
                      dist="不能飞；翅鳍状善潜水；直立行走；仅南半球分布",
                      children=[
                          N("企鹅科", "Spheniscidae", wiki_zh="企鵝科",
                            children=[
                                genus_species("帝企鹅属", "Aptenodytes", [("帝企鹅", "Aptenodytes forsteri", "帝企鵝")], wiki_zh_gen="帝企鵝屬"),
                                genus_species("阿德利企鹅属", "Pygoscelis", [("阿德利企鹅", "Pygoscelis adeliae", "阿德利企鵝")], wiki_zh_gen="阿德利企鵝屬"),
                            ])
                      ]),
                    N("鹳形目", "Ciconiiformes", wiki_zh="鸛形目"),
                    N("鸻形目", "Charadriiformes", wiki_zh="鴴形目", note="鸥、鹬、燕鸻",
                      dist="多水边或海鸟；喙细长；多迁徙；含鸥、燕鸥、千鸟",
                      children=[
                          N("鸥科", "Laridae", wiki_zh="鷗科", dist="翅长尖；多群居海岸；黑白灰为主"),
                          N("鹬科", "Scolopacidae", wiki_zh="鷸科", dist="喙细长探泥滩；腿长"),
                      ]),
                    N("鹤形目", "Gruiformes", wiki_zh="鶴形目", note="鹤、秧鸡",
                      dist="多为涉禽或湿地鸟；颈长腿长；发声响亮；鹤、秧鸡",
                      children=[
                          N("鹤科", "Gruidae", wiki_zh="鶴科", dist="大型涉禽；颈直长；迁徙结群",
                            children=[
                                genus_species("鹤属", "Grus", [
                                    ("丹顶鹤", "Grus japonensis", "丹頂鶴"),
                                    ("灰鹤", "Grus grus", "灰鶴"),
                                ], wiki_zh_gen="鶴屬"),
                            ]),
                      ]),
                    N("鹈形目", "Pelecaniformes", wiki_zh="鵜形目", note="鹈鹕、鹭、朱鹮",
                      dist="多具喉囊或长颈大型水鸟；食鱼；鹭科亦归此",
                      children=[
                          N("鹭科", "Ardeidae", wiki_zh="鷺科", dist="涉禽；颈长S形，飞行颈缩",
                            children=[
                                genus_species("白鹭属", "Egretta", [("白鹭", "Egretta garzetta", "白鷺")], wiki_zh_gen="白鷺屬"),
                                genus_species("苍鹭属", "Ardea", [("苍鹭", "Ardea cinerea", "蒼鷺")], wiki_zh_gen="蒼鷺屬"),
                            ]),
                          N("鹈鹕科", "Pelecanidae", wiki_zh="鵜鶘科", dist="大型水鸟；下颌具大喉囊兜鱼",
                            children=[
                                genus_species("鹈鹕属", "Pelecanus", [("斑嘴鹈鹕", "Pelecanus philippensis", "斑嘴鵜鶘")], wiki_zh_gen="鵜鶘屬"),
                            ]),
                      ]),
                    N("鸵鸟目", "Struthioniformes", wiki_zh="鴕鳥目",
                      dist="不能飞；腿长善跑；无龙骨突；鸵鸟(现存最大鸟类)",
                      children=[
                          N("鸵鸟科", "Struthionidae", wiki_zh="鴕鳥科",
                            children=[
                                N("鸵鸟属", "Struthio", wiki_zh="鴕鳥屬",
                                  children=[N("非洲鸵鸟", "Struthio camelus", wiki_zh="鴕鳥")])
                            ])
                      ]),
                    N("雨燕目", "Apodiformes", wiki_zh="雨燕目", note="雨燕、蜂鸟",
                      dist="翅长窄善高速飞行；腿极短不善行走；飞行摄食",
                      children=[
                          N("雨燕科", "Apodidae", wiki_zh="雨燕科", dist="形似燕但更紧凑；全天飞行"),
                          N("蜂鸟科", "Trochilidae", wiki_zh="蜂鳥科", dist="极小；翅频扇动悬停；舌细长吸食花蜜"),
                      ]),
                    N("佛法僧目", "Coraciiformes", wiki_zh="佛法僧目", note="翠鸟、蜂虎",
                      dist="多色彩艳丽树栖鸟；喙长直；含翠鸟、蜂虎、犀鸟(部分)",
                      children=[
                          N("翠鸟科", "Alcedinidae", wiki_zh="翠鳥科", dist="头大喙长直；捕鱼；翠绿蓝色",
                            children=[
                                genus_species("翠鸟属", "Alcedo", [("普通翠鸟", "Alcedo atthis", "普通翠鳥")], wiki_zh_gen="翠鳥屬"),
                            ]),
                      ]),
                    N("鹃形目", "Cuculiformes", wiki_zh="鵑形目", note="杜鹃",
                      dist="对趾足；多种营巢寄生；尾长；杜鹃、大杜鹃"),
                    N("夜鹰目", "Caprimulgiformes", wiki_zh="夜鷹目",
                      dist="夜行昆虫食鸟；嘴短宽口裂大；羽色隐蔽"),
                    N("潜鸟目", "Gaviiformes", wiki_zh="潛鳥目",
                      dist="水生；擅潜水；尖喙；腿靠后走路笨拙"),
                    N("鸊鷉目", "Podicipediformes", wiki_zh="鸊鷉目", note="䴙䴘",
                      dist="水生；潜水觅食；趾具瓣蹼；冬羽夏羽差异大"),
                ]),
              N("哺乳纲", "Mammalia", wiki_zh="哺乳動物",
                dist="恒温；体表毛发；胎生哺乳(单孔目除外)；有膈；红细胞无核",
                children=[
                    N("灵长目", "Primates", wiki_zh="靈長目",
                      dist="脑发达；对生拇指(可抓握)；双眼前置具立体视；多树栖",
                      children=[
                          N("人科", "Hominidae", wiki_zh="人科",
                            dist="大型类人猿：无尾，肩关节灵活，脑容量大；含人/黑猩猩/大猩猩/红毛猩猩",
                            children=[
                                N("人属", "Homo", wiki_zh="人屬",
                                  dist="直立行走，颅骨高大，现仅存智人",
                                  children=[N("智人", "Homo sapiens", wiki_zh="智人")]),
                                N("黑猩猩属", "Pan", wiki_zh="黑猩猩屬",
                                  dist="与人亲缘最近；指关节行走，高度社会性",
                                  children=[N("黑猩猩", "Pan troglodytes", wiki_zh="黑猩猩")]),
                                N("大猩猩属", "Gorilla", wiki_zh="大猩猩屬",
                                  dist="体型最大的灵长类；素食，地栖为主",
                                  children=[N("西部大猩猩", "Gorilla gorilla", wiki_zh="西部大猩猩")]),
                                N("猩猩属", "Pongo", wiki_zh="猩猩屬",
                                  dist="亚洲类人猿；树栖，长毛红棕色"),
                            ]),
                          N("长臂猿科", "Hylobatidae", wiki_zh="長臂猿科",
                            dist="小型类人猿；臂特长，树上臂行(Brachiation)，无尾",
                            children=[
                                genus_species("长臂猿属", "Hylobates", [("白掌长臂猿", "Hylobates lar", "白掌長臂猿")], wiki_zh_gen="長臂猿屬"),
                            ]),
                          N("猴科", "Cercopithecidae", wiki_zh="猴科",
                            dist="旧大陆猴；有尾(不能缠绕)，颊囊、坐骨胼胝；猕猴、狒狒归此",
                            children=[
                                genus_species("猕猴属", "Macaca", [
                                    ("猕猴", "Macaca mulatta", "獼猴"),
                                    ("日本猕猴", "Macaca fuscata", "日本獼猴"),
                                ], wiki_zh_gen="獼猴屬"),
                                genus_species("金丝猴属", "Rhinopithecus", [("川金丝猴", "Rhinopithecus roxellana", "川金絲猴")], wiki_zh_gen="仰鼻猴屬"),
                                genus_species("狒狒属", "Papio", [("狒狒", "Papio hamadryas", "狒狒")], wiki_zh_gen="狒狒屬"),
                            ]),
                      ]),
                    N("食肉目", "Carnivora", wiki_zh="食肉目",
                      dist="肉食为主；犬齿发达、有裂齿；趾行/跖行；爪锐利",
                      children=[
                          N("犬科", "Canidae", wiki_zh="犬科",
                            dist="趾行；爪不可缩；嗅觉发达；多为群居奔袭猎食",
                            children=[
                                N("犬属", "Canis", wiki_zh="犬屬",
                                  children=[
                                      N("家犬", "Canis lupus familiaris", wiki_zh="狗", wiki_en="Dog"),
                                      N("灰狼", "Canis lupus", wiki_zh="狼"),
                                      N("郊狼", "Canis latrans", wiki_zh="郊狼"),
                                  ]),
                                N("狐属", "Vulpes", wiki_zh="狐屬",
                                  children=[N("赤狐", "Vulpes vulpes", wiki_zh="赤狐")]),
                            ]),
                          N("猫科", "Felidae", wiki_zh="貓科",
                            dist="趾行；爪可缩入；视觉锐利；多独居伏击猎食",
                            children=[
                                N("猫属", "Felis", wiki_zh="貓屬",
                                  children=[
                                      N("家猫", "Felis catus", wiki_zh="貓", wiki_en="Cat"),
                                      N("野猫", "Felis silvestris", wiki_zh="野貓"),
                                  ]),
                                N("豹属", "Panthera", wiki_zh="豹屬",
                                  children=[
                                      N("虎", "Panthera tigris", wiki_zh="虎"),
                                      N("狮", "Panthera leo", wiki_zh="獅"),
                                      N("豹", "Panthera pardus", wiki_zh="豹"),
                                      N("美洲豹", "Panthera onca", wiki_zh="美洲豹"),
                                      N("雪豹", "Panthera uncia", wiki_zh="雪豹"),
                                  ]),
                                genus_species("猞猁属", "Lynx", [("欧亚猞猁", "Lynx lynx", "猞猁")], wiki_zh_gen="猞猁屬"),
                                genus_species("云豹属", "Neofelis", [("云豹", "Neofelis nebulosa", "雲豹")], wiki_zh_gen="雲豹屬"),
                                genus_species("猎豹属", "Acinonyx", [("猎豹", "Acinonyx jubatus", "獵豹")], wiki_zh_gen="獵豹屬"),
                            ]),
                          N("熊科", "Ursidae", wiki_zh="熊科",
                            dist="跖行(脚掌着地)；大体型杂食；爪不可缩；无裂齿特化",
                            children=[
                                N("大熊猫属", "Ailuropoda", wiki_zh="大熊貓屬",
                                  children=[N("大熊猫", "Ailuropoda melanoleuca", wiki_zh="大熊貓")]),
                                N("熊属", "Ursus", wiki_zh="熊屬",
                                  children=[
                                      N("棕熊", "Ursus arctos", wiki_zh="棕熊"),
                                      N("北极熊", "Ursus maritimus", wiki_zh="北極熊"),
                                      N("亚洲黑熊", "Ursus thibetanus", wiki_zh="亞洲黑熊"),
                                      N("美洲黑熊", "Ursus americanus", wiki_zh="美洲黑熊"),
                                  ]),
                                genus_species("马来熊属", "Helarctos", [("马来熊", "Helarctos malayanus", "馬來熊")], wiki_zh_gen="馬來熊屬"),
                            ]),
                          N("鼬科", "Mustelidae", wiki_zh="鼬科", note="黄鼠狼、水獭、獾",
                            dist="身长、腿短；有臭腺；食肉目中种类最多",
                            children=[
                                genus_species("水獭属", "Lutra", [("欧亚水獭", "Lutra lutra", "歐亞水獺")], wiki_zh_gen="水獺屬"),
                                genus_species("鼬属", "Mustela", [("黄鼬", "Mustela sibirica", "黃鼬")], wiki_zh_gen="鼬屬"),
                                genus_species("獾属", "Meles", [("狗獾", "Meles leucurus", "狗獾")], wiki_zh_gen="獾屬"),
                            ]),
                          N("浣熊科", "Procyonidae", wiki_zh="浣熊科",
                            dist="面部黑色眼斑；尾有环纹；杂食性",
                            children=[
                                genus_species("浣熊属", "Procyon", [("浣熊", "Procyon lotor", "浣熊")], wiki_zh_gen="浣熊屬"),
                            ]),
                          N("海豹科", "Phocidae", wiki_zh="海豹科",
                            dist="鳍足；无外耳廓；陆上只能蠕动；深潜能力强",
                            children=[
                                genus_species("海豹属", "Phoca", [("斑海豹", "Phoca largha", "斑海豹")], wiki_zh_gen="海豹屬"),
                            ]),
                      ]),
                    N("啮齿目", "Rodentia", wiki_zh="齧齒目", note="哺乳纲最大目",
                      dist="上下各一对门齿终生生长；无犬齿；植食/杂食；数量最多",
                      children=[
                          N("鼠科", "Muridae", wiki_zh="鼠科",
                            children=[
                                N("大鼠属", "Rattus", wiki_zh="大鼠屬",
                                  children=[N("褐家鼠", "Rattus norvegicus", wiki_zh="褐家鼠")]),
                                N("小鼠属", "Mus", wiki_zh="小鼠屬",
                                  children=[N("小家鼠", "Mus musculus", wiki_zh="小家鼠")]),
                            ]),
                          N("松鼠科", "Sciuridae", wiki_zh="松鼠科",
                            children=[
                                genus_species("松鼠属", "Sciurus", [
                                    ("红松鼠", "Sciurus vulgaris", "紅松鼠"),
                                ], wiki_zh_gen="松鼠屬"),
                                genus_species("花鼠属", "Tamias", [("东北花鼠", "Tamias sibiricus", "花鼠")], wiki_zh_gen="花鼠屬"),
                                genus_species("旱獭属", "Marmota", [("喜马拉雅旱獭", "Marmota himalayana", "喜馬拉雅旱獺")], wiki_zh_gen="旱獺屬"),
                            ]),
                          N("仓鼠科", "Cricetidae", wiki_zh="倉鼠科",
                            children=[
                                genus_species("仓鼠属", "Cricetulus", [("中华仓鼠", "Cricetulus griseus", "中華倉鼠")], wiki_zh_gen="倉鼠屬"),
                                genus_species("田鼠属", "Microtus", [("东方田鼠", "Microtus fortis", "東方田鼠")], wiki_zh_gen="田鼠屬"),
                            ]),
                          N("豪猪科", "Hystricidae", wiki_zh="豪豬科",
                            children=[
                                genus_species("豪猪属", "Hystrix", [("中国豪猪", "Hystrix hodgsoni", "中國豪豬")], wiki_zh_gen="豪豬屬"),
                            ]),
                          N("河狸科", "Castoridae", wiki_zh="河狸科", dist="半水生；尾扁阔鳞状；能筑水坝",
                            children=[
                                genus_species("河狸属", "Castor", [("欧亚河狸", "Castor fiber", "歐亞河狸")], wiki_zh_gen="河狸屬"),
                            ]),
                          N("豚鼠科", "Caviidae", wiki_zh="豚鼠科",
                            children=[
                                genus_species("豚鼠属", "Cavia", [("豚鼠", "Cavia porcellus", "豚鼠")], wiki_zh_gen="豚鼠屬"),
                                genus_species("水豚属", "Hydrochoerus", [("水豚", "Hydrochoerus hydrochaeris", "水豚")], wiki_zh_gen="水豚屬"),
                            ]),
                      ]),
                    N("偶蹄目", "Artiodactyla", wiki_zh="偶蹄目", note="牛、猪、羊、鹿、骆驼",
                      dist="每足偶数趾(2或4)着地；多反刍；植食",
                      children=[
                          N("牛科", "Bovidae", wiki_zh="牛科",
                            children=[
                                N("牛属", "Bos", wiki_zh="牛屬",
                                  children=[
                                      N("普通牛", "Bos taurus", wiki_zh="黃牛"),
                                      N("瘤牛", "Bos indicus", wiki_zh="瘤牛"),
                                      N("牦牛", "Bos grunniens", wiki_zh="犛牛"),
                                  ]),
                                N("水牛属", "Bubalus", wiki_zh="水牛屬",
                                  children=[N("水牛", "Bubalus bubalis", wiki_zh="水牛")]),
                                N("绵羊属", "Ovis", wiki_zh="綿羊屬",
                                  children=[N("绵羊", "Ovis aries", wiki_zh="家綿羊")]),
                                N("山羊属", "Capra", wiki_zh="山羊屬",
                                  children=[N("山羊", "Capra hircus", wiki_zh="家山羊")]),
                                genus_species("羚牛属", "Budorcas", [("秦岭羚牛", "Budorcas bedfordi", None)], wiki_zh_gen="羚牛屬"),
                                genus_species("角马属", "Connochaetes", [("角马", "Connochaetes taurinus", "斑紋角馬")], wiki_zh_gen="角馬屬"),
                            ]),
                          N("猪科", "Suidae", wiki_zh="豬科",
                            children=[
                                N("猪属", "Sus", wiki_zh="豬屬",
                                  children=[
                                      N("家猪", "Sus scrofa domesticus", wiki_zh="家豬"),
                                      N("野猪", "Sus scrofa", wiki_zh="野豬"),
                                  ]),
                            ]),
                          N("鹿科", "Cervidae", wiki_zh="鹿科", note="梅花鹿、驼鹿",
                            children=[
                                genus_species("鹿属", "Cervus", [
                                    ("梅花鹿", "Cervus nippon", "梅花鹿"),
                                    ("马鹿", "Cervus elaphus", "馬鹿"),
                                ], wiki_zh_gen="鹿屬"),
                                genus_species("驼鹿属", "Alces", [("驼鹿", "Alces alces", "駝鹿")], wiki_zh_gen="駝鹿屬"),
                                genus_species("驯鹿属", "Rangifer", [("驯鹿", "Rangifer tarandus", "馴鹿")], wiki_zh_gen="馴鹿屬"),
                            ]),
                          N("骆驼科", "Camelidae", wiki_zh="駱駝科",
                            children=[
                                genus_species("骆驼属", "Camelus", [
                                    ("双峰驼", "Camelus bactrianus", "雙峰駱駝"),
                                    ("单峰驼", "Camelus dromedarius", "單峰駱駝"),
                                ], wiki_zh_gen="駱駝屬"),
                                genus_species("羊驼属", "Vicugna", [("羊驼", "Vicugna pacos", "羊駝")], wiki_zh_gen="羊駝屬"),
                            ]),
                          N("长颈鹿科", "Giraffidae", wiki_zh="長頸鹿科",
                            children=[
                                genus_species("长颈鹿属", "Giraffa", [("长颈鹿", "Giraffa camelopardalis", "長頸鹿")], wiki_zh_gen="長頸鹿屬"),
                            ]),
                      ]),
                    N("鲸目", "Cetacea", wiki_zh="鯨", note="鲸、海豚(现合并入鲸偶蹄目)",
                      dist="完全水生；前肢鳍状、后肢退化；尾平行水平；哺乳",
                      children=[
                          N("须鲸科", "Balaenopteridae",
                            children=[
                                genus_species("须鲸属", "Balaenoptera", [
                                    ("蓝鲸", "Balaenoptera musculus", "藍鯨"),
                                    ("长须鲸", "Balaenoptera physalus", "長鬚鯨"),
                                ], wiki_zh_gen="鬚鯨屬"),
                                genus_species("座头鲸属", "Megaptera", [("座头鲸", "Megaptera novaeangliae", "座頭鯨")], wiki_zh_gen="座頭鯨屬"),
                            ]),
                          N("抹香鲸科", "Physeteridae", wiki_zh="抹香鯨科", dist="头巨大占体长三分之一；单鼻孔偏左；深潜能手",
                            children=[
                                genus_species("抹香鲸属", "Physeter", [("抹香鲸", "Physeter macrocephalus", "抹香鯨")], wiki_zh_gen="抹香鯨屬"),
                            ]),
                          N("一角鲸科", "Monodontidae", wiki_zh="一角鯨科", dist="北极海域；无背鳍；含一角鲸和白鲸",
                            children=[
                                genus_species("一角鲸属", "Monodon", [("一角鲸", "Monodon monoceros", "一角鯨")], wiki_zh_gen="獨角鯨屬"),
                                genus_species("白鲸属", "Delphinapterus", [("白鲸", "Delphinapterus leucas", "白鯨")], wiki_zh_gen="白鯨屬"),
                            ]),
                          N("海豚科", "Delphinidae", wiki_zh="海豚科",
                            children=[
                                genus_species("瓶鼻海豚属", "Tursiops", [("宽吻海豚", "Tursiops truncatus", "寬吻海豚")], wiki_zh_gen="瓶鼻海豚屬"),
                                genus_species("虎鲸属", "Orcinus", [("虎鲸", "Orcinus orca", "虎鯨")], wiki_zh_gen="虎鯨屬"),
                            ]),
                      ]),
                    N("奇蹄目", "Perissodactyla", wiki_zh="奇蹄目", note="马、犀、貘",
                      dist="每足奇数趾(1或3)着地；不反刍；植食",
                      children=[
                          N("马科", "Equidae", wiki_zh="馬科",
                            children=[
                                genus_species("马属", "Equus", [
                                    ("家马", "Equus ferus caballus", "馬"),
                                    ("驴", "Equus africanus asinus", "驢"),
                                    ("斑马", "Equus zebra", None),
                                ], wiki_zh_gen="馬屬")
                            ]),
                          N("犀科", "Rhinocerotidae", wiki_zh="犀科",
                            children=[
                                genus_species("犀属", "Rhinoceros", [("印度犀", "Rhinoceros unicornis", "印度犀")], wiki_zh_gen="犀屬"),
                            ]),
                      ]),
                    N("长鼻目", "Proboscidea", wiki_zh="長鼻目",
                      dist="象鼻(上唇和鼻融合)；门齿特化为象牙；巨型植食",
                      children=[
                          N("象科", "Elephantidae", wiki_zh="象科",
                            children=[
                                genus_species("非洲象属", "Loxodonta", [("非洲草原象", "Loxodonta africana", "非洲草原象")], wiki_zh_gen="非洲象屬"),
                                genus_species("亚洲象属", "Elephas", [("亚洲象", "Elephas maximus", "亞洲象")], wiki_zh_gen="亞洲象屬"),
                            ])
                      ]),
                    N("翼手目", "Chiroptera", wiki_zh="翼手目", note="蝙蝠",
                      dist="前肢延长+翼膜；唯一能真正飞行的哺乳动物；多夜行回声定位",
                      children=[
                          N("狐蝠科", "Pteropodidae", wiki_zh="狐蝠科", dist="大型果食；不用回声定位",
                            children=[
                                genus_species("狐蝠属", "Pteropus", [("马来大狐蝠", "Pteropus vampyrus", "馬來大狐蝠")], wiki_zh_gen="狐蝠屬"),
                            ]),
                          N("蝙蝠科", "Vespertilionidae", wiki_zh="蝙蝠科", dist="小型食虫；超声波回声定位",
                            children=[
                                genus_species("鼠耳蝠属", "Myotis", [("大鼠耳蝠", "Myotis myotis", "大鼠耳蝠")], wiki_zh_gen="鼠耳蝠屬"),
                            ]),
                      ]),
                    N("食虫目", "Eulipotyphla", wiki_zh="真盲缺目", note="刺猬、鼩鼱、鼹鼠",
                      dist="吻尖长；小型夜行；食虫；原始哺乳形态",
                      children=[
                          N("猬科", "Erinaceidae", wiki_zh="蝟科", dist="背密生角质棘刺；遇险卷球",
                            children=[
                                genus_species("猬属", "Erinaceus", [("东北刺猬", "Erinaceus amurensis", "東北刺蝟")], wiki_zh_gen="刺蝟屬"),
                            ]),
                      ]),
                    N("兔形目", "Lagomorpha", wiki_zh="兔形目",
                      dist="上颌4门齿(后小前大)；植食；粪便二次食用",
                      children=[
                          N("兔科", "Leporidae", wiki_zh="兔科",
                            children=[
                                genus_species("穴兔属", "Oryctolagus", [("家兔", "Oryctolagus cuniculus", "家兔")], wiki_zh_gen="穴兔屬")
                            ])
                      ]),
                    N("海牛目", "Sirenia", wiki_zh="海牛目", note="儒艮、海牛",
                      dist="水生植食；体型笨重；前肢鳍状"),
                    N("袋鼠目", "Diprotodontia", wiki_zh="雙門齒目", note="袋鼠、考拉",
                      dist="有袋；下颌2门齿；后足2/3趾并合",
                      children=[
                          N("袋鼠科", "Macropodidae", wiki_zh="袋鼠科", dist="后肢特长善跳跃；长尾平衡；澳洲特有",
                            children=[
                                genus_species("大袋鼠属", "Macropus", [("红袋鼠", "Macropus rufus", "紅袋鼠")], wiki_zh_gen="大袋鼠屬"),
                            ]),
                          N("树袋熊科", "Phascolarctidae", wiki_zh="無尾熊科", dist="仅考拉一属；树栖食桉叶",
                            children=[
                                genus_species("树袋熊属", "Phascolarctos", [("树袋熊", "Phascolarctos cinereus", "無尾熊")], wiki_zh_gen="無尾熊屬"),
                            ]),
                      ]),
                    N("树鼩目", "Scandentia", wiki_zh="樹鼩目", note="树鼩",
                      dist="小型树栖；似松鼠但属真盲缺近亲；东南亚分布"),
                    N("鳞甲目", "Pholidota", wiki_zh="鱗甲目", note="穿山甲",
                      dist="体被角质鳞片；长吻无牙；舌长黏；食蚁",
                      children=[
                          N("鲮鲤科", "Manidae", wiki_zh="穿山甲科",
                            children=[
                                genus_species("穿山甲属", "Manis", [("中华穿山甲", "Manis pentadactyla", "中華穿山甲")], wiki_zh_gen="穿山甲屬"),
                            ])
                      ]),
                    N("管齿目", "Tubulidentata", wiki_zh="管齒目", note="土豚",
                      dist="牙小无珐琅质(管状结构)；长耳长吻；非洲分布；食白蚁"),
                    N("蹄兔目", "Hyracoidea", wiki_zh="蹄兔目",
                      dist="体型似啮齿但与象亲缘；非洲中东；岩居或林栖"),
                    N("象鼩目", "Macroscelidea", wiki_zh="象鼩目",
                      dist="小型；吻细长灵活如小象鼻；善跳；非洲分布"),
                    N("有袋总目", "Marsupialia", wiki_zh="有袋類", note="袋类动物统称",
                      dist="胎盘不发达；幼体在母体育儿袋中完成发育"),
                    N("单孔目", "Monotremata", wiki_zh="單孔目", note="鸭嘴兽、针鼹",
                      dist="产卵的哺乳动物；泄殖腔(单孔)；无乳头，汗状泌乳",
                      children=[
                          N("鸭嘴兽科", "Ornithorhynchidae", wiki_zh="鴨嘴獸科",
                            children=[
                                genus_species("鸭嘴兽属", "Ornithorhynchus", [("鸭嘴兽", "Ornithorhynchus anatinus", "鴨嘴獸")], wiki_zh_gen="鴨嘴獸屬"),
                            ]),
                          N("针鼹科", "Tachyglossidae", wiki_zh="針鼴科",
                            children=[
                                genus_species("针鼹属", "Tachyglossus", [("短吻针鼹", "Tachyglossus aculeatus", "短吻針鼴")], wiki_zh_gen="針鼴屬"),
                            ]),
                      ]),
                    N("贫齿总目", "Xenarthra", wiki_zh="貧齒總目", note="食蚁兽、树懒、犰狳",
                      dist="牙齿退化/缺失；脊椎附加关节；多分布美洲"),
                ]),
          ]),
    ]
)

# ============================================================
root = N("生物", "Life", wiki_zh="生物", wiki_en="Life",
         children=[kingdom_monera, kingdom_protista, kingdom_fungi, kingdom_plantae, kingdom_animalia])


# ============================================================
# Stats & output
# ============================================================
def walk(n, d=0, counts=None):
    if counts is None:
        counts = {}
    counts[d] = counts.get(d, 0) + 1
    for c in n.get("children", []):
        walk(c, d+1, counts)
    return counts


def merge_distinctions(node, mapping):
    """Fill node.distinction from mapping[latin] if not already set."""
    latin = node.get("latin")
    if latin and "distinction" not in node and latin in mapping:
        node["distinction"] = mapping[latin]
    for c in node.get("children", []):
        merge_distinctions(c, mapping)


if __name__ == "__main__":
    dist_path = Path(__file__).parent / "distinctions.json"
    if dist_path.exists():
        mapping = json.loads(dist_path.read_text(encoding="utf-8"))
        merge_distinctions(root, mapping)
        print(f"Merged {len(mapping)} distinctions from {dist_path.name}")
    out = Path(__file__).parent.parent / "data" / "taxa.json"
    out.write_text(json.dumps(root, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = walk(root)
    ranks = ["生物(根)", "界", "门", "纲", "目", "科", "属", "种"]
    total = sum(counts.values())
    print(f"Wrote {out} ({total} nodes)")
    for i, r in enumerate(ranks):
        print(f"  {r}: {counts.get(i, 0)}")
