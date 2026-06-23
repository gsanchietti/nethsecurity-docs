---
title: "Monitoraggio"
sidebar_position: 1
---

# Monitoraggio {#monitoring-section}

NethSecurity fornisce capacità di monitoraggio complete per aiutare gli amministratori a tracciare le prestazioni e lo stato di salute del firewall. Il monitoraggio è essenziale per garantire il funzionamento ottimale del firewall e identificare potenziali problemi che potrebbero compromettere la sua funzionalità.

NethSecurity offre 3 viste di monitoraggio:

- **Monitoraggio in tempo reale**: sfrutta Telegraf, Netifyd e i log per fornire informazioni immediate sulle prestazioni e lo stato del firewall, con grafici e avvisi dettagliati. Utilizza anche l'agente Netify e i log per fornire informazioni immediate sul traffico del firewall, sulle connessioni VPN e sugli eventi di sicurezza.
- **Monitoraggio storico**: Telegraf scrive i suoi dati all'interno di VictoriaMetrics, che salva le metriche nell'archiviazione persistente locale, quando disponibile. Il monitoraggio storico locale è disponibile a partire da NethSecurity 8.8 e non richiede una sottoscrizione.
- **Monitoraggio remoto**: quando il firewall è collegato a un controller, le metriche vengono anche archiviate in remoto utilizzando Prometheus. Ciò consente di conservare le metriche per un periodo più lungo e abilita il monitoraggio centralizzato. Si noti che il controller archivierà le metriche solo se sia il firewall che il controller stesso dispongono di una sottoscrizione valida.

## Monitoraggio in tempo reale {#real_time_monitoring-section}

Il monitoraggio in tempo reale è una funzione essenziale nei moderni sistemi firewall, che consente agli amministratori di avere una visibilità istantanea sul traffico di rete, sulle connessioni VPN e sulle minacce di sicurezza. In NethSecurity, il monitoraggio in tempo reale fornisce dati in diretta, assicurando che problemi come congestione di rete, accesso non autorizzato e violazioni della sicurezza siano identificati e mitigati tempestivamente. Il monitoraggio in tempo reale memorizza i dati in RAM e si ripristina ad ogni riavvio della macchina.

La pagina `Real-time monitor` fornisce una panoramica completa delle prestazioni e dello stato del firewall, con informazioni dettagliate sul traffico di rete. È divisa in quattro sezioni principali: `Traffic`, `Live Flows`, `Top Talkers`, `WAN uplinks`, `VPN` e `Security`.

### Daily Traffic

