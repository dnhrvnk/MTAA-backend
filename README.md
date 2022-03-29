
# MTAA zadanie 2 - backend

### Backend
Databázu používame PostgreSQL.

Kód je písaný v programovacom jazyku Python vo frameworku Django.

Na získanie dát z databázy využívame Modely, ktoré sú v priečinku Modely. V priečinkoch Auth_api, Club, Search a User sa nachádzajú samotné API volania. Na prepísanie dát z modelov do jazyka json používame triedy serializers.Serializer, do ktorých sa pošlú serializable triedy (podľa nášho formátovania) modelov. V súboroch *views.py* sa volajú samotná aplikačná logika API volaní.

Štruktúra projektu sa delí na 8 priečinkov:
 - Backend – konfigurácia djanga
 -  Auth_api – API volania /auth/
 - Club – API volania /group/
 - Modely – obsahuje modely databázy
-- Modely: Genre, Author, Book, User, Club, Status, User_Club a User_Book
- Search - API volania /find/
- User – API volania /user/
- Video – kód na konferenčný hovor

### API volania

Všetky finálne API volania s popismy môžeme nájsť na https://app.swaggerhub.com/apis/RobJun/MTAA/1.5.0-oas3#/.

### Config file
`config.json` musí obsahovať:
```json
{
"database": {
"host" : "<host>",
"port" : "<port>",
"name" : "<db name>",
"user" : "<user>",
"pass" : "<password>"
},
"hosts": [
"<IPaddress>",
"...",
],
"salt": "SECRET_KEY"
}
```
### Webrtc support
from tutorial: https://www.youtube.com/watch?v=MBOlZMLaQ8g