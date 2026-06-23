---
title: "Sistema di prevenzione delle intrusioni (Snort)"
sidebar_position: 6
---

# Sistema di prevenzione delle intrusioni (Snort) {#intrusion_prevention_system-section}

Snort 3 è un sistema aperto di prevenzione delle intrusioni di rete in grado di eseguire analisi del traffico in tempo reale e registrazione dei pacchetti su reti IP. Può eseguire analisi dei protocolli, ricerca/corrispondenza dei contenuti ed essere utilizzato per rilevare una varietà di attacchi e sonde, come overflow del buffer, scansioni di porte stealth, attacchi CGI, sonde SMB, tentativi di fingerprinting del sistema operativo e molto altro.

## Abilita IPS

IPS è disabilitato per impostazione predefinita. Per abilitarlo, vai alla pagina `IPS` nella sezione `Security`. L'interfaccia segnalerà che il servizio è disabilitato e fornirà un collegamento rapido per accedere direttamente alla scheda `Settings`.

Una volta attivato l'interruttore **Status**, potrai configurare il servizio.

### Politica delle regole

Le regole sono raggruppate in politiche, ogni politica è un insieme di regole ottimizzate per un caso d'uso specifico, le politiche sono:

- **connectivity**: privilegia le prestazioni rispetto alla sicurezza, minimizzando i falsi positivi e garantendo prestazioni elevate del dispositivo nel rilevamento di minacce comuni.
- **balanced**: consigliata per distribuzioni iniziali, equilibrando sicurezza e prestazioni con un tasso di prestazione relativamente elevato con strumenti di valutazione e test.
- **security**: per ambienti ad alta sicurezza con larghezza di banda inferiore e maggiore tolleranza ai falsi positivi. Fornisce la massima protezione riducendo al minimo il rischio di interruzione della rete.

### Reti domestiche

Le reti domestiche definiscono le reti interne protette e specificano gli indirizzi IP o le subnet che IPS dovrebbe considerare come reti locali, consentendogli di distinguere il traffico interno da quello esterno e riducendo i falsi positivi nel rilevamento delle minacce.

Seleziona una politica, definisci le tue reti domestiche e quindi fai clic sul pulsante **Save** per salvare le modifiche.

:::note

I valori di Home Networks non vengono aggiornati automaticamente. Se l'indirizzo IP di un'interfaccia locale viene modificato e ciò comporta una rete diversa, la configurazione di Home network di IPS deve essere aggiornata manualmente per riflettere la nuova rete.

:::

### Abilita Hyperscan

Hyperscan è un motore di corrispondenza di pattern avanzato che può migliorare le prestazioni di Snort3 su hardware supportato. Richiede che flag specifici del processore siano supportati dalla tua CPU.

Prima di abilitare Hyperscan, verifica che il tuo processore supporti i flag CPU richiesti:

``` bash
grep --color=auto -E 'sse3|ssse3|sse4_1|sse4_2|avx|avx2' /proc/cpuinfo
```

Se il comando restituisce risultati, il tuo processore è compatibile con Hyperscan.

Per abilitare Hyperscan, innanzitutto crea il file di configurazione in `/etc/snort/hyperscan.config`:

``` bash
cat > /etc/snort/hyperscan.config << 'EOF'
search_engine = { search_method = hyperscan }
detection = { hyperscan_literals = true, pcre_to_regex = true }
EOF
```

Quindi abilitalo con i seguenti comandi:

``` bash
uci set snort.snort.include=/etc/snort/hyperscan.config
uci commit snort
reload_config
```

Per disabilitare Hyperscan:

``` bash
uci del snort.snort.include
uci commit snort
reload_config
```

:::note

Hyperscan è una funzionalità opzionale di miglioramento delle prestazioni. Abilitalo solo se la tua CPU supporta i flag del processore richiesti e desideri migliorare le prestazioni di IPS a costo di requisiti più elevati delle funzionalità della CPU.

:::

## Accesso alle regole Snort tramite Oinkcode {#oinkcode-section}

NethSecurity supporta l'uso di un abbonamento a Snort per ottenere regole `Registered` e `Subscriber` tramite Oinkcode. L'`Oinkcode` è un codice univoco assegnato agli utenti registrati su Snort.org, questo codice è necessario per autenticare il download delle regole di Snort.