I grafici sottostanti leggono i dati dal daemon [dpireport](https://dev.nethsecurity.org/packages/ns-report/):

- `Daily total traffic`: questo contatore mostra il volume totale di dati trasferiti attraverso il firewall per il giorno corrente.
- `Recent traffic`: l'istogramma del traffico giornaliero rappresenta visivamente il traffico di rete nel tempo, aggiornato ogni 60 minuti. Aiuta a identificare i periodi di picco e analizzare le fluttuazioni del traffico durante il giorno. I picchi o i cali improvvisi potrebbero indicare potenziali problemi di prestazioni o minacce di sicurezza.
- `Local Hosts`: questo grafico si concentra sugli host (locali) interni e sul loro traffico. Aiuta a identificare i dispositivi più attivi sulla rete, facilitando la gestione della larghezza di banda e il rilevamento di potenziali rischi di sicurezza interna, come dispositivi compromessi che generano traffico inaspettato.
- `Applications`: questo grafico mostra il traffico per applicazione, consentendo di monitorare quale software o servizi generano il maggior traffico. È utile per comprendere il comportamento dell'applicazione, rilevare i consumatori di larghezza di banda e monitorare la conformità alle politiche di utilizzo.
- `Remote Hosts`: questo grafico elenca gli host esterni (remoti) che hanno scambiato il maggior volume di dati con la rete. Analizzando questi dati, gli amministratori possono tracciare le interazioni con entità esterne specifiche, aiutando a rilevare fonti esterne dannose o modelli di traffico in uscita insoliti.
- `Protocol`: questo grafico mostra la ripartizione del traffico giornaliero per protocollo (ad es. HTTP, HTTPS, FTP). È utile per identificare quali protocolli consumano la maggior larghezza di banda e garantire che le risorse di rete vengano utilizzate in modo appropriato. L'elevato utilizzo di protocolli sconosciuti potrebbe indicare attività non autorizzate.

È possibile restringere la ricerca per un host, un'applicazione o un protocollo specifico facendo clic sulla rispettiva etichetta nella tabella sotto il grafico.

### Live Flows

La sezione Live Flows fornisce una visualizzazione in tempo reale di tutte le connessioni di rete attive, consentendo agli amministratori di monitorare il traffico mentre accade, questa sezione è visualizzata in formato tabella, con ogni riga che rappresenta un singolo flusso. La tabella include le seguenti informazioni per ogni connessione:

- `Application`: l'applicazione rilevata che genera il traffico.
- `Protocol`: il protocollo di rete utilizzato per il flusso (ad es. TCP, UDP, HTTP).
- `Tags`: eventuali tag rilevanti assegnati al flusso per la classificazione (ad es. Outgoing, Remote, Internal)
- `Source`: l'origine della connessione, in genere mostrando l'indirizzo IP e la porta del dispositivo che avvia.
- `Destination`: la destinazione della connessione, in genere mostrando il nome host o l'indirizzo IP e la porta del dispositivo di destinazione.
- `Download`: la velocità di trasferimento di download corrente del flusso, indicando la velocità con cui i dati vengono ricevuti.
- `Upload`: la velocità di trasferimento di upload corrente del flusso, indicando la velocità con cui i dati vengono inviati.
- `Duration`: il tempo totale durante il quale il flusso è rimasto attivo dal primo rilevamento. Questo aiuta a comprendere per quanto tempo una particolare connessione è stata mantenuta.
- `Last Seen At`: il timestamp dell'attività più recente per il flusso, questo indica quando il flusso ha trasmesso o ricevuto dati l'ultima volta, aiutando a identificare le connessioni inattive o inattive.
- `Details`: l'icona della lente d'ingrandimento con un segno più, facendo clic su questa icona si apre una visualizzazione dettagliata del flusso, mostrando tutte le informazioni disponibili, inclusi i dati non direttamente visualizzati nella tabella principale. Questo consente agli amministratori di accedere ai metadati completi del flusso per un'analisi più approfondita o per la risoluzione dei problemi.

Questa tabella in tempo reale consente agli operatori di identificare rapidamente gli utenti pesanti, monitorare il comportamento dell'applicazione e risolvere i problemi di rete man mano che si verificano.

#### Configuration

La sezione Live Flows include anche opzioni di configurazione per gestire il comportamento del servizio di monitoraggio dei flussi:

- `Flows Daemon Enabled`: un interruttore per abilitare o disabilitare il servizio di monitoraggio dei flussi in diretta, disattivando il daemon interrompe la raccolta dei dati di flusso in tempo reale.
- `Flows Persistence After Expiration`: un'impostazione che determina per quanto tempo i record di flusso vengono conservati dopo la fine del flusso, questo consente agli amministratori di regolare la conservazione dei dati in base alle esigenze di monitoraggio e alla disponibilità di archiviazione.

### Top Talkers

Lo scopo principale della sezione Top Talkers è fornire un'iniziale panoramica dell'utilizzo della larghezza di banda, identificando rapidamente i principali "contributori" al traffico di rete. Queste informazioni possono fungere da punto di partenza per un'analisi più profonda, la risoluzione dei problemi o il monitoraggio generale dell'efficienza di rete.

La sezione Top Talkers visualizza i dati sul traffico aggiornati ogni 30 secondi, fornendo una panoramica rapida e aggiornata di quali entità stanno generando il maggior traffico di rete, è divisa in tre categorie:

- `Local Hosts`: elenca tutti gli host locali rilevati e il loro stato di traffico corrente, ordinati per volume di traffico. Ciò consente di identificare rapidamente quali dispositivi utilizzano la maggior larghezza di banda, senza distinguere il tipo di connessione o il protocollo.
- `Applications`: mostra tutte le applicazioni rilevate e il loro traffico corrente, ordinati per volume. Questa visualizzazione aiuta a comprendere quali servizi o applicazioni sono in grado di consumare il maggior volume di risorse di rete, indipendentemente dal dispositivo che le esegue.
- `Protocols`: elenca tutti i protocolli rilevati e il loro traffico corrente, ordinati per volume. Ciò fornisce una visione immediata di quali tipi di traffico (ad esempio, HTTP, DNS, SMTP) dominano la rete, senza considerare quale host o applicazione li genera.

### WAN uplinks

La sezione WAN uplinks fornisce una panoramica delle connessioni WAN, inclusi stato, allocazione della larghezza di banda e dati sul traffico.

Questa pagina mostra le seguenti informazioni:

- `WANs`: elenco delle connessioni WAN con il loro stato attuale (UP/DOWN) e indirizzo IP pubblico. Le informazioni sullo stato aiutano a garantire che le connessioni di rete critiche siano online, e qualsiasi tempo di inattività venga affrontato immediatamente. I dati provengono dallo stato mwan3 del firewall.
- `WAN events`: questa sezione elenca gli eventi recenti di connessione e disconnessione WAN delle ultime 24 ore, fornendo informazioni sulla stabilità della rete e sulle interruzioni. Aiuta gli amministratori a comprendere la frequenza e la durata dei disturbi di rete, facilitando la risoluzione dei problemi e la pianificazione della capacità. I dati vengono recuperati dai log degli ultimi 24 ore. Se i log non coprono il periodo completo di 24 ore, i dati potrebbero essere incompleti. I risultati vengono memorizzati nella cache per 5 minuti.
- `WAN interface traffic`: questo istogramma mostra i dati sul traffico per ogni connessione WAN negli ultimi 60 minuti. Aiuta a tracciare le prestazioni in tempo reale e a diagnosticare i problemi come il bilanciamento del carico non uniforme o la saturazione del collegamento WAN.
- `Latency to <address>`: questa sezione fornisce dati di latenza in tempo reale per uno specifico indirizzo IP configurato all'interno del modulo [Ping latency monitoring](#ping_latency-section). Il grafico aiuta a monitorare le prestazioni di rete e a identificare potenziali problemi di connettività.
- `Packet delivery rate to <address>`: questa sezione fornisce dati di tasso di consegna dei pacchetti in tempo reale per uno specifico indirizzo IP configurato all'interno del modulo [Ping latency monitoring](#ping_latency-section). Se la velocità è inferiore al 100%, potrebbe indicare congestione di rete o problemi di connettività.

### VPN

La sezione VPN fornisce informazioni dettagliate sui server OpenVPN Road Warrior, sui tunnel OpenVPN e sui tunnel IPsec.

Per ogni server OpenVPN Road Warrior, vengono visualizzate le seguenti informazioni:

- `Status`: questa sezione mostra lo stato corrente del server OpenVPN. Aiuta gli amministratori a monitorare la disponibilità del servizio VPN e a rilevare eventuali problemi che potrebbero influire sulla connettività dell'utente.
- `Connected clients`: questo visualizza il numero totale di utenti attualmente registrati sul server VPN. Il monitoraggio degli utenti registrati è cruciale per garantire la pianificazione della capacità e le prestazioni VPN, in particolare quando il sistema si avvicina all'utilizzo massimo.
- `Total traffic by hour`: questo grafico mostra il totale dei dati trasferiti da tutti i client VPN durante ogni ora, fornendo una panoramica dell'utilizzo della larghezza di banda VPN. Aiuta a tracciare la quantità di traffico di rete generata dalla VPN e a identificare le ore con utilizzo pesante, che potrebbe portare a problemi di prestazioni.
- `Daily connections`: questa sezione elenca tutti gli utenti VPN attualmente connessi e l'ora in cui si sono connessi. È utile per tracciare la durata della sessione e rilevare potenziali abusi della VPN, come connessioni che durano insolitamente a lungo. I dati provengono dal database di connessione SQLite locale.
- `Connected clients by hour`: questo grafico mostra il numero di client connessi alla VPN nel tempo. Consente agli amministratori di monitorare l'attività VPN durante il giorno, aiutando a identificare i momenti di picco e a pianificare l'aumento della capacità quando necessario. I dati provengono dal database di connessione SQLite locale.
- `Client traffic by hour`: questo grafico suddivide il traffico VPN per singoli client nel tempo. Aiuta a rilevare gli utenti che potrebbero consumare una larghezza di banda eccessiva o partecipare ad attività non autorizzate, facilitando l'identificazione di potenziali minacce interne. I dati provengono dal database di connessione SQLite locale.

La sezione Site-to-Site VPN fornisce informazioni sui tunnel OpenVPN e IPsec:

- `Connected tunnels`: questo contatore mostra il numero di tunnel VPN da sito a sito attivi.
- `Configured tunnels`: questo contatore mostra l'elenco di tutti i tunnel VPN da sito a sito configurati, incluso il loro stato e tipo.
- `Tunnel traffic`: questo istogramma fornisce dati di traffico in tempo reale per ogni tunnel VPN da sito a sito negli ultimi 60 minuti. Aiuta a rilevare problemi come scarso throughput o instabilità della connessione.

### Security

La sezione di sicurezza fornisce informazioni su rilevamento di malware e monitoraggio degli attacchi, aiutando gli amministratori a identificare e mitigare le minacce di sicurezza. Per abilitare questa sezione, il modulo [Threat shield IP](../security/threat_shield_ip.md) deve essere abilitato. I dati provengono dai log che coprono le ultime 24 ore. Se i log non si estendono all'intero periodo di 24 ore, i dati potrebbero essere incompleti. I risultati vengono memorizzati nella cache per 5 minuti per migliorare le prestazioni.

La sezione `Blocklist` fornisce una panoramica dei pacchetti bloccati in base alle blocklist abilitate. I grafici disponibili sono:

- `Blocked threats`: questo contatore mostra il numero totale di pacchetti bloccati dal firewall a causa del rilevamento di malware per il giorno corrente. Fornisce una chiara panoramica del volume delle minacce intercettate, dando agli amministratori una misura dell'efficacia del firewall.
- `Blocked threats by hour`: questo grafico traccia il numero di pacchetti bloccati ogni ora. Aiuta a identificare i momenti della giornata in cui la rete è più vulnerabile agli attacchi, facilitando le misure preventive.
- `Threats by direction`: un grafico che mostra la distribuzione del malware bloccato per catena firewall. A seconda dell'opzione di registrazione abilitata, il firewall può registrare pacchetti dalle seguenti catene:
  - *inp-wan*: pacchetti provenienti dall'interfaccia WAN e destinati al firewall
  - *fwd-wan*: pacchetti provenienti dall'interfaccia WAN e destinati alla rete LAN
  - *fwd-lan*: pacchetti provenienti dalla rete LAN e destinati all'interfaccia WAN
  - *pre-ct*: pacchetti di flood che si trovano in uno stato non valido
  - *pre-syn*: pacchetti di flood che fanno parte di una connessione TCP e si trovano nello stato SYN
  - *pre-udp*: pacchetti di flood che fanno parte di una connessione UDP
- `Threats by category`: un grafico che suddivide il malware bloccato per categoria, aiutando gli amministratori a trovare le blocklist più efficaci.

La sezione `Brute force attacks` fornisce informazioni sul numero di IP bloccati in base al numero di tentativi di accesso non riusciti. I dati provengono dai log che coprono le ultime 24 ore. Se i log non si estendono all'intero periodo di 24 ore, i dati potrebbero essere incompleti. I risultati vengono memorizzati nella cache per 5 minuti per migliorare le prestazioni. I grafici disponibili sono:

- `Blocked IP addresses`: questo contatore mostra il numero totale di indirizzi IP bloccati a causa di attività dannose per il giorno corrente. Aiuta a tracciare il volume dei tentativi di intrusione.
- `Blocked IP addresses by hour`: questo grafico traccia il numero di indirizzi IP bloccati nel tempo, aiutando a identificare i periodi di aumento dell'attività di attacco.
- `Most frequently blocked IP address`: questo grafico mostra gli indirizzi IP che sono stati bloccati più frequentemente. È utile per identificare le minacce persistenti o le fonti di attacco che dovrebbero essere investigate o inserite nella lista nera.

## Monitoraggio storico {#historical_monitoring-section}

A partire da NethSecurity 8.8, la pagina Monitoraggio include una nuova visualizzazione `Metrics` alimentata da VictoriaMetrics, Telegraf e vmalert. Telegraf legge le metriche e le scrive in VictoriaMetrics, mentre vmalert valuta le regole di avviso. VictoriaMetrics memorizza i dati in RAM per impostazione predefinita, ma passa automaticamente all'archiviazione persistente quando disponibile. Se l'archiviazione locale viene rimossa, il sistema passa di nuovo all'archiviazione in RAM.

Di conseguenza, le metriche di NethSecurity 8.8 rimangono persistenti anche senza un controller.

I periodi di conservazione dei dati sono i seguenti:

- **Archiviazione in RAM**: 7 giorni
- **Archiviazione persistente**: 1 anno

La pagina `Metrics` ha due schede: `Charts` e `Alerts`.

### Charts

La scheda `Charts` mostra i seguenti grafici:

- `CPU usage`
- `System load`
- `Disk I/O`
- `Disk usage (%)`
- `Total processes`
- `RAM usage`
- `Network interface traffic`: un grafico per ogni interfaccia configurata sull'unità
- `Network packets`
- `Connections (conntrack)`
- `Latency`: un grafico per ogni host ping configurato
- `Packet delivery`: un grafico per ogni host ping configurato, configurato nella sezione [Ping latency monitoring](#ping_latency-section)

L'intervallo di tempo del grafico può essere modificato tra 5 minuti, 30 minuti, 1 ora, 12 ore, 24 ore e 7 giorni.

#### Ping latency monitoring {#ping_latency-section}

Configura lo strumento di monitoraggio per valutare il tempo di andata e ritorno e la perdita di pacchetti trasmettendo messaggi ping agli host di rete. Questo strumento viene utilizzato per monitorare la qualità della connettività di rete. Hai la possibilità di includere uno o più host per il monitoraggio, ed è anche possibile aggiungere indirizzi IP all'interno di una VPN per valutare la qualità del tunnel.

Per monitorare un nuovo host o indirizzo IP, fai clic sul pulsante **Add host** e immetti le informazioni richieste, infine fai clic sul pulsante **Save** per confermare le modifiche.

Le modifiche vengono applicate immediatamente. Per rimuovere un host dall'elenco, fai clic sull'icona di eliminazione.

Puoi visualizzare i grafici di latenza e consegna dei pacchetti nella pagina `Metrics` dopo aver configurato gli host.

### Alerts {#alert-section}

Il sistema di avviso dà priorità solo agli avvisi che hanno il potenziale di interrompere o compromettere la funzionalità del firewall. Concentrandosi su indicatori critici, gli amministratori possono affrontare in modo efficiente i problemi che rappresentano una vera minaccia alla sicurezza e al funzionamento del firewall.

La scheda `Alerts` legge gli avvisi attuali in sospeso e in corso da vmalert. Questi avvisi vengono visualizzati localmente nella pagina `Metrics` e nel cassetto di notifica aperto dall'icona della campana nell'angolo in alto a destra.

Avvisi disponibili:

- `BackupEncryptionDisabled`: la crittografia di backup è disabilitata perché `/etc/backup.pass` è mancante o vuoto.
- `HighCpuUsage`: l'utilizzo della CPU è superiore al 70%.
- `CriticalCpuUsage`: l'utilizzo della CPU è superiore all'85%.
- `HighMemoryUsage`: l'utilizzo della memoria è superiore all'80%.
- `CriticalMemoryUsage`: l'utilizzo della memoria è superiore al 90%.
- `DiskSpaceWarning`: un file system montato è al di sopra dell'80% di utilizzo.
- `DiskSpaceCritical`: un file system montato è al di sopra del 90% di utilizzo.
- `HighSystemLoad`: il carico di sistema per CPU è superiore a 2.
- `WanDown`: un'interfaccia WAN monitorata è offline.
- `ServiceDown`: un servizio `procd` configurato non è in esecuzione.
- `StorageStatus`: l'archiviazione dati configurata non è montata o è in errore.

#### Remote alert notifications

Se il server ha una [Subscription](../system/subscription.md) valida, le notifiche di avviso vengono inviate senza problemi ai server remoti per il monitoraggio e la gestione centralizzati. Sia `my.nethesis.it` che `my.nethserver.com` fungono da hub centrali per la ricezione degli avvisi, consentendo agli amministratori di rimanere informati sullo stato del firewall e di rispondere tempestivamente a qualsiasi situazione critica.

Attualmente, sono inoltrati ai server di monitoraggio remoti solo i seguenti avvisi:

- Disk Space: l'avviso di spazio su disco si attiva quando lo spazio su disco disponibile nel sistema raggiunge un livello critico. Questa notifica proattiva aiuta a prevenire potenziali interruzioni affrontando i problemi di spazio su disco prima che influiscono sulle operazioni del firewall.
- MultiWAN Status (Up/Down): questo avviso notifica agli amministratori quando ci sono cambiamenti nello stato di MultiWAN, indicando se le connessioni sono attive o inattive. La consapevolezza tempestiva dei cambiamenti di stato di MultiWAN è fondamentale per mantenere una connettività Internet continua e affidabile.

Altri avvisi, come l'utilizzo della CPU e della memoria, non vengono inoltrati ai server di monitoraggio remoto in questo momento.

## Monitoraggio remoto {#remote_monitoring-section}

:::note

Sottoscrizione richiesta

Questa funzione è disponibile solo se il firewall e il controller hanno una sottoscrizione valida.

:::

Il monitoraggio storico è disponibile localmente sull'unità e in remoto sul controller quando il firewall è collegato ad esso. Tutti i dati vengono automaticamente inviati al controller e archiviati in Prometheus, consentendo la conservazione a lungo termine e il monitoraggio centralizzato.

La pagina `Controller` mostrerà un messaggio indicando che il monitoraggio remoto è disabilitato.

Per abilitarlo, segui questi passaggi:

1.  Disconnetti l'unità dal controller.
2.  Assicurati che il NethServer 8 dove il controller è installato abbia una sottoscrizione valida.
3.  Ricollega l'unità al controller.

Vedi [controller metrics](../system/controller.md#controller_metrics-section) per ulteriori informazioni.

:::note

Se l'unità era collegata al controller prima che la sottoscrizione venisse attivata, il monitoraggio remoto non verrà abilitato automaticamente. Per abilitarlo, devi disconnettere l'unità dal controller e ricolllegarla dopo che la sottoscrizione è attiva.

:::

### Legacy Netdata {#legacy_netdata-section}

:::warning

A partire da 8.8, Netdata è stato deprecato e rimosso dall'installazione predefinita. Se hai ancora dashboard Grafana personalizzate che si basano su metriche Netdata, è consigliabile passare al nuovo formato Telegraf.

:::

NethSecurity 8.7.2 e versioni precedenti utilizza [Netdata](https://www.netdata.cloud/) come strumento di monitoraggio in tempo reale. Netdata è uno strumento open-source di monitoraggio delle prestazioni e risoluzione dei problemi in tempo reale per sistemi e applicazioni. Fornisce informazioni complete sulla prestazione e lo stato di salute di sistemi e applicazioni attraverso visualizzazioni e metriche dettagliate. Netdata è progettato per essere leggero, veloce e facile da usare.

Netdata è abilitato per impostazione predefinita su NethSecurity 8.7.2 e versioni precedenti ed è accessibile dalla rete LAN. Per accedervi, vai alla pagina `Monitoring` e fai clic sul pulsante **Open report** dalla scheda `Real-time report`.

Le metriche di Netdata vengono salvate in RAM e verranno ripristinate ad ogni riavvio della macchina. Se il firewall è collegato al [controller remoto](../system/controller.md), le metriche verranno archiviate al controller stesso e conservate attraverso i riavvii.

### Install Netdata on NethSecurity 8.8 {#install-netdata-on-nethsecurity-8.8}

Se hai configurato dashboard Grafana personalizzate che si basano su metriche Netdata sul Controller, si interromperanno dopo l'aggiornamento a NethSecurity 8.8 poiché Netdata è stato rimosso.

Per ripristinare i tuoi dashboard, puoi reinstallare manualmente Netdata su NethSecurity 8.8 utilizzando il seguente comando:

    apk update
    apk add netdata

Tuttavia, è fortemente consigliato migrare invece i tuoi dashboard personalizzati al nuovo formato Telegraf. Ciò garantisce una migliore compatibilità a lungo termine e il supporto, poiché Netdata non è più mantenuto come parte di NethSecurity.
