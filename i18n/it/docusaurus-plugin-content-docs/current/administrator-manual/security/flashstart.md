---
title: "Filtro DNS FlashStart"
sidebar_position: 5
---

# Filtro DNS FlashStart {#flashstart-section}

Il filtraggio DNS si integra con software di filtraggio dei contenuti basato su DNS di terze parti. Il filtro dei contenuti predefinito supportato è quello fornito da [FlashStart](https://www.flashstart.com).

Essenzialmente collega 2 componenti: configurazione del filtro e configurazione di rete.

1.  La configurazione del filtro dei contenuti avviene interamente sulla piattaforma di terze parti, in genere è possibile bloccare singoli siti web, nonché categorie di siti (ad es. contenuti per adulti), gestire eccezioni, visualizzare report e così via.
2.  La configurazione di rete è completamente automatizzata ed è eseguita su NethSecurity che si occupa di:

- connettere il firewall all'istanza specifica di terze parti
- reindirizzare tutte le richieste DNS al servizio esterno
- aggiornare automaticamente gli indirizzi IP di tutte le connettività

:::note

Abbonamento richiesto

Questa funzione è disponibile solo se il firewall ha un abbonamento valido.

:::

:::note

Prima di configurare NethSecurity è necessario creare un account su FlashStart e configurare il servizio. FlashStart è un servizio a pagamento che consente di utilizzare licenze di prova. Fare riferimento alla documentazione del fornitore [doc](https://cloud.flashstart.com/customerarea/support/docs).

:::

:::warning

Non specificare manualmente gli indirizzi IP dei server DNS FlashStart, in quanto vengono gestiti automaticamente dall'integrazione.

:::

Una volta creato l'account e configurato il servizio, NethSecurity può essere configurato.

## Raccomandazioni prima di configurare il filtro DNS FlashStart

Prima di abilitare il filtro DNS FlashStart, si prega di considerare le seguenti raccomandazioni importanti:

1.  **Comportamento del reindirizzamento DNS** Quando il filtraggio dei contenuti è abilitato, tutto il traffico DNS dai client verrà automaticamente reindirizzato al servizio di filtraggio FlashStart esterno, indipendentemente dalla loro configurazione. **Non apportare modifiche ai server DNS configurati in NethSecurity o nei client di rete.**
2.  **Bloccare i protocolli DNS alternativi** Per preservare l'efficacia del filtro dei contenuti, è fortemente consigliato bloccare i protocolli DNS alternativi come DoT e DoH. L'approccio più efficace è utilizzare l'elenco IP di Threat Shield "public DoH-Provider" per bloccare i provider DoH noti e rifiutare tutte le connessioni TCP in uscita sulla porta 853 per bloccare il traffico DoT.
3.  **Evitare conflitti con DNS Threat Shield** Usa FlashStart solo se **non stai già utilizzando il servizio Threat Shield DNS**, in quanto l'utilizzo simultaneo di entrambi potrebbe portare a conflitti.

## Configurazione

### Configurazione della piattaforma FlashStart

Prima di configurare FlashStart sul tuo firewall, devi prima acquistare e configurare il servizio **Pro** o **Pro Plus** sulla piattaforma FlashStart. Una volta acquistato il servizio, dovrai configurare le reti nel portale FlashStart.

Durante il processo di configurazione, il sistema ti guiderà attraverso l'installazione. Segui i suggerimenti e seleziona le seguenti opzioni:

Connetti il router della tua rete → Ho un IP dinamico → Nethesis Dynamic DNS → NethSecurity → Scegli PRO o PRO PLUS.

:::note

A partire dal 2 luglio 2025, la piattaforma FlashStart richiede di creare un nuovo nome utente e una nuova password durante questo passaggio di configurazione. Si noti che non è più possibile utilizzare l'accesso basato su email precedentemente associato al tuo account. Una volta create le nuove credenziali, devono essere utilizzate per l'autenticazione sul lato firewall.

:::

Le reti precedentemente configurate utilizzando l'accesso basato su email continueranno a funzionare normalmente finché non vengono rimosse. Se una rete viene rimossa, il sistema richiederà una nuova coppia di nome utente e password e le credenziali corrispondenti devono essere aggiornate anche sul lato NethSecurity.

### Configurazione di NethSecurity

- `Stato` : Puoi abilitare o disabilitare il filtro DNS utilizzando l'interruttore di attivazione `Stato`
- `Tipo di servizio` : Seleziona il tipo di servizio che hai acquistato: **Pro** o **Pro Plus**
- `Nome utente` : Immetti lo stesso nome utente utilizzato per il tuo account FlashStart
- `Password` : Immetti la stessa password utilizzata per il tuo account FlashStart
- `Zone da filtrare` : Seleziona le zone di rete che desideri proteggere con il filtraggio DNS. Solo le zone selezionate saranno interessate dal filtro DNS FlashStart.
- `IP sorgente o reti bypass` : Puoi specificare un elenco di indirizzi IP o reti (formato CIDR) che dovrebbero bypassare il filtraggio DNS. Il traffico da queste fonti non sarà soggetto ad alcuna regola di filtraggio.
- `Server DNS personalizzati` : Se hai bisogno di definire **resolver DNS personalizzati per domini specifici**, puoi configurarli qui. La sintassi è la stessa utilizzata nella sezione DNS di NethSecurity. Per riferimento, consulta la documentazione ufficiale: `Server DNS specifici per dominio <https://docs.nethsecurity.org/en/latest/dns_dhcp.html#domain-specific-dns-servers>`_

Una volta configurato il servizio FlashStart sul firewall, tutte le ulteriori configurazioni e la gestione devono essere eseguite esclusivamente tramite il portale web FlashStart. Non sono richiesti ulteriori modifiche sul firewall stesso.

### Configurazione del server DNS

I server DNS utilizzati da FlashStart vengono configurati automaticamente da NethSecurity quando il servizio è abilitato. È possibile personalizzare alcune opzioni:

- **Registrazione delle query**: Puoi abilitare la registrazione delle query eseguendo il seguente comando:

  ``` 
  uci set flashstart.global.logqueries='1'
  uci commit flashstart
  reload_config
  ```

  Questo registrerà le query DNS nel log di sistema del firewall, che può essere utile per il tracciamento e la risoluzione dei problemi.

- **Protezione da DNS Rebind**

La protezione da DNS Rebind è disabilitata per impostazione predefinita per i client FlashStart al fine di prevenire blocchi indesiderati quando i server DNS interni risolvono domini privati o interni che potrebbero altrimenti essere segnalati dal meccanismo di protezione da DNS Rebind del firewall. Se necessario, questa protezione può essere abilitata manualmente utilizzando la seguente configurazione:

``` 
uci set flashstart.global.rebind_protection='1'
uci commit flashstart
reload_config
```

## Presenza di un controller Active Directory (AD)

Se è presente un controller AD, è possibile abilitare la profilazione basata sull'utente. Per farlo, è necessario installare prima il connettore FlashStart specifico (fare riferimento alla [documentazione](https://cloud.flashstart.com/customerarea/support/docs) ufficiale di FlashStart per le istruzioni di installazione), **questo è attualmente disponibile solo per Microsoft Windows Server**.

### Gestione DNS nella rete

Tutti i client sulla rete devono instradare le loro richieste DNS attraverso NethSecurity invece di interrogare direttamente il controller AD, questo impedisce ai client di ereditare la politica di profilazione del controller AD.

#### Dettagli di configurazione

- Il controller AD utilizza un resolver DNS esterno.
- Nell'interfaccia utente DNS FlashStart su NethSecurity, aggiungi il dominio locale del controller AD per la risoluzione, specificando l'indirizzo IP del controller AD per risolvere questi nomi locali (ad es., `/ad.mydomain.local/192.168.55.1`).
- Configura i client per utilizzare come resolver DNS un server DNS esterno o il firewall stesso.

#### Note importanti

È necessario impedire ai client di interrogare il controller AD per la risoluzione di domini non locali, questo può essere ottenuto da:

- Bloccare la porta UDP/TCP 53 in ingresso sul controller AD
- disabilitare la ricorsione DNS per i client sul server AD, in modo che il server risponda solo alle query per la sua zona locale.

## FlashStart Pro vs FlashStart Pro Plus

FlashStart fornisce soluzioni di filtraggio dei contenuti basate su cloud integrate con NethSecurity. I due principali tipi di servizio, FlashStart Pro e FlashStart Pro Plus, offrono diverse capacità in termini di granularità del filtraggio e gestione dei profili. Di seguito è riportato un breve confronto evidenziando le principali differenze.

### FlashStart Pro

FlashStart Pro abilita il filtraggio dei contenuti utilizzando un singolo profilo di filtro, applicato alla rete o alle zone di rete selezionate.

- **Filtraggio con profilo singolo:** Tutti gli IP filtrati seguono le stesse regole e blocchi di categoria definiti sulla piattaforma FlashStart.
- **Applicazione basata su zona:** Gli amministratori possono scegliere quali zone di rete sono soggette al filtraggio.
- **Gestione del profilo basata su IP:** FlashStart Pro su NethSecurity supporta implicitamente tre profili di traffico, basati su IP:
  - IP filtrati : Soggetti al singolo profilo di filtro definito in FlashStart.
  - IP non filtrati : Nessun filtraggio applicato (vedi Esclusioni di seguito)
  - IP bloccati : Accesso negato a livello di firewall utilizzando le regole del firewall.
- **Esclusioni:** Le eccezioni possono essere configurate utilizzando indirizzi IP o blocchi CIDR.

### FlashStart Pro Plus (Beta)

FlashStart Pro Plus estende la funzionalità con il supporto per più profili di filtraggio indipendenti, consentendo maggiore flessibilità e applicazione della politica a livello di utente.

- **Supporto multi-profilo:** È possibile definire fino a 5 profili indipendenti, ciascuno con la propria configurazione di filtraggio.
- **Configurazione del profilo indipendente:** Ogni profilo può essere personalizzato individualmente (categorie, ricerca sicura, restrizioni YouTube, ecc.).
- **Opzioni dei criteri di filtraggio:** I profili possono essere assegnati utilizzando:
  - **Oggetti firewall (set di host):** Dal pannello di configurazione FlashStart, gli amministratori possono associare set di host specifici (definiti nel firewall) a un profilo.
  - **Utenti Active Directory:** Se il connettore FlashStart AD è installato, i profili possono essere assegnati agli utenti AD direttamente, eliminando la necessità di fare affidamento su indirizzi IP.

:::note

A causa dei limiti della piattaforma, il sistema può gestire set di host con un numero limitato di elementi.

Se il set contiene solo host, può includere fino a 16 voci. Se contiene solo reti CIDR, può includere fino a 13 voci. Se il set di host contiene dati misti (sia host che reti), è consigliabile fare riferimento al limite inferiore (13).

:::

### Funzioni comuni (Pro e Pro Plus)

- **Stesse capacità di filtraggio:**
  - Filtraggio basato su categoria di URL (liste nere)
  - Filtraggio del motore di ricerca (Ricerca sicura)
  - Modalità limitata di YouTube
  - Protezione dalle minacce
- **Configurazione gestita dal cloud:** Tutte le regole di filtraggio e i profili vengono gestiti tramite l'interfaccia web FlashStart.

| Funzione | FlashStart Pro | FlashStart Pro Plus |
|----|----|----|
| Filtraggio basato su zona | Sì | Sì |
| Esclusioni del profilo (IP/CIDR) | Sì | Sì |
| Numero di profili di filtro | 1 | Fino a 5 |
| Blocco IP | No | Sì |
| Blocco app | No | Sì |
| Agente remoto per Win/Mac/Android/iOS | No | Sì |
| Filtraggio per utente AD | No | Sì |
| Integrazione di oggetti firewall | No | Sì |
| Gestione dei conflitti (utente vs oggetto) | N/A | L'oggetto firewall ha la priorità |

:::note

Sebbene non siano stati segnalati bug noti in questo momento, la funzione Pro Plus è attualmente rilasciata come **Beta**. Si consiglia di testarla in un ambiente non critico prima di distribuirla in produzione.

:::

## Risoluzione dei problemi

### 1. Il mio IP pubblico non è elencato nelle reti FlashStart {#my-public-ip-is-not-listed-in-the-flashstart-networks}

Se il tuo indirizzo IP pubblico non appare nel dashboard FlashStart sotto le reti registrate, attendi fino a 15 minuti. Questo ritardo potrebbe essere causato da meccanismi di protezione sulla piattaforma FlashStart progettati per mitigare i tentativi di registrazione ripetuti o automatizzati.

### 2. Il filtraggio DNS non sembra funzionare {#dns-filtering-does-not-seem-to-be-working}

Se il filtraggio non è efficace immediatamente dopo la configurazione:

- Tieni presente che FlashStart potrebbe richiedere alcuni minuti per propagare le impostazioni applicate nella sua infrastruttura.
- Considera anche l'impatto della cache DNS del browser, che potrebbe ritardare gli effetti visibili.

Per verificare se il filtraggio è effettivamente in atto e funzionante, puoi eseguire una query DNS manuale **dal tuo client locale** utilizzando il comando `dig`:

``` bash
dig @8.8.8.8 www.mydomain.com
```

Sostituisci `www.mydomain.com` con il dominio effettivo che stai testando.

Se il dominio è ancora risolto e dovrebbe essere bloccato, verifica di nuovo il profilo attivo e le impostazioni di blocco sul dashboard FlashStart.

:::note

Questo test `dig` deve sempre essere eseguito dal **client** e **mai dal firewall**. Il firewall **non viene mai** filtrato dai server DNS FlashStart, in quanto ciò potrebbe potenzialmente entrare in conflitto con alcuni dei servizi che fornisce.

:::

### 3. Test del filtraggio DNS con dig direttamente dal firewall {#testing-dns-filtering-with-dig-directly-from-the-firewall}

Se desideri eseguire test utilizzando `dig` direttamente dal firewall, puoi farlo specificando la porta. Ogni porta corrisponde a un profilo di filtraggio diverso.

#### FlashStart Pro

Se stai utilizzando **FlashStart Pro**, la porta è sempre **5300**. Puoi verificare se la richiesta è correttamente filtrata con il seguente comando:

``` bash
dig @127.0.0.1 -p 5300 mydomain.com
```

#### FlashStart Pro Plus

Se stai utilizzando **FlashStart Pro Plus**, ogni profilo è associato a una porta diversa. Puoi inviare una richiesta per profilo per verificare che il filtraggio si comporti come previsto.

Innanzitutto, devi identificare la porta corretta per ogni profilo. Usa il seguente comando per visualizzare la configurazione:

``` bash
uci show dhcp
```

Vedrai più voci come questa:

``` bash
dhcp.ns_56e6071cbd=dnsmasq
dhcp.ns_56e6071cbd.ns_flashstart='1'
dhcp.ns_56e6071cbd.ns_tag='automated'
dhcp.ns_56e6071cbd.ns_flashstart_profile='Guests'
dhcp.ns_56e6071cbd.ns_flashstart_dns_code='143'
dhcp.ns_56e6071cbd.port='5301'
dhcp.ns_56e6071cbd.noresolv='1'
dhcp.ns_56e6071cbd.max_ttl='60'
dhcp.ns_56e6071cbd.max_cache_ttl='60'
dhcp.ns_56e6071cbd.server='185.236.104.124' '185.236.105.125'
```

In questo esempio, il profilo **"Guests"** è associato alla porta **5301**, quindi eseguiresti:

``` bash
dig @127.0.0.1 -p 5301 mydomain.com
```
