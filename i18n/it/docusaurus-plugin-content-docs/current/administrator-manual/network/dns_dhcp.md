---
title: "DNS e DHCP"
sidebar_position: 2
---

# DNS e DHCP {#dns_dhcp-section}

NethSecurity può fornire servizi DNS e DHCP a ogni rete locale. Questa sezione è divisa in 5 schede:

- DHCP e associazione MAC
- Lease statiche
- Lease dinamiche
- DNS
- Record DNS
- Scansione rete

## DHCP e associazione MAC {#dhcp_and_mac_binding-section}

Questa sezione ti consente di abilitare e gestire un server DHCP per ogni rete locale configurata nel tuo NethSecurity. Ogni interfaccia locale è dotata di una scheda in cui puoi abilitare il servizio facendo clic sul pulsante **Modifica**.

Campi disponibili:

- `Associazione MAC`:
  - `Stato`: abilita/disabilita la funzionalità di associazione MAC-IP per questa interfaccia
  - `Tipo`: è possibile scegliere tra due tipi di associazione MAC-IP:
    - `Associazione soft`: consente agli host senza prenotazione di accedere, blocca IP/MAC non corrispondenti

      **Esempio**: Una rete aziendale in cui i dipendenti portano frequentemente i propri dispositivi (BYOD). In questo caso l'associazione soft consente ai dispositivi senza prenotazione di accedere alla rete, ma garantisce che qualsiasi dispositivo con un indirizzo IP/MAC non corrispondente venga bloccato. Ciò fornisce flessibilità ai dipendenti mantenendo un livello di sicurezza.

    - `Associazione rigorosa`: Solo gli host con una prenotazione sono consentiti, gli altri sono bloccati

      **Esempio**: Una rete aziendale con politiche di sicurezza rigorose. In questo caso l'associazione hard garantisce che solo i dispositivi con una prenotazione preconfigurata possano accedere alla rete. Ciò impedisce che i dipendenti rubino un IP con autorizzazioni superiori.
- `DHCP`:
  - `Abilita DHCP` : abilita/disabilita il servizio
  - `Inizio intervallo IP` : primo indirizzo IP dell'intervallo DHCP
  - `Fine intervallo IP` : ultimo indirizzo IP dell'intervallo DHCP
  - `Tempo lease` : tempo di lease (predefinito 1 ora)

**Impostazioni avanzate DHCP**

`Forza l'avvio del server DHCP`

All'avvio, il server DHCP controlla se ci sono altri server DHCP sulla rete. Con questa opzione disabilitata, il server DHCP non verrà attivato se ne viene rilevato un altro sulla rete. Se l'opzione di forzatura è abilitata, il server DHCP verrà avviato anche se ci sono altri server DHCP nella rete.

`Opzione DHCP`

È possibile dichiarare opzioni DHCP molto specifiche, cercando il campo da configurare (ad esempio DNS passato ai client, indirizzo IP tftp e così via) e quindi specificando il valore. Il valore può essere anche un elenco di valori separati da una virgola.

Esempio per sovrascrivere il DNS passato ai client con 2 server:

- opzione selezionata: `dns-server`
- valore: `1.1.1.1,8.8.8.8`

