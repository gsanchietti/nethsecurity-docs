---
title: "Filtro Deep Packet Inspection (DPI)"
sidebar_position: 4
---

# Filtro Deep Packet Inspection (DPI) {#dpi_filter-section}

NethSecurity utilizza [Netify Agent](https://www.netify.ai/resources) per impiegare tecniche di Deep Packet Inspection (DPI) per il filtraggio del traffico di rete.

Netify Agent funziona come server di deep-packet inspection, sfruttando nDPI (precedentemente OpenDPI) per identificare i protocolli di rete e le applicazioni. Le informazioni rilevate possono essere archiviate localmente, accedute tramite socket UNIX o TCP, oppure inviate tramite HTTP POST a un server remoto di terze parti. Dettagli quali metadati di flusso, statistiche di rete e classificazioni di rilevamento possono essere utilizzati per prendere decisioni sul flusso.

Ecco come funziona:

- il plugin delle azioni di flusso Netify assegna etichette alle connessioni corrispondenti
- le regole nft possono quindi bloccare o regolare la priorità (DSCP) per le connessioni in base a queste etichette

L'amministratore può creare regole di Deep Packet Inspection (DPI) per ogni interfaccia.

## Configurazione

Per configurare queste regole, l'amministratore inizia il processo selezionando la particolare interfaccia di rete su cui si intende applicare la regola. Questo passaggio garantisce che la regola sia applicata precisamente al segmento di rete designato, consentendo una gestione mirata ed efficace del traffico di rete.

Dopo la selezione dell'interfaccia, all'amministratore viene richiesto di specificare le applicazioni che devono essere bloccate o regolate. Questo passaggio essenziale implica la scelta da un elenco completo di applicazioni accessibile tramite l'interfaccia di sistema.

L'interfaccia, come funzione predefinita, presenta un catalogo di applicazioni comunemente utilizzate. Tuttavia, fornisce una funzionalità di ricerca avanzata che consente all'amministratore di esplorare e individuare specifiche applicazioni e categorie di applicazioni che richiedono particolare attenzione.

### Firme di applicazioni premium

:::note

Abbonamento richiesto

Questa funzione è disponibile solo se il firewall ha un [abbonamento Community o Enterprise](../system/subscription.md) valido.

:::

In assenza di un abbonamento, il sistema riconosce intrinsecamente una linea di base di circa 400 applicazioni. Tuttavia, con un abbonamento attivo, questa capacità si espande significativamente, comprendendo più di 2300 applicazioni. In questo scenario, l'elenco delle applicazioni riconosciute viene aggiornato quotidianamente, assicurando che il sistema rimanga al passo con il panorama sempre in evoluzione delle applicazioni e dei servizi digitali.

### Elenco di applicazioni e protocolli

L'elenco completo di tutte le applicazioni e i protocolli supportati dalla versione Enterprise è disponibile qui:

- [Applicazioni](https://www.netify.ai/resources/applications_reference)
- [Protocolli](https://www.netify.ai/resources/protocols)

### Eccezioni

L'esclusione DPI consente l'esclusione di specifici indirizzi di rete, come il gateway o altre infrastrutture critiche, impedendo loro di essere bloccati.

Per aggiungere una nuova eccezione, fai clic sul pulsante `Aggiungi eccezione`. Immettere l'`indirizzo IP o CIDR` che deve essere escluso dal filtro. È possibile includere una descrizione che spieghi il motivo dell'esclusione.

Ogni eccezione può essere abilitata o disabilitata come desiderato.

### Esclusione dell'interfaccia Netify

Per impostazione predefinita, Netifyd monitora tutte le interfacce. Per escludere interfacce specifiche, è possibile definire un elenco di esclusione. Di seguito sono riportati i comandi per aggiungere, modificare o rimuovere interfacce escluse. L'elenco di esclusione è configurato utilizzando l'opzione `ns_exclude` che accetta un elenco di pattern. Ogni voce è un pattern glob di shell.

- Aggiungere interfacce all'elenco di esclusione. Il sistema escluderà l'interfaccia `eth1` e tutte le interfacce OpenVPN e WireGuard: :

      uci add_list netifyd.@netifyd[0].ns_exclude='eth1'
      uci add_list netifyd.@netifyd[0].ns_exclude='tun*'
      uci add_list netifyd.@netifyd[0].ns_exclude='wg*'
      uci commit netifyd
      echo '{"changes": {"network": {}}}' | /usr/libexec/rpcd/ns.commit call commit

In questo caso il sistema escluderà l'interfaccia `eth1`, tutte le interfacce WireGuard `wgX` e tutte le interfacce OpenVPN indirizzate.

- Modificare l'elenco di esclusione: :

      uci delete netifyd.@netifyd[0].ns_exclude='eth1'
      uci add_list netifyd.@netifyd[0].ns_exclude='eth2'
      uci commit netifyd
      echo '{"changes": {"network": {}}}' | /usr/libexec/rpcd/ns.commit call commit

- Cancellare l'elenco di esclusione: :

      uci delete netifyd.@netifyd[0].ns_exclude
      uci commit netifyd
      echo '{"changes": {"network": {}}}' | /usr/libexec/rpcd/ns.commit call commit

- Restituire l'elenco di esclusione: :

      uci show netifyd.@netifyd[0].ns_exclude
