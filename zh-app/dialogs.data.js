/* Kleine Gespräche, eins pro Ort. Nur Wörter, die bis zum Ende der Etappe gelernt sind (plus Namen).
   Erzeugt mit scripts/build_dialogs.js aus scripts/dialogs_src.js. s: "a" = Gesprächspartner, "me" = Florian.
   Zeilen mit alt: Florian wählt seine Antwort, alt sind die falschen Möglichkeiten mit Begründung. */
window.ZH_DIALOGS = {
  u1: {title:"Am Flughafen", who:{zh:"李娜", py:"Lǐ Nà", de:"Li Na, eine Studentin, die dich abholt"}, lines:[
    {s:"a", zh:"你好！是你吗？", py:"Nǐ_hǎo! Shì nǐ ma?", de:"Hallo! Bist du's?"},
    {s:"me", zh:"是我！你好！", py:"Shì wǒ! Nǐ_hǎo!", de:"Ja, ich bin's! Hallo!", alt:[
      {zh:"不是我。", py:"Bú shì wǒ.", de:"Ich bin's nicht.", why:"Sie holt dich ab, du bist es ja."},
      {zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!", why:"Ihr habt euch gerade erst getroffen."}]},
    {s:"a", zh:"你好吗？", py:"Nǐ_hǎo ma?", de:"Wie geht's dir?"},
    {s:"me", zh:"我很好，谢谢！你好吗？", py:"Wǒ hěn hǎo, xiè_xie! Nǐ_hǎo ma?", de:"Mir geht's gut, danke! Und dir?", alt:[
      {zh:"我很好吗？", py:"Wǒ hěn hǎo ma?", de:"Geht es mir gut?", why:"吗 macht aus dem Satz eine Frage. Du sollst aber antworten."},
      {zh:"不是。", py:"Bú shì.", de:"Nein, ist es nicht.", why:"Sie fragt, wie es dir geht. 不是 passt nicht zu dieser Frage."}]},
    {s:"a", zh:"我很好！", py:"Wǒ hěn hǎo!", de:"Mir geht's gut!"},
    {s:"a", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"},
    {s:"me", zh:"再见！谢谢！", py:"Zài_jiàn! Xiè_xie!", de:"Tschüss! Danke!", alt:[
      {zh:"你好！", py:"Nǐ_hǎo!", de:"Hallo!", why:"Sie verabschiedet sich. Darauf sagt man auch 再见."},
      {zh:"我很好。", py:"Wǒ hěn hǎo.", de:"Mir geht's gut.", why:"Das hast du schon gesagt. Jetzt geht es ums Verabschieden."}]}
  ]},
  u2: {title:"Neue Nachbarn", who:{zh:"王爷爷", py:"Wáng yé_ye", de:"Opa Wang, ein Nachbar"}, lines:[
    {s:"a", zh:"你好！你叫什么名字？", py:"Nǐ_hǎo! Nǐ jiào shén_me míng_zi?", de:"Hallo! Wie heißt du?"},
    {s:"me", zh:"我叫弗洛里安。", py:"Wǒ jiào Fú_luò_lǐ_'ān.", de:"Ich heiße Florian.", alt:[
      {zh:"我是中国人。", py:"Wǒ shì Zhōng_guó rén.", de:"Ich bin Chinese.", why:"Er fragt nach deinem Namen, nicht nach dem Land."},
      {zh:"他叫什么？", py:"Tā jiào shén_me?", de:"Wie heißt er?", why:"Er hat dich gefragt. Antworte mit 我叫 …"}]},
    {s:"a", zh:"弗洛里安，你好！你是哪国人？", py:"Fú_luò_lǐ_'ān, nǐ_hǎo! Nǐ shì nǎ guó rén?", de:"Florian, hallo! Aus welchem Land kommst du?"},
    {s:"me", zh:"我是德国人。", py:"Wǒ shì Dé_guó rén.", de:"Ich bin Deutscher.", alt:[
      {zh:"我是德国。", py:"Wǒ shì Dé_guó.", de:"Ich bin Deutschland.", why:"德国 ist das Land. Für den Menschen kommt 人 dahinter: 德国人."},
      {zh:"你是哪国人？", py:"Nǐ shì nǎ guó rén?", de:"Aus welchem Land kommst du?", why:"Erst antworten, dann zurückfragen."}]},
    {s:"me", zh:"你是中国人吗？", py:"Nǐ shì Zhōng_guó rén ma?", de:"Sind Sie Chinese?", alt:[
      {zh:"你是哪国人吗？", py:"Nǐ shì nǎ guó rén ma?", de:"Aus welchem Land kommen Sie?", why:"Mit einem Fragewort wie 哪 steht kein 吗 am Ende."},
      {zh:"你是中国吗？", py:"Nǐ shì Zhōng_guó ma?", de:"Sind Sie China?", why:"Auch hier fehlt 人: 中国人."}]},
    {s:"a", zh:"是，我是中国人。", py:"Shì, wǒ shì Zhōng_guó rén.", de:"Ja, ich bin Chinese."},
    {s:"me", zh:"他叫什么名字？", py:"Tā jiào shén_me míng_zi?", de:"Wie heißt er?", cue:"Ein Junge läuft vorbei. Du willst wissen, wie er heißt.", alt:[
      {zh:"他是什么名字？", py:"Tā shì shén_me míng_zi?", de:"Er ist welcher Name?", why:"Nach dem Namen fragt man mit 叫: 他叫什么名字？"},
      {zh:"她叫什么名字？", py:"Tā jiào shén_me míng_zi?", de:"Wie heißt sie?", why:"Es geht um einen Jungen, also 他. Gesprochen klingen 他 und 她 gleich, nur die Schrift ist anders."}]},
    {s:"a", zh:"他叫小明。", py:"Tā jiào Xiǎo_Míng.", de:"Er heißt Xiao Ming."},
    {s:"a", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"},
    {s:"me", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!", alt:[
      {zh:"你好！", py:"Nǐ_hǎo!", de:"Hallo!", why:"Er verabschiedet sich. Darauf sagt man auch 再见."},
      {zh:"我叫弗洛里安。", py:"Wǒ jiào Fú_luò_lǐ_'ān.", de:"Ich heiße Florian.", why:"Das weiß er schon. Jetzt sagt ihr Tschüss."}]}
  ]},
  u3: {title:"Wachtürme zählen", who:{zh:"小明", py:"Xiǎo Míng", de:"Xiao Ming, ein Junge auf der Mauer"}, lines:[
    {s:"a", zh:"你好！我叫小明。你叫什么名字？", py:"Nǐ_hǎo! Wǒ jiào Xiǎo_Míng. Nǐ jiào shén_me míng_zi?", de:"Hallo! Ich heiße Xiao Ming. Wie heißt du?"},
    {s:"me", zh:"我叫弗洛里安。", py:"Wǒ jiào Fú_luò_lǐ_'ān.", de:"Ich heiße Florian.", alt:[
      {zh:"我叫小明。", py:"Wǒ jiào Xiǎo_Míng.", de:"Ich heiße Xiao Ming.", why:"So heißt er. Du sagst deinen eigenen Namen."},
      {zh:"你好吗？", py:"Nǐ_hǎo ma?", de:"Wie geht's dir?", why:"Er hat nach deinem Namen gefragt."}]},
    {s:"a", zh:"一、二、三……", py:"Yī, èr, sān …", de:"Eins, zwei, drei …"},
    {s:"me", zh:"四、五、六！", py:"Sì, wǔ, liù!", de:"Vier, fünf, sechs!", alt:[
      {zh:"三、二、一！", py:"Sān, èr, yī!", de:"Drei, zwei, eins!", why:"Er zählt nach oben. Nach 三 kommt 四."},
      {zh:"七、八、九！", py:"Qī, bā, jiǔ!", de:"Sieben, acht, neun!", why:"Da fehlen 四, 五 und 六."}]},
    {s:"a", zh:"七、八……", py:"Qī, bā …", de:"Sieben, acht …"},
    {s:"me", zh:"九、十！", py:"Jiǔ, shí!", de:"Neun, zehn!", alt:[
      {zh:"六、七！", py:"Liù, qī!", de:"Sechs, sieben!", why:"Die hatten wir schon. Nach 八 kommt 九."},
      {zh:"十、九！", py:"Shí, jiǔ!", de:"Zehn, neun!", why:"Falsche Reihenfolge: erst 九, dann 十."}]},
    {s:"a", zh:"很好！", py:"Hěn hǎo!", de:"Sehr gut!"},
    {s:"me", zh:"谢谢！", py:"Xiè_xie!", de:"Danke!", alt:[
      {zh:"不是。", py:"Bú shì.", de:"Nein, ist es nicht.", why:"Er lobt dich. Darauf sagt man 谢谢."},
      {zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!", why:"Ihr seid noch nicht fertig. Auf ein Lob sagt man 谢谢."}]},
    {s:"a", zh:"你是中国人吗？", py:"Nǐ shì Zhōng_guó rén ma?", de:"Bist du Chinese?"},
    {s:"me", zh:"不是，我是德国人。", py:"Bú shì, wǒ shì Dé_guó rén.", de:"Nein, ich bin Deutscher.", alt:[
      {zh:"是，我是德国人。", py:"Shì, wǒ shì Dé_guó rén.", de:"Ja, ich bin Deutscher.", why:"Du bist kein Chinese. Auf die Frage antwortest du deshalb mit 不是."},
      {zh:"不是，我不是德国人。", py:"Bú shì, wǒ bú shì Dé_guó rén.", de:"Nein, ich bin kein Deutscher.", why:"Doch, du bist Deutscher. Nur 中国人 bist du nicht."}]},
    {s:"a", zh:"德国很好！再见！", py:"Dé_guó hěn hǎo! Zài_jiàn!", de:"Deutschland ist toll! Tschüss!"},
    {s:"me", zh:"再见，小明！", py:"Zài_jiàn, Xiǎo_Míng!", de:"Tschüss, Xiao Ming!"}
  ]},
  u4: {title:"Im Teehaus bestellen", who:{zh:"服务员", py:"fú_wù_yuán", de:"die Bedienung"}, lines:[
    {s:"a", zh:"你好！你要什么？", py:"Nǐ_hǎo! Nǐ yào shén_me?", de:"Hallo! Was möchtest du?"},
    {s:"me", zh:"我要茶。", py:"Wǒ yào chá.", de:"Ich möchte Tee.", alt:[
      {zh:"你要什么？", py:"Nǐ yào shén_me?", de:"Was möchtest du?", why:"Sie hat dich gefragt. Antworte mit 我要 …"},
      {zh:"我喜欢德国。", py:"Wǒ xǐ_huan Dé_guó.", de:"Ich mag Deutschland.", why:"Schön, aber sie will wissen, was du bestellst."}]},
    {s:"a", zh:"你喜欢喝咖啡吗？", py:"Nǐ xǐ_huan hē kā_fēi ma?", de:"Trinkst du gern Kaffee?"},
    {s:"me", zh:"不喜欢。我喜欢喝茶。", py:"Bù xǐ_huan. Wǒ xǐ_huan hē chá.", de:"Nicht so. Ich trinke gern Tee.", cue:"Kaffee magst du nicht so, Tee schon.", alt:[
      {zh:"不喜欢。我喜欢吃茶。", py:"Bù xǐ_huan. Wǒ xǐ_huan chī chá.", de:"Nicht so. Ich esse gern Tee.", why:"Tee trinkt man: 喝茶, nicht 吃."},
      {zh:"我不喜欢喝咖啡吗？", py:"Wǒ bù xǐ_huan hē kā_fēi ma?", de:"Trinke ich nicht gern Kaffee?", why:"Mit 吗 wird es eine Frage. Du sollst aber antworten."}]},
    {s:"a", zh:"好！你吃什么？", py:"Hǎo! Nǐ chī shén_me?", de:"Gut! Was isst du?"},
    {s:"me", zh:"我要米饭。", py:"Wǒ yào mǐ_fàn.", de:"Ich möchte Reis.", cue:"Du möchtest Reis.", alt:[
      {zh:"我喝米饭。", py:"Wǒ hē mǐ_fàn.", de:"Ich trinke Reis.", why:"Reis isst man: 吃, nicht 喝. Beim Bestellen sagt man einfach 我要 …"},
      {zh:"我很好。", py:"Wǒ hěn hǎo.", de:"Mir geht's gut.", why:"Sie fragt nach dem Essen."}]},
    {s:"a", zh:"你喝水吗？", py:"Nǐ hē shuǐ ma?", de:"Trinkst du Wasser?"},
    {s:"me", zh:"不喝，谢谢。", py:"Bù hē, xiè_xie.", de:"Nein, danke.", cue:"Wasser möchtest du nicht.", alt:[
      {zh:"不是，谢谢。", py:"Bú shì, xiè_xie.", de:"Nein, ist es nicht, danke.", why:"Auf eine Frage mit Verb antwortet man mit dem Verb: 喝 (ja) oder 不喝 (nein). Ein eigenes Wort für »nein« gibt es nicht."},
      {zh:"我不喜欢茶。", py:"Wǒ bù xǐ_huan chá.", de:"Ich mag keinen Tee.", why:"Du hast gerade Tee bestellt."}]},
    {s:"a", zh:"好吃吗？", py:"Hǎo_chī ma?", de:"Schmeckt es?"},
    {s:"me", zh:"很好吃！", py:"Hěn hǎo_chī!", de:"Sehr lecker!", alt:[
      {zh:"我要茶。", py:"Wǒ yào chá.", de:"Ich möchte Tee.", why:"Den Tee hast du schon. Sie fragt, ob es schmeckt."},
      {zh:"不是。", py:"Bú shì.", de:"Nein, ist es nicht.", why:"Auf 好吃吗？ antwortet man mit 好吃 oder 不好吃."}]},
    {s:"a", zh:"谢谢！你喜欢中国菜吗？", py:"Xiè_xie! Nǐ xǐ_huan Zhōng_guó cài ma?", de:"Danke! Magst du chinesisches Essen?"},
    {s:"me", zh:"我很喜欢中国菜！", py:"Wǒ hěn xǐ_huan Zhōng_guó cài!", de:"Ich mag chinesisches Essen sehr!", alt:[
      {zh:"我很好吃中国菜！", py:"Wǒ hěn hǎo_chī Zhōng_guó cài!", de:"Ich lecker chinesisches Essen!", why:"好吃 heißt lecker. Mögen heißt 喜欢: 我很喜欢中国菜."},
      {zh:"是，我是中国菜。", py:"Shì, wǒ shì Zhōng_guó cài.", de:"Ja, ich bin chinesisches Essen.", why:"Mit 是 sagst du, was du bist. Hier brauchst du 喜欢."}]},
    {s:"a", zh:"谢谢！再见！", py:"Xiè_xie! Zài_jiàn!", de:"Danke! Tschüss!"},
    {s:"me", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"}
  ]},
  u5: {title:"Handeln auf dem Markt", who:{zh:"阿姨", py:"ā_yí", de:"eine Händlerin"}, lines:[
    {s:"a", zh:"你好！你要什么？", py:"Nǐ_hǎo! Nǐ yào shén_me?", de:"Hallo! Was möchtest du?"},
    {s:"me", zh:"这个多少钱？", py:"Zhè_ge duō_shao qián?", de:"Wie viel kostet das?", alt:[
      {zh:"这个太贵了！", py:"Zhè_ge tài guì le!", de:"Das ist zu teuer!", why:"Du kennst den Preis noch gar nicht. Frag erst mit 多少钱."},
      {zh:"你好吗？", py:"Nǐ_hǎo ma?", de:"Wie geht's dir?", why:"Freundlich, aber du willst den Preis wissen."}]},
    {s:"a", zh:"十块。", py:"Shí kuài.", de:"Zehn Kuai."},
    {s:"me", zh:"太贵了！", py:"Tài guì le!", de:"Zu teuer!", alt:[
      {zh:"很好吃！", py:"Hěn hǎo_chī!", de:"Sehr lecker!", why:"Es geht um den Preis, nicht ums Essen."},
      {zh:"我没有钱。", py:"Wǒ méi_yǒu qián.", de:"Ich habe kein Geld.", why:"Das stimmt hoffentlich nicht. Zum Handeln sagt man 太贵了."}]},
    {s:"a", zh:"那个五块。", py:"Nà_ge wǔ kuài.", de:"Das da kostet fünf Kuai."},
    {s:"me", zh:"我要那个。", py:"Wǒ yào nà_ge.", de:"Ich nehme das da.", alt:[
      {zh:"那个多少钱？", py:"Nà_ge duō_shao qián?", de:"Wie viel kostet das da?", why:"Den Preis hat sie gerade gesagt: 五块."},
      {zh:"太贵了！", py:"Tài guì le!", de:"Zu teuer!", why:"Fünf Kuai sind ein guter Preis."}]},
    {s:"a", zh:"我有茶。你喝茶吗？", py:"Wǒ yǒu chá. Nǐ hē chá ma?", de:"Ich habe Tee. Trinkst du Tee?"},
    {s:"me", zh:"有咖啡吗？", py:"Yǒu kā_fēi ma?", de:"Gibt es Kaffee?", cue:"Du hättest lieber einen Kaffee.", alt:[
      {zh:"你不有咖啡吗？", py:"Nǐ bù yǒu kā_fēi ma?", de:"Hast du nicht Kaffee?", why:"有 verneint man nie mit 不, immer mit 没: 没有."},
      {zh:"我没有咖啡。", py:"Wǒ méi_yǒu kā_fēi.", de:"Ich habe keinen Kaffee.", why:"Du willst wissen, ob sie Kaffee hat. Dann fragst du: 有咖啡吗？"}]},
    {s:"a", zh:"没有咖啡，有茶。", py:"Méi_yǒu kā_fēi, yǒu chá.", de:"Kaffee gibt es nicht, nur Tee."},
    {s:"me", zh:"一杯茶多少钱？", py:"Yì bēi chá duō_shao qián?", de:"Was kostet eine Tasse Tee?", cue:"Dann eben Tee. Du willst wissen, was eine Tasse kostet.", alt:[
      {zh:"一茶多少钱？", py:"Yì chá duō_shao qián?", de:"Was kostet ein Tee?", why:"Zwischen Zahl und Nomen steht immer ein Zählwort: 一杯茶."},
      {zh:"一杯茶太贵了！", py:"Yì bēi chá tài guì le!", de:"Eine Tasse Tee ist zu teuer!", why:"Du kennst den Preis noch nicht."}]},
    {s:"a", zh:"三块。", py:"Sān kuài.", de:"Drei Kuai."},
    {s:"me", zh:"好，我要一杯茶。", py:"Hǎo, wǒ yào yì bēi chá.", de:"Gut, ich nehme eine Tasse Tee.", alt:[
      {zh:"好，我有一杯茶。", py:"Hǎo, wǒ yǒu yì bēi chá.", de:"Gut, ich habe eine Tasse Tee.", why:"有 heißt haben. Kaufen willst du: 我要 …"},
      {zh:"好，我要三杯钱。", py:"Hǎo, wǒ yào sān bēi qián.", de:"Gut, ich will drei Tassen Geld.", why:"杯 zählt Tassen, nicht Geld. Du willst einen Tee: 一杯茶."}]},
    {s:"a", zh:"那个五块，茶三块。八块钱。", py:"Nà_ge wǔ kuài, chá sān kuài. Bā kuài qián.", de:"Das da fünf, der Tee drei. Acht Kuai."},
    {s:"me", zh:"好，谢谢！", py:"Hǎo, xiè_xie!", de:"Gut, danke!"},
    {s:"a", zh:"谢谢！再见！", py:"Xiè_xie! Zài_jiàn!", de:"Danke! Tschüss!"}
  ]},
  u6: {title:"Ankunft am Bahnhof", who:{zh:"乘客", py:"chéng_kè", de:"ein Mitreisender"}, lines:[
    {s:"a", zh:"你好！你去哪里？", py:"Nǐ_hǎo! Nǐ qù nǎ_lǐ?", de:"Hallo! Wohin fährst du?"},
    {s:"me", zh:"我想去酒店。", py:"Wǒ xiǎng qù jiǔ_diàn.", de:"Ich möchte zum Hotel.", alt:[
      {zh:"我是酒店。", py:"Wǒ shì jiǔ_diàn.", de:"Ich bin das Hotel.", why:"是 heißt »sein« im Sinn von »gleich sein«. Für ein Ziel nimmt man 去."},
      {zh:"我想去在酒店。", py:"Wǒ xiǎng qù zài jiǔ_diàn.", de:"Ich möchte gehen in Hotel.", why:"Hinter 去 steht das Ziel direkt, ohne 在."}]},
    {s:"a", zh:"酒店在那里。", py:"Jiǔ_diàn zài nà_lǐ.", de:"Das Hotel ist dort."},
    {s:"me", zh:"谢谢！地铁在哪里？", py:"Xiè_xie! Dì_tiě zài nǎ_lǐ?", de:"Danke! Wo ist die U-Bahn?", alt:[
      {zh:"谢谢！地铁在那里。", py:"Xiè_xie! Dì_tiě zài nà_lǐ.", de:"Danke! Die U-Bahn ist dort.", why:"Du willst etwas wissen. Für die Frage brauchst du 哪里 (wo), nicht 那里 (dort)."},
      {zh:"谢谢！你在哪里？", py:"Xiè_xie! Nǐ zài nǎ_lǐ?", de:"Danke! Wo bist du?", why:"Er steht ja neben dir. Du suchst die U-Bahn."}]},
    {s:"a", zh:"地铁在这里。你想喝水吗？我有水。", py:"Dì_tiě zài zhè_lǐ. Nǐ xiǎng hē shuǐ ma? Wǒ yǒu shuǐ.", de:"Die U-Bahn ist hier. Möchtest du Wasser? Ich habe Wasser."},
    {s:"me", zh:"不喝，谢谢。厕所在哪里？", py:"Bù hē, xiè_xie. Cè_suǒ zài nǎ_lǐ?", de:"Nein, danke. Wo ist die Toilette?", cue:"Wasser möchtest du nicht, aber du suchst die Toilette.", alt:[
      {zh:"不喝，谢谢。厕所在那里？", py:"Bù hē, xiè_xie. Cè_suǒ zài nà_lǐ?", de:"Nein, danke. Die Toilette ist dort?", why:"Du suchst die Toilette. Gefragt wird mit 哪里 (wo), nicht mit 那里 (dort)."},
      {zh:"不喝，谢谢。我在厕所。", py:"Bù hē, xiè_xie. Wǒ zài cè_suǒ.", de:"Nein, danke. Ich bin auf der Toilette.", why:"我在厕所 heißt »Ich bin auf der Toilette«. Du willst wissen, wo sie ist."}]},
    {s:"a", zh:"厕所在那里。", py:"Cè_suǒ zài nà_lǐ.", de:"Die Toilette ist dort."},
    {s:"me", zh:"谢谢！你去哪里？", py:"Xiè_xie! Nǐ qù nǎ_lǐ?", de:"Danke! Wohin fährst du?", alt:[
      {zh:"谢谢！你去哪里吗？", py:"Xiè_xie! Nǐ qù nǎ_lǐ ma?", de:"Danke! Wohin fährst du ja?", why:"Mit einem Fragewort wie 哪里 steht kein 吗 am Ende."},
      {zh:"谢谢！你在哪里？", py:"Xiè_xie! Nǐ zài nǎ_lǐ?", de:"Danke! Wo bist du?", why:"Er steht neben dir. Du willst wissen, wohin er fährt: 去哪里."}]},
    {s:"a", zh:"我去火车站。我想喝咖啡。", py:"Wǒ qù huǒ_chē_zhàn. Wǒ xiǎng hē kā_fēi.", de:"Ich gehe zum Bahnhof. Ich möchte einen Kaffee trinken."},
    {s:"me", zh:"火车站有咖啡吗？", py:"Huǒ_chē_zhàn yǒu kā_fēi ma?", de:"Gibt es am Bahnhof Kaffee?", cue:"Du fragst, ob es am Bahnhof Kaffee gibt.", alt:[
      {zh:"火车站是咖啡吗？", py:"Huǒ_chē_zhàn shì kā_fēi ma?", de:"Ist der Bahnhof Kaffee?", why:"Ob es etwas gibt, fragt man mit 有: Ort + 有 + Ding."},
      {zh:"火车站不有咖啡吗？", py:"Huǒ_chē_zhàn bù yǒu kā_fēi ma?", de:"Hat der Bahnhof nicht Kaffee?", why:"有 verneint man nie mit 不."}]},
    {s:"a", zh:"有！再见！", py:"Yǒu! Zài_jiàn!", de:"Ja! Tschüss!"},
    {s:"me", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"}
  ]},
  u7: {title:"Uhrzeit am Bund", who:{zh:"摄影师", py:"shè_yǐng_shī", de:"ein Fotograf"}, lines:[
    {s:"me", zh:"你好！现在几点？", py:"Nǐ_hǎo! Xiàn_zài jǐ diǎn?", de:"Hallo! Wie spät ist es?", cue:"Du willst wissen, wie spät es ist.", alt:[
      {zh:"你好！你什么时候去？", py:"Nǐ_hǎo! Nǐ shén_me shí_hou qù?", de:"Hallo! Wann gehst du?", why:"Du willst die Uhrzeit wissen. Die Frage dafür ist 现在几点？"},
      {zh:"你好！现在三点。", py:"Nǐ_hǎo! Xiàn_zài sān diǎn.", de:"Hallo! Es ist drei Uhr.", why:"Das ist eine Antwort. Du willst aber fragen."}]},
    {s:"a", zh:"现在下午三点。", py:"Xiàn_zài xià_wǔ sān diǎn.", de:"Es ist drei Uhr nachmittags."},
    {s:"a", zh:"你什么时候去酒店？", py:"Nǐ shén_me shí_hou qù jiǔ_diàn?", de:"Wann gehst du ins Hotel?"},
    {s:"me", zh:"我晚上去酒店。", py:"Wǒ wǎn_shang qù jiǔ_diàn.", de:"Ich gehe abends ins Hotel.", alt:[
      {zh:"我去酒店晚上。", py:"Wǒ qù jiǔ_diàn wǎn_shang.", de:"Ich gehe ins Hotel abends.", why:"Die Zeit steht vor dem Verb, nie am Ende: 我晚上去酒店."},
      {zh:"现在三点。", py:"Xiàn_zài sān diǎn.", de:"Es ist drei Uhr.", why:"Er fragt, wann du ins Hotel gehst."}]},
    {s:"a", zh:"晚上几点？", py:"Wǎn_shang jǐ diǎn?", de:"Um wie viel Uhr am Abend?"},
    {s:"me", zh:"晚上八点。", py:"Wǎn_shang bā diǎn.", de:"Um acht Uhr abends.", cue:"Du gehst um acht Uhr abends.", alt:[
      {zh:"八点晚上。", py:"Bā diǎn wǎn_shang.", de:"Acht Uhr abends.", why:"Vom Großen zum Kleinen: erst 晚上, dann 八点."},
      {zh:"晚上八块。", py:"Wǎn_shang bā kuài.", de:"Abends acht Kuai.", why:"块 ist Geld. Die Uhrzeit sagt man mit 点."}]},
    {s:"a", zh:"明天你去哪里？", py:"Míng_tiān nǐ qù nǎ_lǐ?", de:"Wohin gehst du morgen?"},
    {s:"me", zh:"明天我去火车站。", py:"Míng_tiān wǒ qù huǒ_chē_zhàn.", de:"Morgen gehe ich zum Bahnhof.", alt:[
      {zh:"昨天我去火车站。", py:"Zuó_tiān wǒ qù huǒ_chē_zhàn.", de:"Gestern ging ich zum Bahnhof.", why:"Er fragt nach morgen (明天), nicht nach gestern (昨天)."},
      {zh:"火车站在哪里？", py:"Huǒ_chē_zhàn zài nǎ_lǐ?", de:"Wo ist der Bahnhof?", why:"Er will wissen, wohin du gehst."}]},
    {s:"a", zh:"你几点去火车站？", py:"Nǐ jǐ diǎn qù huǒ_chē_zhàn?", de:"Um wie viel Uhr gehst du zum Bahnhof?"},
    {s:"me", zh:"上午十点。", py:"Shàng_wǔ shí diǎn.", de:"Um zehn Uhr vormittags.", cue:"Du gehst um zehn Uhr vormittags.", alt:[
      {zh:"下午十点。", py:"Xià_wǔ shí diǎn.", de:"Zehn Uhr nachmittags.", why:"Zehn Uhr nachmittags gibt es nicht. Vormittags heißt 上午, nachmittags 下午."},
      {zh:"十点上午。", py:"Shí diǎn shàng_wǔ.", de:"Zehn Uhr vormittags.", why:"Vom Großen zum Kleinen: erst 上午, dann 十点."}]},
    {s:"a", zh:"好！再见！", py:"Hǎo! Zài_jiàn!", de:"Gut! Tschüss!"},
    {s:"me", zh:"谢谢！再见！", py:"Xiè_xie! Zài_jiàn!", de:"Danke! Tschüss!"}
  ]},
  u8: {title:"Plaudern am Kanal", who:{zh:"船娘", py:"chuán_niáng", de:"eine Bootsfrau"}, lines:[
    {s:"a", zh:"你好！你会说汉语吗？", py:"Nǐ_hǎo! Nǐ huì shuō Hàn_yǔ ma?", de:"Hallo! Kannst du Chinesisch?"},
    {s:"me", zh:"我会说一点汉语。", py:"Wǒ huì shuō yì_diǎn Hàn_yǔ.", de:"Ich kann ein bisschen Chinesisch.", alt:[
      {zh:"我会汉语说一点。", py:"Wǒ huì Hàn_yǔ shuō yì_diǎn.", de:"Ich kann Chinesisch sprechen ein bisschen.", why:"Das Verb 说 kommt direkt nach 会, dann 一点 und die Sprache: 会说一点汉语."},
      {zh:"我是汉语。", py:"Wǒ shì Hàn_yǔ.", de:"Ich bin Chinesisch.", why:"Mit 是 sagst du, was du bist. Hier brauchst du 会说 (sprechen können)."}]},
    {s:"a", zh:"你是学生吗？", py:"Nǐ shì xué_sheng ma?", de:"Bist du Student?"},
    {s:"me", zh:"是，我是学生。", py:"Shì, wǒ shì xué_sheng.", de:"Ja, ich bin Student.", alt:[
      {zh:"是，我是工作。", py:"Shì, wǒ shì gōng_zuò.", de:"Ja, ich bin Arbeit.", why:"工作 ist arbeiten oder die Arbeit, kein Beruf. Sie fragt, ob du Student bist."},
      {zh:"我会说一点。", py:"Wǒ huì shuō yì_diǎn.", de:"Ich kann ein bisschen.", why:"Das war die Frage davor."}]},
    {s:"a", zh:"你在哪里学习汉语？", py:"Nǐ zài nǎ_lǐ xué_xí Hàn_yǔ?", de:"Wo lernst du Chinesisch?"},
    {s:"me", zh:"我在德国学习汉语。", py:"Wǒ zài Dé_guó xué_xí Hàn_yǔ.", de:"Ich lerne in Deutschland Chinesisch.", alt:[
      {zh:"我学习汉语在德国。", py:"Wǒ xué_xí Hàn_yǔ zài Dé_guó.", de:"Ich lerne Chinesisch in Deutschland.", why:"Wo man etwas tut, steht vor dem Verb: 在德国学习."},
      {zh:"我在德国是汉语。", py:"Wǒ zài Dé_guó shì Hàn_yǔ.", de:"Ich bin in Deutschland Chinesisch.", why:"Hier fehlt das Verb lernen: 学习."}]},
    {s:"a", zh:"你的汉语很好！", py:"Nǐ de Hàn_yǔ hěn hǎo!", de:"Dein Chinesisch ist gut!"},
    {s:"me", zh:"谢谢！你在这里工作吗？", py:"Xiè_xie! Nǐ zài zhè_lǐ gōng_zuò ma?", de:"Danke! Arbeitest du hier?", cue:"Du willst wissen, ob sie hier arbeitet.", alt:[
      {zh:"谢谢！你工作在这里吗？", py:"Xiè_xie! Nǐ gōng_zuò zài zhè_lǐ ma?", de:"Danke! Arbeitest du in hier?", why:"Wo man etwas tut, steht mit 在 vor dem Verb: 在这里工作."},
      {zh:"谢谢！我在这里工作吗？", py:"Xiè_xie! Wǒ zài zhè_lǐ gōng_zuò ma?", de:"Danke! Arbeite ich hier?", why:"Du willst wissen, ob sie hier arbeitet: 你 …"}]},
    {s:"a", zh:"是，我在这里工作。这里很漂亮！", py:"Shì, wǒ zài zhè_lǐ gōng_zuò. Zhè_lǐ hěn piào_liang!", de:"Ja, ich arbeite hier. Hier ist es sehr schön!"},
    {s:"me", zh:"很漂亮！", py:"Hěn piào_liang!", de:"Sehr schön!", alt:[
      {zh:"很好吃！", py:"Hěn hǎo_chī!", de:"Sehr lecker!", why:"好吃 passt nur zu Essen."},
      {zh:"我很漂亮！", py:"Wǒ hěn piào_liang!", de:"Ich bin sehr hübsch!", why:"Sie meint den Ort, nicht dich."}]},
    {s:"a", zh:"你有中国朋友吗？", py:"Nǐ yǒu Zhōng_guó péng_you ma?", de:"Hast du chinesische Freunde?"},
    {s:"me", zh:"有，我有中国朋友。", py:"Yǒu, wǒ yǒu Zhōng_guó péng_you.", de:"Ja, ich habe chinesische Freunde.", cue:"Du hast chinesische Freunde.", alt:[
      {zh:"是，我是中国朋友。", py:"Shì, wǒ shì Zhōng_guó péng_you.", de:"Ja, ich bin ein chinesischer Freund.", why:"Sie fragt, ob du chinesische Freunde hast. Die Antwort nimmt das Verb der Frage: 有."},
      {zh:"没有，我有中国朋友。", py:"Méi_yǒu, wǒ yǒu Zhōng_guó péng_you.", de:"Nein, ich habe chinesische Freunde.", why:"Erst nein und dann ja, das passt nicht zusammen."}]},
    {s:"a", zh:"很好！再见！", py:"Hěn hǎo! Zài_jiàn!", de:"Sehr gut! Tschüss!"},
    {s:"me", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"}
  ]},
  u9: {title:"Bei Familie Wang", who:{zh:"王阿姨", py:"Wáng ā_yí", de:"Frau Wang"}, lines:[
    {s:"a", zh:"你好！这是我家。", py:"Nǐ_hǎo! Zhè shì wǒ jiā.", de:"Hallo! Das ist mein Zuhause."},
    {s:"me", zh:"你家很漂亮！", py:"Nǐ jiā hěn piào_liang!", de:"Dein Zuhause ist sehr schön!", alt:[
      {zh:"你家很好吃！", py:"Nǐ jiā hěn hǎo_chī!", de:"Dein Zuhause ist sehr lecker!", why:"好吃 sagt man nur über Essen. Für eine Wohnung passt 漂亮."},
      {zh:"这是谁？", py:"Zhè shì shéi?", de:"Wer ist das?", why:"Sie zeigt dir ihr Zuhause, keine Person."}]},
    {s:"a", zh:"谢谢！这是我女儿。", py:"Xiè_xie! Zhè shì wǒ nǚ_ér.", de:"Danke! Das ist meine Tochter."},
    {s:"me", zh:"她几岁？", py:"Tā jǐ suì?", de:"Wie alt ist sie?", cue:"Du möchtest wissen, wie alt die Tochter ist.", alt:[
      {zh:"她是谁？", py:"Tā shì shéi?", de:"Wer ist sie?", why:"Das hat Frau Wang gerade gesagt: ihre Tochter."},
      {zh:"她几个？", py:"Tā jǐ ge?", de:"Wie viele Stück ist sie?", why:"Nach dem Alter fragt man mit 岁: 几岁."}]},
    {s:"a", zh:"她五岁。", py:"Tā wǔ suì.", de:"Sie ist fünf."},
    {s:"me", zh:"你有儿子吗？", py:"Nǐ yǒu ér_zi ma?", de:"Hast du einen Sohn?", cue:"Du fragst, ob sie auch einen Sohn hat.", alt:[
      {zh:"你是儿子吗？", py:"Nǐ shì ér_zi ma?", de:"Bist du ein Sohn?", why:"Du willst wissen, ob sie einen Sohn hat: 有, nicht 是."},
      {zh:"你有女儿吗？", py:"Nǐ yǒu nǚ_ér ma?", de:"Hast du eine Tochter?", why:"Die Tochter hast du gerade kennengelernt."}]},
    {s:"a", zh:"有，我有一个儿子。他八岁。", py:"Yǒu, wǒ yǒu yí ge ér_zi. Tā bā suì.", de:"Ja, ich habe einen Sohn. Er ist acht."},
    {s:"me", zh:"那是谁？", py:"Nà shì shéi?", de:"Wer ist das?", cue:"An der Wand hängt ein Foto. Du fragst, wer das ist.", alt:[
      {zh:"那是什么？", py:"Nà shì shén_me?", de:"Was ist das?", why:"什么 fragt nach Dingen. Nach Menschen fragt man mit 谁."},
      {zh:"那是谁吗？", py:"Nà shì shéi ma?", de:"Ist das wer?", why:"Mit einem Fragewort wie 谁 steht kein 吗 am Ende."}]},
    {s:"a", zh:"那是我爸爸妈妈。你爸爸妈妈在德国吗？", py:"Nà shì wǒ bà_ba mā_ma. Nǐ bà_ba mā_ma zài Dé_guó ma?", de:"Das sind meine Eltern. Sind deine Eltern in Deutschland?"},
    {s:"me", zh:"是，我爸爸妈妈在德国。", py:"Shì, wǒ bà_ba mā_ma zài Dé_guó.", de:"Ja, meine Eltern sind in Deutschland.", alt:[
      {zh:"是，我爸爸妈妈是德国。", py:"Shì, wǒ bà_ba mā_ma shì Dé_guó.", de:"Ja, meine Eltern sind Deutschland.", why:"Für Orte nimmt man 在, nicht 是."},
      {zh:"不是，我爸爸妈妈在德国。", py:"Bú shì, wǒ bà_ba mā_ma zài Dé_guó.", de:"Nein, meine Eltern sind in Deutschland.", why:"Erst nein und dann ja, das passt nicht zusammen."}]},
    {s:"a", zh:"我女儿很喜欢你！", py:"Wǒ nǚ_ér hěn xǐ_huan nǐ!", de:"Meine Tochter mag dich sehr!"},
    {s:"me", zh:"谢谢！她很漂亮！", py:"Xiè_xie! Tā hěn piào_liang!", de:"Danke! Sie ist sehr hübsch!"},
    {s:"a", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"},
    {s:"me", zh:"再见！谢谢！", py:"Zài_jiàn! Xiè_xie!", de:"Tschüss! Danke!"}
  ]},
  u10: {title:"Erster Schultag", who:{zh:"安娜", py:"Ān_nà", de:"Anna, eine Mitschülerin aus Deutschland"}, lines:[
    {s:"a", zh:"你好！你是这里的学生吗？", py:"Nǐ_hǎo! Nǐ shì zhè_lǐ de xué_sheng ma?", de:"Hallo! Bist du Schüler hier?"},
    {s:"me", zh:"是，我在这里学习汉语。", py:"Shì, wǒ zài zhè_lǐ xué_xí Hàn_yǔ.", de:"Ja, ich lerne hier Chinesisch.", alt:[
      {zh:"是，我学习汉语在这里。", py:"Shì, wǒ xué_xí Hàn_yǔ zài zhè_lǐ.", de:"Ja, ich lerne Chinesisch hier.", why:"Wo man etwas tut, steht vor dem Verb: 在这里学习."},
      {zh:"不是，我是这里。", py:"Bú shì, wǒ shì zhè_lǐ.", de:"Nein, ich bin hier.", why:"Für Orte nimmt man 在, nicht 是. Und du lernst ja hier."}]},
    {s:"a", zh:"我们是同学！我叫安娜。", py:"Wǒ_men shì tóng_xué! Wǒ jiào Ān_nà.", de:"Wir sind Mitschüler! Ich heiße Anna."},
    {s:"me", zh:"你好！我叫弗洛里安。", py:"Nǐ_hǎo! Wǒ jiào Fú_luò_lǐ_'ān.", de:"Hallo! Ich heiße Florian.", alt:[
      {zh:"你好！我们叫弗洛里安。", py:"Nǐ_hǎo! Wǒ_men jiào Fú_luò_lǐ_'ān.", de:"Hallo! Wir heißen Florian.", why:"我们 heißt wir. Du stellst dich selbst vor: 我叫 …"},
      {zh:"你好！你叫弗洛里安。", py:"Nǐ_hǎo! Nǐ jiào Fú_luò_lǐ_'ān.", de:"Hallo! Du heißt Florian.", why:"Sie heißt Anna. Du sprichst von dir: 我叫 …"}]},
    {s:"a", zh:"你是哪国人？", py:"Nǐ shì nǎ guó rén?", de:"Aus welchem Land kommst du?"},
    {s:"me", zh:"我是德国人。你是哪国人？", py:"Wǒ shì Dé_guó rén. Nǐ shì nǎ guó rén?", de:"Ich bin Deutscher. Woher kommst du?", alt:[
      {zh:"我是德国人。你是哪国人吗？", py:"Wǒ shì Dé_guó rén. Nǐ shì nǎ guó rén ma?", de:"Ich bin Deutscher. Woher kommst du ja?", why:"Mit einem Fragewort wie 哪 steht kein 吗 am Ende."},
      {zh:"我是哪国人。", py:"Wǒ shì nǎ guó rén.", de:"Ich bin welches Land.", why:"In der Antwort steht das Land an der Stelle von 哪: 我是德国人."}]},
    {s:"a", zh:"我是德国人！这个字怎么读？", py:"Wǒ shì Dé_guó rén! Zhè_ge zì zěn_me dú?", de:"Ich bin Deutsche! Wie liest man dieses Zeichen?"},
    {s:"me", zh:"我不认识这个字。", py:"Wǒ bú rèn_shi zhè_ge zì.", de:"Ich kenne dieses Zeichen nicht.", alt:[
      {zh:"这个字很好吃。", py:"Zhè_ge zì hěn hǎo_chī.", de:"Dieses Zeichen ist lecker.", why:"好吃 passt nur zu Essen."},
      {zh:"我有三本书。", py:"Wǒ yǒu sān běn shū.", de:"Ich habe drei Bücher.", why:"Sie fragt nach der Aussprache des Zeichens."}]},
    {s:"me", zh:"你会读这个字吗？", py:"Nǐ huì dú zhè_ge zì ma?", de:"Kannst du dieses Zeichen lesen?", cue:"Du fragst Anna, ob sie das Zeichen lesen kann.", alt:[
      {zh:"你会写这个字吗？", py:"Nǐ huì xiě zhè_ge zì ma?", de:"Kannst du dieses Zeichen schreiben?", why:"Ihr wollt wissen, wie man es liest (读), nicht wie man es schreibt (写)."},
      {zh:"你会读这本书吗？", py:"Nǐ huì dú zhè běn shū ma?", de:"Kannst du dieses Buch lesen?", why:"Es geht um ein Zeichen, nicht um ein Buch."}]},
    {s:"a", zh:"我不会。老师会读。", py:"Wǒ bú huì. Lǎo_shī huì dú.", de:"Ich nicht. Die Lehrerin kann es."},
    {s:"me", zh:"谢谢，安娜！", py:"Xiè_xie, Ān_nà!", de:"Danke, Anna!"}
  ]},
  u11: {title:"Im Kleidergeschäft", who:{zh:"店员", py:"diàn_yuán", de:"eine Verkäuferin"}, lines:[
    {s:"a", zh:"你好！你想买什么？", py:"Nǐ_hǎo! Nǐ xiǎng mǎi shén_me?", de:"Hallo! Was möchtest du kaufen?"},
    {s:"me", zh:"我想买衣服。", py:"Wǒ xiǎng mǎi yī_fu.", de:"Ich möchte Kleidung kaufen.", alt:[
      {zh:"我买什么？", py:"Wǒ mǎi shén_me?", de:"Was kaufe ich?", why:"Sie hat dich gefragt. Antworte mit 我想买 …"},
      {zh:"我想买米饭。", py:"Wǒ xiǎng mǎi mǐ_fàn.", de:"Ich möchte Reis kaufen.", why:"Du bist in einem Kleidergeschäft."}]},
    {s:"a", zh:"这些衣服都很漂亮。", py:"Zhè xiē yī_fu dōu hěn piào_liang.", de:"Diese Kleider sind alle sehr schön."},
    {s:"me", zh:"这个太大了。有小的吗？", py:"Zhè_ge tài dà le. Yǒu xiǎo de ma?", de:"Das ist zu groß. Gibt es ein kleineres?", cue:"Das Kleid ist dir zu groß.", alt:[
      {zh:"这个太大了。有大的吗？", py:"Zhè_ge tài dà le. Yǒu dà de ma?", de:"Das ist zu groß. Gibt es ein großes?", why:"Wenn es zu groß ist, brauchst du ein kleines: 小的."},
      {zh:"这个太小了。有小的吗？", py:"Zhè_ge tài xiǎo le. Yǒu xiǎo de ma?", de:"Das ist zu klein. Gibt es ein kleines?", why:"Wenn es zu klein ist, brauchst du ein großes."}]},
    {s:"a", zh:"有，这个是小的。", py:"Yǒu, zhè_ge shì xiǎo de.", de:"Ja, das hier ist ein kleines."},
    {s:"me", zh:"很漂亮！多少钱？", py:"Hěn piào_liang! Duō_shao qián?", de:"Sehr schön! Wie viel kostet es?", alt:[
      {zh:"很漂亮！几钱？", py:"Hěn piào_liang! Jǐ qián?", de:"Sehr schön! Wie wenig Geld?", why:"Nach dem Preis fragt man mit 多少钱. 几 braucht ein Zählwort."},
      {zh:"很漂亮！太贵了！", py:"Hěn piào_liang! Tài guì le!", de:"Sehr schön! Zu teuer!", why:"Du kennst den Preis noch nicht."}]},
    {s:"a", zh:"九十块。", py:"Jiǔ shí kuài.", de:"Neunzig Kuai."},
    {s:"me", zh:"太贵了！", py:"Tài guì le!", de:"Zu teuer!", alt:[
      {zh:"太小了！", py:"Tài xiǎo le!", de:"Zu klein!", why:"Die Größe passt ja jetzt. Es geht um den Preis."},
      {zh:"很好吃！", py:"Hěn hǎo_chī!", de:"Sehr lecker!", why:"好吃 passt nur zu Essen."}]},
    {s:"a", zh:"八十块，好吗？", py:"Bā shí kuài, hǎo ma?", de:"Achtzig Kuai, okay?"},
    {s:"me", zh:"六十块，好吗？", py:"Liù shí kuài, hǎo ma?", de:"Sechzig Kuai, okay?", cue:"Du willst handeln und bietest 60 Kuai.", alt:[
      {zh:"九十块，好吗？", py:"Jiǔ shí kuài, hǎo ma?", de:"Neunzig Kuai, okay?", why:"Das ist mehr als ihr Angebot. Beim Handeln bietest du weniger."},
      {zh:"六十钱，好吗？", py:"Liù shí qián, hǎo ma?", de:"Sechzig Geld, okay?", why:"Beim Geld zählt man mit 块: 六十块."}]},
    {s:"a", zh:"好，六十块。", py:"Hǎo, liù shí kuài.", de:"Gut, sechzig Kuai."},
    {s:"me", zh:"谢谢！我很喜欢这个商店。", py:"Xiè_xie! Wǒ hěn xǐ_huan zhè_ge shāng_diàn.", de:"Danke! Ich mag diesen Laden sehr."},
    {s:"a", zh:"谢谢！再见！", py:"Xiè_xie! Zài_jiàn!", de:"Danke! Tschüss!"}
  ]},
  u12: {title:"Die Katze im Garten", who:{zh:"小朋友", py:"xiǎo_péng_you", de:"ein Kind"}, lines:[
    {s:"a", zh:"猫在哪儿？", py:"Māo zài nǎ_r?", de:"Wo ist die Katze?"},
    {s:"me", zh:"猫在椅子上。", py:"Māo zài yǐ_zi shang.", de:"Die Katze ist auf dem Stuhl.", cue:"Du glaubst, die Katze sitzt auf dem Stuhl.", alt:[
      {zh:"猫是椅子上。", py:"Māo shì yǐ_zi shang.", de:"Die Katze ist Stuhl-auf.", why:"Für Orte nimmt man 在, nicht 是."},
      {zh:"椅子在猫上。", py:"Yǐ_zi zài māo shang.", de:"Der Stuhl ist auf der Katze.", why:"Andersherum: Die Katze ist auf dem Stuhl."}]},
    {s:"a", zh:"不是，椅子上没有猫。", py:"Bú shì, yǐ_zi shang méi_yǒu māo.", de:"Nein, auf dem Stuhl ist keine Katze."},
    {s:"me", zh:"猫在桌子后面！", py:"Māo zài zhuō_zi hòu_miàn!", de:"Die Katze ist hinter dem Tisch!", cue:"Da! Hinter dem Tisch sitzt die Katze.", alt:[
      {zh:"猫在后面桌子！", py:"Māo zài hòu_miàn zhuō_zi!", de:"Die Katze ist hinter Tisch!", why:"Erst der Bezugspunkt, dann das Ortswort: 桌子后面."},
      {zh:"猫是桌子后面！", py:"Māo shì zhuō_zi hòu_miàn!", de:"Die Katze ist Tisch-hinten!", why:"Für Orte nimmt man 在, nicht 是."}]},
    {s:"a", zh:"是！谢谢！你喜欢猫吗？", py:"Shì! Xiè_xie! Nǐ xǐ_huan māo ma?", de:"Stimmt! Danke! Magst du Katzen?"},
    {s:"me", zh:"很喜欢！我家里有猫。", py:"Hěn xǐ_huan! Wǒ jiā li yǒu māo.", de:"Sehr! Wir haben zu Hause eine Katze.", cue:"Du hast zu Hause auch eine Katze.", alt:[
      {zh:"很喜欢！我家里是猫。", py:"Hěn xǐ_huan! Wǒ jiā li shì māo.", de:"Sehr! Mein Zuhause ist eine Katze.", why:"Was es an einem Ort gibt, sagt man mit 有: 家里有猫."},
      {zh:"很喜欢！猫在我家里有。", py:"Hěn xǐ_huan! Māo zài wǒ jiā li yǒu.", de:"Sehr! Katze ist bei mir zu Hause hat.", why:"Ort + 有 + Ding: 我家里有猫."}]},
    {s:"a", zh:"你去哪儿？", py:"Nǐ qù nǎ_r?", de:"Wohin gehst du?"},
    {s:"me", zh:"我坐出租车去酒店。", py:"Wǒ zuò chū_zū_chē qù jiǔ_diàn.", de:"Ich fahre mit dem Taxi zum Hotel.", cue:"Du nimmst ein Taxi zum Hotel.", alt:[
      {zh:"我坐酒店去出租车。", py:"Wǒ zuò jiǔ_diàn qù chū_zū_chē.", de:"Ich fahre mit dem Hotel zum Taxi.", why:"Hinter 坐 steht das Fahrzeug, hinter 去 das Ziel."},
      {zh:"出租车在前面。", py:"Chū_zū_chē zài qián_miàn.", de:"Das Taxi ist vorne.", why:"Das Kind fragt, wohin du gehst."}]},
    {s:"a", zh:"出租车在前面！", py:"Chū_zū_chē zài qián_miàn!", de:"Das Taxi ist da vorne!"},
    {s:"me", zh:"谢谢！再见！", py:"Xiè_xie! Zài_jiàn!", de:"Danke! Tschüss!"}
  ]},
  u13: {title:"Bootsfahrt auf dem Westsee", who:{zh:"船夫", py:"chuán_fū", de:"ein Bootsmann"}, lines:[
    {s:"a", zh:"今天天气怎么样？", py:"Jīn_tiān tiān_qì zěn_me_yàng?", de:"Wie findest du das Wetter heute?"},
    {s:"me", zh:"太冷了！", py:"Tài lěng le!", de:"Zu kalt!", cue:"Es ist eiskalt.", alt:[
      {zh:"太好吃了！", py:"Tài hǎo_chī le!", de:"Zu lecker!", why:"Er fragt nach dem Wetter. 好吃 passt nur zu Essen."},
      {zh:"今天十月二十五号。", py:"Jīn_tiān shí yuè èr shí wǔ hào.", de:"Heute ist der 25. Oktober.", why:"Das ist das Datum. Er fragt nach dem Wetter."}]},
    {s:"a", zh:"明天不冷。", py:"Míng_tiān bù lěng.", de:"Morgen ist es nicht kalt."},
    {s:"me", zh:"明天下雨吗？", py:"Míng_tiān xià_yǔ ma?", de:"Regnet es morgen?", cue:"Du fragst, ob es morgen regnet.", alt:[
      {zh:"明天下雨了吗？", py:"Míng_tiān xià_yǔ le ma?", de:"Hat es morgen geregnet?", why:"Morgen ist noch nicht passiert. 了 passt hier nicht."},
      {zh:"明天是下雨吗？", py:"Míng_tiān shì xià_yǔ ma?", de:"Ist morgen Regen?", why:"下雨 ist ein Verb, davor steht kein 是."}]},
    {s:"a", zh:"不下雨。明天天气很好。", py:"Bú xià_yǔ. Míng_tiān tiān_qì hěn hǎo.", de:"Es regnet nicht. Morgen ist das Wetter schön."},
    {s:"me", zh:"明天星期几？", py:"Míng_tiān xīng_qī jǐ?", de:"Welcher Wochentag ist morgen?", cue:"Du weißt nicht, welcher Wochentag morgen ist.", alt:[
      {zh:"明天几星期？", py:"Míng_tiān jǐ xīng_qī?", de:"Morgen wie viele Wochen?", why:"Nach dem Wochentag fragt man mit 星期几: 星期 und dann die Zahl."},
      {zh:"明天星期什么？", py:"Míng_tiān xīng_qī shén_me?", de:"Morgen ist Woche was?", why:"Wochentage sind Zahlen. Gefragt wird mit 几: 星期几？"}]},
    {s:"a", zh:"明天星期六。", py:"Míng_tiān xīng_qī liù.", de:"Morgen ist Samstag."},
    {s:"me", zh:"太好了！", py:"Tài hǎo le!", de:"Super!", alt:[
      {zh:"太贵了！", py:"Tài guì le!", de:"Zu teuer!", why:"Es geht um das Wochenende, nicht um einen Preis."},
      {zh:"明天下雨吗？", py:"Míng_tiān xià_yǔ ma?", de:"Regnet es morgen?", why:"Wie das Wetter morgen wird, hat er schon gesagt."}]},
    {s:"a", zh:"今天几号？", py:"Jīn_tiān jǐ hào?", de:"Der Wievielte ist heute?"},
    {s:"me", zh:"今天十月二十五号。", py:"Jīn_tiān shí yuè èr shí wǔ hào.", de:"Heute ist der 25. Oktober.", cue:"Heute ist der 25. Oktober.", alt:[
      {zh:"今天二十五号十月。", py:"Jīn_tiān èr shí wǔ hào shí yuè.", de:"Heute ist der 25. im Oktober.", why:"Vom Großen zum Kleinen: erst der Monat, dann der Tag."},
      {zh:"今天十月二十五月。", py:"Jīn_tiān shí yuè èr shí wǔ yuè.", de:"Heute ist Oktober 25. Monat.", why:"Der Tag heißt 号: 二十五号."}]},
    {s:"a", zh:"下雨了！", py:"Xià_yǔ le!", de:"Jetzt regnet es!"},
    {s:"me", zh:"我们去酒店！", py:"Wǒ_men qù jiǔ_diàn!", de:"Wir gehen ins Hotel!"}
  ]},
  u14: {title:"Essen bei Familie Wang", who:{zh:"王叔叔", py:"Wáng shū_shu", de:"Herr Wang"}, lines:[
    {s:"a", zh:"请坐！请喝茶。", py:"Qǐng zuò! Qǐng hē chá.", de:"Setz dich bitte! Trink bitte Tee."},
    {s:"me", zh:"谢谢！", py:"Xiè_xie!", de:"Danke!", alt:[
      {zh:"不客气！", py:"Bú_kè_qi!", de:"Gern geschehen!", why:"不客气 sagt man, wenn sich jemand bei dir bedankt. Hier bedankst du dich."},
      {zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!", why:"Du bist gerade erst angekommen."}]},
    {s:"a", zh:"不客气。你喜欢吃水果吗？", py:"Bú_kè_qi. Nǐ xǐ_huan chī shuǐ_guǒ ma?", de:"Gern geschehen. Isst du gern Obst?"},
    {s:"me", zh:"喜欢！我很喜欢苹果。", py:"Xǐ_huan! Wǒ hěn xǐ_huan píng_guǒ.", de:"Ja! Ich mag Äpfel sehr.", alt:[
      {zh:"喜欢！我喜欢吃咖啡。", py:"Xǐ_huan! Wǒ xǐ_huan chī kā_fēi.", de:"Ja! Ich esse gern Kaffee.", why:"Kaffee trinkt man: 喝, nicht 吃. Und gefragt war nach Obst."},
      {zh:"喜欢！我很喜欢杯子。", py:"Xǐ_huan! Wǒ hěn xǐ_huan bēi_zi.", de:"Ja! Ich mag Becher sehr.", why:"Ein Becher ist kein Obst."}]},
    {s:"a", zh:"请吃苹果！", py:"Qǐng chī píng_guǒ!", de:"Nimm dir bitte einen Apfel!"},
    {s:"me", zh:"谢谢！很好吃！", py:"Xiè_xie! Hěn hǎo_chī!", de:"Danke! Sehr lecker!"},
    {s:"a", zh:"你喜欢吃中国菜吗？", py:"Nǐ xǐ_huan chī Zhōng_guó cài ma?", de:"Isst du gern chinesisch?"},
    {s:"me", zh:"很喜欢！你呢？", py:"Hěn xǐ_huan! Nǐ ne?", de:"Sehr gern! Und du?", alt:[
      {zh:"很喜欢！你吗？", py:"Hěn xǐ_huan! Nǐ ma?", de:"Sehr gern! Du?", why:"Zurückfragen geht mit 呢, nicht mit 吗: 你呢？"},
      {zh:"很喜欢！你是呢？", py:"Hěn xǐ_huan! Nǐ shì ne?", de:"Sehr gern! Du bist und?", why:"Kurz und ohne Verb: 你呢？"}]},
    {s:"a", zh:"我很喜欢德国菜！", py:"Wǒ hěn xǐ_huan Dé_guó cài!", de:"Ich mag deutsches Essen sehr!"},
    {s:"me", zh:"德国菜和中国菜都很好吃！", py:"Dé_guó cài hé Zhōng_guó cài dōu hěn hǎo_chī!", de:"Deutsches und chinesisches Essen sind beide lecker!", cue:"Du findest beides lecker.", alt:[
      {zh:"德国菜都中国菜很好吃！", py:"Dé_guó cài dōu Zhōng_guó cài hěn hǎo_chī!", de:"Deutsches alle chinesisches Essen lecker!", why:"和 verbindet die beiden Nomen. 都 steht danach, vor 很."},
      {zh:"德国菜和中国菜很都好吃！", py:"Dé_guó cài hé Zhōng_guó cài hěn dōu hǎo_chī!", de:"Deutsches und chinesisches Essen sehr alle lecker!", why:"都 steht vor 很: 都很好吃."}]},
    {s:"a", zh:"认识你很高兴！", py:"Rèn_shi nǐ hěn gāo_xìng!", de:"Schön, dich kennenzulernen!"},
    {s:"me", zh:"认识你很高兴！", py:"Rèn_shi nǐ hěn gāo_xìng!", de:"Schön, dich kennenzulernen!", alt:[
      {zh:"认识你是高兴！", py:"Rèn_shi nǐ shì gāo_xìng!", de:"Dich kennen ist froh!", why:"Vor einem Adjektiv steht kein 是, sondern 很."},
      {zh:"不客气！", py:"Bú_kè_qi!", de:"Gern geschehen!", why:"不客气 antwortet auf ein Danke. Hier sagst du einfach dasselbe zurück."}]},
    {s:"a", zh:"明天我们去饭店，好吗？", py:"Míng_tiān wǒ_men qù fàn_diàn, hǎo ma?", de:"Morgen gehen wir ins Restaurant, okay?"},
    {s:"me", zh:"好！谢谢！", py:"Hǎo! Xiè_xie!", de:"Gern! Danke!", alt:[
      {zh:"好！我们去酒店。", py:"Hǎo! Wǒ_men qù jiǔ_diàn.", de:"Gern! Wir gehen ins Hotel.", why:"Ins Restaurant heißt 饭店. 酒店 ist das Hotel."},
      {zh:"不客气！", py:"Bú_kè_qi!", de:"Gern geschehen!", why:"Er lädt dich ein. Du bedankst dich: 谢谢."}]}
  ]},
  u15: {title:"Ein Anruf am Abend", who:{zh:"李娜", py:"Lǐ Nà", de:"Li Na, am Telefon"}, lines:[
    {s:"a", zh:"喂？", py:"Wèi?", de:"Hallo?"},
    {s:"me", zh:"喂，你好！我是弗洛里安。", py:"Wèi, nǐ_hǎo! Wǒ shì Fú_luò_lǐ_'ān.", de:"Hallo! Ich bin's, Florian.", alt:[
      {zh:"喂，你好！你是弗洛里安。", py:"Wèi, nǐ_hǎo! Nǐ shì Fú_luò_lǐ_'ān.", de:"Hallo! Du bist Florian.", why:"Du bist Florian, also 我是."},
      {zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!", why:"Das Gespräch fängt gerade erst an."}]},
    {s:"a", zh:"你好！你在看电视吗？", py:"Nǐ_hǎo! Nǐ zài kàn diàn_shì ma?", de:"Hallo! Schaust du gerade fern?"},
    {s:"me", zh:"不是，我在看电影。", py:"Bú shì, wǒ zài kàn diàn_yǐng.", de:"Nein, ich schaue gerade einen Film.", cue:"Du schaust gerade einen Film, nicht fern.", alt:[
      {zh:"不是，我在电影。", py:"Bú shì, wǒ zài diàn_yǐng.", de:"Nein, ich bin im Film.", why:"Da fehlt das Verb. »Gerade einen Film schauen« heißt 在看电影."},
      {zh:"是，我在睡觉。", py:"Shì, wǒ zài shuì_jiào.", de:"Ja, ich schlafe gerade.", why:"Dann könntest du nicht telefonieren. Und sie fragte nach dem Fernsehen."}]},
    {s:"a", zh:"什么电影？", py:"Shén_me diàn_yǐng?", de:"Was für ein Film?"},
    {s:"me", zh:"中国电影。我很喜欢。", py:"Zhōng_guó diàn_yǐng. Wǒ hěn xǐ_huan.", de:"Ein chinesischer Film. Er gefällt mir sehr."},
    {s:"a", zh:"明天我们看电影，好吗？", py:"Míng_tiān wǒ_men kàn diàn_yǐng, hǎo ma?", de:"Wollen wir morgen einen Film schauen?"},
    {s:"me", zh:"好！明天几点？", py:"Hǎo! Míng_tiān jǐ diǎn?", de:"Gern! Um wie viel Uhr morgen?", alt:[
      {zh:"好！昨天几点？", py:"Hǎo! Zuó_tiān jǐ diǎn?", de:"Gern! Um wie viel Uhr gestern?", why:"Ihr verabredet euch für morgen (明天), nicht gestern."},
      {zh:"我能睡觉吗？", py:"Wǒ néng shuì_jiào ma?", de:"Darf ich schlafen?", why:"Sie hat dich zum Film eingeladen."}]},
    {s:"a", zh:"下午三点。", py:"Xià_wǔ sān diǎn.", de:"Um drei Uhr nachmittags."},
    {s:"me", zh:"下午三点我不能去。中午，好吗？", py:"Xià_wǔ sān diǎn wǒ bù néng qù. Zhōng_wǔ, hǎo ma?", de:"Um drei kann ich nicht. Mittags, geht das?", cue:"Um drei hast du keine Zeit. Du schlägst mittags vor.", alt:[
      {zh:"下午三点我不会去。", py:"Xià_wǔ sān diǎn wǒ bú huì qù.", de:"Um drei kann ich das nicht.", why:"不会 heißt »nicht können, weil man es nicht gelernt hat«. Wenn es zeitlich nicht klappt, sagt man 不能."},
      {zh:"我去不能下午三点。", py:"Wǒ qù bù néng xià_wǔ sān diǎn.", de:"Ich gehe nicht kann um drei.", why:"Die Zeit steht vorne, 不能 direkt vor dem Verb: 下午三点我不能去."}]},
    {s:"a", zh:"好，中午十二点。", py:"Hǎo, zhōng_wǔ shí èr diǎn.", de:"Gut, um zwölf Uhr mittags."},
    {s:"me", zh:"好！现在我想睡觉。再见！", py:"Hǎo! Xiàn_zài wǒ xiǎng shuì_jiào. Zài_jiàn!", de:"Gut! Jetzt will ich schlafen. Tschüss!"},
    {s:"a", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"}
  ]},
  u16: {title:"Ein Hund im Park", who:{zh:"张先生", py:"Zhāng xiān_sheng", de:"Herr Zhang mit Hund"}, lines:[
    {s:"me", zh:"对不起！", py:"Duì_bu_qǐ!", de:"Entschuldigung!", cue:"Du bist aus Versehen gegen einen Mann gelaufen.", alt:[
      {zh:"没关系！", py:"Méi_guān_xi!", de:"Macht nichts!", why:"Du hast ihn angerempelt. 没关系 sagt der andere."},
      {zh:"不客气！", py:"Bú_kè_qi!", de:"Gern geschehen!", why:"Das sagt man auf ein Danke."}]},
    {s:"a", zh:"没关系。你看见我的狗了吗？", py:"Méi_guān_xi. Nǐ kàn_jiàn wǒ de gǒu le ma?", de:"Macht nichts. Hast du meinen Hund gesehen?"},
    {s:"me", zh:"我没有看见你的狗。", py:"Wǒ méi_yǒu kàn_jiàn nǐ de gǒu.", de:"Ich habe deinen Hund nicht gesehen.", cue:"Den Hund hast du nicht gesehen.", alt:[
      {zh:"我没有看见你的狗了。", py:"Wǒ méi_yǒu kàn_jiàn nǐ de gǒu le.", de:"Ich habe deinen Hund nicht gesehen (mit 了).", why:"Mit 没有 fällt 了 weg."},
      {zh:"我不看见你的狗。", py:"Wǒ bú kàn_jiàn nǐ de gǒu.", de:"Ich sehe deinen Hund nicht.", why:"Was nicht passiert ist, verneint man mit 没有, nicht mit 不."}]},
    {s:"a", zh:"我的狗在那里！", py:"Wǒ de gǒu zài nà_lǐ!", de:"Da ist mein Hund!"},
    {s:"me", zh:"你的狗很漂亮！", py:"Nǐ de gǒu hěn piào_liang!", de:"Dein Hund ist sehr schön!"},
    {s:"a", zh:"谢谢！", py:"Xiè_xie!", de:"Danke!"},
    {s:"me", zh:"不客气！", py:"Bú_kè_qi!", de:"Gern geschehen!", alt:[
      {zh:"没关系！", py:"Méi_guān_xi!", de:"Macht nichts!", why:"没关系 antwortet auf eine Entschuldigung, nicht auf ein Danke."},
      {zh:"对不起！", py:"Duì_bu_qǐ!", de:"Entschuldigung!", why:"Er bedankt sich. Darauf sagt man 不客气."}]},
    {s:"a", zh:"你是学生吗？", py:"Nǐ shì xué_sheng ma?", de:"Bist du Student?"},
    {s:"me", zh:"是，我在这里学习汉语。你呢？", py:"Shì, wǒ zài zhè_lǐ xué_xí Hàn_yǔ. Nǐ ne?", de:"Ja, ich lerne hier Chinesisch. Und du?", cue:"Du lernst hier Chinesisch und fragst zurück.", alt:[
      {zh:"是，我学习汉语在这里。你呢？", py:"Shì, wǒ xué_xí Hàn_yǔ zài zhè_lǐ. Nǐ ne?", de:"Ja, ich lerne Chinesisch hier. Und du?", why:"Wo man etwas tut, steht mit 在 vor dem Verb: 在这里学习."},
      {zh:"不是，我是学生。你呢？", py:"Bú shì, wǒ shì xué_sheng. Nǐ ne?", de:"Nein, ich bin Student. Und du?", why:"Erst nein und dann ja, das passt nicht zusammen."}]},
    {s:"a", zh:"我是医生。我在医院工作。医院在那里，坐出租车十分钟。", py:"Wǒ shì yī_shēng. Wǒ zài yī_yuàn gōng_zuò. Yī_yuàn zài nà_lǐ, zuò chū_zū_chē shí fēn_zhōng.", de:"Ich bin Arzt. Ich arbeite im Krankenhaus. Es ist dort drüben, mit dem Taxi zehn Minuten."},
    {s:"me", zh:"你几点去医院？", py:"Nǐ jǐ diǎn qù yī_yuàn?", de:"Um wie viel Uhr gehst du ins Krankenhaus?", cue:"Du fragst, wann er ins Krankenhaus geht.", alt:[
      {zh:"你去医院几点？", py:"Nǐ qù yī_yuàn jǐ diǎn?", de:"Du gehst ins Krankenhaus um wie viel Uhr?", why:"Die Uhrzeit steht vor dem Verb: 几点去."},
      {zh:"你几点去医生？", py:"Nǐ jǐ diǎn qù yī_shēng?", de:"Um wie viel Uhr gehst du zum Arzt?", why:"医生 ist der Arzt, 医院 das Krankenhaus. Er arbeitet im 医院."}]},
    {s:"a", zh:"下午三点。再见！", py:"Xià_wǔ sān diǎn. Zài_jiàn!", de:"Um drei Uhr nachmittags. Tschüss!"},
    {s:"me", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"}
  ]},
  u17: {title:"Abschied am Flughafen", who:{zh:"李娜", py:"Lǐ Nà", de:"Li Na"}, lines:[
    {s:"a", zh:"你什么时候回德国？", py:"Nǐ shén_me shí_hou huí Dé_guó?", de:"Wann fliegst du zurück nach Deutschland?"},
    {s:"me", zh:"我今天回德国。", py:"Wǒ jīn_tiān huí Dé_guó.", de:"Ich fliege heute zurück nach Deutschland.", cue:"Dein Flug geht heute.", alt:[
      {zh:"我回德国今天。", py:"Wǒ huí Dé_guó jīn_tiān.", de:"Ich fliege zurück nach Deutschland heute.", why:"Die Zeit steht vor dem Verb: 我今天回德国."},
      {zh:"昨天我回德国。", py:"Zuó_tiān wǒ huí Dé_guó.", de:"Gestern flog ich zurück.", why:"Du stehst noch am Flughafen. Gestern passt nicht."}]},
    {s:"a", zh:"你几点的飞机？", py:"Nǐ jǐ diǎn de fēi_jī?", de:"Um wie viel Uhr geht dein Flug?"},
    {s:"me", zh:"下午四点的飞机。", py:"Xià_wǔ sì diǎn de fēi_jī.", de:"Mein Flug geht um vier Uhr nachmittags.", cue:"Dein Flug geht um 16 Uhr.", alt:[
      {zh:"下午四点飞机的。", py:"Xià_wǔ sì diǎn fēi_jī de.", de:"Vier Uhr nachmittags Flug von.", why:"的 steht zwischen Uhrzeit und Flugzeug: 四点的飞机."},
      {zh:"下午四个点的飞机。", py:"Xià_wǔ sì ge diǎn de fēi_jī.", de:"Um vier Stück Uhr.", why:"Bei der Uhrzeit steht kein 个: 四点."}]},
    {s:"a", zh:"你喜欢中国吗？", py:"Nǐ xǐ_huan Zhōng_guó ma?", de:"Gefällt dir China?"},
    {s:"me", zh:"很喜欢！我想住在中国。", py:"Hěn xǐ_huan! Wǒ xiǎng zhù zài Zhōng_guó.", de:"Sehr! Ich möchte in China wohnen.", alt:[
      {zh:"很喜欢！我想在住中国。", py:"Hěn xǐ_huan! Wǒ xiǎng zài zhù Zhōng_guó.", de:"Sehr! Ich möchte in wohnen China.", why:"Bei 住 steht 在 mit dem Ort dahinter: 住在中国."},
      {zh:"很喜欢！我想住中国在。", py:"Hěn xǐ_huan! Wǒ xiǎng zhù Zhōng_guó zài.", de:"Sehr! Ich möchte wohnen China in.", why:"在 steht vor dem Ort, nicht dahinter."}]},
    {s:"a", zh:"你什么时候来北京？", py:"Nǐ shén_me shí_hou lái Běi_jīng?", de:"Wann kommst du nach Peking?"},
    {s:"me", zh:"下个月我来北京！", py:"Xià ge yuè wǒ lái Běi_jīng!", de:"Nächsten Monat komme ich nach Peking!", cue:"Du kommst nächsten Monat nach Peking.", alt:[
      {zh:"我来北京下个月。", py:"Wǒ lái Běi_jīng xià ge yuè.", de:"Ich komme nach Peking nächsten Monat.", why:"Auch hier: Die Zeit steht vor dem Verb."},
      {zh:"我住在北京。", py:"Wǒ zhù zài Běi_jīng.", de:"Ich wohne in Peking.", why:"Sie fragt, wann du kommst."}]},
    {s:"a", zh:"太好了！请来我家！", py:"Tài hǎo le! Qǐng lái wǒ jiā!", de:"Super! Komm mich bitte besuchen!"},
    {s:"me", zh:"好！谢谢！", py:"Hǎo! Xiè_xie!", de:"Gern! Danke!", alt:[
      {zh:"不客气！", py:"Bú_kè_qi!", de:"Gern geschehen!", why:"Sie lädt dich ein. Du bedankst dich: 谢谢."},
      {zh:"没关系！", py:"Méi_guān_xi!", de:"Macht nichts!", why:"没关系 antwortet auf eine Entschuldigung."}]},
    {s:"a", zh:"再见！", py:"Zài_jiàn!", de:"Tschüss!"},
    {s:"me", zh:"谢谢！再见！", py:"Xiè_xie! Zài_jiàn!", de:"Danke! Tschüss!", alt:[
      {zh:"你好！", py:"Nǐ_hǎo!", de:"Hallo!", why:"Ihr verabschiedet euch, also 再见."},
      {zh:"对不起！", py:"Duì_bu_qǐ!", de:"Entschuldigung!", why:"Du musst dich für nichts entschuldigen."}]}
  ]}
};