Vedi anche [Opzioni personalizzate non standard](#dns_dhcp_custom-section) per ulteriori informazioni sulle opzioni non standard.

## Lease statiche {#static_leases-section}

Le lease statiche assegnano indirizzi IP stabili e nomi host simbolici ai client DHCP. L'host viene identificato dal suo indirizzo MAC, assegnato a un indirizzo IP fisso e fornito di un nome host simbolico per un facile riconoscimento.

Fai clic sul pulsante **Aggiungi prenotazione** per aggiungere la prenotazione di un nuovo dispositivo.

Campi disponibili:

- `Nome host` : Nome host associato all'indirizzo IP
- `Indirizzo IP` : Indirizzo IP da assegnare all'indirizzo MAC specificato. L'indirizzo IP deve essere all'interno dell'intervallo DHCP
- `Indirizzo MAC` : Indirizzo MAC del dispositivo per il quale desideri effettuare la prenotazione
- `Nome prenotazione` : Opzionale, campo liberamente configurabile

## Lease dinamiche {#dynamic_leases-section}

Le lease dinamiche rappresentano gli indirizzi IP attualmente in uso e allocati ai dispositivi sulla rete. Questa scheda mostra tutte le lease attualmente attive.

:::note

Quando [Storage](../system/storage.md) è configurato, dnsmasq memorizza il file di lease in `/mnt/data/dnsmasq/dhcp.leases`, quindi le lease dinamiche sopravvivono ai riavvii. Altrimenti continua a utilizzare `/tmp/dhcp.leases`.

:::

### Configurazione predefinita

Per impostazione predefinita, il server DHCP ha un limite di 1000 concurrent lease per prevenire attacchi DoS. Imposta l'opzione dnsmasq `dhcpleasemax` per modificare il limite.

Esegui questi comandi: :

``` bash
uci set dhcp.@dnsmasq[0].dhcpleasemax='2500'
uci commit dhcp
reload_config
```

### Opzioni personalizzate non standard {#dns_dhcp_custom-section}

Oltre alle opzioni DHCP standard, NethSecurity ti consente di configurare opzioni personalizzate non standard, come l'opzione 82 (DHCP Relay Agent Information). Queste opzioni possono essere utili per configurazioni avanzate o requisiti di rete specifici.

Per impostare un'opzione personalizzata dalla riga di comando, utilizza i seguenti comandi:

``` bash
uci add_list dhcp.lan.dhcp_option='82,myvalue'
uci commit dhcp
reload_config
```

Le opzioni personalizzate configurate dalla riga di comando vengono conservate anche quando vengono apportate modifiche tramite l'interfaccia utente. Le opzioni personalizzate possono essere rimosse in modo sicuro dall'interfaccia utente.

Tuttavia, gli utenti dovrebbero evitare di modificare direttamente queste opzioni personalizzate dall'interfaccia utente per evitare comportamenti imprevisti.

## DNS {#dns-section}

Il sistema utilizza [Dnsmasq](https://thekelleys.org.uk/dnsmasq/doc.html) a come server DNS cache downstream. Dnsmasq funziona come nameserver cache locale, che per impostazione predefinita inoltra le query DNS ai server DNS upstream forniti dal server DHCP delle interfacce WAN. Tuttavia, questo comportamento può essere personalizzato utilizzando le seguenti opzioni di configurazione:

- `Server di inoltro DNS`: Fai clic sul pulsante **Aggiungi server DNS** per specificare il DNS upstream desiderato, puoi aggiungere più server, ognuno è gestito individualmente.
- `Dominio DNS` : Inserisci il dominio DNS locale, assicurandoti che le query per questo dominio vengano sempre risolte localmente.
- `Registra query DNS`: abilitalo se desideri che tutte le query DNS vengano registrate dal sistema.

### Server di inoltro {#forwarding_servers-section}

Devi configurare i forwarder solo se le tue interfacce WAN sono impostate con indirizzi IP statici. Se le tue interfacce WAN sono configurate tramite DHCP, solitamente fornite dal tuo ISP, il sistema utilizzerà automaticamente i server DNS forniti dalle interfacce WAN. I server DNS upstream configurati automaticamente possono essere trovati nel file `/tmp/resolv.conf.d/resolv.conf.auto`.

Puoi configurare quanto segue:

- **Specifica un singolo server DNS upstream:** immetti l'indirizzo IP del server DNS desiderato nel campo designato.
- **Configura server DNS specifici del dominio:** ciò ti consente di instradare le query per domini specifici a server diversi.

Per la configurazione DNS incentrata sulla privacy utilizzando connessioni crittografate, vedi [DNS over HTTPS con filtro](../advanced-cli/dns_over_http.md) per la configurazione DNS over HTTPS (DoH).

#### Server DNS specifici del dominio

Per utilizzare un server DNS personalizzato per un dominio specifico, utilizza la seguente sintassi:

`/DOMAIN/IP_ADDRESS#PORT`

dove:

- IP_ADDRESS: specifica l'indirizzo IP del server desiderato
- PORT: aggiungi la porta desiderata (dopo l'indirizzo IP utilizzando il carattere `\#`).

Il valore `PORT` è opzionale, quindi di solito la configurazione appare semplicemente come:

`/DOMAIN/IP_ADDRESS`

Queste sono le opzioni principali supportate:

- Dominio vuoto (`//`): corrisponde ai nomi non qualificati (senza punti).
- Dominio specifico (`/google.com/`): corrisponde al dominio esatto e a tutti i suoi sottodomini (ad esempio, google.com, www.google.com, drive.google.com\...).
- Dominio wildcard (`*google.com/`): corrisponde a qualsiasi dominio **contenente** \"google.com\" (ad esempio, google.com, www.google.com, supergoogle.com).

Esempi:

- Invia tutte le query per \"google.com\" e i suoi sottodomini a 1.2.3.4: `/google.com/1.2.3.4`
- Invia tutti i nomi non qualificati (ad esempio, \"localhost\") a 10.0.0.1 e tutto il resto ai server standard: `//10.0.0.1`
- Invia le query per il dominio \"ad.nethserver.org\" e i suoi sottodomini a 192.168.1.1 e tutto il resto ai server standard: `/ad.nethserver.org/192.168.1.1`

I domini più specifici hanno la precedenza sui domini meno specifici, quindi per una configurazione come questa:

- `/google.com/1.2.3.4`
- `/www.google.com/2.3.4.5`

NethSecurity invierà le query per google.com e gmail.google.com a 1.2.3.4, ma www.google.com andrà a 2.3.4.5

Questo vale anche per i wildcard: se sia domini specifici che wildcard sono definiti per lo stesso pattern, il dominio specifico ha la precedenza (ad esempio, avendo `/google.com/` e `/*google.com/` : il primo gestirà google.com e www.google.com, il wildcard gestirà supergoogle.com.

### Massimo numero di query DNS simultanee {#dns_forward_max-section}

Per impostazione predefinita, dnsmasq ha un limite di 150 query DNS simultanee per prevenire attacchi DoS. Se questo limite viene raggiunto, dnsmasq registrerà un errore e smetterà di elaborare nuove query DNS fino al completamento di alcune delle query esistenti.

In questo caso, dnsmasq registrerà un errore simile a:

``` text
May 12 09:27:23 fw1 dnsmasq[1]: Maximum number of concurrent DNS queries reached (max: 150)
```

Per aumentare il limite dalla CLI, esegui i seguenti comandi: :

``` bash
uci set dhcp.@dnsmasq[0].dnsforwardmax=5000
uci commit dhcp
reload_config
```

Questa opzione non è esposta nell'interfaccia utente, ma la modifica persisterà tra gli aggiornamenti e non verrà sovrascritta dall'interfaccia utente.

### Intervallo di aggiornamento del set di domini {#dns_dhcp_domain_set_refresh-section}

Gli indirizzi del [set di domini](../users-objects/objects.md#domain_sets-section) vengono aggiornati quando dnsmasq esegue una nuova ricerca per il dominio. Quando le risposte vengono servite dalla cache locale invece di eseguire una nuova ricerca, gli indirizzi IP non vengono aggiunti nuovamente al set. Ciò può causare lacune intermittenti se il set IP scade prima della scadenza del DNS TTL, oppure se la cache impedisce a dnsmasq di eseguire ricerche aggiornate. Si noti che Adblock può alterare il comportamento di dnsmasq e influire sull'aggiornamento del set di domini.

Un lavoro cron viene eseguito ogni 10 minuti per aggiornare tutti i set di domini, ma dipende anche da dnsmasq che esegue ricerche effettive piuttosto che servire risultati cache.

Per risolvere i problemi di aggiornamento del set di domini, regola le impostazioni della cache DNS TTL:

``` text
uci set dhcp.@dnsmasq[0].max_cache_ttl=300
uci set dhcp.@dnsmasq[0].max_ttl=300
uci commit dhcp
reload_config
```

Queste impostazioni garantiscono che le voci cache scadano tempestivamente, consentendo a dnsmasq di eseguire ricerche aggiornate e aggiornare correttamente i set di domini. Si prega di notare che questa impostazione sostituirà il TTL predefinito fornito dai server DNS upstream. Un TTL così basso può aumentare il numero di query inviate ai server DNS upstream, il che può portare a un maggiore traffico di rete e a potenziali problemi di prestazioni se i server upstream hanno limiti di velocità o se ci sono molti client che effettuano frequenti richieste DNS. Utilizza questa configurazione con cautela e monitora le prestazioni del sistema dopo averla applicata.

### Protezione dal DNS Rebind

La protezione dal DNS Rebind è una funzionalità di sicurezza che protegge dagli attacchi di DNS rebinding. Blocca l'uso di intervalli IP privati per domini pubblici, impedendo ai siti web dannosi di manipolare i browser per effettuare richieste non autorizzate ai dispositivi della rete locale.

La protezione dal DNS Rebind è abilitata per impostazione predefinita su NethSecurity e di solito non ha conseguenze operative. In presenza di DNS split, risolvendo domini pubblici con risorse interne, la protezione dal rebind potrebbe portare a problemi di risoluzione. In tali scenari, i potenziali problemi possono essere trovati nel log (`/var/log/messages`), dove potrebbero apparire linee simili a queste:

``` text
Sep 21 13:09:36 fw1 dnsmasq[1]: possible DNS-rebind attack detected: ad.nethesis.it
```

:::note

Per garantire la massima compatibilità e prevenire malfunzionamenti nelle installazioni migrate utilizzando lo strumento dedicato da NethServer 7.9, la protezione dal DNS Rebind è disabilitata, garantendo lo stesso comportamento della versione precedente.

:::

#### Come risolvere i problemi di protezione dal DNS rebind

Puoi facilmente risolvere qualsiasi problema di questi dal CLI.

**Soluzione 1**: Whitelist il dominio

Metti il dominio specifico in una whitelist (consigliato): :

``` bash
uci add_list dhcp.@dnsmasq[0].rebind_domain="nethesis.it"
```

quindi commit e restart: :

``` bash
uci commit dhcp
/etc/init.d/dnsmasq restart
```

**Soluzione 2**: disabilita la protezione DNS

Disabilita completamente la protezione dal DNS rebind utilizzando questi comandi: :

``` bash
uci set dhcp.@dnsmasq[0].rebind_protection='0'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

#### Come abilitare la protezione dal DNS rebind

Se in precedenza hai disabilitato la protezione dal rebind o se la tua configurazione proviene da una migrazione e desideri abilitare la protezione dal rebind, è consigliabile attivare anche il parametro `rebind_localhost`. Questa impostazione ha effetto esclusivamente quando la protezione dal rebind è abilitata e consente le risposte upstream da 127.0.0.0/8, essenziale per i servizi di blacklist basati su DNS. Esegui questi comandi: :

``` bash
uci set dhcp.@dnsmasq[0].rebind_protection='1'
uci set dhcp.@dnsmasq[0].rebind_localhost='1'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

## Record DNS {#dns_records-section}

Il sistema può gestire record DNS locali. Quando il server esegue una ricerca DNS, prima cercherà all'interno dei record DNS locali. Se non viene trovato alcun record locale, verrà eseguita una query DNS esterna.

:::note

I record DNS locali sostituiranno sempre i record dai server DNS esterni.

:::

Fai clic sul pulsante **Aggiungi record DNS** per aggiungere un nuovo nome host DNS.

Campi disponibili:

- `Nome host` : Nome host DNS
- `Indirizzo IP` : Indirizzo IP associato al nome host
- `Nome` : campo opzionale
- `Record DNS wildcard`: abilitalo se desideri questa risposta per qualsiasi sottodominio che non hai già definito

## Scansione rete {#scan network-section}

Questa sezione descrive la funzionalità di scansione della rete locale. La pagina consente la scansione di tutte le reti locali disponibili, escludendo le reti WAN. La pagina mostra un elenco delle reti locali rilevate, ogni rete include un pulsante Scansione rete, selezionando questo pulsante si avvia una scansione completa della rete scelta.

### Risultati della scansione

Al completamento dell'operazione, la pagina mostra una tabella con tutti gli host rilevati. Per ogni host vengono fornite le seguenti informazioni:

- Indirizzo IP
- Indirizzo MAC
- Nome host (se rilevato)
- Descrizione

Puoi selezionare qualsiasi host dalla tabella e creare una voce di record DNS o una prenotazione DHCP utilizzando il menu a tre punti corrispondente.

:::note

Il sistema supporta la scansione solo su reti con una netmask massima di 255.255.240.0 (CIDR /20), che corrisponde a un massimo di 4094 host. Le scansioni su reti più grandi non sono supportate.

:::

## DHCP Relay

Il relay DHCP consente al firewall di inoltrare le richieste DHCP dai client a un server DHCP esterno, il relay DHCP non è disponibile dall'interfaccia utente, ma è possibile configurarlo dal terminale utilizzando `uci`.

- Sostituisci `\<INTERFACE_NAME\>` con il nome dell'interfaccia in cui il relay DHCP dovrebbe ascoltare.
- Sostituisci `\<LOCAL_ADDR\>` con l'indirizzo IP del firewall su quell'interfaccia.
- Sostituisci `\<SERVER_ADDR\>` con l'indirizzo IP del server DHCP upstream.

1.Crea una nuova voce di relay DHCP:

``` bash
uci add dhcp relay
```

2.Imposta l'interfaccia:

``` bash
uci set dhcp.@relay[-1].interface='<INTERFACE_NAME>'
```

3.Imposta l'indirizzo locale del firewall:

``` bash
uci set dhcp.@relay[-1].local_addr='<LOCAL_ADDR>'
```

4.Imposta l'indirizzo del server DHCP upstream:

``` bash
uci set dhcp.@relay[-1].server_addr='<SERVER_ADDR>'
```

5.Commit della configurazione:

``` bash
uci commit dhcp
```

6.Ricarica la configurazione del sistema:

``` bash
reload_config
```

### Esempio

``` bash
uci add dhcp relay
uci set dhcp.@relay[-1].interface='LAN'
uci set dhcp.@relay[-1].local_addr='192.168.1.1'
uci set dhcp.@relay[-1].server_addr='192.168.10.100'
uci commit dhcp
reload_config
```

## Riferimenti esterni

- [Documentazione OpenWrt DNS e DHCP](https://openwrt.org/docs/guide-user/base-system/dhcp)
- [Manuale Dnsmasq](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)
