/* Kurze Texte zum Lesen mit Verständnisfragen. Nur Wörter aus dem Lernpfad (plus Namen).
   Erzeugt mit scripts/build_texts.js aus scripts/texts_src.js. lesson: ab dieser Lektion lesbar. */
window.ZH_TEXTS = [
  {id:"t01", kind:"Nachricht", title:"Eine Nachricht von Li Na", lesson:4, from:{zh:"李娜", de:"Li Na"}, lines:[
    {zh:"你好，弗洛里安！", py:"Nǐ_hǎo, Fú_luò_lǐ_'ān!", de:"Hallo, Florian!"},
    {zh:"我是李娜，我是中国人。", py:"Wǒ shì Lǐ_Nà, wǒ shì Zhōng_guó rén.", de:"Ich bin Li Na, ich bin Chinesin."},
    {zh:"你是哪国人？你是德国人吗？", py:"Nǐ shì nǎ guó rén? Nǐ shì Dé_guó rén ma?", de:"Aus welchem Land kommst du? Bist du Deutscher?"},
    {zh:"他叫小明。他很好。", py:"Tā jiào Xiǎo_Míng. Tā hěn hǎo.", de:"Er heißt Xiao Ming. Er ist sehr nett."},
    {zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"}],
   qs:[
    {q:"Wer schreibt dir?", opts:["Li Na","Xiao Ming","Anna"], a:0, l:1},
    {q:"Woher kommt Li Na?", opts:["Aus China","Aus Deutschland","Das steht nicht da"], a:0, l:1},
    {q:"Was will sie von dir wissen?", opts:["Aus welchem Land du kommst","Wie du heißt","Ob du Tee trinkst"], a:0, l:2}]},
  {id:"t02", kind:"Nachricht", title:"Xiao Ming lädt zum Tee", lesson:8, from:{zh:"小明", de:"Xiao Ming"}, lines:[
    {zh:"你好！你喝茶吗？", py:"Nǐ_hǎo! Nǐ hē chá ma?", de:"Hallo! Trinkst du Tee?"},
    {zh:"我很喜欢喝茶，我不喝咖啡。", py:"Wǒ hěn xǐ_huan hē chá, wǒ bù hē kā_fēi.", de:"Ich trinke sehr gern Tee, Kaffee trinke ich nicht."},
    {zh:"你要吃什么？米饭很好吃。", py:"Nǐ yào chī shén_me? Mǐ_fàn hěn hǎo_chī.", de:"Was möchtest du essen? Der Reis ist sehr lecker."},
    {zh:"你喜欢吃菜吗？", py:"Nǐ xǐ_huan chī cài ma?", de:"Magst du Gemüse?"}],
   qs:[
    {q:"Was trinkt Xiao Ming gern?", opts:["Tee","Kaffee","Wasser"], a:0, l:1},
    {q:"Was trinkt er nicht?", opts:["Kaffee","Tee","Wasser"], a:0, l:1},
    {q:"Was findet er lecker?", opts:["Den Reis","Das Gemüse","Den Tee"], a:0, l:2}]},
  {id:"t03", kind:"Speisekarte", title:"Die Karte am Teestand", lesson:10, from:{zh:"茶", de:"Teestand auf dem Markt"}, lines:[
    {zh:"茶 五块", py:"Chá wǔ kuài", de:"Tee, 5 Kuai"},
    {zh:"咖啡 二十块", py:"Kā_fēi èr shí kuài", de:"Kaffee, 20 Kuai"},
    {zh:"水 三块", py:"Shuǐ sān kuài", de:"Wasser, 3 Kuai"},
    {zh:"米饭 四块", py:"Mǐ_fàn sì kuài", de:"Reis, 4 Kuai"},
    {zh:"菜 十块", py:"Cài shí kuài", de:"Gemüsegericht, 10 Kuai"},
    {zh:"没有米饭了！", py:"Méi_yǒu mǐ_fàn le!", de:"Es gibt keinen Reis mehr!"}],
   qs:[
    {q:"Was kostet der Kaffee?", opts:["20 Kuai","12 Kuai","2 Kuai"], a:0, l:1},
    {q:"Was ist am billigsten?", opts:["Wasser","Tee","Reis"], a:0, l:2},
    {q:"Was gibt es nicht mehr?", opts:["Reis","Tee","Gemüse"], a:0, l:5}]},
  {id:"t04", kind:"Nachricht", title:"Wo bist du?", lesson:12, from:{zh:"李娜", de:"Li Na"}, lines:[
    {zh:"弗洛里安，你在哪里？", py:"Fú_luò_lǐ_'ān, nǐ zài nǎ_lǐ?", de:"Florian, wo bist du?"},
    {zh:"我在火车站。", py:"Wǒ zài huǒ_chē_zhàn.", de:"Ich bin am Bahnhof."},
    {zh:"你想去酒店吗？酒店在那里。", py:"Nǐ xiǎng qù jiǔ_diàn ma? Jiǔ_diàn zài nà_lǐ.", de:"Willst du zum Hotel? Das Hotel ist dort."},
    {zh:"厕所在这里。", py:"Cè_suǒ zài zhè_lǐ.", de:"Die Toilette ist hier."},
    {zh:"你要喝水吗？我有水。", py:"Nǐ yào hē shuǐ ma? Wǒ yǒu shuǐ.", de:"Möchtest du Wasser trinken? Ich habe Wasser."}],
   qs:[
    {q:"Wo ist Li Na?", opts:["Am Bahnhof","Im Hotel","In der U-Bahn"], a:0, l:1},
    {q:"Was hat sie dabei?", opts:["Wasser","Tee","Kaffee"], a:0, l:4},
    {q:"Wohin will sie mit dir?", opts:["Zum Hotel","Zur Toilette","Zum Bahnhof"], a:0, l:2}]},
  {id:"t05", kind:"Notiz", title:"Annas Plan für morgen", lesson:14, from:{zh:"安娜", de:"Anna"}, lines:[
    {zh:"明天上午十点去火车站。", py:"Míng_tiān shàng_wǔ shí diǎn qù huǒ_chē_zhàn.", de:"Morgen um 10 Uhr vormittags zum Bahnhof."},
    {zh:"下午三点喝茶。", py:"Xià_wǔ sān diǎn hē chá.", de:"Um 3 Uhr nachmittags Tee trinken."},
    {zh:"晚上八点去酒店。", py:"Wǎn_shang bā diǎn qù jiǔ_diàn.", de:"Um 8 Uhr abends zum Hotel."},
    {zh:"现在几点？现在是晚上九点。", py:"Xiàn_zài jǐ diǎn? Xiàn_zài shì wǎn_shang jiǔ diǎn.", de:"Wie spät ist es jetzt? Jetzt ist es 9 Uhr abends."}],
   qs:[
    {q:"Wann geht es zum Bahnhof?", opts:["Morgen um 10 Uhr vormittags","Heute um 10 Uhr","Morgen um 3 Uhr nachmittags"], a:0, l:0},
    {q:"Was ist um 3 Uhr nachmittags geplant?", opts:["Tee trinken","Zum Hotel gehen","Zum Bahnhof gehen"], a:0, l:1},
    {q:"Wie spät ist es gerade?", opts:["9 Uhr abends","8 Uhr abends","9 Uhr vormittags"], a:0, l:3}]},
  {id:"t06", kind:"Nachricht", title:"Li Na stellt Anna vor", lesson:16, from:{zh:"李娜", de:"Li Na"}, lines:[
    {zh:"我的朋友叫安娜。", py:"Wǒ de péng_you jiào Ān_nà.", de:"Meine Freundin heißt Anna."},
    {zh:"她是学生，她学习汉语。", py:"Tā shì xué_sheng, tā xué_xí Hàn_yǔ.", de:"Sie ist Studentin, sie lernt Chinesisch."},
    {zh:"她会说一点汉语。", py:"Tā huì shuō yì_diǎn Hàn_yǔ.", de:"Sie kann ein bisschen Chinesisch sprechen."},
    {zh:"她很漂亮，她不工作。", py:"Tā hěn piào_liang, tā bù gōng_zuò.", de:"Sie ist sehr hübsch, sie arbeitet nicht."},
    {zh:"你会说汉语吗？", py:"Nǐ huì shuō Hàn_yǔ ma?", de:"Kannst du Chinesisch sprechen?"}],
   qs:[
    {q:"Wer ist Anna?", opts:["Li Nas Freundin","Li Nas Lehrerin","Li Nas Tochter"], a:0, l:0},
    {q:"Was macht Anna?", opts:["Sie studiert","Sie arbeitet","Sie ist Lehrerin"], a:0, l:1},
    {q:"Wie gut spricht Anna Chinesisch?", opts:["Ein bisschen","Sehr gut","Gar nicht"], a:0, l:2}]},
  {id:"t07", kind:"Nachricht", title:"Xiao Mings Familie", lesson:18, from:{zh:"小明", de:"Xiao Ming"}, lines:[
    {zh:"这是我家。", py:"Zhè shì wǒ jiā.", de:"Das ist meine Familie."},
    {zh:"这是我爸爸，他四十五岁。", py:"Zhè shì wǒ bà_ba, tā sì shí wǔ suì.", de:"Das ist mein Papa, er ist 45 Jahre alt."},
    {zh:"这是我妈妈，她很漂亮。", py:"Zhè shì wǒ mā_ma, tā hěn piào_liang.", de:"Das ist meine Mama, sie ist sehr hübsch."},
    {zh:"那是我的女儿，她三岁。", py:"Nà shì wǒ de nǚ_ér, tā sān suì.", de:"Das da ist meine Tochter, sie ist 3."},
    {zh:"我没有儿子。我爱我家。", py:"Wǒ méi_yǒu ér_zi. Wǒ ài wǒ jiā.", de:"Einen Sohn habe ich nicht. Ich liebe meine Familie."}],
   qs:[
    {q:"Wie alt ist Xiao Mings Vater?", opts:["45","54","35"], a:0, l:1},
    {q:"Wen hat Xiao Ming nicht?", opts:["Einen Sohn","Eine Tochter","Eine Mutter"], a:0, l:4},
    {q:"Wie alt ist die Tochter?", opts:["3","13","30"], a:0, l:3}]},
  {id:"t08", kind:"Schild", title:"Der Plan an der Sprachschule", lesson:20, from:{zh:"学校", de:"Aushang in der Schule"}, lines:[
    {zh:"上午九点：读书", py:"Shàng_wǔ jiǔ diǎn: dú shū", de:"9 Uhr vormittags: Lesen"},
    {zh:"上午十点：写字", py:"Shàng_wǔ shí diǎn: xiě zì", de:"10 Uhr vormittags: Zeichen schreiben"},
    {zh:"下午三点：说汉语", py:"Xià_wǔ sān diǎn: shuō Hàn_yǔ", de:"3 Uhr nachmittags: Chinesisch sprechen"},
    {zh:"老师：李娜", py:"Lǎo_shī: Lǐ_Nà", de:"Lehrerin: Li Na"},
    {zh:"学生：十二个", py:"Xué_sheng: shí èr ge", de:"Schüler: 12"}],
   qs:[
    {q:"Was steht um 10 Uhr an?", opts:["Zeichen schreiben","Lesen","Sprechen"], a:0, l:1},
    {q:"Wie viele Schüler sind es?", opts:["12","20","2"], a:0, l:4},
    {q:"Wer unterrichtet?", opts:["Li Na","Xiao Ming","Anna"], a:0, l:3}]},
  {id:"t09", kind:"Preisschild", title:"Die Preise im Laden", lesson:22, from:{zh:"商店", de:"Schild im Geschäft"}, lines:[
    {zh:"大衣服 九十块", py:"Dà yī_fu jiǔ shí kuài", de:"Große Kleidung, 90 Kuai"},
    {zh:"小衣服 六十块", py:"Xiǎo yī_fu liù shí kuài", de:"Kleine Kleidung, 60 Kuai"},
    {zh:"书 十五块", py:"Shū shí wǔ kuài", de:"Buch, 15 Kuai"},
    {zh:"茶 二十块", py:"Chá èr shí kuài", de:"Tee, 20 Kuai"},
    {zh:"今天的东西都很好！", py:"Jīn_tiān de dōng_xi dōu hěn hǎo!", de:"Alle Sachen sind heute sehr gut!"}],
   qs:[
    {q:"Was kostet die große Kleidung?", opts:["90 Kuai","60 Kuai","19 Kuai"], a:0, l:0},
    {q:"Was ist billiger?", opts:["Die kleine Kleidung","Die große Kleidung","Beide kosten gleich viel"], a:0, l:1},
    {q:"Wie viel kosten zwei Bücher?", opts:["30 Kuai","15 Kuai","50 Kuai"], a:0, l:2}]},
  {id:"t10", kind:"Chat", title:"Wo ist die Katze?", lesson:24, from:{zh:"李娜", de:"Li Na"}, lines:[
    {zh:"弗洛里安，猫在哪儿？", py:"Fú_luò_lǐ_'ān, māo zài nǎ_r?", de:"Florian, wo ist die Katze?"},
    {zh:"猫在桌子上吗？", py:"Māo zài zhuō_zi shang ma?", de:"Ist die Katze auf dem Tisch?", s:"me"},
    {zh:"不在。", py:"Bú zài.", de:"Nein, da nicht."},
    {zh:"猫在椅子后面！", py:"Māo zài yǐ_zi hòu_miàn!", de:"Die Katze ist hinter dem Stuhl!", s:"me"},
    {zh:"好。我坐出租车去火车站，你在哪里？", py:"Hǎo. Wǒ zuò chū_zū_chē qù huǒ_chē_zhàn, nǐ zài nǎ_lǐ?", de:"Gut. Ich fahre mit dem Taxi zum Bahnhof, wo bist du?"},
    {zh:"我在酒店前面。", py:"Wǒ zài jiǔ_diàn qián_miàn.", de:"Ich bin vor dem Hotel.", s:"me"}],
   qs:[
    {q:"Wo ist die Katze?", opts:["Hinter dem Stuhl","Auf dem Tisch","Vor dem Hotel"], a:0, l:3},
    {q:"Womit fährt Li Na?", opts:["Mit dem Taxi","Mit der U-Bahn","Mit dem Zug"], a:0, l:4},
    {q:"Wo ist Florian?", opts:["Vor dem Hotel","Hinter dem Hotel","Am Bahnhof"], a:0, l:5}]},
  {id:"t17", kind:"Schild", title:"Schilder im Yu-Garten", lesson:24, from:{zh:"豫园", de:"Schilder im Garten"}, lines:[
    {zh:"厕所在前面。", py:"Cè_suǒ zài qián_miàn.", de:"Die Toilette ist vorne."},
    {zh:"出租车在后面。", py:"Chū_zū_chē zài hòu_miàn.", de:"Taxis stehen hinten."},
    {zh:"这里没有水。", py:"Zhè_lǐ méi_yǒu shuǐ.", de:"Hier gibt es kein Wasser."},
    {zh:"猫不坐椅子！", py:"Māo bú zuò yǐ_zi!", de:"Katzen sitzen nicht auf den Stühlen!"}],
   qs:[
    {q:"Wo ist die Toilette?", opts:["Vorne","Hinten","Hier"], a:0, l:0},
    {q:"Was gibt es hier nicht?", opts:["Wasser","Taxis","Stühle"], a:0, l:2},
    {q:"Wo stehen die Taxis?", opts:["Hinten","Vorne","Am Wasser"], a:0, l:1}]},
  {id:"t11", kind:"Notiz", title:"Das Wetter am Westsee", lesson:26, from:{zh:"天气", de:"Wetterzettel"}, lines:[
    {zh:"五月三号，星期一：天气很好，不冷不热。", py:"Wǔ yuè sān hào, xīng_qī yī: tiān_qì hěn hǎo, bù lěng bú rè.", de:"3. Mai, Montag: Das Wetter ist sehr gut, nicht kalt, nicht heiß."},
    {zh:"五月四号，星期二：下雨，很冷。", py:"Wǔ yuè sì hào, xīng_qī èr: xià_yǔ, hěn lěng.", de:"4. Mai, Dienstag: Es regnet, sehr kalt."},
    {zh:"五月五号，星期三：很热。", py:"Wǔ yuè wǔ hào, xīng_qī sān: hěn rè.", de:"5. Mai, Mittwoch: Sehr heiß."},
    {zh:"下星期四我不工作。", py:"Xià xīng_qī sì wǒ bù gōng_zuò.", de:"Nächsten Donnerstag arbeite ich nicht."}],
   qs:[
    {q:"Wann regnet es?", opts:["Am 4. Mai","Am 3. Mai","Am 5. Mai"], a:0, l:1},
    {q:"Wie ist das Wetter am 5. Mai?", opts:["Sehr heiß","Sehr kalt","Regnerisch"], a:0, l:2},
    {q:"Welcher Wochentag ist der 3. Mai?", opts:["Montag","Dienstag","Mittwoch"], a:0, l:0}]},
  {id:"t12", kind:"Nachricht", title:"Eine Einladung ins Restaurant", lesson:28, from:{zh:"小明", de:"Xiao Ming"}, lines:[
    {zh:"弗洛里安，你好！", py:"Fú_luò_lǐ_'ān, nǐ_hǎo!", de:"Florian, hallo!"},
    {zh:"明天晚上七点，我请你去饭店。", py:"Míng_tiān wǎn_shang qī diǎn, wǒ qǐng nǐ qù fàn_diàn.", de:"Morgen Abend um 7 lade ich dich ins Restaurant ein."},
    {zh:"饭店里有很好吃的菜和水果。", py:"Fàn_diàn li yǒu hěn hǎo_chī de cài hé shuǐ_guǒ.", de:"Im Restaurant gibt es sehr leckere Gerichte und Obst."},
    {zh:"你喜欢苹果吗？", py:"Nǐ xǐ_huan píng_guǒ ma?", de:"Magst du Äpfel?"},
    {zh:"我很高兴！你呢？", py:"Wǒ hěn gāo_xìng! Nǐ ne?", de:"Ich freue mich sehr! Und du?"}],
   qs:[
    {q:"Wann ist die Einladung?", opts:["Morgen um 7 Uhr abends","Heute um 7 Uhr abends","Morgen um 5 Uhr nachmittags"], a:0, l:1},
    {q:"Wer lädt ein?", opts:["Xiao Ming","Li Na","Anna"], a:0, l:1},
    {q:"Was gibt es im Restaurant?", opts:["Gerichte und Obst","Nur Tee","Kaffee und Reis"], a:0, l:2}]},
  {id:"t13", kind:"Einkaufszettel", title:"Annas Einkaufszettel", lesson:28, from:{zh:"安娜", de:"Anna"}, lines:[
    {zh:"请买：", py:"Qǐng mǎi:", de:"Bitte kaufen:"},
    {zh:"五个苹果", py:"Wǔ ge píng_guǒ", de:"5 Äpfel"},
    {zh:"一本书", py:"Yì běn shū", de:"1 Buch"},
    {zh:"四个杯子", py:"Sì ge bēi_zi", de:"4 Tassen"},
    {zh:"茶和水", py:"Chá hé shuǐ", de:"Tee und Wasser"},
    {zh:"不买咖啡！", py:"Bù mǎi kā_fēi!", de:"Keinen Kaffee kaufen!"}],
   qs:[
    {q:"Wie viele Äpfel sollst du kaufen?", opts:["5","4","1"], a:0, l:1},
    {q:"Was soll nicht gekauft werden?", opts:["Kaffee","Tee","Ein Buch"], a:0, l:5},
    {q:"Wie viele Tassen stehen auf dem Zettel?", opts:["4","5","14"], a:0, l:3}]},
  {id:"t14", kind:"Nachricht", title:"Xiao Ming am Abend", lesson:30, from:{zh:"小明", de:"Xiao Ming"}, lines:[
    {zh:"喂，弗洛里安！你现在能打电话吗？", py:"Wèi, Fú_luò_lǐ_'ān! Nǐ xiàn_zài néng dǎ_diàn_huà ma?", de:"Hallo, Florian! Kannst du jetzt telefonieren?"},
    {zh:"我在看电视，电影很好。", py:"Wǒ zài kàn diàn_shì, diàn_yǐng hěn hǎo.", de:"Ich sehe gerade fern, der Film ist sehr gut."},
    {zh:"中午我睡觉了。", py:"Zhōng_wǔ wǒ shuì_jiào le.", de:"Mittags habe ich geschlafen."},
    {zh:"明天中午你能去饭店吗？", py:"Míng_tiān zhōng_wǔ nǐ néng qù fàn_diàn ma?", de:"Kannst du morgen Mittag ins Restaurant gehen?"}],
   qs:[
    {q:"Was macht Xiao Ming gerade?", opts:["Er sieht fern","Er schläft","Er telefoniert"], a:0, l:1},
    {q:"Wann hat er geschlafen?", opts:["Mittags","Abends","Vormittags"], a:0, l:2},
    {q:"Was fragt er zuerst?", opts:["Ob du jetzt telefonieren kannst","Ob du Tee möchtest","Wo du bist"], a:0, l:0}]},
  {id:"t15", kind:"Nachricht", title:"Li Na muss ins Krankenhaus", lesson:32, from:{zh:"李娜", de:"Li Na"}, lines:[
    {zh:"对不起，今天我不能去学校。", py:"Duì_bu_qǐ, jīn_tiān wǒ bù néng qù xué_xiào.", de:"Entschuldige, heute kann ich nicht zur Schule."},
    {zh:"我去医院，医生说：睡觉！", py:"Wǒ qù yī_yuàn, yī_shēng shuō: shuì_jiào!", de:"Ich gehe ins Krankenhaus, der Arzt sagt: schlafen!"},
    {zh:"我的狗在家。请你看我的狗，好吗？", py:"Wǒ de gǒu zài jiā. Qǐng nǐ kàn wǒ de gǒu, hǎo ma?", de:"Mein Hund ist zu Hause. Siehst du bitte nach meinem Hund, ja?"},
    {zh:"十分钟，没关系。", py:"Shí fēn_zhōng, méi_guān_xi.", de:"Zehn Minuten, das macht nichts."},
    {zh:"明天我去学校。", py:"Míng_tiān wǒ qù xué_xiào.", de:"Morgen gehe ich zur Schule."}],
   qs:[
    {q:"Wohin geht Li Na heute?", opts:["Ins Krankenhaus","Zur Schule","Ins Restaurant"], a:0, l:1},
    {q:"Worum bittet sie dich?", opts:["Nach ihrem Hund zu sehen","Tee zu kaufen","Den Arzt anzurufen"], a:0, l:2},
    {q:"Was sagt der Arzt?", opts:["Schlafen","Wasser trinken","Nicht arbeiten"], a:0, l:1}]},
  {id:"t16", kind:"Nachricht", title:"Vor dem Abflug", lesson:33, from:{zh:"李娜", de:"Li Na"}, lines:[
    {zh:"弗洛里安，明天你坐飞机回德国。", py:"Fú_luò_lǐ_'ān, míng_tiān nǐ zuò fēi_jī huí Dé_guó.", de:"Florian, morgen fliegst du zurück nach Deutschland."},
    {zh:"我很高兴认识你！", py:"Wǒ hěn gāo_xìng rèn_shi nǐ!", de:"Ich freue mich sehr, dich kennengelernt zu haben!"},
    {zh:"下个月我去德国。你住在哪里？", py:"Xià ge yuè wǒ qù Dé_guó. Nǐ zhù zài nǎ_lǐ?", de:"Nächsten Monat fahre ich nach Deutschland. Wo wohnst du?"},
    {zh:"我想看见你。再见！", py:"Wǒ xiǎng kàn_jiàn nǐ. Zài_jiàn!", de:"Ich möchte dich sehen. Tschüss!"}],
   qs:[
    {q:"Womit reist Florian nach Deutschland?", opts:["Mit dem Flugzeug","Mit dem Zug","Mit dem Taxi"], a:0, l:0},
    {q:"Was hat Li Na vor?", opts:["Nächsten Monat nach Deutschland zu fahren","Nach Peking zu fahren","Fernzusehen"], a:0, l:2},
    {q:"Was will sie wissen?", opts:["Wo du wohnst","Was du isst","Wie alt du bist"], a:0, l:2}]}
];
