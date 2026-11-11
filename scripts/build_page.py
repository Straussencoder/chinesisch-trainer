# Setzt index.html aus Vorlage, Inhaltsdaten und Lernpfad zusammen.
import sys
d = sys.argv[1]
src = open(d+"/index.src.html", encoding="utf-8").read()
data = open(d+"/data.js", encoding="utf-8").read()
lessons = open(d+"/lessons.data.js", encoding="utf-8").read()
import re, urllib.parse
# Zeichen für die Pinsel-Schrift: alles aus Siegeln, Überschriften und Lektionsthemen
units = "".join(re.findall(r'\{id:"u\d+", title:"[^"]*", zh:"([^"]+)"', lessons)) + "".join(re.findall(r'place:\{zh:"([^"]+)"', lessons))
fixed = "学你好声调句子复习设置火今词复新意听字声对错句读完成很好存一二三四五六七八九十护照到了市北京上海龙舟赛胜输起点终开始旅程弗洛里安法理写说话对回家考金"
chars = "".join(sorted(set(c for c in units + fixed if "\u4e00" <= c <= "\u9fff")))
out = src.replace("BRUSH_TEXT", urllib.parse.quote(chars))
out = out.replace("/*SCENES*/", open(d+"/scenes.part.js", encoding="utf-8").read())
out = out.replace("/*FX*/", open(d+"/fx.part.js", encoding="utf-8").read())
out = out.replace("/*PITCH*/", open(d+"/pitch.part.js", encoding="utf-8").read())
out = out.replace("/*GAME*/", open(d+"/game.part.js", encoding="utf-8").read())
assert "/*FX*/" not in out and "/*GAME*/" not in out
out = out.replace("<!--ZH_DATA-->", data.rstrip()).replace("<!--ZH_LESSONS-->", lessons.rstrip())
out = out.replace("<!--ZH_GRAMMAR-->", open(d+"/grammar.data.js", encoding="utf-8").read().rstrip())
assert "<!--ZH_GRAMMAR-->" not in out
out = out.replace("<!--ZH_DIALOGS-->", open(d+"/dialogs.data.js", encoding="utf-8").read().rstrip())
assert "<!--ZH_DIALOGS-->" not in out
out = out.replace("<!--ZH_DRILL-->", open(d+"/drill.data.js", encoding="utf-8").read().rstrip())
assert "<!--ZH_DRILL-->" not in out
out = out.replace("<!--ZH_MNEMO-->", open(d+"/mnemo.data.js", encoding="utf-8").read().rstrip())
assert "<!--ZH_MNEMO-->" not in out
out = out.replace("<!--ZH_TEXTS-->", open(d+"/texts.data.js", encoding="utf-8").read().rstrip())
assert "<!--ZH_TEXTS-->" not in out
if len(sys.argv) > 2 and sys.argv[2] == "test":
    out = out.replace("/*TEST_HOOK*/", "window.__t={getS:function(){return S;},notePat:notePat,patScore:patScore,focusPat:focusPat,patStatus:patStatus,sentWeight:sentWeight,POINTS:POINTS,POINT:POINT,exitSession:exitSession,startListen:startListen,startText:startText,startSay:startSay,audioHas:audioHas,loadAudioPart:loadAudioPart,partOfLesson:partOfLesson,sayScore:sayScore,sayMatch:sayMatch,sayNorm:sayNorm,srSupported:srSupported,TEXTS:TEXTS,textUnits:textUnits,textPick:textPick,lsnUnits:lsnUnits,lsnPick:lsnPick,speak:speak,ownAnalyze:ownAnalyze,wordTarget:wordTarget,toneTarget:toneTarget,voicedRuns:voicedRuns,ownWordText:ownWordText,recSupported:recSupported,getOwn:function(){return own;},LESSONS:LESSONS,SENTS:SENTS,WORDS:WORDS,clipsFor:clipsFor,seqClips:seqClips,blobCache:blobCache,sandhiNotes:sandhiNotes,state:function(){return state;},toneOf:toneOf,TONE_SYL:TONE_SYL,TONE_WORDS:TONE_WORDS,CARDS:CARDS,chunksOf:chunksOf,getG:function(){return G;},startGame:startGame,gameAnswer:gameAnswer,gameFinish:gameFinish,closeGame:closeGame,RIVALS:RIVALS,learnedWords:learnedWords,dueWords:dueWords,today:today,addDays:addDays,POINTS:POINTS,POINT:POINT,buildLesson:buildLesson,GR:GR,checkTyped:checkTyped,WORD:WORD,stumbles:stumbles,yinTrack:yinTrack,semis:semis,shapeOk:shapeOk,toneSchema:toneSchema,pitchOfClip:pitchOfClip,clip:clip,VOICE:VOICE,audioBufferOf:audioBufferOf,startDialog:startDialog,play:playClips,startReview:startReview,srsNext:srsNext,boxOf:boxOf,ivOf:ivOf,weakSort:weakSort,buildReview:buildReview,MNEMO:MNEMO,DRILL:DRILL,startSentences:startSentences,startNumbers:startNumbers,startDayRound:startDayRound,startHsk:startHsk,hskReady:hskReady,dayRoundPlan:dayRoundPlan,weakestPair:weakestPair,newToneQ:newToneQ,pickTone:pickTone,getTq:function(){return tq;},numToks:numToks,numConfusers:numConfusers,makeNum:makeNum,makeNumCtx:makeNumCtx,NUMHAND:NUMHAND,sentPool:sentPool,makeGap:makeGap,makeJudge:makeJudge,makeBuild:makeBuild,markSyl:markSyl,CONFMAP:CONFMAP,confFor:confFor,introSeen:introSeen,checkBuild:checkBuild,qPairFor:qPairFor,applyResults:applyResults,nextEx:nextEx,setQuiet:setQuiet,quiet:quiet,isGold:isGold,pyOf:pyOf,startTest:startTest,testDue:testDue,startDrawPractice:startDrawPractice,startLesson:startLesson,renderSession:renderSession,dlgChoose:dlgChoose,DIALOGS:DIALOGS,dlgDone:dlgDone,UNITS:UNITS,matchPinyin:matchPinyin,toneSet:function(zh){ tq = {item:TONE_SYL.find(function(i){ return i.zh===zh; }) || TONE_WORDS.find(function(i){ return i.zh===zh; }), picks:[], done:false}; renderTone(); }};window.__t_next=gameNextQ;")
test = len(sys.argv) > 2 and sys.argv[2] == "test"
# Im Prüfbau sind alle Teile sofort da, im echten Bau kommt Teil 1 gleich und der Rest nach Bedarf
tags = "".join('<script src="audio-%d.js"></script>' % n for n in (1, 2, 3, 4)) if test else '<script src="audio-1.js" async></script>'
out = out.replace("<!--AUDIO_TAGS-->", tags)
assert "<!--AUDIO_TAGS-->" not in out
open(sys.argv[3] if len(sys.argv) > 3 else d+"/index.html", "w", encoding="utf-8").write(out)
print("ok", len(out))
