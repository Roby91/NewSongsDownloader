import urllib
import urllib2
import string
import os
import sys
import subprocess
import glob
import shutil
import unicodedata
import time
from subprocess import CalledProcessError, check_output



################################################################### Definizione variabili: ###############################################################

global output_1, output_2
posizioneYoutube_dlExe = "C:\Users\Roby\Dropbox\Backup\Documents\Python Scripts\Progetto ''New Songs Downloader''\youtube-dl.exe" #posizioneYoutube_dlExe = 'C:\Users\Roby\Desktop\youtube-dl.exe'
posizioneFFMPEG = "C:\Users\Roby\Dropbox\Backup\Documents\Python Scripts\Progetto ''New Songs Downloader''\MP4 to MP3 script\\ffmpeg\\ff-prompt.bat"
posizioneFileOutputAusiliare = 'C:\outputNewsDownloader.txt' # viene rimosso automaticamente al termine dello script
posizioneMP3gain = 'C:\Users\Roby\Dropbox\Backup\Portable\MP3Gain\mp3gain.exe'
cartellaDownloadVideo_TEMP = 'C:\TempNewSongDownloader\\'
percorsoRimuoviNonASCII = u'C:\TempNewSongDownloader\*'
cartellaDownloadMusica = "C:\Users\Roby\Dropbox\Backup\Documents\Python Scripts\Progetto ''New Songs Downloader''\Canzoni scaricate\\"
cartellaSyncMusica = "C:\Users\Roby\Dropbox\Sync\\"
logFileVideoMusicaliScaricati = "C:\Users\Roby\Dropbox\Backup\Documents\Python Scripts\Progetto ''New Songs Downloader''\logVideoMusicaliScaricati.txt"
#canaleVideoMusicale_1 = "https://www.youtube.com/user/SpinninRec/videos/" # ATTENZIONE allo slash finale del collegamento: il layout della pagina cambia
canaleVideoMusicale_1 = "https://www.youtube.com/user/SpinninRec/videos" # pagina dei video canale musicale Youtube "SpinninRec"
linkUltimoYoutubeDl = ""
videoDaScaricare = 0
conta = 0




################################################################# Definizione procedure: #################################################################

def remove_accents(s): 
    nkfd_form = unicodedata.normalize('NFKD', s) 
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])


def elimina_file_se_esiste(path):
  try:
      os.remove(path)
  except OSError:
      pass


def appendi_su_file(path, s):
  f = open(path,'a')
  #f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
  # da finire di implementare
  f.close()


######################################################################### Main: ###########################################################################

# scarico l'ultma versione del file "youtube-dl.exe" (se non e' aggiornato all'ultima versione da sempre errore):
print "\nControllo se ho la versione di 'youtube-dl.exe' piu' recente:\n"
if not os.path.isfile(posizioneYoutube_dlExe) : # se il file non esiste viene creato un file vuoto
  f = open(posizioneYoutube_dlExe,'w')
  f.close()
file_size2 = os.path.getsize(posizioneYoutube_dlExe)
print file_size2,
print "Bytes"
try:
  f = open(posizioneFileOutputAusiliare,'w')
except:
  os.system(['clear','cls'][os.name == 'nt'])
  print "\n\nSi e' verificato un errore nell'apertura di: 'C:\outputNewsDownloader.txt'\n"
  print "Questo script e' stato eseguito con privilegi di Amministratore (cmd) ???"
  raw_input("\n\n\n\n\nPress enter to close")
opener = urllib.FancyURLopener({})
source = opener.open('http://rg3.github.io/youtube-dl/download.html')
f.write(source.read()) # scrive l'intero codice sorgente sul file
f.close()
f = open(posizioneFileOutputAusiliare,'r')
for line in f.readlines():
    verificaStringa = string.find(line, '/youtube-dl.exe">Windows exe</a> ')
    if verificaStringa != -1:
      #print "\n"
      linkUltimoYoutubeDl = line.replace('	<a href="', "")[:61].replace('">', "").replace('Windows', "").replace('Window', "").replace('Windo', "").replace('Wind', "").replace('Win', "")
      #print linkUltimoYoutubeDl
