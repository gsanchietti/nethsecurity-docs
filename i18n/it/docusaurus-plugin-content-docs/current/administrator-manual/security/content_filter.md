---
title: "Filtrage dei contenuti"
sidebar_position: 1
---

# Filtrage dei contenuti

Il filtrage dei contenuti è un aspetto cruciale della sicurezza di rete e serve a due scopi principali:

1.  Bloccare il malware e prevenire gli attacchi dannosi
2.  Filtrare i siti indesiderati, come quelli contenenti contenuti per adulti

NethSecurity offre quattro meccanismi di filtrage distinti per affrontare queste esigenze:

- **Threat Shield IP**: Sistema di blocco basato su IP per colpire minacce di malware
- **Threat Shield DNS**: Sistema di blocco basato su DNS per malware e filtrage base dei contenuti
- **Deep Packet Inspection (DPI) filter**: Filtrage specifico per applicazioni e protocolli utilizzando netifyd
- **FlashStart DNS filter**: Soluzione commerciale di filtrage basato su DNS con funzioni di controllo dei contenuti complete

## Threat Shield IP

Threat Shield IP è un sistema di blocco basato su IP progettato specificamente per combattere le minacce di malware. Funziona bloccando le connessioni verso o da indirizzi IP noti come dannosi.

**Ambito**: Colpisce i malware e fornisce funzioni limitate di rimozione della privacy e della pubblicità

**Elenchi**:

- Elenchi comunitari, gratuiti, rivolti a malware generali, annunci e tracker
- Elenchi aziendali, a pagamento, incentrati sulla protezione da malware ad alto valore

Vantaggi:

- Elaborazione veloce poiché funziona a livello di IP
- Efficace contro interi network dannosi

Limitazioni:

- Non può filtrare in base al tipo di contenuto
- Potrebbe occasionalmente bloccare servizi legittimi che condividono un IP con quelli dannosi

Per configurare Threat Shield IP, vedere [Threat shield IP](./threat_shield_ip.md).

## Threat Shield DNS

Threat Shield DNS fornisce il blocco basato su DNS, offrendo protezione contro i malware e capacità di filtrage base dei contenuti.

**Ambito**: Copre malware e categorie di contenuti limitate (ad es., contenuti per adulti, gioco d'azzardo)

**Elenchi**:

- Elenchi comunitari, gratuiti, incentrati su malware generali e filtrage semplice dei contenuti
- Elenchi aziendali, a pagamento, incentrati sulla protezione da malware ad alto valore

Vantaggi:

- Può bloccare domini specifici indipendentemente dall'indirizzo IP
- Offre categorizzazione base dei contenuti (ad es., adulti, gioco d'azzardo)

Limitazioni:

- Potrebbe essere aggirato utilizzando server DNS alternativi, ma può essere mitigato con il filtrage DPI e abilitando categorie di blocco speciali
- Meno granulare del filtrage URL completo

Per configurare Threat Shield DNS, vedere [Threat shield DNS](./threat_shield_dns.md).

## FlashStart DNS filter

FlashStart è una soluzione commerciale di filtrage basato su DNS che offre funzioni complete di controllo dei contenuti e reporting.

**Ambito**: Filtrage completo dei contenuti oltre al solo malware e contenuti per adulti

**Elenchi**: Elenchi commerciali mantenuti da FlashStart

Vantaggi:

- Elenchi di blocco di alta qualità
- Report personalizzabili
- Configurazione basata su cloud, nessun accesso diretto al firewall richiesto
- Categorie di contenuti estese
- Facile da gestire
- Scalabile per organizzazioni di varie dimensioni

Per configurare il filtrage DNS FlashStart, vedere [FlashStart DNS filter](./flashstart.md).

## Deep Packet Inspection (DPI) filter

NethSecurity utilizza tecniche di Deep Packet Inspection (DPI) per il filtrage del traffico di rete utilizzando Netify Agent.

**Ambito**: Filtrage specifico per applicazioni e protocolli

**Elenchi**:

- Firme della comunità, gratuite ma limitate nel numero e nella frequenza degli aggiornamenti
- Firme aziendali, incluse in qualsiasi abbonamento, che offrono una copertura più completa

Vantaggi:

- Fornisce un controllo granulare sul traffico di rete
- Può identificare e filtrare in base a applicazioni o protocolli specifici
- Consente la gestione dinamica del traffico basata su analisi in tempo reale

Considerazioni:

- Potrebbe richiedere più potenza di elaborazione rispetto al filtrage basato su IP o DNS
- Richiede una configurazione attenta per bilanciare la sicurezza e le prestazioni
- L'amministratore deve creare regole DPI per ogni interfaccia

Per configurare il filtrage DPI, vedere [Deep Packet Inspection (DPI) filter](./dpi_filter.md).

## Confronto delle opzioni di filtrage

| Funzione | Threat Shield IP | Threat Shield DNS | Flashstart DNS Filtering | DPI Filter |
|----|----|----|----|----|
| Metodo di blocco | Basato su IP | Basato su DNS | Basato su DNS | Ispezione dei pacchetti |
| Obiettivo principale | Malware | Malware + contenuti base | Contenuti completi | Specifico per applicazioni/protocolli |
| Tipi di elenco | Comunità, Aziendali | Comunità, Aziendali | Commerciali | N/A (analisi in tempo reale) |
| Configurazione | Firewall | Firewall | Cloud | Firewall (per interfaccia) |
| Reporting | Nessuno | Nessuno | Avanzato, personalizzabile | Limitato |

**Strategie di implementazione**

Per una sicurezza ottimale, considera un approccio a strati:

1.  Utilizza Threat Shield IP come prima linea di difesa contro i network dannosi noti.
2.  Implementa un filtro DNS, scegli una delle seguenti opzioni:
    - Threat Shield DNS per catturare minacce basate su dominio e fornire filtrage base dei contenuti oppure
    - Flashstart DNS Filtering per il controllo completo dei contenuti, specialmente in ambienti che richiedono una gestione politica dettagliata e reporting.
3.  Utilizza il filtrage DPI per un controllo granulare su applicazioni e protocolli specifici, e per gestire il traffico basato su analisi in tempo reale.

Questa combinazione fornisce una difesa in profondità, affrontando vari vettori di minaccia e esigenze di filtrage dei contenuti.