### Categorie di regole disponibili

- **Community Rules (Regole gratuite)**: Disponibili a tutti gli utenti registrati senza restrizioni. Mantenute dalla comunità Snort. Forniscono una protezione di base ma ricevono aggiornamenti meno frequenti rispetto alle regole ufficiali. Non è necessario Oinkcode per accedere a queste regole.
- **Registered Rules (Regole gratuite con ritardo)**: Regole ufficiali aggiornate dal team di Snort. Disponibili gratuitamente agli utenti registrati, ma con un ritardo di 30 giorni rispetto alla versione più recente. Oinkcode è necessario per accedere a queste regole.
- **Subscriber Rules (Regole a pagamento, aggiornamenti in tempo reale)**: Accesso immediato alle regole più aggiornate senza alcun ritardo. Disponibile solo agli utenti con un abbonamento a Snort Subscriber Rule Set. Oinkcode è necessario per accedere a queste regole.

### Come ottenere e utilizzare l'Oinkcode

- Registrati su Snort.org
- Recupera il tuo Oinkcode dalla sezione del profilo dell'account
- Su NethSecurity, incolla il tuo codice personale nel campo `Oinkcode`. Puoi verificare se il codice è valido facendo clic sul pulsante **Test code**

## Elenco degli eventi odierni

L'IPS controlla automaticamente il traffico all'interno della rete e genera avvisi o blocca il traffico in base al ruleset. Un elenco navigabile può essere trovato nella scheda `Today event list`. Durante la navigazione nell'elenco, puoi visualizzare le regole che hanno attivato l'avviso, gli indirizzi IP di origine e destinazione, il protocollo e l'azione intrapresa dal sistema.

Questo elenco può essere filtrato utilizzando la casella di filtro nella parte superiore della pagina. Inoltre, per ogni record visualizzato, è possibile saltare direttamente alla documentazione della regola facendo clic sull'ID della regola.

Facendo clic sull'icona del menu sul lato destro del record, è possibile aprire un modulo precompilato per sopprimere o disabilitare la regola che ha generato l'avviso.

## Bypass del filtro

Tutto il traffico che passa attraverso il firewall viene analizzato dall'IPS. Il sistema supporta regole di bypass per indirizzi IPv4 e IPv6 specifici. Qualsiasi indirizzo IP aggiunto a una regola di bypass verrà valutato sia per il traffico in ingresso che in uscita.

Per farlo, accedi alla scheda `Filter bypass` e premi il pulsante **Add bypass**. Un modulo viene fornito per aggiungere una regola di bypass per uno specifico indirizzo IP, la regola si applica al traffico in entrambe le direzioni e include i seguenti campi:

- `Address type`: se l'IP fornito è IPv4 o IPv6
- `IP address`: l'indirizzo IP o CIDR da ignorare
- `Description`: una descrizione della regola di bypass, è facoltativa e può essere omessa

## Disabilita regole

In alcuni ambienti, le regole possono essere troppo restrittive o generare troppi falsi positivi. Per evitare ciò, è possibile disabilitare alcune regole. Una regola disabilitata è una regola non inclusa nel ruleset di Snort.

Accedi alla scheda `Disabled Rules` e premi il pulsante **Disable rule**. Il sistema chiederà i seguenti campi:

- `GID`: il GID della regola, è un numero e di solito è sempre `1`
- `SID`: il SID della regola, è un numero
- `Description`: una descrizione della regola disabilitata, è facoltativa e può essere omessa

## Avvisi soppressi

Una regola di soppressione è una regola ignorata da Snort per uno specifico indirizzo IP o CIDR. La regola viene comunque valutata per tutti gli altri indirizzi IP.

Per aggiungere una regola di soppressione, accedi alla scheda `Suppressed alerts` e premi il pulsante **Suppress alert**. Compila i campi con le seguenti informazioni:

- `GID`: il GID della regola, è un numero e di solito è sempre `1`
- `SID`: il SID della regola, è un numero
- `Direction`: se la soppressione è per l'indirizzo IP di origine o destinazione
- `IP address`: l'indirizzo IP per il quale sopprimere l'avviso, può essere un intervallo CIDR
- `Description`: una descrizione della regola di soppressione, è facoltativa e può essere omessa
