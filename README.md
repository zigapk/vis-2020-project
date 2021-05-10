# Analiza rezultatov tednskih kvizov pri predmetu v VS v šolskem letu 2020/21

Za uporabo skript v tem repozitoriju je potrebno namestiti nekatere Python pakete: 
```bash
pip3 install -r requirements.txt
```

## Podatki
Podatki so v bazo MariaDB uvoženi iz sql varnostne kopije prave baze.

Kvizi (`exam`), ki pridejo v poštev:

**ID**|**IME**
:-----:|:-----:
6199|Tedenski kviz 27. oktober
6233|Tedenski kviz 3. november
6261|Tedenski kviz 10. november
6287|Tedenski kviz 17. november
6307|Tedenski kviz 26. november
6332|Tedenski kviz 8. december
6339|Tedenski kviz 15. december
6350|Tedenski kviz 22. december
6389|Tedenski kviz 29. december
6410|Tedenski kviz 12. januar


Iz baze so bili nato z uporabo sql skript izvoženi naslednji dokumenti:
- [`data/events.json`](data/events.json) - Vsi dogodki (oddaje odgovorov in zaključki kvizov) za vse uporabnike pri teh kvizih (examih).
- [`data/exercises.json`](data/exercises.json) - Vse naloge, vključene v omenjene kvize.
- [`data/ratings.json`](data/ratings.json) - Podatki o ratingih za vse naloge, ki se pojavijo v teh kvizih.


Podatki iz teh datotek so bili preoblikovani v eno samo datoteko z uporabo skripte `convert.py`. Rezultati so shranjeni v csv datoteki [`data/export.csv`](data/export.csv).

## Analiza podatkov

Preprosto analizo podatkov lahko zaženemo z
```bash
python3 analysis.py
```
