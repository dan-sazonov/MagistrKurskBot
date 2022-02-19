import psycopg2

import config

db = psycopg2.connect(config.DATABASE_URL, sslmode='require')
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS memes(id SERIAL PRIMARY KEY, file_id TEXT, file_path TEXT, "
               "asks_count INTEGER, is_last BOOLEAN)")

db.commit()

j = 0
for i in '''file_id: AgACAgIAAxkBAAIZPWIQ9lrtrANXWT5WYZv5jQAB0JzytwACu7kxG9R9iUguzGzpE0bD-wEAAwIAA3MAAyME
file_path: photos/file_0.jpg

file_id: AgACAgIAAxkBAAIZP2IQ9mCZweVoKYZtaGvOIjw_RysOAAK8uTEb1H2JSPWygFuycet1AQADAgADcwADIwQ
file_path: photos/file_1.jpg

file_id: AgACAgIAAxkBAAIZQWIQ9masCbWwGd-Khkr9Pj2KlENBAALAuTEb1H2JSDH2NpiC0EguAQADAgADcwADIwQ
file_path: photos/file_2.jpg

file_id: AgACAgIAAxkBAAIZQ2IQ9m4jFxzG5whl-95LL_dZ2ieEAALSuTEb1H2JSB3yfniK2-DDAQADAgADcwADIwQ
file_path: photos/file_3.jpg

file_id: AgACAgIAAxkBAAIZRWIQ9npcz3KPGvagtVcmjH7-C470AALTuTEb1H2JSLMHSIfvit13AQADAgADcwADIwQ
file_path: photos/file_4.jpg

file_id: AgACAgIAAxkBAAIZR2IQ9oW29A1teyoT7ixH_VMF3OcoAALUuTEb1H2JSOrFGPE_dgYLAQADAgADcwADIwQ
file_path: photos/file_5.jpg

file_id: AgACAgIAAxkBAAIZSWIQ9o0no63dTftSEiKc5PhqsUIbAALVuTEb1H2JSMeQ2lelSbg2AQADAgADcwADIwQ
file_path: photos/file_6.jpg

file_id: AgACAgIAAxkBAAIZS2IQ9pcP62MJLKQK_mUqGHXHyMIrAALWuTEb1H2JSBebJTDraPEXAQADAgADcwADIwQ
file_path: photos/file_7.jpg

file_id: AgACAgIAAxkBAAIZTWIQ9qCabLwjryercxqeKWT6RA7nAALXuTEb1H2JSBLHCDQ08e89AQADAgADcwADIwQ
file_path: photos/file_8.jpg

file_id: AgACAgIAAxkBAAIZT2IQ9rN_CTKkBgtB7VR1y21gat-zAALYuTEb1H2JSLG6QLAuSpw1AQADAgADcwADIwQ
file_path: photos/file_9.jpg

file_id: AgACAgIAAxkBAAIZUWIQ9slAv3UPP6kDaI-22oKzcIVYAALZuTEb1H2JSIMfplFsYrWdAQADAgADcwADIwQ
file_path: photos/file_10.jpg	

file_id: AgACAgIAAxkBAAIZU2IQ9s9Dl8Fg6ndu8PGdKDcK9eVRAALauTEb1H2JSPTRFEftIAwwAQADAgADcwADIwQ
file_path: photos/file_11.jpg

file_id: AgACAgIAAxkBAAIZVWIQ9tz5_53uXzNu_9uxFKpauFXxAALbuTEb1H2JSJ3iICE1RVApAQADAgADcwADIwQ
file_path: photos/file_12.jpg'''.split('\n\n'):
    file_id = i.split('\n')[0].split(': ')[1]
    file_path = i.split('\n')[1].split(': ')[1]
    cursor.execute("INSERT INTO memes(id, file_id, file_path, asks_count, is_last) VALUES (%s, %s, %s, %s, %s)",
                   (j, file_id, file_path, 0, False))
    db.commit()
    j += 1
