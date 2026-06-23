---
title: "Registri"
sidebar_position: 7
---

# Registri {#logs-section}

I registri vengono inizialmente scritti in una directory temporanea in memoria per evitare potenziali errori nel file system root in caso di guasto.

1.  **Archiviazione locale**: I registri possono essere scritti direttamente nell'archiviazione. Questo può essere configurato dall'interfaccia utente, consultare la sezione [Archiviazione](../system/storage.md).
2.  **Controller remoto**: I registri possono essere inoltrati automaticamente a un [controller remoto](../system/controller.md#controller_logs-section).
3.  **Forwarder Syslog personalizzato**: I registri possono essere inviati a un server syslog remoto.
4.  **Cloud Log Manager**: I registri possono essere inoltrati al servizio Nethesis Cloud Log Manager (CLM).

I paragrafi successivi spiegheranno come configurare queste ultime opzioni.

## Inoltro a un server remoto

È sufficiente configurare il database UCI con le opzioni desiderate, quindi eseguire il commit delle modifiche e infine riavviare il servizio. I registri temporanei continueranno a essere visibili in `/var/log/messages` e verranno anche inviati al server remoto.

La maggior parte dei server syslog è configurata per stare in ascolto sulla porta UDP 514 per impostazione predefinita.

Configurazione di esempio per l'invio di registri al server syslog con IP 192.168.1.88 sulla porta UDP 514. La configurazione è denominata `clm` (gestore registri personalizzato):

    uci set rsyslog.clm=forwarder
    uci set rsyslog.clm.source=*.* 
    uci set rsyslog.clm.protocol=udp
    uci set rsyslog.clm.port=514
    uci set rsyslog.clm.target=192.168.1.88

Una volta configurato, è sufficiente eseguire il commit delle modifiche con il comando: :

    uci commit rsyslog

E infine, riavviare il servizio: :

    /etc/init.d/rsyslog restart

Per impostazione predefinita, il forwarder utilizza TraditionalFileFormat (RFC 3164) per i registri. È anche possibile configurare RFC 5424 utilizzando la stessa sintassi: :

    uci set rsyslog.clm.rfc=5424

È possibile configurare più forwarder ripetendo l'operazione utilizzando un nome di configurazione diverso come `clm2`.

## Inoltro a Nethesis Cloud Log Manager

:::note

Diritto di servizio richiesto

È necessario acquistare un abbonamento per il servizio CLM da Nethesis e ottenere l'identificatore del tenant. Il servizio è attualmente riservato ai clienti Enterprise. Per ulteriori informazioni, contattare il team di vendita di Nethesis.

:::

Il pacchetto `ns-clm` inoltra i messaggi syslog al servizio Nethesis Cloud Log Manager (CLM). Fornisce il daemon `ns-clm-forwarder`, che legge `/var/log/messages` e traccia la sua posizione di lettura in `/var/run/ns-clm/last_offset`. Le nuove righe syslog vengono analizzate, raggruppate e inviate in formato JSON tramite HTTP POST all'endpoint CLM. Il daemon esegue il polling delle nuove righe ogni 10 secondi, rileva automaticamente la rotazione dei registri e persiste l'offset all'arresto in modo da poter riprendere dopo un riavvio.

Il pacchetto non è incluso per impostazione predefinita su NethSecurity 8.7.2 o versioni precedenti, ma è disponibile nel repository dei pacchetti e può essere installato manualmente.

Se stai eseguendo NethSecurity 8.8, usa:

    apk update
    apk add ns-clm

Se stai eseguendo NethSecurity 8.7.2 o versioni precedenti, usa:

    opkg update
    opkg install ns-clm

La configurazione UCI è memorizzata in `/etc/config/ns-clm`:

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 30%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th>Opzione</th>
<th>Predefinito</th>
<th>Descrizione</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>enabled</code></td>
<td><code>0</code></td>
<td>Abilita (<code>1</code>) o disabilita (<code>0</code>) il forwarder</td>
</tr>
<tr>
<td><p><code>uuid</code></p></td>
<td><p>(vuoto)</p></td>
<td><p>Identificatore univoco del dispositivo, generato con <code>uuidgen</code> e preceduto da "L" per garantire che inizi con una lettera.</p>
<p>Questo è richiesto dal servizio CLM per identificare l'origine dei registri.</p>
<p>Esempio: <code>L3d50ca11-4415-4e46-9ee9-b1da0f62c337</code></p></td>
</tr>
<tr>
<td><code>address</code></td>
<td><code>https://nar.nethesis.it</code></td>
<td>Indirizzo del server CLM</td>
</tr>
<tr>
<td><code>tenant</code></td>
<td>(vuoto)</td>
<td>Identificatore del tenant CLM, disponibile all'interno del portale CLM, sotto <code>Users and Companies</code> -&gt; <code>Companies</code></td>
</tr>
<tr>
<td><code>debug</code></td>
<td><code>0</code></td>
<td>Abilita output di debug su stderr (<code>1</code>)</td>
</tr>
</tbody>
</table>

Per abilitare il forwarder e impostare l'identificatore del tenant, esegui: :

    uci set ns-clm.config.uuid="L$(uuidgen)"
    uci set ns-clm.config.enabled=1
    uci set ns-clm.config.tenant=<tenant_id>
    uci commit ns-clm
    reload_config

Puoi trovare l'identificatore del tenant nel portale CLM, sotto `Users and Companies` -\> `Companies`.

Per abilitare anche il servizio all'avvio: :

    /etc/init.d/ns-clm enable && /etc/init.d/ns-clm start

Per interrompere e disabilitare il forwarder: :

    /etc/init.d/ns-clm stop && /etc/init.d/ns-clm disable

## Rotazione dei registri {#log-rotation-section}

I registri vengono ruotati per gestire lo spazio su disco e garantire che i file di registro non crescano indefinitamente.

### Rotazione dei registri in memoria

Il file di registro `/var/log/messages` è memorizzato nella RAM e viene ruotato in base alle dimensioni. Una volta raggiunto un limite di dimensioni predefinito, il registro viene ruotato e compresso per conservare spazio. Il registro ruotato viene salvato come `/var/log/messages.1.gz` in formato gzip. Il sistema conserva solo due versioni del registro: il file di registro attivo e l'ultimo file ruotato e compresso. Dalla versione 1.4.0, per impostazione predefinita, la soglia di rotazione dei registri è impostata al 10% del file system tmpfs montato in `/tmp`.

Lo script `ns-log-size` gestisce le dimensioni di rotazione dei registri per il servizio Rsyslog. Consente di **ottenere** e **impostare** le dimensioni di rotazione dei registri definite in byte per il file di registro situato in `/var/log/messages`.

- **Ottenere la dimensione corrente**: Recuperare la dimensione di rotazione dei registri corrente in byte.
- **Impostare una nuova dimensione**: Modificare la dimensione di rotazione dei registri su un valore specificato, assicurandosi che la nuova dimensione sia un numero intero positivo e non inferiore a 52428800 byte (50 MB).
- **Sicurezza della configurazione**: Se la dimensione specificata è inferiore alla soglia minima, lo script avverte l'utente e non apporta alcuna modifica alla configurazione.

#### Utilizzo

Per utilizzare lo script, eseguilo con la seguente sintassi:

    ns-log-size {get|set <size>}

- **get**: Restituisce la dimensione di rotazione dei registri corrente in byte.
- **set \<size\>**: Imposta la dimensione di rotazione dei registri sul valore specificato (in byte).

##### Esempio

Per ottenere la dimensione di rotazione dei registri corrente:

    ns-log-size get

Per impostare una nuova dimensione di rotazione dei registri a 104857600 byte (100 MB):

    ns-log-size set 104857600

Il servizio rsyslog viene riavviato automaticamente dopo l'impostazione della dimensione.

Tutte le modifiche alla dimensione di rotazione dei registri vengono scritte direttamente nel file di configurazione Rsyslog `/etc/rsyslog.conf`.

### Rotazione dei registri di archiviazione {#storage-log-rotation-section}

Quando si utilizza l'archiviazione persistente, la rotazione dei registri viene gestita dall'utilità `logrotate`, che è configurata per ruotare i registri settimanalmente e mantenere un massimo di 52 settimane (1 anno) di registri. Dopo la rotazione, i registri vengono compressi utilizzando gzip e archiviati nella stessa directory con una convenzione di denominazione che include la data di rotazione (ad es. `/mnt/data/log/messages-20260315.gz`).

Il file di configurazione per logrotate si trova in `/etc/logrotate.d/data.conf` e può essere modificato per cambiare la frequenza di rotazione e il periodo di conservazione secondo le necessità. Il file di configurazione viene aggiunto automaticamente al backup e preservato durante gli aggiornamenti, quindi le impostazioni personalizzate persistono.