f.close()
u = urllib2.urlopen(linkUltimoYoutubeDl)
#u = urllib2.urlopen("https://yt-dl.org/downloads/2014.08.10/youtube-dl-2014.08.10.tar.gz", timeout=600)
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print file_size,
print "Bytes"
if (file_size != file_size2) :
  if (linkUltimoYoutubeDl!="") :
    file_name = linkUltimoYoutubeDl.split('/')[-1]
    u = urllib2.urlopen(linkUltimoYoutubeDl)
    f = open(posizioneYoutube_dlExe, 'wb') #f = open("C:\Users\Roby\Desktop\youtube-dl.exe", 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "\nDownload della versione piu recente di " +'"%s" (%s Bytes)\n' % (file_name, file_size)
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d Bytes  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()
  else:
    print '\n\nAttenzione! Errore nel download dell'+"'"+'ultima versione di "youtube-dl.exe".'
    raw_input('\n\nPremi invio per continuare ma potrebbero verificarsi degli errori..')

# mi salvo l'intero codice HTML del canale YouTube:
f = open(posizioneFileOutputAusiliare,'w')
opener = urllib.FancyURLopener({})
source = opener.open(canaleVideoMusicale_1)
f.write(source.read()) # scrive l'intero codice sorgente sul file
f.close()

# creo un array di 300 elementi (da 0 a 299)
ArrayCodiciURLvideo = range(300)
codiceURLvideo = ''

# azzero l'arrey
for count in range(0,len(ArrayCodiciURLvideo)):
  ArrayCodiciURLvideo[count] = ""

# pulisco lo schermo:
os.system(['clear','cls'][os.name == 'nt']) # "os.system('cls')" on windows; "os.system('clear')" on linux / os x

f = open(posizioneFileOutputAusiliare,'r')
for line in f.readlines():
    #verificaStringa = string.find(line, 'class="yt-uix-button  shelves-play') # non funziona su tutti i canali
    verificaStringa = string.find(line, 'data-context-item-id=')
    if verificaStringa != -1:
      #codiceURL = line[26:37]
      codiceURL = line
      #print "\n\nCodice video: '"+codiceURL+"'"
      #print "\n\n'"+line[16:47]+"'"
      #print "\nCodice video: '"+codiceURL+"'\n"
      codiceURL = codiceURL.replace('data-context-item-id=', "").replace("deos?title=", "").replace("deos?featur", "").replace("deos?video_", "").replace("deos?type=0", "").replace(" ", "").replace('"', "").rstrip()
      if codiceURL != "" :
        ArrayCodiciURLvideo[conta] = codiceURL
        conta=conta+1
f.close()

os.remove(posizioneFileOutputAusiliare)

# conto le celle non vuote dell'arrey:
for count in range(0,len(ArrayCodiciURLvideo)):
  if (ArrayCodiciURLvideo[count] != "") :
    #print ArrayCodiciURLvideo[count]
    videoDaScaricare = videoDaScaricare + 1

