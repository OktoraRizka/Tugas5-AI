import json

def load_kb(filename="internet.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def tanya_fakta(kb):
    fakta_dasar = set()
    hasil_aturan = set()

    for aturan in kb["aturan"]:
        for f in aturan["jika"]:
            fakta_dasar.add(f)
        hasil_aturan.add(aturan["maka"])

    fakta_yang_ditanya = sorted(fakta_dasar - hasil_aturan)

    print(f"\n{kb['judul']}")
    print("Jawab dengan y / t\n")

    memori = set()
    for i, fakta in enumerate(fakta_yang_ditanya, 1):
        jawaban = input(f"{i}. Apakah {fakta}? (y/t) > ").strip().lower()
        if jawaban == "y":
            memori.add(fakta)

    return memori

def forward_chaining(kb, memori):
    alasan = {}       
    siklus = 1
    log = []

    while True:
        cocok = []
        for aturan in kb["aturan"]:
            maka = aturan["maka"]
            if maka in memori:
                continue 

            jika = aturan["jika"]
            mode = aturan["mode"]

            if mode == "dan":
                terpenuhi = all(f in memori for f in jika)
            else:
                terpenuhi = any(f in memori for f in jika)

            if terpenuhi:
                cocok.append(aturan)

        if not cocok:
            break

        r = cocok[0]
        memori.add(r["maka"])
        alasan[r["maka"]] = r
        log.append(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
        siklus += 1

    return memori, alasan, log

def tampilkan_hasil(kb, memori_awal, memori_akhir, alasan, log):
    print("\n" + "="*50)
    print("Fakta awal:", ", ".join(memori_awal) if memori_awal else "(tidak ada)")
    print()

    if log:
        for l in log:
            print(l)
    else:
        print("Tidak ada aturan yang terpicu.")

    kesimpulan = [f for f in memori_akhir if f in alasan]

    print("\nKesimpulan:")
    if kesimpulan:
        for k in kesimpulan:
            print(f"  - {k}")
    else:
        print("  Tidak ditemukan kesimpulan yang cocok.")

    print("\nAlasan:")
    if kesimpulan:
        for k in kesimpulan:
            r = alasan[k]
            syarat = ", ".join(r["jika"])
            print(f"  {k}  <- {r['id']} ({syarat})  [sumber: {r['sumber']}]")
    else:
        print("  -")

    print("\nCatatan:")
    print(kb["batas"])
    print("="*50)

def main():
    kb = load_kb()
    memori_awal = tanya_fakta(kb)
    memori_akhir, alasan, log = forward_chaining(kb, memori_awal.copy())
    tampilkan_hasil(kb, memori_awal, memori_akhir, alasan, log)

if __name__ == "__main__":
    main()