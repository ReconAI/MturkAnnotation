# -*- coding: utf-8 -*-
"""

"""

import boto3
import time
import os
from credentials import *

SensorIDs = ['C0150200', 'C0150201', 'C0150202', 'C0150204', 'C0150209', 'C0150301', 'C0150302', 'C0150309', 'C0150401', 'C0150402', 'C0150409', 'C0150501', 'C0150701', 'C0150801', 'C0150802', 'C0150803', 'C0150804', 'C0150809', 'C0150901', 'C0150902', 'C0150903', 'C0150904', 'C0150909', 'C0151001', 'C0151002', 'C0151009', 'C0151101', 'C0151102', 'C0151104', 'C0151109', 'C0151301', 'C0151302', 'C0151303', 'C0151309', 'C0152101', 'C0152102', 'C0152109', 'C0152201', 'C0152202', 'C0152209', 'C0152301', 'C0152302', 'C0152309', 'C0152401', 'C0152402', 'C0152403', 'C0152404', 'C0152409', 'C0152600', 'C0152700', 'C0152801', 'C0152900', 'C0153000', 'C0153100', 'C0153201', 'C0153202', 'C0153209', 'C0153300', 'C0153501', 'C0153502', 'C0153503', 'C0153504', 'C0153509', 'C0153601', 'C0153602', 'C0153609', 'C0153801', 'C0153802', 'C0153803', 'C0153809', 'C0153900', 'C0155500', 'C0156800', 'C0156900', 'C0157000', 'C0157100', 'C0157200', 'C0157300', 'C0157400', 'C0158101', 'C0158200', 'C0158301', 'C0158302', 'C0158309', 'C0158401', 'C0158402', 'C0158403', 'C0158404', 'C0158409', 'C0158700', 'C0159000', 'C0160000', 'C0160100', 'C0160200', 'C0160300', 'C0161600', 'C0161700', 'C0161800', 'C0161900', 'C0162000', 'C0162100', 'C0162201', 'C0162202', 'C0162209', 'C0162300', 'C0162401', 'C0162402', 'C0162409', 'C0162501', 'C0162502', 'C0162509', 'C0162601', 'C0162602', 'C0162604', 'C0162609', 'C0162701', 'C0162702', 'C0162709', 'C0162801', 'C0162802', 'C0162900', 'C0163000', 'C0163100', 'C0163201', 'C0163202', 'C0163209', 'C0163301', 'C0163400', 'C0163500', 'C0163600', 'C0164500', 'C0164600', 'C0164700', 'C0164900', 'C0165100', 'C0165200', 'C0165300', 'C0165400', 'C0165500', 'C0165600', 'C0165700', 'C0166000', 'C0166100', 'C0166400', 'C0166500', 'C0166700', 'C0166800', 'C0167000', 'C0167100', 'C0167200', 'C0167301', 'C0167302', 'C0167309', 'C0167400', 'C0167500', 'C0167600', 'C0167701', 'C0167702', 'C0167709', 'C0167800', 'C0167900', 'C0168000', 'C0170301', 'C0170302', 'C0170309', 'C0170311', 'C0170312', 'C0250201', 'C0250402', 'C0250509', 'C0250601', 'C0250701', 'C0250702', 'C0250709', 'C0250801', 'C0250802', 'C0250809', 'C0250901', 'C0251101', 'C0251102', 'C0251109', 'C0251201', 'C0251202', 'C0251209', 'C0251309', 'C0251401', 'C0251501', 'C0251502', 'C0251503', 'C0251504', 'C0251509', 'C0251601', 'C0251602', 'C0251604', 'C0251609', 'C0251701', 'C0251702', 'C0251709', 'C0251802', 'C0251902', 'C0252001', 'C0252002', 'C0252003', 'C0252004', 'C0252008', 'C0252009', 'C0252101', 'C0252102', 'C0252103', 'C0252104', 'C0252109', 'C0252201', 'C0252202', 'C0252203', 'C0252204', 'C0252209', 'C0252301', 'C0252302', 'C0252303', 'C0252304', 'C0252309', 'C0252401', 'C0252402', 'C0252409', 'C0252501', 'C0252502', 'C0252503', 'C0252504', 'C0252509', 'C0252601', 'C0252602', 'C0252609', 'C0252701', 'C0252702', 'C0252709', 'C0252801', 'C0252802', 'C0252809', 'C0252900', 'C0253000', 'C0253100', 'C0253200', 'C0253300', 'C0253401', 'C0253500', 'C0253600', 'C0253700', 'C0253800', 'C0253900', 'C0254501', 'C0254502', 'C0254509', 'C0254601', 'C0254602', 'C0254609', 'C0255000', 'C0255001', 'C0255002', 'C0255101', 'C0255102', 'C0255109', 'C0256301', 'C0256302', 'C0256309', 'C0256400', 'C0256500', 'C0256901', 'C0256902', 'C0256909', 'C0350202', 'C0350401', 'C0350402', 'C0350409', 'C0350501', 'C0350502', 'C0350504', 'C0350509', 'C0350601', 'C0350602', 'C0350603', 'C0350604', 'C0350609', 'C0350701', 'C0350702', 'C0350703', 'C0350709', 'C0350802', 'C0351002', 'C0351201', 'C0351202', 'C0351500', 'C0351600', 'C0351700', 'C0351800', 'C0351901', 'C0351902', 'C0351903', 'C0351904', 'C0351909', 'C0352201', 'C0352202', 'C0352204', 'C0352209', 'C0352301', 'C0352302', 'C0352309', 'C0352401', 'C0352402', 'C0352408', 'C0352409', 'C0352502', 'C0352509', 'C0352701', 'C0352702', 'C0352709', 'C0352801', 'C0352901', 'C0352902', 'C0352909', 'C0353000', 'C0353101', 'C0353102', 'C0353103', 'C0353104', 'C0353109', 'C0353201', 'C0353202', 'C0353209', 'C0353301', 'C0353302', 'C0353309', 'C0353401', 'C0353402', 'C0353409', 'C0353601', 'C0353602', 'C0353701', 'C0353702', 'C0353801', 'C0353802', 'C0353809', 'C0353901', 'C0353902', 'C0353909', 'C0354001', 'C0354002', 'C0354009', 'C0354100', 'C0354202', 'C0354301', 'C0354302', 'C0354309', 'C0354401', 'C0354402', 'C0354409', 'C0354500', 'C0354600', 'C0354700', 'C0354801', 'C0354802', 'C0354809', 'C0355003', 'C0355104', 'C0355201', 'C0355202', 'C0355209', 'C0355301', 'C0355302', 'C0355309', 'C0355401', 'C0355402', 'C0355501', 'C0355502', 'C0355601', 'C0355602', 'C0355701', 'C0355702', 'C0355709', 'C0355801', 'C0355802', 'C0355809', 'C0355901', 'C0355902', 'C0355909', 'C0356001', 'C0356002', 'C0356009', 'C0356101', 'C0356102', 'C0356105', 'C0356109', 'C0356201', 'C0356202', 'C0356203', 'C0356204', 'C0356209', 'C0356301', 'C0356302', 'C0356309', 'C0356401', 'C0356402', 'C0356409', 'C0356501', 'C0356502', 'C0356509', 'C0356601', 'C0356602', 'C0356609', 'C0356701', 'C0356702', 'C0356709', 'C0356801', 'C0356802', 'C0356809', 'C0357001', 'C0357002', 'C0357009', 'C0357101', 'C0357102', 'C0357109', 'C0357201', 'C0357202', 'C0357209', 'C0357301', 'C0357302', 'C0357309', 'C0357401', 'C0357402', 'C0357501', 'C0357502', 'C0357509', 'C0357601', 'C0357602', 'C0357609', 'C0357701', 'C0357702', 'C0357801', 'C0357802', 'C0357809', 'C0357901', 'C0357902', 'C0357909', 'C0358001', 'C0358002', 'C0358009', 'C0358101', 'C0358102', 'C0358109', 'C0358401', 'C0358501', 'C0358601', 'C0358701', 'C0358802', 'C0358901', 'C0359001', 'C0359101', 'C0359201', 'C0359301', 'C0359401', 'C0359501', 'C0359601', 'C0359701', 'C0359800', 'C0359900', 'C0360000', 'C0360100', 'C0360200', 'C0360300', 'C0360400', 'C0361300', 'C0361400', 'C0361500', 'C0361600', 'C0362100', 'C0362200', 'C0362300', 'C0362703', 'C0362704', 'C0362801', 'C0362802', 'C0363101', 'C0363201', 'C0363400', 'C0363500', 'C0363800', 'C0363900', 'C0364000', 'C0364700', 'C0364800', 'C0364900', 'C0365000', 'C0365900', 'C0366000', 'C0366101', 'C0366102', 'C0366103', 'C0366104', 'C0366109', 'C0366301', 'C0366302', 'C0366309', 'C0366400', 'C0366501', 'C0366502', 'C0366509', 'C0367502', 'C0367602', 'C0450109', 'C0450201', 'C0450202', 'C0450203', 'C0450204', 'C0450209', 'C0450301', 'C0450302', 'C0450303', 'C0450304', 'C0450309', 'C0450401', 'C0450402', 'C0450409', 'C0450501', 'C0450601', 'C0450602', 'C0450609', 'C0450701', 'C0450702', 'C0450703', 'C0450704', 'C0450709', 'C0450801', 'C0450802', 'C0450804', 'C0450809', 'C0450901', 'C0450902', 'C0450903', 'C0450904', 'C0450909', 'C0451002', 'C0451201', 'C0451202', 'C0451301', 'C0451302', 'C0451309', 'C0451401', 'C0451602', 'C0451701', 'C0451801', 'C0451802', 'C0451803', 'C0451804', 'C0451809', 'C0451901', 'C0451902', 'C0451909', 'C0452001', 'C0452201', 'C0452202', 'C0452209', 'C0452401', 'C0452402', 'C0452409', 'C0452601', 'C0452602', 'C0452603', 'C0452604', 'C0452701', 'C0452702', 'C0452709', 'C0452801', 'C0452802', 'C0452809', 'C0453001', 'C0453002', 'C0453009', 'C0453101', 'C0453102', 'C0453104', 'C0453109', 'C0453301', 'C0453302', 'C0453309', 'C0453401', 'C0453402', 'C0453403', 'C0453404', 'C0453408', 'C0453409', 'C0453501', 'C0453502', 'C0453509', 'C0453601', 'C0453602', 'C0453609', 'C0453702', 'C0453801', 'C0453802', 'C0453809', 'C0453901', 'C0454001', 'C0454002', 'C0454003', 'C0454004', 'C0454009', 'C0454109', 'C0454201', 'C0454202', 'C0454203', 'C0454204', 'C0454209', 'C0454301', 'C0454302', 'C0454309', 'C0454401', 'C0454402', 'C0454409', 'C0454601', 'C0454602', 'C0454603', 'C0454604', 'C0454701', 'C0454702', 'C0454703', 'C0454704', 'C0454709', 'C0454801', 'C0454802', 'C0454809', 'C0455501', 'C0455502', 'C0455509', 'C0455600', 'C0455800', 'C0456300', 'C0456401', 'C0456500', 'C0456601', 'C0456602', 'C0456603', 'C0456604', 'C0456609', 'C0456701', 'C0456702', 'C0456709', 'C0456800', 'C0456900', 'C0457000', 'C0457100', 'C0457200', 'C0459100', 'C0459400', 'C0460700', 'C0460800', 'C0460900', 'C0461000', 'C0461100', 'C0461201', 'C0461202', 'C0461203', 'C0461204', 'C0461209', 'C0461301', 'C0461302', 'C0461303', 'C0461304', 'C0461309', 'C0461401', 'C0461402', 'C0461403', 'C0461404', 'C0461409', 'C0461501', 'C0461502', 'C0461503', 'C0461504', 'C0461509', 'C0461601', 'C0461602', 'C0461609', 'C0461611', 'C0650101', 'C0650102', 'C0650103', 'C0650104', 'C0650109', 'C0650201', 'C0650202', 'C0650203', 'C0650301', 'C0650302', 'C0650303', 'C0650309', 'C0650401', 'C0650402', 'C0650408', 'C0650409', 'C0650501', 'C0650502', 'C0650504', 'C0650509', 'C0650601', 'C0650700', 'C0650801', 'C0650802', 'C0650808', 'C0650809', 'C0650901', 'C0650909', 'C0651001', 'C0651002', 'C0651009', 'C0651101', 'C0651102', 'C0651109', 'C0651201', 'C0651202', 'C0651209', 'C0651301', 'C0651302', 'C0651303', 'C0651304', 'C0651309', 'C0651401', 'C0651402', 'C0651409', 'C0651501', 'C0651601', 'C0651602', 'C0651609', 'C0651701', 'C0651702', 'C0651709', 'C0651801', 'C0651802', 'C0651808', 'C0651809', 'C0750101', 'C0750201', 'C0750301', 'C0750401', 'C0750501', 'C0850302', 'C0850501', 'C0850502', 'C0850503', 'C0850504', 'C0850509', 'C0850601', 'C0850602', 'C0850609', 'C0850801', 'C0850802', 'C0850809', 'C0850901', 'C0850902', 'C0850903', 'C0850904', 'C0850909', 'C0851001', 'C0851002', 'C0851101', 'C0851102', 'C0851109', 'C0851701', 'C0851702', 'C0851709', 'C0851801', 'C0851802', 'C0851809', 'C0851901', 'C0851902', 'C0851909', 'C0852001', 'C0852002', 'C0852009', 'C0852101', 'C0852102', 'C0852109', 'C0852201', 'C0852202', 'C0852209', 'C0852301', 'C0852302', 'C0852401', 'C0852402', 'C0852409', 'C0852501', 'C0852502', 'C0852503', 'C0852601', 'C0852602', 'C0852603', 'C0852604', 'C0852609', 'C0852701', 'C0852702', 'C0852709', 'C0852801', 'C0852802', 'C0852809', 'C0852901', 'C0852902', 'C0852909', 'C0853001', 'C0853002', 'C0853009', 'C0853101', 'C0853102', 'C0853109', 'C0853201', 'C0853202', 'C0853209', 'C0853301', 'C0853302', 'C0853309', 'C0853401', 'C0853402', 'C0853403', 'C0853404', 'C0853409', 'C0853501', 'C0853502', 'C0853504', 'C0853509', 'C0853601', 'C0853602', 'C0853609', 'C0853701', 'C0853702', 'C0853709', 'C0853801', 'C0853802', 'C0853803', 'C0853804', 'C0853809', 'C0854001', 'C0854002', 'C0854101', 'C0854102', 'C0854109', 'C0854301', 'C0854302', 'C0854304', 'C0854309', 'C0854401', 'C0854402', 'C0854403', 'C0854409', 'C0854501', 'C0854502', 'C0854509', 'C0854601', 'C0854602', 'C0854603', 'C0854604', 'C0854701', 'C0854702', 'C0854709', 'C0854801', 'C0854802', 'C0854803', 'C0854804', 'C0854901', 'C0854902', 'C0854909', 'C0855002', 'C0855100', 'C0855201', 'C0855202', 'C0855204', 'C0855209', 'C0855301', 'C0855302', 'C0855309', 'C0855400', 'C0855500', 'C0855601', 'C0855602', 'C0855609', 'C0855701', 'C0855702', 'C0855706', 'C0855707', 'C0855708', 'C0855709', 'C0855801', 'C0855802', 'C0855809', 'C0855901', 'C0855902', 'C0855909', 'C0856001', 'C0856002', 'C0856003', 'C0856009', 'C0856101', 'C0856102', 'C0856109', 'C0857201', 'C0857202', 'C0857209', 'C0857301', 'C0857302', 'C0857309', 'C0857401', 'C0857402', 'C0857409', 'C0857502', 'C0857503', 'C0857504', 'C0857509', 'C0857601', 'C0857602', 'C0857603', 'C0857604', 'C0857609', 'C0857701', 'C0857801', 'C0857901', 'C0858301', 'C0858302', 'C0858304', 'C0858309', 'C0858401', 'C0858402', 'C0858409', 'C0858501', 'C0858502', 'C0858509', 'C0858601', 'C0858602', 'C0858609', 'C0858701', 'C0858702', 'C0858706', 'C0858708', 'C0858709', 'C0858801', 'C0858802', 'C0858809', 'C0950101', 'C0950102', 'C0950109', 'C0950201', 'C0950202', 'C0950209', 'C0950301', 'C0950302', 'C0950309', 'C0950401', 'C0950402', 'C0950409', 'C0950501', 'C0950502', 'C0950509', 'C0950601', 'C0950602', 'C0950609', 'C0950701', 'C0950702', 'C0950709', 'C0950901', 'C0950902', 'C0950909', 'C0951002', 'C0951101', 'C0951102', 'C0951109', 'C0951201', 'C0951202', 'C0951208', 'C0951209', 'C0951301', 'C0951302', 'C0951309', 'C0951401', 'C0951402', 'C0951409', 'C0951501', 'C0951502', 'C0951509', 'C0951601', 'C0951602', 'C0951609', 'C0951801', 'C0951802', 'C0951809', 'C0951901', 'C0951902', 'C0951909', 'C0952001', 'C0952002', 'C0952009', 'C0952101', 'C0952102', 'C0952109', 'C0952201', 'C0952202', 'C0952209', 'C0952301', 'C0952302', 'C0952309', 'C0952401', 'C0952402', 'C0952409', 'C0952501', 'C0952502', 'C0952509', 'C0952601', 'C0952702', 'C0952801', 'C0952901', 'C0953001', 'C0953101', 'C0953102', 'C0953109', 'C1050101', 'C1050102', 'C1050109', 'C1050201', 'C1050202', 'C1050209', 'C1050301', 'C1050302', 'C1050309', 'C1050401', 'C1050402', 'C1050409', 'C1050501', 'C1050502', 'C1050509', 'C1050601', 'C1050602', 'C1050607', 'C1050608', 'C1050609', 'C1050701', 'C1050702', 'C1050709', 'C1050801', 'C1050802', 'C1050803', 'C1050804', 'C1050809', 'C1051001', 'C1051002', 'C1051009', 'C1051101', 'C1051102', 'C1051109', 'C1051201', 'C1051202', 'C1051209', 'C1051301', 'C1051302', 'C1051309', 'C1051401', 'C1051402', 'C1051409', 'C1051501', 'C1051502', 'C1051509', 'C1051601', 'C1051602', 'C1051609', 'C1051701', 'C1051702', 'C1051709', 'C1051801', 'C1051802', 'C1051809', 'C1051901', 'C1051902', 'C1051909', 'C1052001', 'C1052002', 'C1052009', 'C1052101', 'C1052102', 'C1052109', 'C1052201', 'C1052202', 'C1052209', 'C1052301', 'C1052302', 'C1052303', 'C1052309', 'C1052401', 'C1052402', 'C1052409', 'C1052501', 'C1052502', 'C1052509', 'C1052601', 'C1052602', 'C1052609', 'C1052701', 'C1052702', 'C1052709', 'C1052801', 'C1052802', 'C1052803', 'C1052804', 'C1052809', 'C1052901', 'C1052902', 'C1052909', 'C1053001', 'C1053002', 'C1053009', 'C1053101', 'C1053102', 'C1053109', 'C1053201', 'C1053202', 'C1053209', 'C1053301', 'C1053302', 'C1053309', 'C1053401', 'C1053402', 'C1053409', 'C1053501', 'C1053502', 'C1053509', 'C1053601', 'C1053602', 'C1053609', 'C1053701', 'C1053702', 'C1053709', 'C1053801', 'C1053802', 'C1053803', 'C1053804', 'C1053809', 'C1053901', 'C1053902', 'C1053909', 'C1054001', 'C1054101', 'C1054102', 'C1054109', 'C1054201', 'C1054202', 'C1054204', 'C1054209', 'C1054301', 'C1054302', 'C1054303', 'C1054304', 'C1054309', 'C1054501', 'C1054502', 'C1054509', 'C1054601', 'C1054602', 'C1054609', 'C1054701', 'C1054702', 'C1054709', 'C1054801', 'C1054901', 'C1054902', 'C1054909', 'C1055001', 'C1055002', 'C1055009', 'C1055101', 'C1055102', 'C1055109', 'C1055201', 'C1055202', 'C1055204', 'C1055209', 'C1055301', 'C1055302', 'C1055309', 'C1055401', 'C1055501', 'C1250101', 'C1250102', 'C1250109', 'C1250201', 'C1250202', 'C1250209', 'C1250301', 'C1250302', 'C1250303', 'C1250304', 'C1250309', 'C1250401', 'C1250402', 'C1250403', 'C1250404', 'C1250409', 'C1250501', 'C1250502', 'C1250509', 'C1250601', 'C1250602', 'C1250609', 'C1250701', 'C1250702', 'C1250709', 'C1250801', 'C1250802', 'C1250803', 'C1250804', 'C1250809', 'C1250901', 'C1250902', 'C1250903', 'C1250907', 'C1250909', 'C1251001', 'C1251002', 'C1251009', 'C1251101', 'C1251102', 'C1251109', 'C1251300', 'C1251401', 'C1251402', 'C1251403', 'C1251404', 'C1251409', 'C1251501', 'C1251502', 'C1251509', 'C1251601', 'C1251602', 'C1251609', 'C1251701', 'C1251702', 'C1251709', 'C1251901', 'C1251902', 'C1251904', 'C1251909', 'C1252001', 'C1252002', 'C1252009', 'C1252101', 'C1252102', 'C1252109', 'C1252201', 'C1252202', 'C1252209', 'C1252401', 'C1252402', 'C1252409', 'C1252601', 'C1252602', 'C1252609', 'C1252702', 'C1252709', 'C1252801', 'C1252802', 'C1252809', 'C1252901', 'C1252902', 'C1252903', 'C1252909', 'C1253001', 'C1253002', 'C1253009', 'C1253101', 'C1253102', 'C1253109', 'C1253201', 'C1253202', 'C1253209', 'C1253301', 'C1253302', 'C1253303', 'C1253309', 'C1253401', 'C1253402', 'C1253409', 'C1253501', 'C1253601', 'C1253602', 'C1253609', 'C1253701', 'C1253702', 'C1253709', 'C1253801', 'C1253802', 'C1253809', 'C1253901', 'C1253902', 'C1253909', 'C1254001', 'C1254101', 'C1254102', 'C1254109', 'C1254201', 'C1254202', 'C1254209', 'C1254301', 'C1254302', 'C1254309', 'C1254400', 'C1254501', 'C1254502', 'C1254504', 'C1254509', 'C1254701', 'C1254702', 'C1254709', 'C1254802', 'C1254809', 'C1255001', 'C1255002', 'C1255007', 'C1255009', 'C1255101', 'C1255102', 'C1255109', 'C1255201', 'C1255202', 'C1255203', 'C1255204', 'C1255209', 'C1255300', 'C1255401', 'C1255402', 'C1255409', 'C1255501', 'C1255502', 'C1255503', 'C1255504', 'C1255509', 'C1255601', 'C1255602', 'C1255609', 'C1255701', 'C1255702', 'C1255703', 'C1255704', 'C1255709', 'C1255801', 'C1255802', 'C1255809', 'C1255901', 'C1255902', 'C1255904', 'C1256001', 'C1256002', 'C1256003', 'C1256004', 'C1256009', 'C1256101', 'C1256102', 'C1256109', 'C1256201', 'C1256202', 'C1256209', 'C1256301', 'C1256302', 'C1256303', 'C1256309', 'C1256401', 'C1256402', 'C1256409', 'C1256501', 'C1256502', 'C1256509', 'C1256601', 'C1256602', 'C1256609', 'C1256701', 'C1256702', 'C1256709', 'C1256801', 'C1256802', 'C1256809', 'C1256901', 'C1256902', 'C1256909', 'C1257001', 'C1257002', 'C1257003', 'C1257004', 'C1257009', 'C1257101', 'C1257102', 'C1257109', 'C1257201', 'C1257301', 'C1257302', 'C1257309', 'C1257401', 'C1257501', 'C1257601', 'C1257701', 'C1257809', 'C1257901', 'C1258101', 'C1258102', 'C1258103', 'C1258104', 'C1258109', 'C1258201', 'C1258202', 'C1258209', 'C1258302', 'C1258401', 'C1258402', 'C1258409', 'C1258501', 'C1258601', 'C1258602', 'C1258609', 'C1258701', 'C1258702', 'C1258703', 'C1258704', 'C1258709', 'C1258801', 'C1258802', 'C1258809', 'C1258901', 'C1258902', 'C1258903', 'C1258904', 'C1258909', 'C1259001', 'C1259002', 'C1259003', 'C1259004', 'C1259009', 'C1259101', 'C1259102', 'C1259109', 'C1259200', 'C1259300', 'C1259400', 'C1259500', 'C1259600', 'C1259701', 'C1259702', 'C1259703', 'C1259704', 'C1259801', 'C1259802', 'C1259803', 'C1259804', 'C1259809', 'C1259901', 'C1259902', 'C1259903', 'C1259904', 'C1259905', 'C1259906', 'C1259907', 'C1259908', 'C1259909', 'C1260101', 'C1260102', 'C1260108', 'C1260109', 'C1260201', 'C1260202', 'C1260209', 'C1260401', 'C1260402', 'C1260403', 'C1260404', 'C1260409', 'C1260501', 'C1260502', 'C1260509', 'C1260601', 'C1260701', 'C1261101', 'C1261200', 'C1261300', 'C1261400', 'C1261801', 'C1261802', 'C1261809', 'C1262000', 'C1262100', 'C1262200', 'C1262401', 'C1262501', 'C1450101', 'C1450102', 'C1450109', 'C1450201', 'C1450301', 'C1450302', 'C1450309', 'C1450401', 'C1450402', 'C1450409', 'C1450501', 'C1450502', 'C1450509', 'C1450701', 'C1450702', 'C1450707', 'C1450709', 'C1450801', 'C1450802', 'C1450809', 'C1450901', 'C1451001', 'C1451002', 'C1451009', 'C1451102', 'C1451201', 'C1451202', 'C1451203', 'C1451209', 'C1451301', 'C1451401', 'C1451402', 'C1451409', 'C1451501', 'C1451502', 'C1451509', 'C1451601', 'C1451602', 'C1451609', 'C1451701', 'C1451702', 'C1451709', 'C1451901', 'C1451902', 'C1451909', 'C1452001', 'C1452002', 'C1452009', 'C1452201', 'C1452202', 'C1452209', 'C1452301', 'C1452302', 'C1452309', 'C1452401', 'C1452402', 'C1452409', 'C1452501', 'C1452502', 'C1452509', 'C1452601', 'C1452602', 'C1452609', 'C1452701', 'C1452702', 'C1452709', 'C1452801', 'C1452802', 'C1452809', 'C1453001', 'C1453002', 'C1453009', 'C1453101', 'C1453102', 'C1453109', 'C1453201', 'C1453202', 'C1453209', 'C1453301', 'C1453302', 'C1453308', 'C1453309', 'C1453401', 'C1453402', 'C1453409', 'C1453502', 'C1453507', 'C1453508', 'C1453509', 'C1453601', 'C1453602', 'C1453609', 'C1453701', 'C1453702', 'C1453709', 'C1453801', 'C1453802', 'C1453809', 'C1453901', 'C1453902', 'C1453909', 'C1454001', 'C1454002', 'C1454007', 'C1454009', 'C1454101', 'C1454102', 'C1454109', 'C1454201', 'C1454202', 'C1454209', 'C1454301', 'C1454302', 'C1454309', 'C1454401', 'C1454402', 'C1454407', 'C1454409', 'C1454601', 'C1454602', 'C1454609', 'C1455401', 'C1455402', 'C1455409', 'C1455501', 'C1455502', 'C1455509', 'C1455601', 'C1455602', 'C1455609', 'C1455701', 'C1455702', 'C1455709', 'C1455801', 'C1455802', 'C1455809', 'C1455901', 'C1455902', 'C1455909', 'C1456001', 'C1456002', 'C1456009', 'C1456101', 'C1456102', 'C1456109', 'C1456209', 'C1456301', 'C1456302', 'C1456309', 'C1456401', 'C1456402', 'C1456409', 'C1456601', 'C1456602', 'C1456606', 'C1456609', 'C1456701', 'C1456801', 'C1456901', 'C1457101', 'C1457102', 'C1457109', 'C1457301', 'C1457302', 'C1457305', 'C1457309', 'C1457401', 'C1457402', 'C1457409', 'C1457501', 'C1457502', 'C1457509', 'C1457801', 'C1457802', 'C1457808', 'C1457809', 'C1457901', 'C1458001', 'C1458101', 'C1458102', 'C1458109', 'C1458201', 'C1458202', 'C1458209', 'C1458301', 'C1458302', 'C1458309', 'C1458401', 'C1458402', 'C1458409', 'C1458501', 'C1458502', 'C1458509', 'C1458601', 'C1458602', 'C1458609', 'C1458701', 'C1458801', 'C1458901', 'C1650101', 'C1650200', 'C1650300', 'C1650400', 'C1650500', 'C1650600', 'C1650700', 'C1650800', 'C1650900', 'C1651000', 'C1651100']

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
reconai_bucket = s3.Bucket('reconai-traffic')

#C0150801_r0_w0_2020-03-15_19-57-12.jpg
#ToDo
# save keys to the array
#For each key
#   append 'images/' to key
#   do filter by prefix and page size = 3
#   pick 3 images and save their path

#Note:
#keys are saved as 'images/C...'
#there's a 'images/' key

sensorslen = len(SensorIDs)

for v_ind, v_sensor in enumerate(SensorIDs):
    print('Processing ',v_ind, ' out of ', sensorslen)
    prefixFilter = 'images/' + v_sensor
    os.mkdir(prefixFilter)
    
    for s3_file in reconai_bucket.objects.filter(Prefix=prefixFilter).limit(5):
        key = s3_file.key
        
        filename = key.split('/')[-1]
        path_save_to = 'images/' + v_sensor + '/' + filename
        print('s3_file:',key)
        
        if (s3_file.size>2000):
            start = time.time()
            reconai_bucket.download_file(key, path_save_to)
            end = time.time()
            print('* processed in: ',(end - start))
        else:
            print('* image is too small')
