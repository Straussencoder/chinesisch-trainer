// Quelle für die Gespräche (Runde 5, länger). Pinyin wird aus dem Wörterbuch der App erzeugt (build_dialogs.js),
// damit Töne, Tonwechsel bei 不 und 一 und unbetonte Silben überall gleich sind.
// Zeile: [wer, Chinesisch, Deutsch, Auswahl?]; Auswahl: [[falsch, Deutsch, Begründung], ...]
module.exports = {
u1: {title:"Am Flughafen", who:{zh:"李娜", py:"Lǐ Nà", de:"Li Na, eine Studentin, die dich abholt"}, lines:[
  ["a", "你好！是你吗？", "Hallo! Bist du's?"],
  ["me", "是我！你好！", "Ja, ich bin's! Hallo!", [
    ["不是我。", "Ich bin's nicht.", "Sie holt dich ab, du bist es ja."],
    ["再见！", "Tschüss!", "Ihr habt euch gerade erst getroffen."]]],
  ["a", "你好吗？", "Wie geht's dir?"],
  ["me", "我很好，谢谢！你好吗？", "Mir geht's gut, danke! Und dir?", [
    ["我很好吗？", "Geht es mir gut?", "吗 macht aus dem Satz eine Frage. Du sollst aber antworten."],
    ["不是。", "Nein, ist es nicht.", "Sie fragt, wie es dir geht. 不是 passt nicht zu dieser Frage."]]],
  ["a", "我很好！", "Mir geht's gut!"],
  ["a", "再见！", "Tschüss!"],
  ["me", "再见！谢谢！", "Tschüss! Danke!", [
    ["你好！", "Hallo!", "Sie verabschiedet sich. Darauf sagt man auch 再见."],
    ["我很好。", "Mir geht's gut.", "Das hast du schon gesagt. Jetzt geht es ums Verabschieden."]]]
]},
u2: {title:"Neue Nachbarn", who:{zh:"王爷爷", py:"Wáng yé_ye", de:"Opa Wang, ein Nachbar"}, lines:[
  ["a", "你好！你叫什么名字？", "Hallo! Wie heißt du?"],
  ["me", "我叫弗洛里安。", "Ich heiße Florian.", [
    ["我是中国人。", "Ich bin Chinese.", "Er fragt nach deinem Namen, nicht nach dem Land."],
    ["他叫什么？", "Wie heißt er?", "Er hat dich gefragt. Antworte mit 我叫 …"]]],
  ["a", "弗洛里安，你好！你是哪国人？", "Florian, hallo! Aus welchem Land kommst du?"],
  ["me", "我是德国人。", "Ich bin Deutscher.", [
    ["我是德国。", "Ich bin Deutschland.", "德国 ist das Land. Für den Menschen kommt 人 dahinter: 德国人."],
    ["你是哪国人？", "Aus welchem Land kommst du?", "Erst antworten, dann zurückfragen."]]],
  ["me", "你是中国人吗？", "Sind Sie Chinese?", [
    ["你是哪国人吗？", "Aus welchem Land kommen Sie?", "Mit einem Fragewort wie 哪 steht kein 吗 am Ende."],
    ["你是中国吗？", "Sind Sie China?", "Auch hier fehlt 人: 中国人."]]],
  ["a", "是，我是中国人。", "Ja, ich bin Chinese."],
  ["me", "他叫什么名字？", "Wie heißt er?", [
    ["他是什么名字？", "Er ist welcher Name?", "Nach dem Namen fragt man mit 叫: 他叫什么名字？"],
    ["她叫什么名字？", "Wie heißt sie?", "Es geht um einen Jungen, also 他. Gesprochen klingen 他 und 她 gleich, nur die Schrift ist anders."]], "Ein Junge läuft vorbei. Du willst wissen, wie er heißt."],
  ["a", "他叫小明。", "Er heißt Xiao Ming."],
  ["a", "再见！", "Tschüss!"],
  ["me", "再见！", "Tschüss!", [
    ["你好！", "Hallo!", "Er verabschiedet sich. Darauf sagt man auch 再见."],
    ["我叫弗洛里安。", "Ich heiße Florian.", "Das weiß er schon. Jetzt sagt ihr Tschüss."]]]
]},
u3: {title:"Wachtürme zählen", who:{zh:"小明", py:"Xiǎo Míng", de:"Xiao Ming, ein Junge auf der Mauer"}, lines:[
  ["a", "你好！我叫小明。你叫什么名字？", "Hallo! Ich heiße Xiao Ming. Wie heißt du?"],
  ["me", "我叫弗洛里安。", "Ich heiße Florian.", [
    ["我叫小明。", "Ich heiße Xiao Ming.", "So heißt er. Du sagst deinen eigenen Namen."],
    ["你好吗？", "Wie geht's dir?", "Er hat nach deinem Namen gefragt."]]],
  ["a", "一、二、三……", "Eins, zwei, drei …"],
  ["me", "四、五、六！", "Vier, fünf, sechs!", [
    ["三、二、一！", "Drei, zwei, eins!", "Er zählt nach oben. Nach 三 kommt 四."],
    ["七、八、九！", "Sieben, acht, neun!", "Da fehlen 四, 五 und 六."]]],
  ["a", "七、八……", "Sieben, acht …"],
  ["me", "九、十！", "Neun, zehn!", [
    ["六、七！", "Sechs, sieben!", "Die hatten wir schon. Nach 八 kommt 九."],
    ["十、九！", "Zehn, neun!", "Falsche Reihenfolge: erst 九, dann 十."]]],
  ["a", "很好！", "Sehr gut!"],
  ["me", "谢谢！", "Danke!", [
    ["不是。", "Nein, ist es nicht.", "Er lobt dich. Darauf sagt man 谢谢."],
    ["再见！", "Tschüss!", "Ihr seid noch nicht fertig. Auf ein Lob sagt man 谢谢."]]],
  ["a", "你是中国人吗？", "Bist du Chinese?"],
  ["me", "不是，我是德国人。", "Nein, ich bin Deutscher.", [
    ["是，我是德国人。", "Ja, ich bin Deutscher.", "Du bist kein Chinese. Auf die Frage antwortest du deshalb mit 不是."],
    ["不是，我不是德国人。", "Nein, ich bin kein Deutscher.", "Doch, du bist Deutscher. Nur 中国人 bist du nicht."]]],
  ["a", "德国很好！再见！", "Deutschland ist toll! Tschüss!"],
  ["me", "再见，小明！", "Tschüss, Xiao Ming!"]
]},
u4: {title:"Im Teehaus bestellen", who:{zh:"服务员", py:"fú_wù_yuán", de:"die Bedienung"}, lines:[
  ["a", "你好！你要什么？", "Hallo! Was möchtest du?"],
  ["me", "我要茶。", "Ich möchte Tee.", [
    ["你要什么？", "Was möchtest du?", "Sie hat dich gefragt. Antworte mit 我要 …"],
    ["我喜欢德国。", "Ich mag Deutschland.", "Schön, aber sie will wissen, was du bestellst."]]],
  ["a", "你喜欢喝咖啡吗？", "Trinkst du gern Kaffee?"],
  ["me", "不喜欢。我喜欢喝茶。", "Nicht so. Ich trinke gern Tee.", [
    ["不喜欢。我喜欢吃茶。", "Nicht so. Ich esse gern Tee.", "Tee trinkt man: 喝茶, nicht 吃."],
    ["我不喜欢喝咖啡吗？", "Trinke ich nicht gern Kaffee?", "Mit 吗 wird es eine Frage. Du sollst aber antworten."]], "Kaffee magst du nicht so, Tee schon."],
  ["a", "好！你吃什么？", "Gut! Was isst du?"],
  ["me", "我要米饭。", "Ich möchte Reis.", [
    ["我喝米饭。", "Ich trinke Reis.", "Reis isst man: 吃, nicht 喝. Beim Bestellen sagt man einfach 我要 …"],
    ["我很好。", "Mir geht's gut.", "Sie fragt nach dem Essen."]], "Du möchtest Reis."],
  ["a", "你喝水吗？", "Trinkst du Wasser?"],
  ["me", "不喝，谢谢。", "Nein, danke.", [
    ["不是，谢谢。", "Nein, ist es nicht, danke.", "Auf eine Frage mit Verb antwortet man mit dem Verb: 喝 (ja) oder 不喝 (nein). Ein eigenes Wort für »nein« gibt es nicht."],
    ["我不喜欢茶。", "Ich mag keinen Tee.", "Du hast gerade Tee bestellt."]], "Wasser möchtest du nicht."],
  ["a", "好吃吗？", "Schmeckt es?"],
  ["me", "很好吃！", "Sehr lecker!", [
    ["我要茶。", "Ich möchte Tee.", "Den Tee hast du schon. Sie fragt, ob es schmeckt."],
    ["不是。", "Nein, ist es nicht.", "Auf 好吃吗？ antwortet man mit 好吃 oder 不好吃."]]],
  ["a", "谢谢！你喜欢中国菜吗？", "Danke! Magst du chinesisches Essen?"],
  ["me", "我很喜欢中国菜！", "Ich mag chinesisches Essen sehr!", [
    ["我很好吃中国菜！", "Ich lecker chinesisches Essen!", "好吃 heißt lecker. Mögen heißt 喜欢: 我很喜欢中国菜."],
    ["是，我是中国菜。", "Ja, ich bin chinesisches Essen.", "Mit 是 sagst du, was du bist. Hier brauchst du 喜欢."]]],
  ["a", "谢谢！再见！", "Danke! Tschüss!"],
  ["me", "再见！", "Tschüss!"]
]},
u5: {title:"Handeln auf dem Markt", who:{zh:"阿姨", py:"ā_yí", de:"eine Händlerin"}, lines:[
  ["a", "你好！你要什么？", "Hallo! Was möchtest du?"],
  ["me", "这个多少钱？", "Wie viel kostet das?", [
    ["这个太贵了！", "Das ist zu teuer!", "Du kennst den Preis noch gar nicht. Frag erst mit 多少钱."],
    ["你好吗？", "Wie geht's dir?", "Freundlich, aber du willst den Preis wissen."]]],
  ["a", "十块。", "Zehn Kuai."],
  ["me", "太贵了！", "Zu teuer!", [
    ["很好吃！", "Sehr lecker!", "Es geht um den Preis, nicht ums Essen."],
    ["我没有钱。", "Ich habe kein Geld.", "Das stimmt hoffentlich nicht. Zum Handeln sagt man 太贵了."]]],
  ["a", "那个五块。", "Das da kostet fünf Kuai."],
  ["me", "我要那个。", "Ich nehme das da.", [
    ["那个多少钱？", "Wie viel kostet das da?", "Den Preis hat sie gerade gesagt: 五块."],
    ["太贵了！", "Zu teuer!", "Fünf Kuai sind ein guter Preis."]]],
  ["a", "我有茶。你喝茶吗？", "Ich habe Tee. Trinkst du Tee?"],
  ["me", "有咖啡吗？", "Gibt es Kaffee?", [
    ["你不有咖啡吗？", "Hast du nicht Kaffee?", "有 verneint man nie mit 不, immer mit 没: 没有."],
    ["我没有咖啡。", "Ich habe keinen Kaffee.", "Du willst wissen, ob sie Kaffee hat. Dann fragst du: 有咖啡吗？"]], "Du hättest lieber einen Kaffee."],
  ["a", "没有咖啡，有茶。", "Kaffee gibt es nicht, nur Tee."],
  ["me", "一杯茶多少钱？", "Was kostet eine Tasse Tee?", [
    ["一茶多少钱？", "Was kostet ein Tee?", "Zwischen Zahl und Nomen steht immer ein Zählwort: 一杯茶."],
    ["一杯茶太贵了！", "Eine Tasse Tee ist zu teuer!", "Du kennst den Preis noch nicht."]], "Dann eben Tee. Du willst wissen, was eine Tasse kostet."],
  ["a", "三块。", "Drei Kuai."],
  ["me", "好，我要一杯茶。", "Gut, ich nehme eine Tasse Tee.", [
    ["好，我有一杯茶。", "Gut, ich habe eine Tasse Tee.", "有 heißt haben. Kaufen willst du: 我要 …"],
    ["好，我要三杯钱。", "Gut, ich will drei Tassen Geld.", "杯 zählt Tassen, nicht Geld. Du willst einen Tee: 一杯茶."]]],
  ["a", "那个五块，茶三块。八块钱。", "Das da fünf, der Tee drei. Acht Kuai."],
  ["me", "好，谢谢！", "Gut, danke!"],
  ["a", "谢谢！再见！", "Danke! Tschüss!"]
]},
u6: {title:"Ankunft am Bahnhof", who:{zh:"乘客", py:"chéng_kè", de:"ein Mitreisender"}, lines:[
  ["a", "你好！你去哪里？", "Hallo! Wohin fährst du?"],
  ["me", "我想去酒店。", "Ich möchte zum Hotel.", [
    ["我是酒店。", "Ich bin das Hotel.", "是 heißt »sein« im Sinn von »gleich sein«. Für ein Ziel nimmt man 去."],
    ["我想去在酒店。", "Ich möchte gehen in Hotel.", "Hinter 去 steht das Ziel direkt, ohne 在."]]],
  ["a", "酒店在那里。", "Das Hotel ist dort."],
  ["me", "谢谢！地铁在哪里？", "Danke! Wo ist die U-Bahn?", [
    ["谢谢！地铁在那里。", "Danke! Die U-Bahn ist dort.", "Du willst etwas wissen. Für die Frage brauchst du 哪里 (wo), nicht 那里 (dort)."],
    ["谢谢！你在哪里？", "Danke! Wo bist du?", "Er steht ja neben dir. Du suchst die U-Bahn."]]],
  ["a", "地铁在这里。你想喝水吗？我有水。", "Die U-Bahn ist hier. Möchtest du Wasser? Ich habe Wasser."],
  ["me", "不喝，谢谢。厕所在哪里？", "Nein, danke. Wo ist die Toilette?", [
    ["不喝，谢谢。厕所在那里？", "Nein, danke. Die Toilette ist dort?", "Du suchst die Toilette. Gefragt wird mit 哪里 (wo), nicht mit 那里 (dort)."],
    ["不喝，谢谢。我在厕所。", "Nein, danke. Ich bin auf der Toilette.", "我在厕所 heißt »Ich bin auf der Toilette«. Du willst wissen, wo sie ist."]], "Wasser möchtest du nicht, aber du suchst die Toilette."],
  ["a", "厕所在那里。", "Die Toilette ist dort."],
  ["me", "谢谢！你去哪里？", "Danke! Wohin fährst du?", [
    ["谢谢！你去哪里吗？", "Danke! Wohin fährst du ja?", "Mit einem Fragewort wie 哪里 steht kein 吗 am Ende."],
    ["谢谢！你在哪里？", "Danke! Wo bist du?", "Er steht neben dir. Du willst wissen, wohin er fährt: 去哪里."]]],
  ["a", "我去火车站。我想喝咖啡。", "Ich gehe zum Bahnhof. Ich möchte einen Kaffee trinken."],
  ["me", "火车站有咖啡吗？", "Gibt es am Bahnhof Kaffee?", [
    ["火车站是咖啡吗？", "Ist der Bahnhof Kaffee?", "Ob es etwas gibt, fragt man mit 有: Ort + 有 + Ding."],
    ["火车站不有咖啡吗？", "Hat der Bahnhof nicht Kaffee?", "有 verneint man nie mit 不."]], "Du fragst, ob es am Bahnhof Kaffee gibt."],
  ["a", "有！再见！", "Ja! Tschüss!"],
  ["me", "再见！", "Tschüss!"]
]},
u7: {title:"Uhrzeit am Bund", who:{zh:"摄影师", py:"shè_yǐng_shī", de:"ein Fotograf"}, lines:[
  ["me", "你好！现在几点？", "Hallo! Wie spät ist es?", [
    ["你好！你什么时候去？", "Hallo! Wann gehst du?", "Du willst die Uhrzeit wissen. Die Frage dafür ist 现在几点？"],
    ["你好！现在三点。", "Hallo! Es ist drei Uhr.", "Das ist eine Antwort. Du willst aber fragen."]], "Du willst wissen, wie spät es ist."],
  ["a", "现在下午三点。", "Es ist drei Uhr nachmittags."],
  ["a", "你什么时候去酒店？", "Wann gehst du ins Hotel?"],
  ["me", "我晚上去酒店。", "Ich gehe abends ins Hotel.", [
    ["我去酒店晚上。", "Ich gehe ins Hotel abends.", "Die Zeit steht vor dem Verb, nie am Ende: 我晚上去酒店."],
    ["现在三点。", "Es ist drei Uhr.", "Er fragt, wann du ins Hotel gehst."]]],
  ["a", "晚上几点？", "Um wie viel Uhr am Abend?"],
  ["me", "晚上八点。", "Um acht Uhr abends.", [
    ["八点晚上。", "Acht Uhr abends.", "Vom Großen zum Kleinen: erst 晚上, dann 八点."],
    ["晚上八块。", "Abends acht Kuai.", "块 ist Geld. Die Uhrzeit sagt man mit 点."]], "Du gehst um acht Uhr abends."],
  ["a", "明天你去哪里？", "Wohin gehst du morgen?"],
  ["me", "明天我去火车站。", "Morgen gehe ich zum Bahnhof.", [
    ["昨天我去火车站。", "Gestern ging ich zum Bahnhof.", "Er fragt nach morgen (明天), nicht nach gestern (昨天)."],
    ["火车站在哪里？", "Wo ist der Bahnhof?", "Er will wissen, wohin du gehst."]]],
  ["a", "你几点去火车站？", "Um wie viel Uhr gehst du zum Bahnhof?"],
  ["me", "上午十点。", "Um zehn Uhr vormittags.", [
    ["下午十点。", "Zehn Uhr nachmittags.", "Zehn Uhr nachmittags gibt es nicht. Vormittags heißt 上午, nachmittags 下午."],
    ["十点上午。", "Zehn Uhr vormittags.", "Vom Großen zum Kleinen: erst 上午, dann 十点."]], "Du gehst um zehn Uhr vormittags."],
  ["a", "好！再见！", "Gut! Tschüss!"],
  ["me", "谢谢！再见！", "Danke! Tschüss!"]
]},
u8: {title:"Plaudern am Kanal", who:{zh:"船娘", py:"chuán_niáng", de:"eine Bootsfrau"}, lines:[
  ["a", "你好！你会说汉语吗？", "Hallo! Kannst du Chinesisch?"],
  ["me", "我会说一点汉语。", "Ich kann ein bisschen Chinesisch.", [
    ["我会汉语说一点。", "Ich kann Chinesisch sprechen ein bisschen.", "Das Verb 说 kommt direkt nach 会, dann 一点 und die Sprache: 会说一点汉语."],
    ["我是汉语。", "Ich bin Chinesisch.", "Mit 是 sagst du, was du bist. Hier brauchst du 会说 (sprechen können)."]]],
  ["a", "你是学生吗？", "Bist du Student?"],
  ["me", "是，我是学生。", "Ja, ich bin Student.", [
    ["是，我是工作。", "Ja, ich bin Arbeit.", "工作 ist arbeiten oder die Arbeit, kein Beruf. Sie fragt, ob du Student bist."],
    ["我会说一点。", "Ich kann ein bisschen.", "Das war die Frage davor."]]],
  ["a", "你在哪里学习汉语？", "Wo lernst du Chinesisch?"],
  ["me", "我在德国学习汉语。", "Ich lerne in Deutschland Chinesisch.", [
    ["我学习汉语在德国。", "Ich lerne Chinesisch in Deutschland.", "Wo man etwas tut, steht vor dem Verb: 在德国学习."],
    ["我在德国是汉语。", "Ich bin in Deutschland Chinesisch.", "Hier fehlt das Verb lernen: 学习."]]],
  ["a", "你的汉语很好！", "Dein Chinesisch ist gut!"],
  ["me", "谢谢！你在这里工作吗？", "Danke! Arbeitest du hier?", [
    ["谢谢！你工作在这里吗？", "Danke! Arbeitest du in hier?", "Wo man etwas tut, steht mit 在 vor dem Verb: 在这里工作."],
    ["谢谢！我在这里工作吗？", "Danke! Arbeite ich hier?", "Du willst wissen, ob sie hier arbeitet: 你 …"]], "Du willst wissen, ob sie hier arbeitet."],
  ["a", "是，我在这里工作。这里很漂亮！", "Ja, ich arbeite hier. Hier ist es sehr schön!"],
  ["me", "很漂亮！", "Sehr schön!", [
    ["很好吃！", "Sehr lecker!", "好吃 passt nur zu Essen."],
    ["我很漂亮！", "Ich bin sehr hübsch!", "Sie meint den Ort, nicht dich."]]],
  ["a", "你有中国朋友吗？", "Hast du chinesische Freunde?"],
  ["me", "有，我有中国朋友。", "Ja, ich habe chinesische Freunde.", [
    ["是，我是中国朋友。", "Ja, ich bin ein chinesischer Freund.", "Sie fragt, ob du chinesische Freunde hast. Die Antwort nimmt das Verb der Frage: 有."],
    ["没有，我有中国朋友。", "Nein, ich habe chinesische Freunde.", "Erst nein und dann ja, das passt nicht zusammen."]], "Du hast chinesische Freunde."],
  ["a", "很好！再见！", "Sehr gut! Tschüss!"],
  ["me", "再见！", "Tschüss!"]
]},
u9: {title:"Bei Familie Wang", who:{zh:"王阿姨", py:"Wáng ā_yí", de:"Frau Wang"}, lines:[
  ["a", "你好！这是我家。", "Hallo! Das ist mein Zuhause."],
  ["me", "你家很漂亮！", "Dein Zuhause ist sehr schön!", [
    ["你家很好吃！", "Dein Zuhause ist sehr lecker!", "好吃 sagt man nur über Essen. Für eine Wohnung passt 漂亮."],
    ["这是谁？", "Wer ist das?", "Sie zeigt dir ihr Zuhause, keine Person."]]],
  ["a", "谢谢！这是我女儿。", "Danke! Das ist meine Tochter."],
  ["me", "她几岁？", "Wie alt ist sie?", [
    ["她是谁？", "Wer ist sie?", "Das hat Frau Wang gerade gesagt: ihre Tochter."],
    ["她几个？", "Wie viele Stück ist sie?", "Nach dem Alter fragt man mit 岁: 几岁."]], "Du möchtest wissen, wie alt die Tochter ist."],
  ["a", "她五岁。", "Sie ist fünf."],
  ["me", "你有儿子吗？", "Hast du einen Sohn?", [
    ["你是儿子吗？", "Bist du ein Sohn?", "Du willst wissen, ob sie einen Sohn hat: 有, nicht 是."],
    ["你有女儿吗？", "Hast du eine Tochter?", "Die Tochter hast du gerade kennengelernt."]], "Du fragst, ob sie auch einen Sohn hat."],
  ["a", "有，我有一个儿子。他八岁。", "Ja, ich habe einen Sohn. Er ist acht."],
  ["me", "那是谁？", "Wer ist das?", [
    ["那是什么？", "Was ist das?", "什么 fragt nach Dingen. Nach Menschen fragt man mit 谁."],
    ["那是谁吗？", "Ist das wer?", "Mit einem Fragewort wie 谁 steht kein 吗 am Ende."]], "An der Wand hängt ein Foto. Du fragst, wer das ist."],
  ["a", "那是我爸爸妈妈。你爸爸妈妈在德国吗？", "Das sind meine Eltern. Sind deine Eltern in Deutschland?"],
  ["me", "是，我爸爸妈妈在德国。", "Ja, meine Eltern sind in Deutschland.", [
    ["是，我爸爸妈妈是德国。", "Ja, meine Eltern sind Deutschland.", "Für Orte nimmt man 在, nicht 是."],
    ["不是，我爸爸妈妈在德国。", "Nein, meine Eltern sind in Deutschland.", "Erst nein und dann ja, das passt nicht zusammen."]]],
  ["a", "我女儿很喜欢你！", "Meine Tochter mag dich sehr!"],
  ["me", "谢谢！她很漂亮！", "Danke! Sie ist sehr hübsch!"],
  ["a", "再见！", "Tschüss!"],
  ["me", "再见！谢谢！", "Tschüss! Danke!"]
]},
u10: {title:"Erster Schultag", who:{zh:"安娜", py:"Ān_nà", de:"Anna, eine Mitschülerin aus Deutschland"}, lines:[
  ["a", "你好！你是这里的学生吗？", "Hallo! Bist du Schüler hier?"],
  ["me", "是，我在这里学习汉语。", "Ja, ich lerne hier Chinesisch.", [
    ["是，我学习汉语在这里。", "Ja, ich lerne Chinesisch hier.", "Wo man etwas tut, steht vor dem Verb: 在这里学习."],
    ["不是，我是这里。", "Nein, ich bin hier.", "Für Orte nimmt man 在, nicht 是. Und du lernst ja hier."]]],
  ["a", "我们是同学！我叫安娜。", "Wir sind Mitschüler! Ich heiße Anna."],
  ["me", "你好！我叫弗洛里安。", "Hallo! Ich heiße Florian.", [
    ["你好！我们叫弗洛里安。", "Hallo! Wir heißen Florian.", "我们 heißt wir. Du stellst dich selbst vor: 我叫 …"],
    ["你好！你叫弗洛里安。", "Hallo! Du heißt Florian.", "Sie heißt Anna. Du sprichst von dir: 我叫 …"]]],
  ["a", "你是哪国人？", "Aus welchem Land kommst du?"],
  ["me", "我是德国人。你是哪国人？", "Ich bin Deutscher. Woher kommst du?", [
    ["我是德国人。你是哪国人吗？", "Ich bin Deutscher. Woher kommst du ja?", "Mit einem Fragewort wie 哪 steht kein 吗 am Ende."],
    ["我是哪国人。", "Ich bin welches Land.", "In der Antwort steht das Land an der Stelle von 哪: 我是德国人."]]],
  ["a", "我是德国人！这个字怎么读？", "Ich bin Deutsche! Wie liest man dieses Zeichen?"],
  ["me", "我不认识这个字。", "Ich kenne dieses Zeichen nicht.", [
    ["这个字很好吃。", "Dieses Zeichen ist lecker.", "好吃 passt nur zu Essen."],
    ["我有三本书。", "Ich habe drei Bücher.", "Sie fragt nach der Aussprache des Zeichens."]]],
  ["me", "你会读这个字吗？", "Kannst du dieses Zeichen lesen?", [
    ["你会写这个字吗？", "Kannst du dieses Zeichen schreiben?", "Ihr wollt wissen, wie man es liest (读), nicht wie man es schreibt (写)."],
    ["你会读这本书吗？", "Kannst du dieses Buch lesen?", "Es geht um ein Zeichen, nicht um ein Buch."]], "Du fragst Anna, ob sie das Zeichen lesen kann."],
  ["a", "我不会。老师会读。", "Ich nicht. Die Lehrerin kann es."],
  ["me", "谢谢，安娜！", "Danke, Anna!"]
]},
u11: {title:"Im Kleidergeschäft", who:{zh:"店员", py:"diàn_yuán", de:"eine Verkäuferin"}, lines:[
  ["a", "你好！你想买什么？", "Hallo! Was möchtest du kaufen?"],
  ["me", "我想买衣服。", "Ich möchte Kleidung kaufen.", [
    ["我买什么？", "Was kaufe ich?", "Sie hat dich gefragt. Antworte mit 我想买 …"],
    ["我想买米饭。", "Ich möchte Reis kaufen.", "Du bist in einem Kleidergeschäft."]]],
  ["a", "这些衣服都很漂亮。", "Diese Kleider sind alle sehr schön."],
  ["me", "这个太大了。有小的吗？", "Das ist zu groß. Gibt es ein kleineres?", [
    ["这个太大了。有大的吗？", "Das ist zu groß. Gibt es ein großes?", "Wenn es zu groß ist, brauchst du ein kleines: 小的."],
    ["这个太小了。有小的吗？", "Das ist zu klein. Gibt es ein kleines?", "Wenn es zu klein ist, brauchst du ein großes."]], "Das Kleid ist dir zu groß."],
  ["a", "有，这个是小的。", "Ja, das hier ist ein kleines."],
  ["me", "很漂亮！多少钱？", "Sehr schön! Wie viel kostet es?", [
    ["很漂亮！几钱？", "Sehr schön! Wie wenig Geld?", "Nach dem Preis fragt man mit 多少钱. 几 braucht ein Zählwort."],
    ["很漂亮！太贵了！", "Sehr schön! Zu teuer!", "Du kennst den Preis noch nicht."]]],
  ["a", "九十块。", "Neunzig Kuai."],
  ["me", "太贵了！", "Zu teuer!", [
    ["太小了！", "Zu klein!", "Die Größe passt ja jetzt. Es geht um den Preis."],
    ["很好吃！", "Sehr lecker!", "好吃 passt nur zu Essen."]]],
  ["a", "八十块，好吗？", "Achtzig Kuai, okay?"],
  ["me", "六十块，好吗？", "Sechzig Kuai, okay?", [
    ["九十块，好吗？", "Neunzig Kuai, okay?", "Das ist mehr als ihr Angebot. Beim Handeln bietest du weniger."],
    ["六十钱，好吗？", "Sechzig Geld, okay?", "Beim Geld zählt man mit 块: 六十块."]], "Du willst handeln und bietest 60 Kuai."],
  ["a", "好，六十块。", "Gut, sechzig Kuai."],
  ["me", "谢谢！我很喜欢这个商店。", "Danke! Ich mag diesen Laden sehr."],
  ["a", "谢谢！再见！", "Danke! Tschüss!"]
]},
u12: {title:"Die Katze im Garten", who:{zh:"小朋友", py:"xiǎo_péng_you", de:"ein Kind"}, lines:[
  ["a", "猫在哪儿？", "Wo ist die Katze?"],
  ["me", "猫在椅子上。", "Die Katze ist auf dem Stuhl.", [
    ["猫是椅子上。", "Die Katze ist Stuhl-auf.", "Für Orte nimmt man 在, nicht 是."],
    ["椅子在猫上。", "Der Stuhl ist auf der Katze.", "Andersherum: Die Katze ist auf dem Stuhl."]], "Du glaubst, die Katze sitzt auf dem Stuhl."],
  ["a", "不是，椅子上没有猫。", "Nein, auf dem Stuhl ist keine Katze."],
  ["me", "猫在桌子后面！", "Die Katze ist hinter dem Tisch!", [
    ["猫在后面桌子！", "Die Katze ist hinter Tisch!", "Erst der Bezugspunkt, dann das Ortswort: 桌子后面."],
    ["猫是桌子后面！", "Die Katze ist Tisch-hinten!", "Für Orte nimmt man 在, nicht 是."]], "Da! Hinter dem Tisch sitzt die Katze."],
  ["a", "是！谢谢！你喜欢猫吗？", "Stimmt! Danke! Magst du Katzen?"],
  ["me", "很喜欢！我家里有猫。", "Sehr! Wir haben zu Hause eine Katze.", [
    ["很喜欢！我家里是猫。", "Sehr! Mein Zuhause ist eine Katze.", "Was es an einem Ort gibt, sagt man mit 有: 家里有猫."],
    ["很喜欢！猫在我家里有。", "Sehr! Katze ist bei mir zu Hause hat.", "Ort + 有 + Ding: 我家里有猫."]], "Du hast zu Hause auch eine Katze."],
  ["a", "你去哪儿？", "Wohin gehst du?"],
  ["me", "我坐出租车去酒店。", "Ich fahre mit dem Taxi zum Hotel.", [
    ["我坐酒店去出租车。", "Ich fahre mit dem Hotel zum Taxi.", "Hinter 坐 steht das Fahrzeug, hinter 去 das Ziel."],
    ["出租车在前面。", "Das Taxi ist vorne.", "Das Kind fragt, wohin du gehst."]], "Du nimmst ein Taxi zum Hotel."],
  ["a", "出租车在前面！", "Das Taxi ist da vorne!"],
  ["me", "谢谢！再见！", "Danke! Tschüss!"]
]},
u13: {title:"Bootsfahrt auf dem Westsee", who:{zh:"船夫", py:"chuán_fū", de:"ein Bootsmann"}, lines:[
  ["a", "今天天气怎么样？", "Wie findest du das Wetter heute?"],
  ["me", "太冷了！", "Zu kalt!", [
    ["太好吃了！", "Zu lecker!", "Er fragt nach dem Wetter. 好吃 passt nur zu Essen."],
    ["今天十月二十五号。", "Heute ist der 25. Oktober.", "Das ist das Datum. Er fragt nach dem Wetter."]], "Es ist eiskalt."],
  ["a", "明天不冷。", "Morgen ist es nicht kalt."],
  ["me", "明天下雨吗？", "Regnet es morgen?", [
    ["明天下雨了吗？", "Hat es morgen geregnet?", "Morgen ist noch nicht passiert. 了 passt hier nicht."],
    ["明天是下雨吗？", "Ist morgen Regen?", "下雨 ist ein Verb, davor steht kein 是."]], "Du fragst, ob es morgen regnet."],
  ["a", "不下雨。明天天气很好。", "Es regnet nicht. Morgen ist das Wetter schön."],
  ["me", "明天星期几？", "Welcher Wochentag ist morgen?", [
    ["明天几星期？", "Morgen wie viele Wochen?", "Nach dem Wochentag fragt man mit 星期几: 星期 und dann die Zahl."],
    ["明天星期什么？", "Morgen ist Woche was?", "Wochentage sind Zahlen. Gefragt wird mit 几: 星期几？"]], "Du weißt nicht, welcher Wochentag morgen ist."],
  ["a", "明天星期六。", "Morgen ist Samstag."],
  ["me", "太好了！", "Super!", [
    ["太贵了！", "Zu teuer!", "Es geht um das Wochenende, nicht um einen Preis."],
    ["明天下雨吗？", "Regnet es morgen?", "Wie das Wetter morgen wird, hat er schon gesagt."]]],
  ["a", "今天几号？", "Der Wievielte ist heute?"],
  ["me", "今天十月二十五号。", "Heute ist der 25. Oktober.", [
    ["今天二十五号十月。", "Heute ist der 25. im Oktober.", "Vom Großen zum Kleinen: erst der Monat, dann der Tag."],
    ["今天十月二十五月。", "Heute ist Oktober 25. Monat.", "Der Tag heißt 号: 二十五号."]], "Heute ist der 25. Oktober."],
  ["a", "下雨了！", "Jetzt regnet es!"],
  ["me", "我们去酒店！", "Wir gehen ins Hotel!"]
]},
u14: {title:"Essen bei Familie Wang", who:{zh:"王叔叔", py:"Wáng shū_shu", de:"Herr Wang"}, lines:[
  ["a", "请坐！请喝茶。", "Setz dich bitte! Trink bitte Tee."],
  ["me", "谢谢！", "Danke!", [
    ["不客气！", "Gern geschehen!", "不客气 sagt man, wenn sich jemand bei dir bedankt. Hier bedankst du dich."],
    ["再见！", "Tschüss!", "Du bist gerade erst angekommen."]]],
  ["a", "不客气。你喜欢吃水果吗？", "Gern geschehen. Isst du gern Obst?"],
  ["me", "喜欢！我很喜欢苹果。", "Ja! Ich mag Äpfel sehr.", [
    ["喜欢！我喜欢吃咖啡。", "Ja! Ich esse gern Kaffee.", "Kaffee trinkt man: 喝, nicht 吃. Und gefragt war nach Obst."],
    ["喜欢！我很喜欢杯子。", "Ja! Ich mag Becher sehr.", "Ein Becher ist kein Obst."]]],
  ["a", "请吃苹果！", "Nimm dir bitte einen Apfel!"],
  ["me", "谢谢！很好吃！", "Danke! Sehr lecker!"],
  ["a", "你喜欢吃中国菜吗？", "Isst du gern chinesisch?"],
  ["me", "很喜欢！你呢？", "Sehr gern! Und du?", [
    ["很喜欢！你吗？", "Sehr gern! Du?", "Zurückfragen geht mit 呢, nicht mit 吗: 你呢？"],
    ["很喜欢！你是呢？", "Sehr gern! Du bist und?", "Kurz und ohne Verb: 你呢？"]]],
  ["a", "我很喜欢德国菜！", "Ich mag deutsches Essen sehr!"],
  ["me", "德国菜和中国菜都很好吃！", "Deutsches und chinesisches Essen sind beide lecker!", [
    ["德国菜都中国菜很好吃！", "Deutsches alle chinesisches Essen lecker!", "和 verbindet die beiden Nomen. 都 steht danach, vor 很."],
    ["德国菜和中国菜很都好吃！", "Deutsches und chinesisches Essen sehr alle lecker!", "都 steht vor 很: 都很好吃."]], "Du findest beides lecker."],
  ["a", "认识你很高兴！", "Schön, dich kennenzulernen!"],
  ["me", "认识你很高兴！", "Schön, dich kennenzulernen!", [
    ["认识你是高兴！", "Dich kennen ist froh!", "Vor einem Adjektiv steht kein 是, sondern 很."],
    ["不客气！", "Gern geschehen!", "不客气 antwortet auf ein Danke. Hier sagst du einfach dasselbe zurück."]]],
  ["a", "明天我们去饭店，好吗？", "Morgen gehen wir ins Restaurant, okay?"],
  ["me", "好！谢谢！", "Gern! Danke!", [
    ["好！我们去酒店。", "Gern! Wir gehen ins Hotel.", "Ins Restaurant heißt 饭店. 酒店 ist das Hotel."],
    ["不客气！", "Gern geschehen!", "Er lädt dich ein. Du bedankst dich: 谢谢."]]]
]},
u15: {title:"Ein Anruf am Abend", who:{zh:"李娜", py:"Lǐ Nà", de:"Li Na, am Telefon"}, lines:[
  ["a", "喂？", "Hallo?"],
  ["me", "喂，你好！我是弗洛里安。", "Hallo! Ich bin's, Florian.", [
    ["喂，你好！你是弗洛里安。", "Hallo! Du bist Florian.", "Du bist Florian, also 我是."],
    ["再见！", "Tschüss!", "Das Gespräch fängt gerade erst an."]]],
  ["a", "你好！你在看电视吗？", "Hallo! Schaust du gerade fern?"],
  ["me", "不是，我在看电影。", "Nein, ich schaue gerade einen Film.", [
    ["不是，我在电影。", "Nein, ich bin im Film.", "Da fehlt das Verb. »Gerade einen Film schauen« heißt 在看电影."],
    ["是，我在睡觉。", "Ja, ich schlafe gerade.", "Dann könntest du nicht telefonieren. Und sie fragte nach dem Fernsehen."]], "Du schaust gerade einen Film, nicht fern."],
  ["a", "什么电影？", "Was für ein Film?"],
  ["me", "中国电影。我很喜欢。", "Ein chinesischer Film. Er gefällt mir sehr."],
  ["a", "明天我们看电影，好吗？", "Wollen wir morgen einen Film schauen?"],
  ["me", "好！明天几点？", "Gern! Um wie viel Uhr morgen?", [
    ["好！昨天几点？", "Gern! Um wie viel Uhr gestern?", "Ihr verabredet euch für morgen (明天), nicht gestern."],
    ["我能睡觉吗？", "Darf ich schlafen?", "Sie hat dich zum Film eingeladen."]]],
  ["a", "下午三点。", "Um drei Uhr nachmittags."],
  ["me", "下午三点我不能去。中午，好吗？", "Um drei kann ich nicht. Mittags, geht das?", [
    ["下午三点我不会去。", "Um drei kann ich das nicht.", "不会 heißt »nicht können, weil man es nicht gelernt hat«. Wenn es zeitlich nicht klappt, sagt man 不能."],
    ["我去不能下午三点。", "Ich gehe nicht kann um drei.", "Die Zeit steht vorne, 不能 direkt vor dem Verb: 下午三点我不能去."]], "Um drei hast du keine Zeit. Du schlägst mittags vor."],
  ["a", "好，中午十二点。", "Gut, um zwölf Uhr mittags."],
  ["me", "好！现在我想睡觉。再见！", "Gut! Jetzt will ich schlafen. Tschüss!"],
  ["a", "再见！", "Tschüss!"]
]},
u16: {title:"Ein Hund im Park", who:{zh:"张先生", py:"Zhāng xiān_sheng", de:"Herr Zhang mit Hund"}, lines:[
  ["me", "对不起！", "Entschuldigung!", [
    ["没关系！", "Macht nichts!", "Du hast ihn angerempelt. 没关系 sagt der andere."],
    ["不客气！", "Gern geschehen!", "Das sagt man auf ein Danke."]], "Du bist aus Versehen gegen einen Mann gelaufen."],
  ["a", "没关系。你看见我的狗了吗？", "Macht nichts. Hast du meinen Hund gesehen?"],
  ["me", "我没有看见你的狗。", "Ich habe deinen Hund nicht gesehen.", [
    ["我没有看见你的狗了。", "Ich habe deinen Hund nicht gesehen (mit 了).", "Mit 没有 fällt 了 weg."],
    ["我不看见你的狗。", "Ich sehe deinen Hund nicht.", "Was nicht passiert ist, verneint man mit 没有, nicht mit 不."]], "Den Hund hast du nicht gesehen."],
  ["a", "我的狗在那里！", "Da ist mein Hund!"],
  ["me", "你的狗很漂亮！", "Dein Hund ist sehr schön!"],
  ["a", "谢谢！", "Danke!"],
  ["me", "不客气！", "Gern geschehen!", [
    ["没关系！", "Macht nichts!", "没关系 antwortet auf eine Entschuldigung, nicht auf ein Danke."],
    ["对不起！", "Entschuldigung!", "Er bedankt sich. Darauf sagt man 不客气."]]],
  ["a", "你是学生吗？", "Bist du Student?"],
  ["me", "是，我在这里学习汉语。你呢？", "Ja, ich lerne hier Chinesisch. Und du?", [
    ["是，我学习汉语在这里。你呢？", "Ja, ich lerne Chinesisch hier. Und du?", "Wo man etwas tut, steht mit 在 vor dem Verb: 在这里学习."],
    ["不是，我是学生。你呢？", "Nein, ich bin Student. Und du?", "Erst nein und dann ja, das passt nicht zusammen."]], "Du lernst hier Chinesisch und fragst zurück."],
  ["a", "我是医生。我在医院工作。医院在那里，坐出租车十分钟。", "Ich bin Arzt. Ich arbeite im Krankenhaus. Es ist dort drüben, mit dem Taxi zehn Minuten."],
  ["me", "你几点去医院？", "Um wie viel Uhr gehst du ins Krankenhaus?", [
    ["你去医院几点？", "Du gehst ins Krankenhaus um wie viel Uhr?", "Die Uhrzeit steht vor dem Verb: 几点去."],
    ["你几点去医生？", "Um wie viel Uhr gehst du zum Arzt?", "医生 ist der Arzt, 医院 das Krankenhaus. Er arbeitet im 医院."]], "Du fragst, wann er ins Krankenhaus geht."],
  ["a", "下午三点。再见！", "Um drei Uhr nachmittags. Tschüss!"],
  ["me", "再见！", "Tschüss!"]
]},
u17: {title:"Abschied am Flughafen", who:{zh:"李娜", py:"Lǐ Nà", de:"Li Na"}, lines:[
  ["a", "你什么时候回德国？", "Wann fliegst du zurück nach Deutschland?"],
  ["me", "我今天回德国。", "Ich fliege heute zurück nach Deutschland.", [
    ["我回德国今天。", "Ich fliege zurück nach Deutschland heute.", "Die Zeit steht vor dem Verb: 我今天回德国."],
    ["昨天我回德国。", "Gestern flog ich zurück.", "Du stehst noch am Flughafen. Gestern passt nicht."]], "Dein Flug geht heute."],
  ["a", "你几点的飞机？", "Um wie viel Uhr geht dein Flug?"],
  ["me", "下午四点的飞机。", "Mein Flug geht um vier Uhr nachmittags.", [
    ["下午四点飞机的。", "Vier Uhr nachmittags Flug von.", "的 steht zwischen Uhrzeit und Flugzeug: 四点的飞机."],
    ["下午四个点的飞机。", "Um vier Stück Uhr.", "Bei der Uhrzeit steht kein 个: 四点."]], "Dein Flug geht um 16 Uhr."],
  ["a", "你喜欢中国吗？", "Gefällt dir China?"],
  ["me", "很喜欢！我想住在中国。", "Sehr! Ich möchte in China wohnen.", [
    ["很喜欢！我想在住中国。", "Sehr! Ich möchte in wohnen China.", "Bei 住 steht 在 mit dem Ort dahinter: 住在中国."],
    ["很喜欢！我想住中国在。", "Sehr! Ich möchte wohnen China in.", "在 steht vor dem Ort, nicht dahinter."]]],
  ["a", "你什么时候来北京？", "Wann kommst du nach Peking?"],
  ["me", "下个月我来北京！", "Nächsten Monat komme ich nach Peking!", [
    ["我来北京下个月。", "Ich komme nach Peking nächsten Monat.", "Auch hier: Die Zeit steht vor dem Verb."],
    ["我住在北京。", "Ich wohne in Peking.", "Sie fragt, wann du kommst."]], "Du kommst nächsten Monat nach Peking."],
  ["a", "太好了！请来我家！", "Super! Komm mich bitte besuchen!"],
  ["me", "好！谢谢！", "Gern! Danke!", [
    ["不客气！", "Gern geschehen!", "Sie lädt dich ein. Du bedankst dich: 谢谢."],
    ["没关系！", "Macht nichts!", "没关系 antwortet auf eine Entschuldigung."]]],
  ["a", "再见！", "Tschüss!"],
  ["me", "谢谢！再见！", "Danke! Tschüss!", [
    ["你好！", "Hallo!", "Ihr verabschiedet euch, also 再见."],
    ["对不起！", "Entschuldigung!", "Du musst dich für nichts entschuldigen."]]]
]}
};
