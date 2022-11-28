import sqlite3
#conn = sqlite3.connect("data.db")
conn = sqlite3.connect("msaw.sqlite")
cur = conn.cursor()
labels=[];agwedde=[];apple_bananas=[];beef=[];cassava_flour=[];cassava_fresh=[]
cavendish_Bogoya=[];coffee_arabic=[];coffee_robusta=[];cow_peas=[];dry_fermented_cassava=[]
exotic_chic=[];exotic_eggs=[];goat_meat=[];groundnuts=[];irish_potato=[]
kayiso_rice=[];local_chicken=[];local_eggs=[];maize_flour=[];maize_grain=[]
matooke=[];matooke_kg=[];milk=[];millet_flour=[];millet_grain=[];mushrooms=[]
nambale_beans=[];nile_perch=[];pineapples=[];pork=[];processed_honey=[]
red_irish_potato=[];simsim=[];sorghum_flour=[];sorghum_grain=[]
soya_beans=[];sun_dried_cassava=[];sunflower=[];super_rice=[];tilapia=[];tobbaco=[]
turkey=[];unprocessed_cotton=[];unprocessed_honey=[];unprocessed_tea=[]
unprocessed_vanilla=[];upland_rice=[];white_fleshed_sweet_potatoes=[]
yellow_beans=[]
data_sets= [labels,agwedde,apple_bananas,beef,cassava_flour,cassava_fresh,cavendish_Bogoya,coffee_arabic,coffee_robusta,cow_peas,
            dry_fermented_cassava,exotic_chic,exotic_eggs,goat_meat,groundnuts,irish_potato,kayiso_rice,local_chicken,local_eggs,
            maize_flour,maize_grain,matooke,matooke_kg,milk,millet_flour,millet_grain,mushrooms,nambale_beans,nile_perch,pineapples,pork,
            processed_honey,red_irish_potato,simsim,sorghum_flour,sorghum_grain,soya_beans,sun_dried_cassava,sunflower,super_rice,
            tilapia,tobbaco,turkey,unprocessed_cotton,unprocessed_honey,unprocessed_tea,unprocessed_vanilla,upland_rice,white_fleshed_sweet_potatoes,
            yellow_beans]
with open("static.txt",'r') as fhand:
        content = fhand.read().splitlines()
        labels.extend(content[0:8])
        agwedde.extend(content[8:24])
        apple_bananas.extend(content[24:40])
        beef.extend(content[40:56])
        cassava_flour.extend(content[56:72])
        cassava_fresh.extend(content[72:88])
        cavendish_Bogoya.extend(content[88:104])
        coffee_arabic.extend(content[104:120])
        coffee_robusta.extend(content[120:136])
        cow_peas.extend(content[136:152])
        dry_fermented_cassava.extend(content[152:168])
        exotic_chic.extend(content[168:184])
        exotic_eggs.extend(content[184:200])
        goat_meat.extend(content[200:216])
        groundnuts.extend(content[216:232])
        irish_potato.extend(content[232:248])
        kayiso_rice.extend(content[248:264])
        local_chicken.extend(content[264:280])
        local_eggs.extend(content[280:296])
        maize_flour.extend(content[296:312])
        maize_grain.extend(content[312:328])
        matooke.extend(content[328:344])
        matooke_kg.extend(content[344:360])
        milk.extend(content[360:376])
        millet_flour.extend(content[376:392])
        millet_grain.extend(content[392:408])
        mushrooms.extend(content[408:424])
        nambale_beans.extend(content[424:440])
        nile_perch.extend(content[440:456])
        pineapples.extend(content[456:472])
        pork.extend(content[472:488])
        processed_honey.extend(content[488:504])
        red_irish_potato.extend(content[504:520])
        simsim.extend(content[520:536])
        sorghum_flour.extend(content[536:552])
        sorghum_grain.extend(content[552:568])
        soya_beans.extend(content[568:584])
        sun_dried_cassava.extend(content[584:600])
        sunflower.extend(content[600:616])
        super_rice.extend(content[616:632])
        tilapia.extend(content[632:648])
        tobbaco.extend(content[648:664])
        turkey.extend(content[664:680])
        unprocessed_cotton.extend(content[680:696])
        unprocessed_honey.extend(content[696:712])
        unprocessed_tea.extend(content[712:728])
        unprocessed_vanilla.extend(content[728:744])
        upland_rice.extend(content[744:760])
        white_fleshed_sweet_potatoes.extend(content[760:776])
        yellow_beans.extend(content[776:792])
        count=1
        for data in data_sets:
            rp = []
            wp = []
            item = []
            if "Commodity" in data[0]:
                continue
            rp.extend(data[0:8])
            item.extend(data[0:2])
            merge = wp+item
            merge.extend(data[10:16])
            conn.execute('INSERT INTO retailprice VALUES (?,?,?,?,?,?,?,?,?)',(count,rp[0].replace(',',""),rp[1].replace(',',""),
                        rp[2].replace(',',""),rp[3].replace(',',""),rp[4].replace(',',""),rp[5].replace(',',""),
                        rp[6].replace(',',""),rp[7].replace(',',"")))
##            conn.execute('INSERT INTO wholesaleprice VALUES (?,?,?,?,?,?,?,?,?)',(count,merge[0].replace(',',""),merge[1].replace(',',""),
##                        merge[2].replace(',',""),merge[3].replace(',',""),merge[4].replace(',',""),merge[5].replace(',',""),
##                        merge[6].replace(',',""),merge[7].replace(',',"")))
            count+=1

conn.commit()
conn.close()
        
