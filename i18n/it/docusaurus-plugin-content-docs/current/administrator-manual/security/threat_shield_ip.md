---
title: "Threat shield IP"
sidebar_position: 2
---

# Threat shield IP {#threat_shield_ip-section}

NethSecurity è dotato di vari strumenti e integrazioni utili per contrastare minacce provenienti da internet. Uno di questi strumenti è Threat Shield IP, che blocca il traffico proveniente da indirizzi IP compromessi o ad essi destinato, nonché qualsiasi richiesta indirizzata a hostname che potrebbero essere dannosi.

Il servizio può caricare liste di blocco gestite dalla comunità oppure può avvalersi di liste di blocco di alta qualità frequentemente aggiornate e gestite da [Nethesis](https://www.nethesis.it) e [Yoroi](https://yoroi.company), un'azienda leader nel settore della Cybersecurity e membro della [Cyber Threat Alliance](https://www.cyberthreatalliance.org). Le liste nere di Yoroi garantiscono grande efficacia e alta affidabilità, minimizzando la possibilità di falsi positivi.

Si prega di notare che per accedere alle liste di blocco di Nethesis e Yoroi, la macchina deve disporre di un'entitlement aggiuntivo valido per questo servizio.

## Configurazione

Il servizio è disabilitato per impostazione predefinita; per abilitarlo, navigare alla pagina `Threat shield IP` nella sezione `Security`. Accedere alla scheda `Settings` e attivare l'interruttore `Status`.

Quando il servizio è abilitato, la scheda `Blocklist feeds` visualizzerà tutte le liste di blocco disponibili. È possibile abilitare o disabilitare ogni lista di blocco utilizzando l'interruttore sul lato destro dell'elenco. Le liste di blocco abilitate verranno aggiornate automaticamente a intervalli regolari. NethSecurity 8 consente l'uso di liste di blocco Community ed Enterprise.

### Liste di blocco Community

Le liste di blocco Community provengono da contributori della comunità e coprono varie aree: blocco degli annunci, blocco del malware, blocco dello spam, blocco dei tracker, e così via. NethSecurity le rende disponibili come sono.

Le liste Community non forniscono una metrica standardizzata di "Affidabilità", pertanto l'interfaccia utente mostra la loro affidabilità come "Sconosciuta". Come euristica pratica, quando il nome della lista contiene un indicatore di severità o affidabilità (ad esempio "lvl 1", "level 1"), generalmente denota il tasso di falsi positivi più basso e la massima affidabilità; al contrario, i livelli indicati più elevati (ad esempio "lvl 2", "lvl 3", "lvl 4") in genere implicano una minore affidabilità e un rischio più elevato di voci aggressive o scorrette. Tuttavia, le convenzioni di denominazione variano e non tutti i provider della comunità includono tali indicatori, quindi è sempre consigliabile esaminare il contenuto e lo scopo di una lista della comunità prima di abilitarla in produzione. Il tipo di licenza d'uso può variare a seconda del provider, quindi se l'uso non è personale, potrebbe essere necessario contattare il provider.

**Manutenzione delle liste Community**

Ogni lista di blocco è gestita dal suo specifico provider. NethSecurity include già gli URL per il download dei feed, che sono validi al momento del rilascio. Tuttavia, poiché questi URL sono codificati, se il provider li modifica, alcune liste di blocco potrebbero non essere più scaricabili.

### Liste di blocco Enterprise

:::note

Sottoscrizione richiesta

Questa funzionalità è disponibile solo se il firewall ha una [sottoscrizione Community o Enterprise](../system/subscription.md) valida.

:::

Le liste di blocco Enterprise sono specificamente focalizzate sulla sicurezza e offrono diversi vantaggi rispetto alle liste di blocco gestite dalla comunità:

1.  **Qualità e accuratezza**: Le liste di blocco Enterprise, come quelle fornite da Nethesis e Yoroi, sono curate e gestite da aziende di cybersecurity rinomate. Queste aziende hanno team dedicati che monitorano continuamente e aggiornano le liste di blocco per garantire che siano accurate ed efficaci nel bloccare il traffico dannoso. Ciò risulta in un livello di qualità e accuratezza superiore rispetto alle liste di blocco gestite dalla comunità, che potrebbero non ricevere lo stesso livello di attenzione e aggiornamenti.
2.  **Tempestività**: Le liste di blocco Enterprise vengono frequentemente aggiornate per includere le minacce più recenti e gli indirizzi IP dannosi. Aziende di cybersecurity come Nethesis e Yoroi monitorano attivamente le minacce emergenti e le aggiungono prontamente alle loro liste di blocco. Ciò garantisce che il vostro sistema sia protetto contro le minacce più recenti e in evoluzione.
3.  **Riduzione dei falsi positivi**: I falsi positivi si verificano quando il traffico legittimo viene bloccato per errore. Le liste di blocco Enterprise sono progettate per minimizzare i falsi positivi mediante una cura attenta e una verifica degli indirizzi IP e degli hostname elencati. Le aziende dietro le liste di blocco Enterprise hanno processi robusti in atto per garantire che solo entità dannose siano incluse nelle liste di blocco. Ciò riduce le possibilità che il traffico legittimo venga bloccato, minimizzando le interruzioni della rete o dei servizi.
4.  **Supporto Enterprise**: Le liste di blocco Enterprise spesso includono supporto e servizi aggiuntivi personalizzati per ambienti aziendali. Ciò include l'accesso al supporto tecnico, alla documentazione e all'assistenza per l'integrazione. Se sorgono problemi o domande durante l'utilizzo delle liste di blocco Enterprise, è possibile affidarsi al supporto fornito dalle aziende di cybersecurity per affrontarli efficacemente.

### Affidabilità

Le liste di blocco Enterprise includono un punteggio di "Affidabilità" che è mostrato nell'interfaccia utente. Il punteggio è espresso come un valore da 1 a 10 e rappresenta la valutazione del provider sulla qualità della lista: valori più alti indicano una maggiore affidabilità e una minore probabilità di falsi positivi. Questa metrica di "Affidabilità" è disponibile solo per le liste Enterprise; le liste Community sono presentate "come sono" e mostrano "Sconosciuta" per l'affidabilità.

Le liste di blocco di Yoroi e Nethesis sono liste di blocco Enterprise. Queste liste saranno elencate solo se la macchina ha una [sottoscrizione Enterprise o Community](../system/subscription.md) valida e un'entitlement valida per il servizio Threat Shield IP.

### Logging

La funzione Threat Shield IP include capacità di logging avanzate per monitorare e tracciare potenziali minacce. La sezione di logging consente di configurare quali tipi di pacchetti bloccati vengono registrati:

1.  Registra pacchetti bloccati nella catena pre-routing: quando abilitata, questa opzione registra i pacchetti bloccati nella catena pre-routing, che elabora i pacchetti prima che entrino nella tabella di routing.
2.  Registra pacchetti bloccati nella catena input: questa opzione, quando attivata, registra i pacchetti bloccati nella catena input, che gestisce i pacchetti destinati al firewall stesso. Si prega di notare che questa opzione può generare un gran numero di log se il firewall è sotto un traffico intenso.
3.  Registra pacchetti bloccati nella catena forward: L'abilitazione di questa opzione registra i pacchetti bloccati nella catena forward, che elabora i pacchetti che vengono instradati attraverso il firewall.
4.  Registra pacchetti bloccati inoltrati dalla LAN: Questa opzione registra i pacchetti che vengono bloccati quando inoltrati dalla Local Area Network (LAN).

Queste opzioni di logging forniscono un controllo granulare su quali pacchetti bloccati vengono registrati, consentendo di esporre metriche all'interno delle sezioni di [monitoraggio in tempo reale](../monitoring/monitoring.md#real_time_monitoring-section) e [monitoraggio storico](../monitoring/monitoring.md#historical_monitoring-section).

### Whitelist locale {#local_allowlist-section}

A volte può essere necessario consentire l'accesso a determinati indirizzi IP; per fare questo è possibile utilizzare la scheda `Local allowlist`. Utilizzare il pulsante **Add address** per aggiungere un nuovo indirizzo all'elenco. L'indirizzo può essere un indirizzo IPv4/IPv6 valido con notazione CIDR opzionale, un indirizzo MAC o un hostname completamente qualificato (FQDN).

Ad esempio, l'indirizzo può essere:

- Indirizzo IPv4: 192.168.0.1
- Indirizzo IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
- Indirizzo IPv4 con notazione CIDR: 192.168.0.0/24
- Indirizzo MAC: 00:0a:95:9d:68:16
- Hostname completamente qualificato: example.com

Un commento può essere associato a ogni indirizzo per facilitare la gestione.

È possibile aggiungere un commento per fornire informazioni aggiuntive sull'indirizzo, come il suo scopo o il proprietario. Ciò può aiutare a organizzare e gestire efficacemente la whitelist.

### Lista di blocco locale {#local_blocklist_ip-section}

Threat Shield IP include una funzionalità di lista di blocco locale, che consente di specificare manualmente gli indirizzi che devono sempre essere bloccati. Ciò fornisce un ulteriore livello di personalizzazione alla vostra configurazione di sicurezza.

Per accedere e personalizzare la lista di blocco, navigare alla scheda `Local blocklist` nell'interfaccia Threat Shield IP. Utilizzare il pulsante **Add address** per includere nuove voci. Ogni voce è composta da un indirizzo e una descrizione. La sintassi valida per l'indirizzo è la stessa della [whitelist locale](#local_allowlist-section).

Quando si aggiungono indirizzi alla lista di blocco locale, assicurarsi di inserirli correttamente per evitare di bloccare accidentalmente il traffico legittimo. È anche una buona pratica includere un commento descrittivo per ogni voce per aiutare con la gestione futura e il controllo della vostra lista di blocco.

## Blocca attacchi brute force {#brute_force-section}

Quando Threat Shield IP è abilitato, il sistema inizia automaticamente a verificare i tentativi di attacco brute force sui servizi del firewall. Per impostazione predefinita, i servizi monitorati includono l'accesso SSH e il login all'interfaccia utente di NethSecurity. Il sistema rileva i tentativi di login e blocca automaticamente gli indirizzi IP che non hanno inserito le credenziali corrette.

Per abilitare o disabilitare la protezione brute force, navigare alla sezione `Block brute force attacks` nell'interfaccia Threat Shield IP, nella scheda `Settings` e utilizzare l'interruttore per attivare o disattivare la funzione.

La funzione può essere personalizzata regolando le seguenti impostazioni:

- `Ban after N failed accesses`: questa impostazione determina il numero di tentativi di login non riusciti consentiti prima che un indirizzo IP venga bannato. Il valore predefinito è in genere 3, ma può essere regolato secondo necessità. Un valore inferiore aumenta la sicurezza ma può anche aumentare il rischio di falsi positivi, come il blocco di utenti legittimi che digitate male le loro credenziali.

- `Patterns to detect attacks`: questo campo consente di specificare i pattern che il sistema utilizza per identificare potenziali attacchi brute force. I pattern comuni includono:

  - *Exit before auth from*: rileva i tentativi di autenticazione non riusciti al servizio SSH
  - *authentication failed for user*: identifica i tentativi di autenticazione non riusciti all'interfaccia web di NethSecurity
  - *TLS Auth Error*, *TLS handshake failed*, *AUTH_FAILED*: rileva i tentativi di autenticazione non riusciti al servizio OpenVPN

  È possibile aggiungere pattern aggiuntivi utilizzando il pulsante **Add pattern** per personalizzare il meccanismo di rilevamento. Ogni pattern può essere un'espressione regolare valida di *grep*.

- `Ban time`: questa impostazione determina la durata per la quale un indirizzo IP rimane bannato dopo aver superato il numero consentito di tentativi non riusciti. L'impostazione predefinita è spesso fissata a 30 minuti, ma può essere regolata in base ai vostri requisiti di sicurezza.

È possibile eseguire ulteriori azioni utilizzando la riga di comando; questi sono i comandi supportati:

- Visualizza tutti gli indirizzi IP attualmente nella lista di blocco: `/etc/init.d/banip survey blocklistv4`
- Cerca un IP specifico nella lista di blocco: `/etc/init.d/banip search IP_ADDRESS`
- Sbanna un indirizzo IP: `nft delete element inet banIP blocklistv4 { IP_ADDRESS }`

Tenete presente che è necessario specificare la lista di blocco corretta nei comandi quando richiesto (`blocklistv4` per IPv4, `blocklistv6` per IPv6).

### Blocca DoS

Threat Shield IP include anche protezione contro vari tipi di attacchi Denial of Service (DoS). La protezione DoS limita il traffico eccessivo di protocolli specifici, bloccando quel tipo di traffico fino a quando la situazione si normalizza. Monitora tutto il traffico WAN in entrata per rilevare e bloccare gli attacchi DoS basati su WAN.

- `Block ICMP DoS`: quando abilitata, questa opzione protegge contro gli attacchi DoS utilizzando Internet Control Message Protocol (ICMP). Il limite è impostato a 100 pacchetti al secondo.
- `Block TCP SYN DoS`: questa opzione, quando attivata, protegge contro gli attacchi DoS basati su TCP limitando il numero di nuove connessioni al secondo. Un pacchetto potrebbe essere considerato dannoso se non fa parte di una connessione stabilita o se fa parte di una connessione che è stata chiusa. Il limite è impostato a 10 connessioni al secondo.
- `Block UDP DoS`: L'abilitazione di questa opzione protegge contro gli attacchi DoS basati su User Datagram Protocol (UDP). Il limite è impostato a 100 pacchetti al secondo.
