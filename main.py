import PIL.Image
import PIL.ExifTags
from gmplot import gmplot
import webbrowser
from geopy.geocoders import Nominatim


class Bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'



def logo():
    print(Bcolors.RED + Bcolors.BOLD)
    logo = """
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,               ,,,     .,,,,,     ,,,,    ,,,,               ,,,,,,,,,
,,,,,,,,,,    ,,,,,,,,,,,,,,,,     ,,     ,,,,,,    ,,,,     ,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,    ,,,,,,,,,,,,,,,,,,        .,,,,,,,    ,,,,     ,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,              ,,,,,,,,,      ,,,,,,,,,    ,,,,              ,,,,,,,,,,
,,,,,,,,,,    ,*,*,*,*,*,,,,,,,,        ,,,,,,,,    ,,,,     ........,,,,,,,,,,,
,,,,,,,,,,    ,,,,,,,,,,,,,,,,     ,,     ,,,,,,    ,,,,     ,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,               .,,,     ,,,,      ,,,,    ,,,,     ,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,               .,     ,,,,,,,,     ,,,    ,,,,     ,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

    # v1.0.0 #
       >> EXIF TOOLS <<
       >> 20/12/2023 <<

    """
    print(logo)
    print(Bcolors.ENDC)



def exif_bilgilerini_incele(dosya_adı):
    try:
        # Görseli aç
        img = PIL.Image.open(dosya_adı)

        # EXIF verilerini alma
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }

        # Telefon marka, model ve tarih bilgilerini alma
        tel_marka = exif.get("Make", "Bilinmiyor")
        tel_model = exif.get("Model", "Bilinmiyor")
        foto_tarih = exif.get("DateTime", "Bilinmiyor")

        # Konum bilgisini alma
        konum = exif.get("GPSInfo")

        if konum:
            print(Bcolors.YELLOW + "Konum Bilgisi Bulundu. HTML Dosyası İçerisine Yazdırılıyor....\n" + Bcolors.ENDC)

            # Enlem ve boylamı al
            north = konum[2]
            east = konum[4]
            lat = ((((north[0] * 60) + north[1]) * 60) + north[2]) / 60 / 60
            long = ((((east[0] * 60) + east[1]) * 60) + east[2]) / 60 / 60
            lat, long = float(lat), float(long)

            # GeoLocator objesini oluştur
            geo_locator = Nominatim(user_agent="GetLoc")

            # Enlem ve boylamı kullanarak adres bilgisini al
            location_info = geo_locator.reverse(f"{lat}, {long}", language="tr")

            # Elde edilen konum bilgisini ekrana bastır
            print(f"Konum Adresi: {location_info.address}\n")

            # Adresi web tarayıcısında aç
            webbrowser.open_new_tab(location_info.address)

        else:
            print(Bcolors.GREEN +"\nKonum Bilgisi Bulunamadı." + Bcolors.ENDC)

        # Diğer bilgileri ekrana bastır
        print(Bcolors.GREEN + f"Telefon Markası: {tel_marka}" + Bcolors.ENDC)
        print(Bcolors.GREEN + f"Telefon Modeli: {tel_model}" + Bcolors.ENDC)
        print(Bcolors.GREEN + f"Fotoğraf Çekilme Tarihi: {foto_tarih}\n" + Bcolors.ENDC)

    except FileNotFoundError:
        print(Bcolors.RED + "Dosya bulunamadı." + Bcolors.ENDC)
    except Exception as e:
        print(Bcolors.RED + f"Hata oluştu: {e}" + Bcolors.ENDC)

if __name__ == "__main__":
    logo()
    while True:
        # Kullanıcıdan dosya adını al
        dosya_adı = input(Bcolors.GREEN + "Lütfen görselin dosya adını girin (örneğin: test333.jpg, çıkış için 'q'): " + Bcolors.ENDC)

        if dosya_adı.lower() == 'q':
            break

        # Fonksiyonu çağır
        exif_bilgilerini_incele(dosya_adı)