---
title: "Controller"
sidebar_position: 7
---

# Controller {#controller-section}

Il controller NethSecurity è un'applicazione che può essere eseguita su [NethServer 8](https://docs.nethserver.org/projects/ns8/en/latest/nethsecurity_controller.html) (NS8). Il controller consente il controllo remoto di più installazioni di NethSecurity, chiamate unità.

Il firewall può operare in modo indipendente senza necessità del controller. Il controller è un componente opzionale che fornisce capacità aggiuntive di gestione e monitoraggio del firewall.

Il controller crea una connessione sicura tra il server centrale e le unità. Ogni firewall si registra con il server utilizzando un client chiamato ns-plug. Una volta registrato, il server genera una configurazione VPN che viene inviata di nuovo al firewall. La VPN consente una comunicazione sicura tra il controller e l'unità.

Caratteristiche principali:

- **Gestione centralizzata**: Gestisci più firewall da un unico server.
- **Comunicazione sicura**: Stabilisci una connessione sicura [OpenVPN](https://openvpn.net/) tra il server e i firewall.
- **Configurazione semplice**: Configura i firewall direttamente dall'interfaccia utente del controller.
- **Monitoraggio e registrazione**: Raccogli e analizza i log dai firewall all'interno di [Loki](https://grafana.com/oss/loki/) per scopi di risoluzione dei problemi e monitoraggio.
- **Visualizzazione delle metriche**: Visualizza le metriche dai firewall utilizzando il dashboard [Grafana](https://grafana.com/) integrato. Le metriche vengono raccolte utilizzando [Prometheus](https://prometheus.io/) e [TimescaleDB](https://www.timescale.com/).
- **SSH basato su web**: Accedi all'interfaccia della riga di comando del firewall utilizzando un client SSH basato su web.

## Installazione e configurazione

Il controller può essere installato su un sistema NethServer 8 dal Software Center. Il modulo è denominato `NethSecurity Controller`.

Dopo l'installazione, il controller deve essere configurato. La configurazione può essere eseguita utilizzando l'interfaccia web di NethServer 8. È necessario impostare i seguenti parametri:

- `Nome host controller`: Il fully qualified domain name (FQDN) del controller, ad esempio: `mycontroller.nethsecurity.org`. Assicurati che il nome host sia risolvibile e raggiungibile dalle unità.
- `Certificato Let\'s Encrypt`: Abilita o disabilita il certificato Let\'s Encrypt per l'interfaccia web del controller. È consigliato abilitarlo.
- `Rete VPN` e `Maschera VPN`: La rete OpenVPN e la maschera di rete. Quando scegli la rete, assicurati che non si sovrapponga con le reti esistenti all'interno di tutte le unità che verranno connesse al controller. Utilizza solo reti di classe C come `192.168.7.0` con maschera `255.255.255.0`.
- `Utente amministratore`: Il nome utente dell'amministratore del controller. L'utente amministratore è l'unico che può creare e gestire altri utenti all'interno del controller. Lo stesso nome utente viene utilizzato per accedere all'interfaccia Grafana.
- `Password amministratore`: Scegli una password forte per l'utente amministratore. Nota che la password predefinita viene visualizzata una sola volta, si prega di salvarla in un luogo sicuro. La stessa password viene utilizzata per accedere all'interfaccia Grafana. Per motivi di sicurezza, è consigliabile modificare la password dopo il primo accesso sia per il controller che per l'interfaccia Grafana.

I seguenti parametri sono facoltativi:

- `Nome controller`: Il nome del controller, utilizzato per creare l'autorità di certificazione VPN. Puoi lasciarla invariata a meno che non abbia un requisito specifico.
- `Conservazione dei log`: Il periodo di conservazione dei log in giorni, il valore predefinito è 180 giorni. Si applica ai log memorizzati in Loki.
- `Conservazione delle metriche`: Il periodo di conservazione delle metriche in giorni, il valore predefinito è 15 giorni. Si applica alle metriche memorizzate in Prometheus e Timescale.
- `Chiave di licenza MaxMind`: Il controller può geolocalizzare gli indirizzi IP dei client VPN connessi e degli aggressori. Una mappa con la posizione dei client e degli aggressori verrà visualizzata all'interno di Grafana. La chiave di licenza è necessaria per abilitare la funzione e scaricare il database MaxMind GeoIP2. Per ottenere una chiave di licenza gratuita, registrati sul [sito web MaxMind](https://www.maxmind.com/en/geolite2/signup), quindi accedi alla pagina `Manage License Keys` nella sezione account. Genera una nuova licenza, copia la chiave di licenza e incollala nel campo.
- `IP consentiti`: L'elenco degli indirizzi IP o degli intervalli CIDR che sono autorizzati ad accedere all'interfaccia web del controller. Per impostazione predefinita, l'elenco è vuoto, il che significa che l'accesso è consentito da tutti gli indirizzi IP. Puoi limitare l'accesso a IP o reti specifiche per motivi di sicurezza. Se abilitato, solo l'endpoint di registrazione (ad es. `https://controller.nethserver.org/api/register`) sarà accessibile dalle unità, consentendo loro di registrarsi con il controller. Tutto il resto del traffico tra il controller e le unità sarà instradato attraverso la connessione VPN. Questa funzione richiede la versione dell'unità 8.6 o successiva.

Dopo aver completato la configurazione, il controller è pronto per essere utilizzato e può essere accessibile utilizzando un browser web al nome host configurato, come `https://mycontroller.nethsecurity.org`.

:::note

Per garantire il corretto funzionamento, il controller deve essere accessibile sulla rete su porte specifiche.

- `Porta TCP 443 (HTTPS)` per accedere a WebUI e consentire la comunicazione delle unità.
- `Una porta UDP allocata dinamicamente` aperta da NethServer 8 e utilizzata per le connessioni VPN dalle unità, questa porta viene generata casualmente al momento della configurazione.

Il numero effettivo della `porta UDP` può essere trovato nella pagina di stato del modulo Controller nella sezione `OpenVPN UDP Port`. Assicurati che queste porte siano aperte su qualsiasi firewall che protegge il nodo che esegue il controller.

:::

## Utenti

Il controller ha due tipi di utenti:

- **Utenti amministratori**: Gli utenti amministratori sono gli unici che possono creare e gestire utenti all'interno del controller. Gli utenti amministratori possono anche accedere a tutte le unità.
- **Utente standard**: Gli utenti standard possono gestire le unità e le configurazioni del firewall. Questi utenti devono essere associati a un gruppo di unità: potranno accedere solo alle unità associate al loro gruppo. Se un utente non è associato a nessun gruppo, non avrà accesso ad alcuna unità. Consulta [Gruppi di unità](#controller_unit_groups-section) per maggiori informazioni sui gruppi di unità.

Un utente amministratore viene creato durante la configurazione del controller dall'interfaccia web di NethServer 8. L'utente amministratore può creare e gestire altri utenti dall'interfaccia web del controller. Un utente può essere associato a un gruppo di unità dall'interfaccia web del controller, all'interno della pagina di gestione degli utenti.

È consigliato creare un utente per ogni persona che ha bisogno di accedere al controller. Quando si crea un nuovo utente, l'amministratore deve specificare il nome utente, il nome visualizzato dell'utente e la password dell'utente. Il nome utente viene utilizzato per accedere al controller, mentre il nome visualizzato viene utilizzato per identificare l'utente nel controller.

L'amministratore può anche:

- ripristinare la password dell'utente ed eliminare gli utenti
- promuovere un utente ad amministratore
- eliminare un account utente

Dopo il login, ogni utente dovrebbe modificare la propria password e generare una coppia di chiavi SSH per accedere alle unità.

### Autenticazione a due fattori (2FA)

Ogni utente del controller può abilitare l'autenticazione a due fattori (2FA) per aumentare la sicurezza dell'account. Per abilitare la 2FA, segui gli stessi passaggi documentati nell'interfaccia web del firewall: [NethSecurity UI 2FA](../installation/remote_access.md#2fa-section).

L'amministratore può vedere lo stato 2FA di ogni utente nell'elenco degli utenti.

#### Ripristino 2FA {#fa-reset}

Se un amministratore del controller ha perso l'accesso al proprio dispositivo OTP e non può accedere, la 2FA può essere ripristinata dal nodo NethServer 8 cancellando i campi `otp_secret` e `otp_recovery_codes` direttamente nel database del controller.

Esegui i seguenti comandi sul nodo NethServer 8, sostituendo `nethsecurity-controller1` con il nome effettivo dell'istanza del modulo controller e `admin` con il nome utente interessato: :

    runagent -m nethsecurity-controller1
    source db.env; podman exec -it timescale psql -U "${POSTGRES_USER}" -p "${POSTGRES_PORT}" \
      -c "UPDATE accounts SET otp_recovery_codes='', otp_secret='' WHERE username = 'admin';"

Dopo il completamento della query, l'utente può accedere con solo la password e re-iscrivere un nuovo dispositivo OTP dall'interfaccia utente del controller.

## Unità

Tutti gli utenti possono gestire le unità. Un'unità è un firewall gestito dal controller.

Per connettere una nuova unità al controller, l'utente deve fare clic sul pulsante **Aggiungi unità** dall'interfaccia web del controller. Quando viene aggiunta una nuova unità, il controller esegue le seguenti azioni:

- crea un identificatore univoco per l'unità
- alloca un indirizzo IP all'interno della rete VPN
- genera una configurazione VPN includendo i certificati
- memorizza in modo sicuro le credenziali necessarie per accedere al firewall remoto

Verrà generato e visualizzato sullo schermo un codice di join. Il codice di join deve essere inserito nell'unità per stabilire la connessione con il controller.

Accedi alla pagina `Controller` nell'interfaccia web dell'unità e inserisci il codice di join nel campo `Join code`. Quando ti unisci al controller, l'unità scaricherà la configurazione VPN e stabilirà una connessione sicura con il controller. Se la connessione ha successo, l'unità sarà visualizzata nell'interfaccia web del controller con lo stato `Connected`.

Tieni presente che se il controller non ha un certificato Let\'s Encrypt valido, dovrai disabilitare l'opzione `Verify TLS certificate` nella configurazione dell'unità.

Quando l'unità è connessa, l'utente può accedere all'interfaccia web dell'unità facendo clic sul collegamento **Apri unità** senza dover inserire le credenziali dell'unità.

:::note

L'interfaccia utente dell'unità [deve ascoltare sulla porta 9090](../installation/remote_access.md#change_ui_port-section) per consentire al controller di accedervi. Il controller accederà all'interfaccia web dell'unità attraverso la connessione VPN. La porta 9090 non deve essere aperta dal lato WAN, ma deve essere aperta dal lato VPN per consentire al controller di accedervi.

:::

**Rimuovere un'unità**

Le unità possono essere scollegate dal controller facendo clic sul pulsante **Rimuovi unità** dall'interfaccia web del controller. Quando un'unità viene scollegata, il controller rimuoverà la configurazione dell'unità e la connessione VPN verrà terminata.

Dopo aver rimosso l'unità dall'interfaccia web del controller, accedi all'interfaccia web dell'unità e fai clic su **Disconnetti unità** nella pagina `Controller`: l'unità distruggerà la configurazione VPN.

## Gruppi di unità {#controller_unit_groups-section}

I gruppi di unità sono un modo per organizzare le unità all'interno del controller. Ogni utente può essere associato a uno o più gruppi di unità. Quando un utente è associato a un gruppo di unità, può accedere solo alle unità che appartengono a quel gruppo. I gruppi di unità sono utili per limitare l'accesso a unità specifiche per utenti specifici.

Per creare un nuovo gruppo di unità, l'amministratore deve fare clic sul pulsante **Aggiungi gruppo** dall'interfaccia web del controller, all'interno della pagina `Unit groups`. L'amministratore può specificare il nome del gruppo, una descrizione e le unità che appartengono al gruppo.

Una volta creato un gruppo di unità, l'amministratore può associare il gruppo di unità a un utente. Per farlo, l'amministratore deve accedere all'elenco degli utenti all'interno della pagina `Users`. Quindi, fare clic sul pulsante **Modifica** accanto all'utente e selezionare il gruppo di unità dal menu a discesa `Unit groups`.

### Rimozione dei gruppi di unità

Un gruppo di unità può essere rimosso solo quando non ci sono utenti associati ad esso. Questo può essere verificato accedendo alla pagina `Users` e cercando eventuali utenti associati al gruppo.

Per rimuovere un gruppo di unità, l'amministratore deve accedere alla pagina `Unit groups` e fare clic sul pulsante **Elimina** accanto al gruppo.

### Gruppo di unità migrato

Quando si esegue l'aggiornamento da una versione del controller precedente a 2.0.0, verrà creato automaticamente un nuovo gruppo di unità `Migrated`. Il gruppo di unità `Migrated` include automaticamente tutte le unità gestite dal controller prima dell'aggiornamento. È anche associato a tutti gli utenti esistenti per garantire che mantengano l'accesso alle loro unità dopo la migrazione.

Il gruppo può essere rimosso tranquillamente una volta che non è più necessario.

## Gestione dei log {#controller_logs-section}

Quando un'unità è connessa, rsyslog viene riconfigurato per inviare i log utilizzando il protocollo syslog (RFC 5424). Potrebbe richiedere alcuni minuti prima che rsyslog inizi a inviare i dati. I log sono etichettati utilizzando il nome host dell'unità: per assicurare che i collegamenti dell'interfaccia utente funzionino correttamente, assicurati che:

- l'FQDN dell'unità è univoco all'interno del cluster
- il nome dell'unità è lo stesso del suo nome host

I log possono essere visualizzati facendo clic sul collegamento **Apri log** per ogni unità. I log vengono visualizzati in un dashboard Grafana specifico che consente anche di ricercare e filtrare.

:::note

Il periodo di conservazione dei log deve essere configurato dall'interfaccia web di NS8.

:::

## Metriche {#controller_metrics-section}

Ogni unità esporta due tipi di metriche:

- metriche operative del sistema (CPU, memoria, disco, rete): queste metriche vengono raccolte utilizzando [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) e memorizzate in [Prometheus](https://prometheus.io/). Non appena un'unità è connessa, il controller inizia a raschiare le metriche. Queste metriche sono disponibili a tutti indipendentemente dallo stato dell'abbonamento.
- metriche del firewall (traffico, sicurezza, VPN): queste metriche vengono inviate dall'unità al controller a intervalli fissi. Il controller le memorizza all'interno di un database [Timescale](https://www.timescale.com/). Queste metriche sono disponibili solo agli utenti con un abbonamento valido.

Tutti i dati raccolti e memorizzati all'interno del controller sono contrassegnati dall'ora utilizzando l'ora universale coordinata (UTC). Ciò garantisce coerenza e precisione in diversi fusi orari, facilitando la correlazione degli eventi e l'analisi delle tendenze.

Gli utenti hanno la flessibilità di visualizzare i dati nel loro fuso orario locale modificando le impostazioni dell'ora in Grafana. Per modificare il fuso orario locale, vai al menu delle preferenze di Grafana e seleziona il fuso orario desiderato. Questo adattamento può essere applicato a ogni dashboard individualmente, consentendo agli utenti di personalizzare la visualizzazione del fuso orario in base alle loro preferenze.

Le metriche possono essere visualizzate all'interno del dashboard Grafana. Gli utenti possono accedere al dashboard facendo clic sul collegamento **Apri metriche** per ogni unità.

Per impostazione predefinita, solo l'utente admin può accedere al dashboard delle metriche. Se desideri consentire ad altri utenti di accedere al dashboard delle metriche, puoi creare un nuovo ruolo e assegnarlo all'utente direttamente dall'interfaccia web di Grafana.

:::note

A partire da NethSecurity 8.8, Netdata non è installato per impostazione predefinita sulle unità. Se hai configurato dashboard personalizzati che si basano sulle metriche di Netdata, puoi reinstallarlo manualmente nell'unità.

Consulta [sezione legacy Netdata](../monitoring/monitoring.md#legacy_netdata-section) per maggiori informazioni su come reinstallarlo.

:::

### Grafana {#grafana-section}

Grafana è una piattaforma open-source utilizzata per il monitoraggio e la visualizzazione dei dati delle serie temporali. Aiuta gli utenti a creare dashboard personalizzati con grafici, diagrammi e tabelle per analizzare le metriche di sistema, i log e altri dati da varie fonti.

Il controller include un'istanza Grafana preconfigurata utilizzata per visualizzare le metriche e i log dalle unità connesse. L'istanza di Grafana è accessibile dall'URL `https://<controller-fqdn>/grafana`.

Per impostazione predefinita, puoi accedervi utilizzando le credenziali predefinite impostate durante la configurazione del controller. Ricorda di modificare la password predefinita dopo il primo accesso. Grafana fornisce anche funzioni per gestire utenti, team e autorizzazioni. Supporta l'autenticazione tramite vari metodi tra cui nome utente/password, OAuth, LDAP e altro.

Puoi anche creare dashboard personalizzati e avvisi per monitorare le metriche e i log dalle unità connesse. Consulta la [documentazione ufficiale](https://grafana.com/docs/grafana/latest/) per maggiori informazioni su come utilizzare Grafana.

#### Metriche Prometheus

Le metriche Prometheus vengono raccolte per impostazione predefinita utilizzando Telegraf. Quando Netdata viene installato manualmente, Prometheus raschia anche le metriche da esso.

Le metriche esportate per ogni unità includono le seguenti etichette:

- `instance` l'IP della VPN della macchina connessa con la porta Netdata (ad es. `172.19.64.3:19999`)
- `job` fisso su `node`
- `node` l'IP della VPN della macchina connessa
- `unit` il nome univoco dell'unità della macchina connessa

Queste metriche sono visibili all'interno del dashboard `Operating system`.

#### Metriche Timescale

:::note

Abbonamento obbligatorio

Questa funzione è disponibile solo se il firewall e il controller hanno un abbonamento valido.

:::

Il database Timescale memorizza le stesse metriche del [Monitoraggio in tempo reale](../monitoring/monitoring.md#real_time_monitoring-section) ma come una serie temporale salvata in un database PostgreSQL. Ogni unità invia dati al controller ogni 15 minuti. Il controller aggrega i dati ogni 15 minuti, il che significa che i dati sono disponibili all'interno dei dashboard nel migliore dei casi con un ritardo di 15 minuti e nel peggiore dei casi con un ritardo di 30 minuti.

Il controller può eseguire un'elaborazione aggiuntiva sui dati per fornire maggiori informazioni. Ad esempio, il controller può geolocalizzare gli indirizzi IP dei client connessi e degli aggressori.

Queste metriche sono visibili all'interno dei seguenti dashboard:

- `Network traffic`: traffico di rete aggregato come visto dall'unità
- `Network traffic by client`: traffico di rete per ogni client (host locale) connesso all'unità
- `Network traffic by host`: traffico di rete per ogni host remoto
- `Security`: eventi di sicurezza rilevati dall'unità
- `VPN`: statistiche VPN per tunnel OpenVPN Road Warrior, tunnel OpenVPN e tunnel IPsec

:::note

Il periodo di conservazione delle metriche deve essere configurato dall'interfaccia web di NS8 e si applica sia ai database Prometheus che Timescale.

:::

## Aggiornamenti delle unità {#controller_updating-section}

Il controller consente di aggiornare le unità direttamente dall'interfaccia, simile al processo nell'[interfaccia web dell'unità](./updates.md). Due tipi di aggiornamenti sono disponibili:

- **Aggiornamenti dei pacchetti**: Aggiorna i pacchetti installati nell'unità. Elenca e installa gli aggiornamenti disponibili facendo clic su **Verifica aggiornamenti pacchetti** nel menu dell'unità. Una finestra modale visualizzerà l'elenco degli aggiornamenti disponibili. Se gli aggiornamenti sono disponibili, applicali facendo clic sul pulsante **Aggiorna** nella finestra modale. Questo è il primo tentativo da fare se la [consapevolezza della versione](#version-awareness-section) ti impedisce di accedere all'unità.
- **Aggiornamento del sistema**: Aggiorna il sistema dell'unità. Se è disponibile un aggiornamento dell'immagine, un badge apparirà nell'elenco delle unità. Pianifica un aggiornamento facendo clic sul pulsante **Aggiornamento del sistema** nel menu dell'unità. Puoi pianificare l'aggiornamento o aggiornare l'unità immediatamente. Questa operazione è disponibile anche come operazione di massa per più unità in **Azioni** -> **Aggiorna sistemi**. Le unità con un aggiornamento dell'immagine pianificato avranno un badge dedicato nell'elenco delle unità. Puoi interrompere l'aggiornamento dell'immagine pianificato facendo clic sul pulsante **Annulla aggiornamento immagine pianificato** nel menu dell'unità.

:::note

Ti avvertimento che le unità potrebbero non inviare informazioni aggiornate durante il processo di aggiornamento prima della versione dell'unità 1.3.0. Per aggiornare manualmente le informazioni, utilizza il pulsante `guilabel`:`Sincronizza informazioni unità` nel menu dell'unità.

:::

## Accesso SSH {#controller_ssh-section}

SSH, o Secure Shell, è un protocollo di rete crittografico per operare i servizi di rete in modo sicuro su una rete non sicura. SSH fornisce un canale sicuro su una rete non sicura in un'architettura client-server, connettendo un'applicazione client SSH a un server SSH.

È possibile connettersi all'unità facendo clic sul collegamento **Apri terminale SSH**. La connessione viene effettuata attraverso un client SSH basato su web che consente l'accesso alla shell dell'unità.

Puoi connetterti alle unità utilizzando una coppia di nome utente e password o una chiave SSH.

Una volta connesso, la sessione SSH verrà avviata in una nuova scheda del browser. Alcuni browser richiedono il permesso di aprire popup affinché la sessione SSH funzioni correttamente. Per chiudere la sessione, semplicemente chiudi la finestra del browser o esci dalla shell utilizzando CTRL + D.

### Nome utente e password

L'utente può connettersi utilizzando una coppia di nome utente e password dell'unità nei seguenti scenari:

- L'utente connesso non ha generato una chiave SSH
- La chiave SSH pubblica dell'utente connesso non è stata copiata nel file delle chiavi SSH autorizzate dell'unità

L'interfaccia utente visualizzerà un modulo per inserire il nome utente e la password. Dopo aver inserito le credenziali, l'utente può fare clic sul pulsante **Apri terminale** per avviare la sessione SSH.

### Chiave SSH

Una coppia di chiavi SSH è un insieme di due chiavi crittografiche utilizzate per l'autenticazione quando si stabilisce una connessione sicura utilizzando il protocollo SSH (Secure Shell). La coppia consiste di una chiave privata e una chiave pubblica:

1.  **Chiave privata**: Questa viene mantenuta segreta e sicura dall'utente. Non dovrebbe mai essere esposta al mondo esterno. Viene utilizzata per decrittare i dati che sono stati crittografati con la chiave pubblica.
2.  **Chiave pubblica**: Questa può essere condivisa liberamente ed è utilizzata per crittare i dati che possono essere decrittati solo con la chiave privata.

Quando ti connetti a un server utilizzando SSH con autenticazione a coppia di chiavi, fornisci la tua chiave pubblica al server. Il server quindi crittografa un messaggio di sfida con la tua chiave pubblica. Il tuo client quindi decrittografa il messaggio con la tua chiave privata e invia il risultato di nuovo al server. Se il risultato è corretto, il server sa che devi avere la chiave privata corretta e ti consente di connetterti.

Questo metodo di autenticazione è più sicuro rispetto all'utilizzo di una password, poiché fornisce una forma di autenticazione a due fattori: qualcosa che possiedi (il file della chiave privata) e qualcosa che conosci (la passphrase per sbloccare la chiave privata).

Per utilizzare una chiave SSH, genera una nuova coppia di chiavi accedendo alla pagina `Account settings` e facendo clic sul pulsante **Genera coppia di chiavi SSH**. Inserisci una passphrase per proteggere la chiave privata e fai clic sul pulsante **Genera chiave SSH**. L'interfaccia utente visualizzerà la chiave pubblica, mentre la chiave privata viene preservata in modo sicuro all'interno del controller.

Prima di connettersi all'unità, devi copiare la chiave pubblica e incollarla nel file delle chiavi SSH autorizzate dell'unità. Puoi farlo dalla pagina `Unit manager`, facendo clic sul pulsante **Azioni** e selezionando **Invia chiave SSH pubblica**. Scegli le unità a cui desideri inviare la chiave e fai clic sul pulsante **Invia chiave SSH**.

Da ora in poi, puoi connetterti all'unità utilizzando la coppia di chiavi SSH. L'interfaccia utente visualizzerà un modulo per inserire la passphrase quando fai clic sul pulsante **Apri terminale**.

Puoi anche revocare la coppia di chiavi SSH facendo clic sul pulsante **Revoca chiave SSH pubblica** dal pulsante **Azioni**.

## Contabilità

Tutte le operazioni eseguite sul controller vengono registrate nel log di NS8. Ecco alcuni esempi di operazioni registrate:

- Login e logout dell'utente
- Creazione/modifica/eliminazione/cambio password dell'utente
- Elenco/creazione/rimozione delle unità

Esempio di log NS8: :

    Mar 26 11:08:23 controller.nethserver.net api[64323]: nethsecurity_controller 2024/03/26 11:08:23 middleware.go:85: [INFO][AUTH] authentication success for user admin
    Mar 26 11:08:23 controller.nethserver.net api[64323]: nethsecurity_controller 2024/03/26 11:08:23 middleware.go:186: [INFO][AUTH] login response success for user admin

Ogni unità ha un utente rpcd specifico per il controller, che viene utilizzato per operazioni di gestione. Quando un utente accede all'interfaccia web dell'unità dal controller, tutte le operazioni eseguite vengono registrate nel log dell'unità, identificate dall'utente rpcd. Ad esempio: :

    Mar 26 11:28:52 NethSec nethsecurity-api[4535]: nethsecurity_api 2024/03/26 11:28:52 middleware.go:166: [INFO][AUTH] authorization success for user 0a891388811ff8dc0ec2fbed. POST /api/ubus/call {"path":"ns.dashboard","method":"interface-traffic","payload":{"interface":"eth1"}}
    Mar 26 11:28:52 NethSec (none) nginx: 172.19.64.1 - - [26/Mar/2024:11:28:52 +0000] "POST /api/ubus/call HTTP/1.1" 200 1490 "https://controller.gs.nethserver.net/" "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"

Per determinare chi ha eseguito un'operazione specifica, è necessario controllare il log dell'unità identificata dall'utente rpcd e correlarlo con l'azione di login eseguita sul controller.

Quando un utente si connette all'unità tramite SSH, il login viene registrato nel log dell'unità, identificato dall'utente SSH. Di solito, l'utente SSH è root. Ad esempio: :

    Mar 26 11:55:03 NethSec dropbear[22798]: Password auth succeeded for 'root' from 172.19.64.1:46460

Se l'utente utilizza una chiave SSH per l'autenticazione, il log conterrà l'impronta digitale della chiave SSH utilizzata per l'autenticazione. Ciò rende più facile associare l'utente SSH alle operazioni eseguite. Esempio: :

    Mar 26 11:09:33 NethSec dropbear[31090]: Child connection from 172.19.64.1:52012
    Mar 26 11:09:33 NethSec dropbear[31090]: Pubkey auth succeeded for 'root' with ssh-rsa key SHA256:FLecvNRKi0hxxxdjfP0urUZxxx6jxxxxNbZceOPFjyk from 172.19.64.1:52012

## Abbonamento e limitazioni

:::note

Abbonamento obbligatorio

Alcune restrizioni possono essere superate solo se il firewall ha un abbonamento valido.

:::

Il comportamento del controller in esecuzione su un NS8 dipende dal suo stato di abbonamento.

Controller senza abbonamento:

- Consente la registrazione di fino a 3 unità.
- Solo i firewall della comunità possono registrarsi con il controller.
- Le metriche storiche non sono accessibili.

Controller con un abbonamento valido:

- Il numero di unità è illimitato.
- Solo i firewall con un abbonamento valido possono registrarsi con il controller.
- Le unità con un abbonamento valido inviano metriche al controller.

## Consapevolezza della versione {#version-awareness-section}

La consapevolezza della versione è un meccanismo che impedisce all'utente di eseguire operazioni non supportate dalla versione dell'unità. Per farlo, quando ci si connette all'interfaccia utente di un'unità, il controller controllerà la versione dell'API durante il processo di connessione. Ci sono tre possibili scenari:

a.  Se le versioni sono compatibili, la connessione procede normalmente.
b.  Se il firewall (unità) è significativamente più vecchio del controller, vedrai un popup che impedisce la connessione. Ciò è per proteggere da potenziali errori.
c.  Se il controller è leggermente più vecchio del firewall, vedrai un avviso sulla mancata corrispondenza. Tuttavia, potrai ancora connetterti se scegli di procedere.

Come amministratore, non è necessario intraprendere azioni specifiche per abilitare la consapevolezza della versione. Funziona automaticamente in background. Tuttavia, dovresti:

1.  Prestare attenzione agli avvisi: se vedi un avviso di mancata corrispondenza della versione, considera di aggiornare il tuo sistema quando opportuno.
2.  Mantieni il tuo sistema aggiornato: controlla regolarmente e applica gli aggiornamenti sia al controller che alle unità firewall per garantire la migliore compatibilità e accesso alle nuove funzioni.
3.  Segnala i problemi: se riscontri un comportamento insolito o errori, specialmente dopo aver visto un avviso di versione, segui la procedura di [risoluzione dei problemi](../best-practices/troubleshooting.md).

La consapevolezza della versione è una funzione dietro le quinte che aiuta a mantenere il sistema NethSecurity in esecuzione senza problemi. Controllando automaticamente la compatibilità tra il controller e le unità, previene molti potenziali problemi prima che possano influenzare la tua rete. Sebbene non richieda alcuna azione da parte tua, essere a conoscenza di questa funzione può aiutarti a comprendere e gestire meglio il tuo sistema.

**Bypass della consapevolezza della versione**

Sebbene la consapevolezza della versione sia una funzione utile, conoscendo i rischi e i potenziali problemi, potresti voler aggirare in alcuni casi. Per farlo, la procedura è la seguente:

1.  Nel controller, vai alla pagina del gestore delle unità e fai clic su **Ulteriori informazioni** dell'unità a cui desideri connetterti.
2.  Copia il valore `Unit ID`.
3.  Fai clic su **Apri terminale SSH**
4.  Quando si apre la finestra modale, puoi chiuderla tranquillamente. Questo era solo necessario per scambiare alcune credenziali con l'unità.
5.  Apri una nuova scheda e vai a questo URL: `https://\<controller-fqdn\>/#/controller/manage/\<unit-id\>/dashboard`. Esempio: `https://controller.nethsecurity.org/#/controller/manage/000000000-0000-0000-0000-000000000000/dashboard`.
6.  Sarai in grado di accedere all'interfaccia utente dell'unità senza il controllo della versione.

**Aggiorna l'unità con SSH**

Puoi aggiornare l'unità senza connetterti ad essa utilizzando il terminale SSH. Segui i passaggi per connetterti all'unità utilizzando l'[Accesso SSH](#controller_ssh-section).

Una volta connesso, puoi verificare gli aggiornamenti a seconda di cosa desideri aggiornare.

a.  Installa gli aggiornamenti dei pacchetti nell'unità:
    1.  Per verificare gli aggiornamenti dei pacchetti, utilizza il seguente comando:

        ``` bash
        /usr/libexec/rpcd/ns.update call check-package-updates
        ```

    2.  Se sei d'accordo con l'installazione dei pacchetti, puoi eseguire il seguente comando:

        ``` bash
        /usr/libexec/rpcd/ns.update call install-package-updates
        ```
b.  Per aggiornare l'immagine, puoi semplicemente pianificare l'installazione, ricorda che questa è un'operazione che riavvia il firewall (causando un downtime)
    1.  Verifica se è disponibile un'immagine aggiornata:

        ``` bash
        /usr/libexec/rpcd/ns.update call check-system-update
        ```

    2.  Se desideri procedere con l'aggiornamento, questo può essere fatto attraverso questo comando:

        ``` bash
        /usr/libexec/rpcd/ns.update call update-system
        ```
