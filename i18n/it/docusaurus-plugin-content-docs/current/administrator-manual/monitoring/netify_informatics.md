---
title: "Netify Informatics"
sidebar_position: 2
---

# Netify Informatics {#netify_informatics-section}

[Netify Informatics](https://www.netify.ai/products/netify-informatics) è un servizio cloud di terze parti che utilizza analitiche e intelligenza artificiale per convertire i metadati locali di DPI ottenuti da NethSecurity in intelligence di rete di alto livello. La soluzione fornisce approfondimenti su vari aspetti dell'attività di rete, inclusi:

- [Device Discovery](https://www.netify.ai/products/netify-informatics/device-discovery)
- [Bandwidth Monitoring](https://www.netify.ai/products/netify-informatics/bandwidth-monitoring)
- [Risk and Reputation Analysis](https://www.netify.ai/products/netify-informatics/risk-and-reputation)
- [Regulatory Compliance](https://www.netify.ai/products/netify-informatics/regulatory-compliance)
- Geolocalizzazione
- Audit e Forensics

Il servizio riceve i dati da netifyd, il motore DPI di NethSecurity che è abilitato per impostazione predefinita sul firewall.

Puoi provare il servizio gratuitamente per 7 giorni. Dopo questo periodo, puoi scegliere il piano che meglio si adatta alle tue esigenze.

Consulta [Netify Informatics Pricing](https://www.netify.ai/products/netify-informatics/pricing) e [Netify Informatics FAQ](https://www.netify.ai/resources/faq) per ulteriori informazioni.

## Prima di iniziare

Assicurati di creare un account sul sito web di Netify Informatics, puoi provare il servizio gratuitamente per 7 giorni. Registrati qui: [Netify Registration](https://portal.netify.ai/register)

Puoi gestire in modo granulare diversi clienti, diverse ubicazioni dello stesso cliente e persino diversi firewall all'interno della stessa ubicazione. La piattaforma è organizzata con questi elementi.

- **Organizzazione**: un'organizzazione è essenzialmente un cliente in cui abbiamo almeno un firewall NethSecurity, sono supportate più organizzazioni.
- **Sito**: la stessa organizzazione (cliente) potrebbe avere un ufficio a Roma, Firenze e Parigi. Un sito è definito per ogni ubicazione fisica per isolare i dati, sono supportati più siti.
- **Agente**: l'agente rappresenta l'unità NethSecurity del tuo cliente. Netify supporta più agenti per sito. Se hai una rete semplice, un agente probabilmente vedrà tutti i flussi di traffico sulla rete di un sito.

## Connetti NethSecurity a Netify Informatics

Sono necessari due step per utilizzare il servizio:

1.  Abilita l'invio di metadati da NethSecurity
2.  Provisioning di un agente su Netify Informatics.

:::warning

È obbligatorio configurare l'invio di dati su NethSecurity **per primo** e quindi provisioning dell'agente sulla piattaforma.

:::

### 1. Abilita l'invio di metadati {#enable-metadata-sending}

Accedi alla pagina `Netify Informatics` nella sezione `Monitoring` nell'interfaccia web di NethSecurity.

Abilita l'opzione `Send metadata to Netify Informatics` e fai clic su `Save`.

Ogni NethSecurity è associato a un UUID Agente univoco, come questo `B3-GV-WQ-SD`. Il codice sarà visibile sulla stessa pagina dopo l'abilitazione dell'opzione di invio dei metadati.

### 2. Provisioning dell'agente {#provision-the-agent}

Una volta che hai un account registrato e hai abilitato l'invio di metadati su NethSecurity, puoi eseguire il provisioning dell'agente sulla piattaforma Netify Informatics:

1.  Copia il codice ottenuto nel passaggio precedente e accedi al sito web di Netify Informatics.
2.  Accedi alla `Provision Agent Wizard` nella sezione `Deployment`.
3.  Segui le istruzioni per creare l'organizzazione (il cliente) e incolla l'UUID dell'agente nel campo appropriato per abilitare l'agente utilizzando il codice ottenuto su NethSecurity.

Da questo momento, Netify Informatics inizierà a mostrare i dati. Puoi quindi connettere altri firewall dello stesso cliente (stessa organizzazione, stesso sito o uno diverso) o creare una nuova organizzazione per un cliente diverso.

## Deployment Manager

La sezione `Deployment` all'interno di Netify Informatics ti consente di gestire Agenti, Siti e Organizzazioni. Mentre la gestione di Agenti e Siti è relativamente semplice, la sezione `Organization Access` ti consente di aggiungere altri membri alla tua organizzazione. Questa funzione consente agli altri di accedere al pannello Netify e visualizzare tutti i dati rilevanti.

Sono disponibili tre profili:

- Administrator
- Manager
- Viewer

Il profilo `Administrator`, tipicamente riservato ai colleghi all'interno della tua azienda, concede il massimo livello di autorizzazioni, consentendo loro di visualizzare, creare e modificare le configurazioni all'interno di Netify Informatics.

Il profilo `Manager` è dedicato agli individui che appartengono alla stessa organizzazione (l'azienda cliente). Concede loro il permesso di visualizzare tutte le sezioni all'interno di Netify Informatics, visualizzare la dashboard di deployment e modificare la sezione Identity manager, ma non di aggiungere altre organizzazioni o di eseguire il provisioning di nuovi agenti.

Il profilo `Viewer`, probabilmente il più comunemente utilizzato, è per qualcuno (ad esempio, un tecnico IT dell'organizzazione del tuo cliente) che può visualizzare tutti i dati all'interno della loro organizzazione ma non ha la capacità di modificare alcuna configurazione di Netify.

Per invitare qualcuno, semplicemente fai clic su `Manage Organization`, inserisci il suo indirizzo email e scegli il profilo desiderato. La persona riceverà un invito da Netify via email e sarà in grado di creare il proprio account.

:::note

Il tipo di profilo può essere modificato in qualsiasi momento da un amministratore, consentendoti di passare una persona da Manager a Viewer, ad esempio.

:::