i = 0
while i <= videoDaScaricare-1:
  os.system(['clear','cls'][os.name == 'nt']) # "os.system('cls')" on windows; "os.system('clear')" on linux / os x
  # rimuovo eventuali file temporanei o non scaricati completamente, all'interno della cartella "cartellaDownloadVideo_TEMP":
  for fname in glob.glob(percorsoRimuoviNonASCII):
              new_fname = remove_accents(fname)
              if new_fname != fname:
                  try:
                      print 'renaming non-ascii filename to', new_fname
                      os.rename(fname, new_fname)
                  except Exception as e:
                      print e
  # creo la cartella "cartellaDownloadVideo_TEMP" se non e' presente su disco (i.e. prima volta che lo script viene avviato):
  if not os.path.exists(cartellaDownloadVideo_TEMP):
    os.makedirs(cartellaDownloadVideo_TEMP)
  for file_name in os.listdir(cartellaDownloadVideo_TEMP) :
    r = (glob.glob(cartellaDownloadVideo_TEMP+"*"))
    if (r) :
      os.remove(r[0])
  print "\nProcedura download video '"+str(i+1)+"' di '"+str(videoDaScaricare)+"'\n\n" # se, durante l'output, nel prompt ci fosse per esempio "Procedura .... 5 di 9" come prima iterazione, e' perche' i primi 5 URL utili sono gia' stati scaricati!!!!
  codiceURLvideo = ArrayCodiciURLvideo[i].replace("['", '').replace("']", '')
  if (codiceURLvideo!="") :
    # Scansiono il file "logVideoMusicaliScaricati.txt" per sapere se ho gia' scaricato il video trovato nel canale:
    flagVideoPresente = -1
    f = open(logFileVideoMusicaliScaricati,'r')
    for line in f.readlines():
        verificaStringa = string.find(line, codiceURLvideo)
        if verificaStringa != -1:
          flagVideoPresente = 0 # "0" = video gia scaricato in precedenza...
    print "Codice URL video: '"+str(codiceURLvideo)+"'"
    f.close()
    if (flagVideoPresente==-1) :
      # prima di scaricarlo, controllo le dimensioni del video (es. starei troppo a scaricare un video da 1 ora)
      command_line = posizioneYoutube_dlExe+" --get-duration http://www.youtube.com/watch?v="+codiceURLvideo # ritorna la lunghezza del video es. "4:37"
      #command_line = posizioneYoutube_dlExe+" --get-duration http://www.youtube.com/watch?v=FFFFFFFFFFF"
      flagErrore = -1
      #from subprocess import CalledProcessError, check_output
      try:
        output_1 = subprocess.check_output(command_line)
        print "\nLunghezza video: ", # la virgola elimina il "\n" inserito di default
        print output_1
        print "\n"
        #output = int(str(output).rstrip().replace(':', '')) # output: valore INTERO della lunghezza del video (es. 1:02:35 -> 10235)
      except CalledProcessError as e:
        flagErrore = 0
        print "\nErrore nell'esecuzione del comando 'output = subprocess.check_output(command_line)'\n"
      if (flagErrore!=0) :
        output1_str = (str(output_1))
        output1_str = output1_str.rstrip().replace(':', '')
        output1_int = int(output1_str)
        #output = output_int
        #output = int(str(output).rstrip().replace(':', '')) # output: valore INTERO della lunghezza del video (es. 1:02:35 -> 10235)
        if (output1_int<=600 and output1_int>=150) : # ossia se minore ai 6 minuti
          # cambiare cartella di destinazione: >> youtube-dl -o 'C:/Users/leegold/Downloads/%(title)s-%(id)s.%(ext)s'
          command_line = posizioneYoutube_dlExe+" -o "+cartellaDownloadVideo_TEMP+"%(title)s.%(ext)s -v http://www.youtube.com/watch?v="+codiceURLvideo
          #print "\n\ncommand_line: '"+command_line+"'\n\n"
          #raw_input("\n\nPress enter to continue")
          p = subprocess.Popen(command_line)
          p.wait()
          nomeFileScaricato = str(glob.glob(cartellaDownloadVideo_TEMP+"*.mp4"))
          nomeFileScaricato = nomeFileScaricato.replace('\\', '').replace('C:', '').replace('UsersRobyDesktopTemp', '').replace("['", '').replace("']", '').replace("TempNewSongDownloadera.mp4", '').replace("TempNewSongDownloader", '').replace("', '", '').replace('.mp4','').replace("[", "").replace("]", "");
          print nomeFileScaricato
          print '\n\nScaricato il file: '+nomeFileScaricato
          # converto il file .mp4 scaricato in .mp3
          # IMPORTANTE: il percorso per arrivare a "ffmpeg.exe" e quello dei suoi parametri non possono contenere spazi!!!!!!!
          # os.system("C:/ffmpeg/bin/ffmpeg.exe -i C:/TempNewSongDownloader/a.mp4 -f mp3 -ab 320000 -vn C:/TempNewSongDownloader/a.mp3") # es funzionante conversione
          print "\n\nnomeFileScaricato: '"+nomeFileScaricato+"'\n"
          if (nomeFileScaricato!="") : # ogni tanto accade che lo script arrivi a questo punto con "nomeFileScaricato" vuoto, generando successivamente un errore
            # elimino i caratteri non ASCII (piu precisamente le lettere accentate) dei file scaricati, in modo che siano successivamente manipolabili dallo script
            for fname in glob.glob(percorsoRimuoviNonASCII):
              new_fname = remove_accents(fname)
              if new_fname != fname:
                  try:
                      print 'renaming non-ascii filename to', new_fname
                      os.rename(fname, new_fname)
                  except Exception as e:
                      print e
            # aggiorno il nome del file scaricato (con le righe di codice sopra, elimino i caratteri non ASCII del file, dunque il nome del file viene modificato):
            nomeFileScaricato = str(glob.glob(cartellaDownloadVideo_TEMP+"*.mp4"))
            nomeFileScaricato = nomeFileScaricato.replace('\\', '').replace('C:', '').replace('UsersRobyDesktopTemp', '').replace("['", '').replace("']", '').replace('["', '').replace('"]', '').replace("TempNewSongDownloadera.mp4", '').replace("TempNewSongDownloader", '').replace("', '", '').replace('.mp4','').replace("[]", "");
            #print "\n\n"
            #print nomeFileScaricato
            #print "\n\n"
            os.rename(cartellaDownloadVideo_TEMP+nomeFileScaricato+'.mp4',cartellaDownloadVideo_TEMP+'a.mp4')
            # converto il file video .mp4 in .mp3
            stringa = "C:/ffmpeg/bin/ffmpeg.exe -i "+cartellaDownloadVideo_TEMP+"a.mp4 -f mp3 -ab 256000 -vn "+cartellaDownloadVideo_TEMP+"a.mp3"
            os.system(stringa)
            print '\n\n'
            # applico la normalizzazione del volume (89db) del brano appena convertito
            # C:\Users\Roby\Dropbox\Backup\Portable\MP3Gain\mp3gain.exe -a -k "C:\Users\Roby\Desktop\a.mp3"
            stringa = posizioneMP3gain + ' -a -k "' + cartellaDownloadVideo_TEMP + 'a.mp3"'
            os.system(stringa)
            print '\n\n'
            os.rename(cartellaDownloadVideo_TEMP+'a.mp3',cartellaDownloadVideo_TEMP+nomeFileScaricato+'.mp3')
            os.rename(cartellaDownloadVideo_TEMP+'a.mp4',cartellaDownloadVideo_TEMP+nomeFileScaricato+'.mp4')
            shutil.copy2(cartellaDownloadVideo_TEMP+nomeFileScaricato+'.mp3', cartellaDownloadMusica+nomeFileScaricato+'.mp3')
            #shutil.copy2(cartellaDownloadVideo_TEMP+nomeFileScaricato+'.mp3', cartellaSyncMusica+nomeFileScaricato+'.mp3')
            r = (glob.glob(cartellaDownloadVideo_TEMP+"*.mp3"))
            if (not r) :
              print "non esistono elementi del tipo cercato..."
            else:
              stringa = r[0]
              os.remove(stringa)
            r = (glob.glob(cartellaDownloadVideo_TEMP+"*.mp4"))
            if (not r) :
              print "non esistono elementi del tipo cercato..."
            else:
              stringa = r[0]
              os.remove(stringa)
            r = (glob.glob(cartellaDownloadVideo_TEMP+"*.part"))
            if (not r) :
              print "non esistono elementi del tipo cercato..."
            else:
              stringa = r[0]
              os.remove(stringa)
            f = open(logFileVideoMusicaliScaricati,"a") # file open in appending mode
            f.write(nomeFileScaricato.replace(".mp4", '')+" | URL: "+codiceURLvideo+"\n")
            f.close()
        else:
          # aggiungo al log "logVideoMusicaliScaricati.txt" il video dalla durata troppo lunga
          command_line = posizioneYoutube_dlExe+" --get-title http://www.youtube.com/watch?v="+codiceURLvideo # ritorna la lunghezza del video es. "4:37"
          output2 = subprocess.check_output(command_line)
          output2_str = str(output2).rstrip()
          f = open(logFileVideoMusicaliScaricati,"a") # file open in appending mode
          f.write(output2_str+" | URL: "+codiceURLvideo+"\n")
          f.close()
  i=i+1 # while
      
print "\nNon ci sono nuovi video musicali da scaricare..."
#raw_input("\n\nPress enter to continue")
time.sleep(10) # dopo 10 secondi, lo script termina in automatico