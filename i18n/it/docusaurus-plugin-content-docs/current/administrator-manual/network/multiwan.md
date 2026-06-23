---
title: "MultiWAN"
sidebar_position: 4
---

# MultiWAN

La configurazione MultiWAN (Wide Area Network) è un'impostazione in cui il firewall utilizza più connessioni Internet da diversi provider di servizi Internet (ISP) contemporaneamente. Questa configurazione mira a migliorare l'affidabilità della rete, aumentare la larghezza di banda e migliorare la velocità di Internet distribuendo il traffico di rete su più collegamenti. Può fornire protezione di failover, assicurando che se una connessione fallisce, il traffico di rete viene automaticamente reindirizzato alla connessione funzionante, riducendo al minimo i tempi di inattività e garantendo un accesso continuo a Internet. Le configurazioni MultiWAN sono spesso utilizzate in aziende e organizzazioni che richiedono una connessione Internet altamente disponibile e stabile per le loro operazioni.

La configurazione MultiWAN richiede almeno due interfacce di rete nella zona WAN del sistema. Questo è il requisito fondamentale per implementare una connessione MultiWAN.

La prima volta che accedi alla pagina di configurazione, è obbligatorio creare una policy predefinita. Questa policy è essenziale e non può essere eliminata. La policy predefinita definisce il comportamento di base del sistema MultiWAN. È necessario specificarne il comportamento. Sono disponibili due opzioni principali:

- `Equilibrata`: In questa modalità, le connessioni WAN vengono utilizzate contemporaneamente e il traffico è bilanciato in base al peso assegnato a ogni WAN. Il peso della WAN può variare da 1 a 1000.
- `Backup`: In modalità backup, la connessione WAN secondaria entra in gioco solo se la connessione primaria fallisce. Questo garantisce una connettività di backup se la WAN primaria fallisce.

È disponibile anche una `Modalità personalizzata` che consente una configurazione più dettagliata, particolarmente utile quando si gestiscono tre o più connessioni WAN. Questa modalità offre maggiore flessibilità nella gestione del traffico tra diverse connessioni WAN.

Nella modalità personalizzata della configurazione Multi-WAN, si applicano i seguenti concetti:

- Livelli di priorità indipendenti: ogni livello di priorità opera indipendentemente dagli altri. Le interfacce WAN all'interno di un particolare livello di priorità non influenzano o dipendono dalle interfacce di altri livelli.
- Più interfacce WAN all'interno di un livello di priorità: ogni livello di priorità può contenere due o più interfacce WAN. Queste interfacce sono raggruppate insieme per configurazioni specifiche.
- I pesi determinano la distribuzione del traffico: i pesi assegnati alle interfacce WAN all'interno di un livello di priorità determinano come il traffico viene distribuito tra queste interfacce. Pesi più elevati indicano una proporzione più alta di allocazione del traffico.
- La priorità diminuisce con i nuovi livelli: l'aggiunta di un nuovo livello di priorità comporta che le interfacce all'interno di questo livello abbiano priorità inferiore. Vengono utilizzate solo se tutte le interfacce nel livello precedente falliscono.

Considera uno scenario in cui le prime due interfacce WAN sono configurate in modalità equilibrata e l'ultima interfaccia funge da backup se entrambe le prime due interfacce falliscono:

1.  seleziona le prime due interfacce WAN e impostale in modalità equilibrata assegnando pesi a entrambe in base alle prestazioni della connessione Internet
2.  aggiungi un nuovo livello di priorità facendo clic sul pulsante **Aggiungi livello di priorità**
3.  seleziona la terza interfaccia WAN e assegna un peso. Tuttavia, in questo scenario, il peso non influenza la distribuzione del traffico poiché è l'unica interfaccia a questo livello. Funge da backup, entrando in gioco solo se entrambe le interfacce nel livello precedente falliscono.

## Regole di instradamento

Gli utenti possono creare regole di traffico in uscita in base a criteri specifici come IP di origine, IP di destinazione, porta(e) di origine, porta(e) di destinazione e tipi di protocollo IP. Questa funzione di instradamento basato su policy consente agli utenti di personalizzare quali connessioni in uscita utilizzano specifiche interfacce WAN, consentendo un'impostazione di rete finemente sintonizzata.

