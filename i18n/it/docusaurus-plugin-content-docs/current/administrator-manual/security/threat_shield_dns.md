---
title: "Threat shield DNS"
sidebar_position: 3
---

# Threat shield DNS {#threat_shield_dns-section}

Threat shield DNS utilizza Adblock che blocca qualsiasi richiesta verso i domini considerati malevoli. Il servizio può caricare liste di blocco gestite dalla comunità oppure utilizzare feed Enterprise forniti da [Nethesis](https://www.nethesis.it) e [Yoroi](https://yoroi.company), un'azienda leader nel campo della sicurezza informatica e membro della [Cyber Threat Alliance](https://www.cyberthreatalliance.org).

Si noti che per accedere alle liste di blocco di Nethesis e Yoroi, l'unità deve disporre di un diritto aggiuntivo valido per questo servizio.

## Configurazione {#configuration-section}

:::note

Utilizzare Threat shield DNS solo se non si sta già utilizzando il servizio FlashStart. Entrambi i servizi operano a livello DNS e non possono essere utilizzati insieme. L'interfaccia utente impedisce di abilitarli contemporaneamente per evitare conflitti.

:::

Il servizio è disabilitato per impostazione predefinita. Per abilitarlo, accedere alla pagina `Threat shield DNS` nella sezione `Security`. Accedere alla scheda `Settings` e attivare l'interruttore `Status`.

Quando il servizio è abilitato, la scheda `Blocklist sources` mostrerà tutte le liste di blocco disponibili. È possibile abilitare o disabilitare ogni lista di blocco utilizzando l'interruttore sul lato destro dell'elenco. Le liste di blocco abilitate verranno aggiornate automaticamente a intervalli regolari.

Per specificare su quali zone il servizio deve essere attivo, selezionarle nella casella combinata `Force DNS redirection on these zones`.

`Redirected ports` consente di specificare quali porte devono essere reindirizzate al servizio Threat shield DNS.

### Blocklist della comunità {#community_blocklists-section}

Le blocklist della comunità provengono da collaboratori della comunità e bloccano vari domini relativi a: annunci pubblicitari, malware, spam, tracker, contenuti sessualmente espliciti, pirateria e così via. NethSecurity le rende disponibili così come sono.

Le liste della comunità non forniscono una metrica standardizzata di "Confidence", quindi l'interfaccia utente mostra la loro fiducia come "Unknown". Come euristica pratica, quando il nome dell'elenco contiene un indicatore di gravità o fiducia (ad es. "lvl 1", "level 1"), generalmente indica il tasso di falsi positivi più basso e la massima fiducia; al contrario, i livelli indicati più alti (ad es. "lvl 2", "lvl 3", "lvl 4") in genere implicano una fiducia inferiore e un rischio più elevato di voci aggressive o errate. Le convenzioni di denominazione variano e non tutti i provider della comunità includono tali indicatori, quindi rivedi sempre i contenuti e lo scopo di una lista della comunità prima di abilitarla in produzione. Il tipo di licenza d'uso può variare a seconda del provider, quindi se l'utilizzo non è personale, potrebbe essere necessario contattare il provider.

**Manutenzione delle liste della comunità**

Ogni blocklist è gestita dal suo specifico provider. NethSecurity include già gli URL per il download dei feed, che sono validi al momento del rilascio. Tuttavia, poiché questi URL sono codificati, se il provider li modifica, alcune blocklist potrebbero non essere più scaricabili.

### Blocklist aziendali {#enterprise_blocklists-section}

:::note

Sottoscrizione richiesta

Questa funzione è disponibile solo se l'unità dispone di una valida [sottoscrizione Community o Enterprise](../system/subscription.md).

:::

Le blocklist aziendali si concentrano specificamente sulla sicurezza e offrono diversi vantaggi rispetto alle blocklist gestite dalla comunità:

1.  **Qualità e precisione**: Le blocklist aziendali, come quelle fornite da Nethesis e Yoroi, sono curate e gestite da rinomate società di sicurezza informatica. Queste società dispongono di team dedicati che monitorano e aggiornano continuamente le blocklist per garantire che siano accurate ed efficaci nel bloccare il traffico malevolo. Ciò si traduce in un livello più elevato di qualità e precisione rispetto alle blocklist gestite dalla comunità, che potrebbero non ricevere lo stesso livello di attenzione e aggiornamenti.
2.  **Tempestività**: Le blocklist aziendali vengono aggiornate frequentemente per includere le minacce più recenti e gli indirizzi IP malevoli. Le società di sicurezza informatica come Nethesis e Yoroi monitorano attivamente le minacce emergenti e le aggiungono prontamente alle loro blocklist. Ciò garantisce che il tuo sistema sia protetto dalle minacce più recenti e in evoluzione.
3.  **Riduzione dei falsi positivi**: I falsi positivi si verificano quando il traffico legittimo viene bloccato per errore. Le blocklist aziendali sono progettate per ridurre al minimo i falsi positivi curando attentamente e verificando gli indirizzi IP e i nomi host elencati. Le società dietro le blocklist aziendali dispongono di processi robusti per garantire che solo entità maligne siano incluse nelle blocklist. Ciò riduce le probabilità che il traffico legittimo venga bloccato, riducendo al minimo le interruzioni della tua rete o dei tuoi servizi.
4.  **Supporto aziendale**: Le blocklist aziendali spesso includono supporto aggiuntivo e servizi personalizzati per ambienti aziendali. Ciò include l'accesso al supporto tecnico, alla documentazione e all'assistenza per l'integrazione. Se sorgono problemi o domande durante l'utilizzo delle blocklist aziendali, puoi contare sul supporto fornito dalle società di sicurezza informatica per affrontarli in modo efficace.

### Fiducia

Le blocklist aziendali includono un punteggio "Confidence" che viene visualizzato nell'interfaccia utente. Il punteggio è espresso come un valore da 1 a 10 e rappresenta la valutazione del provider della qualità dell'elenco: i valori più alti indicano una fiducia più elevata e una minore probabilità di falsi positivi. Questa metrica "Confidence" è disponibile solo per le liste aziendali; le liste della comunità vengono presentate "così come sono" e visualizzano "Unknown" per la fiducia.

Le blocklist di Yoroi e Nethesis sono blocklist aziendali. Questi elenchi verranno visualizzati solo se l'unità dispone di una valida [sottoscrizione Enterprise o Community](../system/subscription.md) e di un valido diritto per il servizio Threat Shield.

## Bypass del filtro {#filter_bypass-section}

Alcuni host o subnet potrebbero avere la necessità di bypassare il filtro Threat shield DNS. Per configurare il bypass del filtro, accedi alla scheda `Filter bypass` di Threat shield DNS. Utilizza il pulsante **Add bypass** per aggiungere un nuovo indirizzo all'elenco. L'indirizzo può essere un indirizzo IPv4/IPv6 valido con notazione CIDR facoltativa.

## Allowlist locale {#local_allowlist_dns-section}

Per consentire domini specifici che potrebbero essere inclusi nelle blocklist, puoi accedere alla scheda `Local allowlist` di Threat shield DNS. Utilizza il pulsante **Add domain** per aggiungere un dominio all'elenco; puoi aggiungere una descrizione al dominio per aiutarti a ricordare perché è stato aggiunto.

I domini nell'allowlist hanno priorità sulle `Blocklists` e sulla `Local blocklist`

## Blocklist locale {#local_blocklist_dns-section}

Per bloccare domini specifici non inclusi nelle blocklist, puoi accedere alla scheda `Local blocklist` di Threat shield DNS. Utilizza il pulsante **Add domain** per aggiungere un dominio all'elenco; puoi aggiungere una descrizione al dominio per aiutarti a ricordare perché è stato aggiunto.

:::warning

La risoluzione DNS per i nomi elencati nella blocklist avrà effetto anche sull'unità stessa

:::

## Verificare se un dominio è bloccato {#check_domain_blocklist-section}

Se stai riscontrando problemi con la risoluzione del dominio e desideri verificare se un dominio specifico è bloccato, puoi eseguire una query direttamente dal terminale locale.

Utilizza il seguente comando per verificare un dominio:

`/etc/init.d/adblock query \<domain\>`

Ad esempio:

`root@nethsecurity8:\~# /etc/init.d/adblock query baddomain.com`

L'output potrebbe essere simile a questo:

    :::
    ::: domain 'baddomain.com' in active blocklist
    :::
      + baddomain.com

    :::
    ::: domain 'baddomain.com' in backups and black-/whitelist
    :::
      + adb_list.adult.gz             baddomain.com

Questo output mostra se il dominio è attualmente bloccato da qualsiasi blocklist attiva. In questo esempio specifico, il dominio `baddomain.com` fa parte della categoria **adult**, come indicato da `adb_list.adult.gz`. Ciò ti aiuta a identificare quale categoria o elenco ha causato il blocco del dominio.

## Risoluzione dei problemi {#adblock_troubleshooting-section}

Dopo aver abilitato Adblock o modificato la sua configurazione, attendi fino a 30 secondi affinché le modifiche vengano applicate. Durante l'avvio, Adblock attende anche circa 30 secondi affinché la rete si avvii prima di caricare i feed.

Utilizza il seguente comando per verificare se Adblock è in esecuzione:

    /etc/init.d/adblock status

Se l'output mostra zero domini bloccati e nessun feed attivo, Adblock non ha ancora caricato nulla. In tal caso, lo stato potrebbe essere simile a questo:

    ::: adblock runtime information
      + adblock_status  : enabled
      + frontend_ver    : 4.5.5-r2
      + backend_ver     : 4.5.5-r3
      + blocked_domains : 0
      + active_feeds    : -
      + dns_backend     : dnsmasq (2.91-r3), /tmp/dnsmasq.d, 3.39 MB
      + run_ifaces      : trigger: -, report: br-lan
      + run_information : base: /tmp, dns: /tmp/dnsmasq.d, backup: /tmp/adblock-backup, report: /tmp/adblock-report, error: /tmp/adb_error.log
      + run_flags       : shift: ✘, custom feed: ✔, ext. DNS (std/prot/remote/bridge): ✘/✘/✘/✘, force: ✔, flush: ✘, tld: ✔, search: ✘, report: ✔, mail: ✘, jail: ✘, debug: ✔
      + last_run        : mode: reload, date / time: 28/05/2026 13:44:31, duration: 0m 5s, memory: 3450.30 MB available
      + system_info     : cores: 2, fetch: wget, Nethesis NethBox Z1+, x86/64, NethSecurity 8.8.0-nethsecurity-8.8.20260528105131.094c098 (r32933-4ccb782af7)

Un sistema caricato correttamente dovrebbe essere simile a questo:

    ::: adblock runtime information
      + adblock_status  : enabled
      + frontend_ver    : 4.5.5-r2
      + backend_ver     : 4.5.5-r3
      + blocked_domains : 237 974
      + active_feeds    : doh_vpn_tor_proxy gambling,
      + dns_backend     : dnsmasq (2.91-r3), /tmp/dnsmasq.ns_dnsmasq.d, 19.74 MB
      + run_ifaces      : trigger: -, report: -
      + run_information : base: /tmp, dns: /tmp/dnsmasq.ns_dnsmasq.d, backup: /tmp/adblock-backup, report: /tmp/adblock-report, error: /dev/null
      + run_flags       : shift: ✘, custom feed: ✔, ext. DNS (std/prot/remote/bridge): ✘/✘/✘/✘, force: ✔, flush: ✘, tld: ✔, search: ✘, report: ✘, mail: ✘, jail: ✘, debug: ✘
      + last_run        : mode: reload, date / time: 28/05/2026 14:30:37, duration: 0m 2s, memory: 708.93 MB available
      + system_info     : cores: 2, fetch: curl, QEMU Standard PC (Q35 + ICH9, 2009), x86/64, NethSecurity 8.8.0-nethsecurity-8.8.20260527151745.8ae1ddcc9 (r32933-4ccb782af7)

Se ci sono stati problemi di rete e Adblock non ha potuto scaricare alcun feed, riavvialo semplicemente:

    /etc/init.d/adblock restart

## Configurazione avanzata {#advanced_configuration-section}

Quando Threat shield DNS è abilitato:

- Viene generato un nuovo file di origine della categoria in base alla registrazione dell'unità e al diritto.
- Tutte le query DNS vengono reindirizzate alla macchina locale.
- Adblock viene configurato per utilizzare il nuovo file di origine della categoria e verrà avviato automaticamente.

Anche se non consigliato, è possibile utilizzare Adblock senza Threat shield DNS. Per opzioni di configurazione più dettagliate, consulta il [manuale dello sviluppatore](https://dev.nethsecurity.org/packages/ns-threat_shield/#ts-dns).