Ecco come puoi creare una regola personalizzata:

1.  Crea una nuova policy: per iniziare a personalizzare l'instradamento del traffico, inizia creando una nuova policy. Fai clic sul pulsante **Crea policy** per avviare il processo.
2.  Crea una nuova regola: quindi fai clic sul pulsante **Crea regola**. Questo passaggio ti consente di definire condizioni specifiche in cui il traffico verrà instradato diversamente dalla policy predefinita.
3.  Dai un nome significativo alla regola: assegna un nome descrittivo e significativo alla regola. Questo nome dovrebbe riflettere lo scopo o le condizioni della regola di instradamento del traffico per una facile identificazione.
4.  Specifica il tipo di traffico: definisci i criteri per il traffico che desideri personalizzare. Questo può includere l'indirizzo IP di origine, l'indirizzo IP di destinazione, protocolli specifici, porte o qualsiasi combinazione di questi fattori. Specificando questi parametri, restringi l'ambito della regola a un tipo specifico di traffico. Con i campi `Indirizzo di origine` e `Indirizzo di destinazione`, puoi scegliere tra le seguenti opzioni:
    - Inserisci un indirizzo o un intervallo: specifica un singolo indirizzo IP o un CIDR. È supportato solo IPv4.
    - Qualsiasi indirizzo: seleziona questa opzione per corrispondere a qualsiasi indirizzo.
    - Seleziona un oggetto firewall: scegli dall'elenco degli oggetti firewall predefiniti.
5.  Seleziona la policy creata per questo tipo di traffico: scegli la policy personalizzata che hai creato nel primo passaggio come preferenza di instradamento per questo tipo di traffico specifico. Associando la regola a una particolare policy, stai istruendo il sistema a instradare il traffico definito secondo le impostazioni specificate all'interno di quella policy.

- Opzione `Sticky`: L'opzione sticky di una regola assicura che il traffico originario dallo stesso IP di origine esce sempre attraverso lo stesso WAN per una durata di 10 minuti. Questo può prevenire problemi durante la connessione a siti web di banche, compagnie assicurative, ecc. Questa opzione è tipicamente utilizzata per il traffico HTTPS (443/TCP).

Le seguenti sono le opzioni disponibili per definire le porte del traffico:

- `<port>`: Porta singola
- `<port>,<port>`: Elenco di porte
- `<port>-<endport>`: Intervallo da \<port\> a \<endport\>

## Impostazioni generali

NethSecurity monitora ogni connessione WAN utilizzando test ICMP ripetuti.

La pagina `Impostazioni generali` consente agli utenti di specificare i seguenti parametri:

- Elenco di host da monitorare: gli utenti possono definire un elenco di host (computer, server o dispositivi) che il sistema monitorerà per lo stato della connettività. Questi host vengono controllati per assicurarsi che siano raggiungibili via rete.
- Numero di pacchetti ICMP (ping) da inviare: gli utenti possono impostare il numero di pacchetti ICMP (Internet Control Message Protocol) da inviare durante ogni test di monitoraggio. Impostando il numero di pacchetti, gli utenti possono controllare l'intensità del monitoraggio.
- Determinazione dell'irraggiungibilità dopo quanti test falliti: gli utenti possono configurare il sistema per determinare quando una connessione WAN deve essere considerata irraggiungibile. Questo viene fatto specificando una soglia - dopo quanti test falliti consecutivi la connessione WAN è considerata irraggiungibile.

## Ripristina configurazione

:::warning

Questo ripristinerà effettivamente la configurazione MultiWAN, con una perdita di connessione Internet se nessuna WAN è configurata.

:::

Se il tuo firewall era precedentemente configurato con due o più interfacce WAN e dopo la riconfigurazione c'è solo un'interfaccia WAN, è consigliabile ripristinare la configurazione MultiWAN. Questo assicurerà che il tuo firewall sia configurato correttamente e funzioni come previsto.

    /usr/libexec/rpcd/ns.mwan call clear_config
    uci commit mwan3
    reload_config
